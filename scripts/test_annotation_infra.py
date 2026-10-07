import json
import os
import subprocess
import copy
from jsonschema import validate, ValidationError

def test_curriculum():
    with open('data/editorial/curriculum-35-modules.json', 'r', encoding='utf-8') as f:
        modules = json.load(f)
    assert len(modules) == 35, "Must be 35 modules"
    codes = [m['code'] for m in modules]
    assert len(set(codes)) == 35, "Must be unique codes"
    for m in modules:
        assert m['code'], "Code must not be empty"
        assert m['title'], "Title must not be empty"
        assert m.get('needs_editorial_definition') is True, "Must explicitly need editorial definition"
        for p in m['prerequisites']:
            assert p in codes, f"Unknown prereq {p} in {m['code']}"
            assert p != m['code'], f"Self prerequisite in {m['code']}"

def test_cross_process_seed():
    code = "import sys; sys.path.append('scripts'); import importlib.util; spec=importlib.util.spec_from_file_location('g', 'scripts/gerar-pacote-anotacao.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g); print(g.stable_seed('cross_test'))"
    out1 = subprocess.check_output(['python', '-c', code]).decode().strip()
    out2 = subprocess.check_output(['python', '-c', code]).decode().strip()
    assert out1 == out2, f"Cross process seed failed: {out1} != {out2}"
    
    # Executing the generator script twice with same parameters
    env = os.environ.copy()
    env["SAEP_CATALOG_OVERRIDE"] = "tmp_cat.json"
    subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--ids', 'Q2_ALTS', 'Q4_ALTS', 'Q5_ALTS', '--output', 'tmp_fidelity_a', '--source-root', 'tmp_source_lots', '--strict-source'], env=env)
    subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--ids', 'Q2_ALTS', 'Q4_ALTS', 'Q5_ALTS', '--output', 'tmp_fidelity_b', '--source-root', 'tmp_source_lots', '--strict-source'], env=env)
    
    with open('tmp_fidelity_a-batch-1/content.json', 'r', encoding='utf-8') as f:
        pa = json.load(f)
    with open('tmp_fidelity_b-batch-1/content.json', 'r', encoding='utf-8') as f:
        pb = json.load(f)
    assert pa['question_ids'] == pb['question_ids']

def test_leakage():
    # We use the fidelity output which we know is created
    def check_dict(d):
        bad_keys = ['primary_module', 'primary_concept', 'semantic_family', 'theme_classification_confidence', 'unclassified_reason', 'module_candidates', 'classification_evidence', 'predicted_module', 'interaction_candidate', 'inspection_priority']
        for k, v in d.items():
            assert k not in bad_keys, f"Leakage detected: {k}"
            if isinstance(v, dict):
                check_dict(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        check_dict(item)

    with open('tmp_fidelity_a-batch-1/content.json', 'r', encoding='utf-8') as f:
        pack = json.load(f)
        check_dict(pack)

    with open('tmp_fidelity_a-batch-1/supplement.json', 'r', encoding='utf-8') as f:
        supp = json.load(f)
        check_dict(supp)

def test_schema_rules():
    with open('data/editorial/schema-anotacao-v3.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)

    valid_base = {
        "source_id": "Q123", "annotation_version": "1.0", "curriculum_version": "1.0",
        "source_question_version": "1.0", "annotator_id": "ANNOTATOR_A",
        "in_curriculum": True, "primary_module": "F01", "acceptable_modules": [],
        "annotation_confidence": "HIGH", "reasoning_summary": "valid reasoning ok",
        "image_status": "AVAILABLE", "image_required": False, "ambiguity": False,
        "ambiguity_reason": "", "supplement_used": False, "supplement_fields_used": [],
        "annotation_status": "ANNOTATED",
        "module_evidence": [{"kind": "STATEMENT", "text": "foo"}]
    }
    
    validate(instance=valid_base, schema=schema)

    def check_invalid(mod):
        c = copy.deepcopy(valid_base)
        c.update(mod)
        try:
            validate(instance=c, schema=schema)
            assert False, f"Expected validation to fail for {mod}"
        except ValidationError:
            pass

    check_invalid({"primary_module": None})
    check_invalid({"annotation_status": "OUT_OF_CURRICULUM", "primary_module": "F01"})
    check_invalid({"annotation_status": "AMBIGUOUS", "ambiguity": False})
    check_invalid({"supplement_used": False, "supplement_fields_used": ["foo"]})
    check_invalid({"acceptable_modules": ["F01", "UNKNOWN"]})
    check_invalid({"acceptable_modules": ["F02", "F02"]}) # duplicate
    check_invalid({"annotation_status": "ANNOTATED", "module_evidence": []})
    check_invalid({"annotation_status": "ANNOTATED", "reasoning_summary": ""})
    check_invalid({"supplement_used": True, "supplement_fields_used": []})

def test_source_fidelity():
    with open('tmp_fidelity_a-batch-1/content.json', 'r', encoding='utf-8') as f:
        pack = json.load(f)
        
    for q in pack['questions']:
        if q['source_id'] == 'Q2_ALTS':
            assert q['alternatives_count_exported'] == 2
            assert q['alternatives'] == ["A", "B"]
            assert q['statement'] == "A and B?"
        elif q['source_id'] == 'Q4_ALTS':
            assert q['alternatives_count_exported'] == 4
        elif q['source_id'] == 'Q5_ALTS':
            assert q['alternatives_count_exported'] == 5
            
def run_tests():
    test_curriculum()
    test_cross_process_seed()
    test_leakage()
    try:
        import jsonschema
        test_schema_rules()
    except ImportError:
        pass
    test_source_fidelity()
    print("ALL TESTS PASSED")

if __name__ == '__main__':
    run_tests()
