import json
import argparse
import sys
import os
import re
import unicodedata
from collections import Counter

MIN_REASONING_CHARS = 60
MIN_STATEMENT_EVIDENCE_CHARS = 18
MAX_IDENTICAL_REASONING_REUSE = 2

_REASONING_PLACEHOLDERS = {
    "auto generated reasoning", "auto-generated reasoning", "generated reasoning",
    "reasoning", "reasoning summary", "placeholder", "todo", "tbd", "n/a", "na",
}
_EVIDENCE_PLACEHOLDERS = {"evidence", "statement", "placeholder", "todo", "tbd", "n/a", "na"}
_GENERIC_REASON_PATTERNS = [
    r"conceito central deste m[oó]dulo",
    r"alinhando-se [aà]s compet[eê]ncias definidas para este m[oó]dulo",
    r"caracter[ií]sticos desta disciplina",
    r"neste agrupamento",
    r"neste n[uú]cleo",
    r"principal m[eé]trica de avalia[cç][aã]o deste t[oó]pico",
]
_STOPWORDS = {
    "a","o","as","os","de","do","da","dos","das","e","em","um","uma","para","por",
    "com","sem","que","se","ao","aos","na","no","nas","nos","como","ou","sua","seu",
    "esta","este","essa","esse","questao","questão","modulo","módulo"
}


def _normalize_text(value):
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.casefold()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _placeholder_key(value):
    return _normalize_text(value).strip(" .,:;!?-_\u2013\u2014")


def _tokens(value):
    raw = re.findall(r"[a-z0-9]+", _normalize_text(value))
    return {t for t in raw if len(t) >= 4 and t not in _STOPWORDS}


def _fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def _load_editorial_curriculum(path):
    if not os.path.exists(path):
        _fail(f"editorial curriculum not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    modules = data if isinstance(data, list) else data.get("modules", [])
    out = {}
    for m in modules:
        code = m.get("code")
        if code:
            out[code] = m
    if not out:
        _fail("editorial curriculum has no modules")
    return out


def _validate_semantic_quality(annotation, pack_q, editorial_modules, legacy=False):
    source_id = annotation.get("source_id")
    reasoning = annotation.get("reasoning_summary", "")
    reasoning_norm = _placeholder_key(reasoning)

    min_reasoning = 20 if legacy else MIN_REASONING_CHARS
    min_statement = 10 if legacy else MIN_STATEMENT_EVIDENCE_CHARS

    if len(reasoning.strip()) < min_reasoning:
        _fail(f"reasoning_summary too short on {source_id}")
    if reasoning_norm in _REASONING_PLACEHOLDERS:
        _fail(f"PLACEHOLDER_REASONING on {source_id}")
    if not legacy:
        for pat in _GENERIC_REASON_PATTERNS:
            if re.search(pat, reasoning_norm):
                _fail(f"GENERIC_REASONING_TEMPLATE on {source_id}")

    status = annotation.get("annotation_status")
    evidence = annotation.get("module_evidence", [])
    statement = pack_q.get("statement") or ""
    statement_norm = _normalize_text(statement)

    statement_evidence_texts = []
    curriculum_evidence = []

    for item in evidence:
        kind = item.get("kind")
        if kind == "STATEMENT":
            text = item.get("text", "")
            text_norm = _placeholder_key(text)
            if len(text.strip()) < min_statement:
                _fail(f"STATEMENT_EVIDENCE_TOO_SHORT on {source_id}")
            if text_norm in _EVIDENCE_PLACEHOLDERS:
                _fail(f"PLACEHOLDER_EVIDENCE on {source_id}")
            probe = _normalize_text(text).rstrip(" .")
            if statement_norm and probe and probe not in statement_norm:
                _fail(f"STATEMENT_EVIDENCE_NOT_GROUNDED on {source_id}")
            statement_evidence_texts.append(text)
        elif kind == "CURRICULUM_SUBTOPIC":
            curriculum_evidence.append(item)

    if status == "ANNOTATED":
        primary = annotation.get("primary_module")
        if not evidence:
            _fail(f"ANNOTATED requires non-empty module_evidence on {source_id}")
        if not statement_evidence_texts:
            _fail(f"ANNOTATED requires STATEMENT evidence on {source_id}")

        if not legacy:
            if not curriculum_evidence:
                _fail(f"ANNOTATED requires CURRICULUM_SUBTOPIC evidence on {source_id}")
            module = editorial_modules.get(primary)
            if not module:
                _fail(f"unknown primary module in editorial curriculum on {source_id}: {primary}")
            valid_subtopics = {_normalize_text(x): x for x in module.get("subtopics", [])}
            bound_ok = False
            selected_subtopics = []
            for item in curriculum_evidence:
                if item.get("module") != primary:
                    _fail(f"CURRICULUM_SUBTOPIC_MODULE_MISMATCH on {source_id}")
                subtopic = (item.get("subtopic") or "").strip()
                if _normalize_text(subtopic) not in valid_subtopics:
                    _fail(f"UNKNOWN_CURRICULUM_SUBTOPIC on {source_id}: {subtopic}")
                selected_subtopics.append(subtopic)
                bound_ok = True
            if not bound_ok:
                _fail(f"ANNOTATED requires primary-module curriculum binding on {source_id}")

            reason_tokens = _tokens(reasoning)
            stmt_tokens = set().union(*[_tokens(x) for x in statement_evidence_texts])
            curriculum_text = " ".join([module.get("title", "")] + selected_subtopics)
            curriculum_tokens = _tokens(curriculum_text)
            if not (reason_tokens & stmt_tokens):
                _fail(f"REASONING_NOT_LINKED_TO_STATEMENT on {source_id}")
            if not (reason_tokens & curriculum_tokens):
                _fail(f"REASONING_NOT_LINKED_TO_CURRICULUM on {source_id}")

    elif status == "OUT_OF_CURRICULUM" and not legacy:
        if not statement_evidence_texts:
            _fail(f"OUT_OF_CURRICULUM requires STATEMENT evidence on {source_id}")
        reason_tokens = _tokens(reasoning)
        stmt_tokens = set().union(*[_tokens(x) for x in statement_evidence_texts])
        if not (reason_tokens & stmt_tokens):
            _fail(f"OOC_REASONING_NOT_LINKED_TO_STATEMENT on {source_id}")

    # Image metadata synchronization.
    pack_has_image = bool(pack_q.get("has_image"))
    pack_image_status = pack_q.get("image_inventory_status", "AVAILABLE" if pack_has_image else "NOT_APPLICABLE")
    annotation_image_status = annotation.get("image_status")
    if pack_has_image:
        if annotation_image_status != pack_image_status:
            _fail(f"image_status mismatch on {source_id}: pack={pack_image_status}, annotation={annotation_image_status}")
    else:
        if annotation_image_status != "NOT_APPLICABLE":
            _fail(f"non-visual question requires image_status=NOT_APPLICABLE on {source_id}")
        if annotation.get("image_required") is True:
            _fail(f"non-visual question cannot set image_required=true on {source_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', default='data/editorial/schema-anotacao-v3.json')
    parser.add_argument('--curriculum', default='data/editorial/curriculum-editorial-authoring-input.json')
    parser.add_argument('--editorial-curriculum', default='data/editorial/curriculum-35-modules-editorial-v1.json')
    parser.add_argument('--annotations', required=True)
    parser.add_argument('--pack', required=True, help='Path to content.json of the batch')
    parser.add_argument('--legacy-v4_1_2', action='store_true', help='Use only for frozen historical V4.1.2 artifacts')
    args = parser.parse_args()

    for p, label in [(args.schema, 'schema'), (args.curriculum, 'curriculum'), (args.pack, 'pack')]:
        if not os.path.exists(p):
            _fail(f"{label} not found: {p}")

    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        _fail("jsonschema library required")

    with open(args.schema, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    with open(args.pack, 'r', encoding='utf-8') as f:
        pack_data = json.load(f)
    editorial_modules = _load_editorial_curriculum(args.editorial_curriculum)

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
            _fail(f"ANNOTATOR_ID_MISMATCH on {source_id}: expected {envelope_annotator}, got {a.get('annotator_id')}")
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
            _fail(f"primary_module '{primary}' cannot be in acceptable_modules on {source_id}")
        if a.get('annotation_status') == 'OUT_OF_CURRICULUM':
            if a.get('in_curriculum') is not False:
                _fail(f"OUT_OF_CURRICULUM requires in_curriculum=False on {source_id}")
            if a.get('primary_module') is not None:
                _fail(f"OUT_OF_CURRICULUM requires primary_module=None on {source_id}")
            if acceptable:
                _fail(f"OUT_OF_CURRICULUM requires acceptable_modules=[] on {source_id}")

        _validate_semantic_quality(a, pack_q, editorial_modules, legacy=args.legacy_v4_1_2)
        reasoning_counter[_normalize_text(a.get('reasoning_summary', ''))] += 1

    missing_ids = set(pack_questions) - seen_ids
    if missing_ids:
        _fail(f"missing source_ids in annotations: {', '.join(sorted(missing_ids))}")

    reuse_limit = 3 if args.legacy_v4_1_2 else MAX_IDENTICAL_REASONING_REUSE
    for reasoning, count in reasoning_counter.items():
        if reasoning and count > reuse_limit:
            _fail(f"REPEATED_REASONING_TEMPLATE: identical reasoning reused {count} times (limit {reuse_limit})")

    print("ANNOTATIONS_VALID = true")
    print("ANNOTATION_QUALITY_VALID = true")
    print("SEMANTIC_BINDING_VALID = true" if not args.legacy_v4_1_2 else "LEGACY_V4_1_2_VALID = true")


if __name__ == '__main__':
    main()
