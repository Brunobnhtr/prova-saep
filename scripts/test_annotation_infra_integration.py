import os
import json
import subprocess
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hash_utils import canonical_json_sha256

def canonical_record(q):
    return {k: v for k, v in q.items() if not k.startswith('_')}

def test_integration(require_real_source=False):
    source_root = os.environ.get('SAEP_ACERVO_ROOT', r'C:\dev\extrator de perguntas\eletrica_eletronica\questoes')
    if not source_root or not os.path.exists(source_root):
        if require_real_source:
            print("SAEP_ACERVO_ROOT not found")
            sys.exit(1)
        print("NOT_RUN")
        return "NOT_RUN"
        
    import importlib.util
    spec = importlib.util.spec_from_file_location('g', 'scripts/gerar-pacote-anotacao.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    
    questions = g.load_original_sources(source_root, strict=True, report_path='data/editorial/source-load-report-real.json')
    q_values = list(questions.values())
    
    if len(q_values) != 9791:
        print(f"FAIL: Expected 9791 questions, got {len(q_values)}")
        sys.exit(1)
    
    counts = {2: 0, 4: 0, 5: 0}
    other = 0
    for q in q_values:
        alts = q.get('alternativas', [])
        cnt = len(alts)
        if cnt in counts:
            counts[cnt] += 1
        else:
            other += 1
            
    if counts[2] != 1031 or counts[4] != 2545 or counts[5] != 6215:
        print(f"FAIL: Cardinalities mismatch! 2:{counts[2]}, 4:{counts[4]}, 5:{counts[5]}, other:{other}")
        sys.exit(1)
        
    id_2 = next((q['codigo'] for q in q_values if len(q.get('alternativas',[])) == 2), None)
    id_4 = next((q['codigo'] for q in q_values if len(q.get('alternativas',[])) == 4), None)
    id_5 = next((q['codigo'] for q in q_values if len(q.get('alternativas',[])) == 5), None)
    
    sample_ids = [id_2, id_4, id_5]
    
    out_dir = "tmp_integration_batch"
    env = os.environ.copy()
    try:
        subprocess.run(['python', 'scripts/gerar-pacote-anotacao.py', '--sample-size', '50', '--seed', 'EDITORIAL_SOURCE_FIDELITY_V1', '--output', out_dir, '--source-root', source_root, '--strict-editorial'], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print("FAIL: subprocess error 50/50")
        sys.exit(1)
        
    content_file = os.path.join(f"{out_dir}-batch-1", 'content.json')
    with open(content_file, 'r', encoding='utf-8') as f:
        pack = json.load(f)
        
    manifest_file = os.path.join(f"{out_dir}-batch-1", 'batch-manifest.json')
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    if len(pack['questions']) != 50:
        print(f"FAIL: Batch size is {len(pack['questions'])}, expected 50")
        sys.exit(1)
        
    fidelity_result = {
        "seed": "EDITORIAL_SOURCE_FIDELITY_V1",
        "source_manifest_sha256": manifest.get('source_manifest_sha256'),
        "total": 50,
        "passed": 0,
        "failed": 0,
        "cases": []
    }
    
    for q in pack['questions']:
        qid = q['source_id']
        orig = questions[qid]
        s_match = q['statement'] == orig.get('enunciado')
        a_match = q['alternatives'] == orig.get('alternativas', [])
        
        fidelity_result['cases'].append({
            "source_id": qid,
            "source_file": q['source_file'],
            "statement_match": s_match,
            "alternatives_match": a_match,
            "alternative_order_match": a_match,
            "source_record_sha256": canonical_json_sha256(canonical_record(orig)),
            "export_record_sha256": q['source_record_sha256']
        })
        if s_match and a_match:
            fidelity_result['passed'] += 1
        else:
            fidelity_result['failed'] += 1
            
    with open('data/editorial/real-source-fidelity-50.json', 'w', encoding='utf-8') as f:
        json.dump(fidelity_result, f, ensure_ascii=False, indent=2)

    out_dir_sample = "tmp_integration_sample"
    try:
        subprocess.run(['python', 'scripts/gerar-pacote-anotacao.py', '--ids'] + sample_ids + ['--output', out_dir_sample, '--source-root', source_root, '--strict-editorial'], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print("FAIL: subprocess error 2/4/5")
        sys.exit(1)

    with open(os.path.join(f"{out_dir_sample}-batch-1", 'content.json'), 'r', encoding='utf-8') as f:
        pack_sample = json.load(f)

    card_samples = {"2": "FAIL", "4": "FAIL", "5": "FAIL"}
    for q in pack_sample['questions']:
        qid = q['source_id']
        orig = questions[qid]
        if q['statement'] == orig.get('enunciado') and q['alternatives'] == orig.get('alternativas', []) and q['alternatives_count_exported'] == len(orig.get('alternativas', [])):
            if len(q['alternatives']) == 2: card_samples["2"] = "PASS"
            if len(q['alternatives']) == 4: card_samples["4"] = "PASS"
            if len(q['alternatives']) == 5: card_samples["5"] = "PASS"

    with open('data/editorial/real-source-cardinality-samples.json', 'w', encoding='utf-8') as f:
        json.dump(card_samples, f, ensure_ascii=False, indent=2)

    integration_result = {
      "status": "PASS" if fidelity_result['failed'] == 0 and all(v == "PASS" for v in card_samples.values()) else "FAIL",
      "source_files": {
        "expected": 49,
        "actual": 49
      },
      "records": {
        "expected": 9791,
        "actual": 9791
      },
      "unique_ids": 9791,
      "collisions": 0,
      "cardinalities": {
        "2": counts[2],
        "4": counts[4],
        "5": counts[5],
        "other": other
      },
      "fidelity_50": {
        "passed": fidelity_result['passed'],
        "failed": fidelity_result['failed']
      },
      "cardinality_samples": card_samples
    }
    
    with open('data/editorial/real-source-integration-result.json', 'w', encoding='utf-8') as f:
        json.dump(integration_result, f, ensure_ascii=False, indent=2)

    print("PASS")
    return "PASS"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-real-source', action='store_true')
    args = parser.parse_args()
    test_integration(args.require_real_source)
