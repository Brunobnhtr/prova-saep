import json
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', default='data/editorial/schema-anotacao-v3.json')
    parser.add_argument('--curriculum', default='data/editorial/curriculum-editorial-authoring-input.json')
    parser.add_argument('--annotations', required=True)
    parser.add_argument('--pack', required=True, help='Path to content.json of the batch')
    args = parser.parse_args()
    
    if not os.path.exists(args.schema):
        print(f"FAIL: schema not found: {args.schema}")
        sys.exit(1)
        
    if not os.path.exists(args.curriculum):
        print(f"FAIL: curriculum not found: {args.curriculum}")
        sys.exit(1)
        
    if not os.path.exists(args.pack):
        print(f"FAIL: pack not found: {args.pack}")
        sys.exit(1)

    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        print("FAIL: jsonschema library required")
        sys.exit(1)
        
    with open(args.schema, 'r', encoding='utf-8') as f:
        schema = json.load(f)
        
    with open(args.pack, 'r', encoding='utf-8') as f:
        pack_data = json.load(f)
        
    pack_questions = {q['source_id']: q for q in pack_data.get('questions', [])}
    pack_batch_id = pack_data.get('batch_id')
        
    with open(args.annotations, 'r', encoding='utf-8') as f:
        envelope = json.load(f)
        
    if 'batch_id' not in envelope or 'annotator_id' not in envelope or 'annotations' not in envelope:
        print("FAIL: annotations file missing envelope fields (batch_id, annotator_id, annotations)")
        sys.exit(1)
        
    if envelope['batch_id'] != pack_batch_id:
        print(f"FAIL: batch_id mismatch (pack: {pack_batch_id}, annotations: {envelope['batch_id']})")
        sys.exit(1)
        
    anots = envelope['annotations']
    
    envelope_annotator = envelope['annotator_id']
    if envelope_annotator not in ['ANNOTATOR_A', 'ANNOTATOR_B', 'ADJUDICATOR']:
        print(f"FAIL: invalid annotator_id in envelope: {envelope_annotator}")
        sys.exit(1)
    
    seen_ids = set()
    for a in anots:
        source_id = a.get('source_id')
        
        if a.get('annotator_id') != envelope_annotator:
            print(f"FAIL: ANNOTATOR_ID_MISMATCH on {source_id}: expected {envelope_annotator}, got {a.get('annotator_id')}")
            sys.exit(1)
        
        # Schema validation
        try:
            validate(instance=a, schema=schema)
        except ValidationError as e:
            print(f"FAIL: validation failed on {source_id}: {e.message}")
            sys.exit(1)
            
        # Duplicate check
        if source_id in seen_ids:
            print(f"FAIL: duplicate source_id in annotations: {source_id}")
            sys.exit(1)
        seen_ids.add(source_id)
        
        # Unknown check
        if source_id not in pack_questions:
            print(f"FAIL: unknown source_id in annotations: {source_id}")
            sys.exit(1)
            
        pack_q = pack_questions[source_id]
        
        # Version checks
        if a.get('curriculum_version') != pack_data.get('curriculum_version'):
            print(f"FAIL: curriculum_version mismatch on {source_id}")
            sys.exit(1)
            
        if a.get('source_question_version') != pack_q.get('source_question_version'):
            print(f"FAIL: source_question_version mismatch on {source_id}")
            sys.exit(1)
            
        # Cross-field logic: primary_module not in acceptable_modules
        primary = a.get('primary_module')
        acceptable = a.get('acceptable_modules', [])
        if primary and primary in acceptable:
            print(f"FAIL: primary_module '{primary}' cannot be in acceptable_modules on {source_id}")
            sys.exit(1)
            
        # Cross-field logic: OUT_OF_CURRICULUM reset
        if a.get('annotation_status') == 'OUT_OF_CURRICULUM':
            if a.get('in_curriculum') is not False:
                print(f"FAIL: OUT_OF_CURRICULUM requires in_curriculum=False on {source_id}")
                sys.exit(1)
            if a.get('primary_module') is not None:
                print(f"FAIL: OUT_OF_CURRICULUM requires primary_module=None on {source_id}")
                sys.exit(1)
            if len(acceptable) > 0:
                print(f"FAIL: OUT_OF_CURRICULUM requires acceptable_modules=[] on {source_id}")
                sys.exit(1)

    # Missing check
    missing_ids = set(pack_questions.keys()) - seen_ids
    if missing_ids:
        print(f"FAIL: missing source_ids in annotations: {', '.join(missing_ids)}")
        sys.exit(1)
            
    print("ANNOTATIONS_VALID = true")

if __name__ == '__main__':
    main()
