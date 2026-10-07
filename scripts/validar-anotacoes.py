import json
import argparse
import sys
import os
import re
import unicodedata
from collections import Counter

MIN_REASONING_CHARS = 20
MIN_STATEMENT_EVIDENCE_CHARS = 10
MAX_IDENTICAL_REASONING_REUSE = 3

_REASONING_PLACEHOLDERS = {
    "auto generated reasoning",
    "auto-generated reasoning",
    "generated reasoning",
    "reasoning",
    "reasoning summary",
    "placeholder",
    "todo",
    "tbd",
    "n/a",
    "na",
}

_EVIDENCE_PLACEHOLDERS = {
    "evidence",
    "statement",
    "placeholder",
    "todo",
    "tbd",
    "n/a",
    "na",
}


def _normalize_text(value):
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _placeholder_key(value):
    value = _normalize_text(value)
    value = value.strip(" .,:;!?-–—_")
    return value


def _fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def _validate_semantic_quality(annotation, pack_q):
    source_id = annotation.get("source_id")
    reasoning = annotation.get("reasoning_summary", "")
    reasoning_norm = _placeholder_key(reasoning)

    if len(reasoning.strip()) < MIN_REASONING_CHARS:
        _fail(f"reasoning_summary too short on {source_id}")

    if reasoning_norm in _REASONING_PLACEHOLDERS:
        _fail(f"PLACEHOLDER_REASONING on {source_id}")

    status = annotation.get("annotation_status")
    evidence = annotation.get("module_evidence", [])

    if status == "ANNOTATED":
        if not evidence:
            _fail(f"ANNOTATED requires non-empty module_evidence on {source_id}")

        grounded = False
        statement = pack_q.get("statement") or ""
        statement_norm = _normalize_text(statement)

        for item in evidence:
            kind = item.get("kind")
            if kind == "STATEMENT":
                text = item.get("text", "")
                text_norm = _placeholder_key(text)

                if len(text.strip()) < MIN_STATEMENT_EVIDENCE_CHARS:
                    _fail(f"STATEMENT_EVIDENCE_TOO_SHORT on {source_id}")

                if text_norm in _EVIDENCE_PLACEHOLDERS:
                    _fail(f"PLACEHOLDER_EVIDENCE on {source_id}")

                if statement_norm:
                    probe = _normalize_text(text).rstrip(" .…")
                    if probe and probe not in statement_norm:
                        _fail(f"STATEMENT_EVIDENCE_NOT_GROUNDED on {source_id}")

                grounded = True

            elif kind == "CURRICULUM_SUBTOPIC":
                module = item.get("module")
                subtopic = (item.get("subtopic") or "").strip()
                if not module or not subtopic:
                    _fail(f"INVALID_CURRICULUM_SUBTOPIC_EVIDENCE on {source_id}")
                grounded = True

        if not grounded:
            _fail(f"ANNOTATED requires grounded evidence on {source_id}")

    # Keep annotation image metadata synchronized with the immutable pack.
    pack_has_image = bool(pack_q.get("has_image"))
    pack_image_status = pack_q.get(
        "image_inventory_status",
        "AVAILABLE" if pack_has_image else "NOT_APPLICABLE",
    )
    annotation_image_status = annotation.get("image_status")

    if pack_has_image:
        if annotation_image_status != pack_image_status:
            _fail(
                f"image_status mismatch on {source_id}: "
                f"pack={pack_image_status}, annotation={annotation_image_status}"
            )
    else:
        if annotation_image_status != "NOT_APPLICABLE":
            _fail(
                f"non-visual question requires image_status=NOT_APPLICABLE on {source_id}"
            )
        if annotation.get("image_required") is True:
            _fail(
                f"non-visual question cannot set image_required=true on {source_id}"
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', default='data/editorial/schema-anotacao-v3.json')
    parser.add_argument('--curriculum', default='data/editorial/curriculum-editorial-authoring-input.json')
    parser.add_argument('--annotations', required=True)
    parser.add_argument('--pack', required=True, help='Path to content.json of the batch')
    args = parser.parse_args()

    if not os.path.exists(args.schema):
        _fail(f"schema not found: {args.schema}")

    if not os.path.exists(args.curriculum):
        _fail(f"curriculum not found: {args.curriculum}")

    if not os.path.exists(args.pack):
        _fail(f"pack not found: {args.pack}")

    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        _fail("jsonschema library required")

    with open(args.schema, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    with open(args.pack, 'r', encoding='utf-8') as f:
        pack_data = json.load(f)

    pack_questions = {q['source_id']: q for q in pack_data.get('questions', [])}
    pack_batch_id = pack_data.get('batch_id')

    with open(args.annotations, 'r', encoding='utf-8') as f:
        envelope = json.load(f)

    if 'batch_id' not in envelope or 'annotator_id' not in envelope or 'annotations' not in envelope:
        _fail("annotations file missing envelope fields (batch_id, annotator_id, annotations)")

    if envelope['batch_id'] != pack_batch_id:
        _fail(f"batch_id mismatch (pack: {pack_batch_id}, annotations: {envelope['batch_id']})")

    anots = envelope['annotations']

    envelope_annotator = envelope['annotator_id']
    if envelope_annotator not in ['ANNOTATOR_A', 'ANNOTATOR_B', 'ADJUDICATOR']:
        _fail(f"invalid annotator_id in envelope: {envelope_annotator}")

    seen_ids = set()
    reasoning_counter = Counter()

    for a in anots:
        source_id = a.get('source_id')

        if a.get('annotator_id') != envelope_annotator:
            _fail(
                f"ANNOTATOR_ID_MISMATCH on {source_id}: "
                f"expected {envelope_annotator}, got {a.get('annotator_id')}"
            )

        try:
            validate(instance=a, schema=schema)
        except ValidationError as e:
            _fail(f"validation failed on {source_id}: {e.message}")

        if source_id in seen_ids:
            _fail(f"duplicate source_id in annotations: {source_id}")
        seen_ids.add(source_id)

        if source_id not in pack_questions:
            _fail(f"unknown source_id in annotations: {source_id}")

        pack_q = pack_questions[source_id]

        if a.get('curriculum_version') != pack_data.get('curriculum_version'):
            _fail(f"curriculum_version mismatch on {source_id}")

        if a.get('source_question_version') != pack_q.get('source_question_version'):
            _fail(f"source_question_version mismatch on {source_id}")

        primary = a.get('primary_module')
        acceptable = a.get('acceptable_modules', [])
        if primary and primary in acceptable:
            _fail(
                f"primary_module '{primary}' cannot be in acceptable_modules on {source_id}"
            )

        if a.get('annotation_status') == 'OUT_OF_CURRICULUM':
            if a.get('in_curriculum') is not False:
                _fail(f"OUT_OF_CURRICULUM requires in_curriculum=False on {source_id}")
            if a.get('primary_module') is not None:
                _fail(f"OUT_OF_CURRICULUM requires primary_module=None on {source_id}")
            if len(acceptable) > 0:
                _fail(f"OUT_OF_CURRICULUM requires acceptable_modules=[] on {source_id}")

        _validate_semantic_quality(a, pack_q)
        reasoning_counter[_normalize_text(a.get("reasoning_summary", ""))] += 1

    missing_ids = set(pack_questions.keys()) - seen_ids
    if missing_ids:
        _fail(f"missing source_ids in annotations: {', '.join(sorted(missing_ids))}")

    for reasoning, count in reasoning_counter.items():
        if reasoning and count > MAX_IDENTICAL_REASONING_REUSE:
            _fail(
                f"REPEATED_REASONING_TEMPLATE: identical reasoning reused "
                f"{count} times (limit {MAX_IDENTICAL_REASONING_REUSE})"
            )

    print("ANNOTATIONS_VALID = true")
    print("ANNOTATION_QUALITY_VALID = true")


if __name__ == '__main__':
    main()
