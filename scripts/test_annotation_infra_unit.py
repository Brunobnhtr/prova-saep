import json
import os
import subprocess
import copy
import tempfile
import sys
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hash_utils import canonical_json_sha256

def test_curriculum():
    path = 'data/editorial/curriculum-editorial-authoring-input.json'
    if not os.path.exists(path):
        assert False, f"Curriculum input not found at {path}"
    with open(path, 'r', encoding='utf-8') as f:
        modules = json.load(f)
    assert len(modules) == 35, "Must be 35 modules"
    codes = set()
    for m in modules:
        assert m['title'], "Title must not be empty"
        assert 'code' in m
        codes.add(m['code'])
    assert len(codes) == 35, "Must be 35 unique codes"
    for m in modules:
        for p in m['prerequisites']:
            assert p in codes, f"Unknown prereq {p} in {m['code']}"
            assert p != m['code'], f"Self prerequisite in {m['code']}"

def test_cross_process_seed():
    code = "import sys; sys.path.append('scripts'); import importlib.util; spec=importlib.util.spec_from_file_location('g', 'scripts/gerar-pacote-anotacao.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g); print(g.stable_seed('cross_test'))"
    out1 = subprocess.check_output(['python', '-c', code]).decode().strip()
    out2 = subprocess.check_output(['python', '-c', code]).decode().strip()
    assert out1 == out2, f"Cross process seed failed: {out1} != {out2}"

def test_pt_hash():
    data = {
      "texto": "tensão elétrica",
      "opcoes": ["não", "sim"]
    }
    h = canonical_json_sha256(data)
    import hashlib
    b = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert h == hashlib.sha256(b).hexdigest()

def test_negative_manifest():
    with tempfile.TemporaryDirectory() as td:
        source_dir = os.path.join(td, 'source')
        os.mkdir(source_dir)
        mock_data = {"questoes": [{"codigo": "MOCK2", "enunciado": "B?", "alternativas": ["c","d"]}]}
        with open(os.path.join(source_dir, 'lote_mock.json'), 'w', encoding='utf-8') as f:
            json.dump(mock_data, f)
            
        out_dir = os.path.join(td, 'out')
        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out_dir, '--source-root', source_dir, '--ids', 'MOCK2'])
        
        batch_dir = f"{out_dir}-batch-1"
        
        cfile = os.path.join(batch_dir, 'content.json')
        with open(cfile, 'r', encoding='utf-8') as f:
            pack = json.load(f)
        pack['questions'][0]['statement'] = "Hacked content!"
        with open(cfile, 'w', encoding='utf-8') as f:
            f.write(json.dumps(pack, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
            
        try:
            subprocess.check_output(['python', 'scripts/validar-batch-anotacao.py', '--batch-dir', batch_dir], stderr=subprocess.STDOUT)
            assert False, "Validation should have failed due to modified content.json"
        except subprocess.CalledProcessError:
            pass

        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out_dir, '--source-root', source_dir, '--ids', 'MOCK2'])
        
        sfile = os.path.join(batch_dir, 'supplement.json')
        with open(sfile, 'r', encoding='utf-8') as f:
            supp = json.load(f)
        supp['questions'][0]['current_theme'] = "Hacked theme!"
        with open(sfile, 'w', encoding='utf-8') as f:
            f.write(json.dumps(supp, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

        try:
            subprocess.check_output(['python', 'scripts/validar-batch-anotacao.py', '--batch-dir', batch_dir], stderr=subprocess.STDOUT)
            assert False, "Validation should have failed due to modified supplement.json"
        except subprocess.CalledProcessError:
            pass

def test_negative_image_manifest():
    with tempfile.TemporaryDirectory() as td:
        source_dir = os.path.join(td, 'source')
        os.mkdir(source_dir)
        
        img_path = os.path.join(source_dir, "test.png")
        img = Image.new('RGB', (10, 10))
        img.save(img_path)
        
        mock_data = {"questoes": [{"codigo": "MOCK3", "enunciado": "C?", "alternativas": ["e"], "imagens": [img_path]}]}
        with open(os.path.join(source_dir, 'lote_mock.json'), 'w', encoding='utf-8') as f:
            json.dump(mock_data, f)
            
        out_dir = os.path.join(td, 'out')
        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out_dir, '--source-root', source_dir, '--ids', 'MOCK3'])
        
        batch_dir = f"{out_dir}-batch-1"
        
        im_file = os.path.join(batch_dir, 'images-manifest.json')
        with open(im_file, 'r', encoding='utf-8') as f:
            iman = json.load(f)
        iman[0]['size_bytes'] = 999
        with open(im_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(iman, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
            
        try:
            subprocess.check_output(['python', 'scripts/validar-batch-anotacao.py', '--batch-dir', batch_dir], stderr=subprocess.STDOUT)
            assert False, "Validation should have failed due to modified images-manifest.json"
        except subprocess.CalledProcessError:
            pass

        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out_dir, '--source-root', source_dir, '--ids', 'MOCK3'])
        
        port_img = os.path.join(batch_dir, iman[0]['portable_path'])
        with open(port_img, 'ab') as f:
            f.write(b"corrupt")
            
        try:
            subprocess.check_output(['python', 'scripts/validar-batch-anotacao.py', '--batch-dir', batch_dir], stderr=subprocess.STDOUT)
            assert False, "Validation should have failed due to modified image file"
        except subprocess.CalledProcessError:
            pass

def test_record_hash_independent():
    with tempfile.TemporaryDirectory() as td:
        dir1 = os.path.join(td, 'd1')
        dir2 = os.path.join(td, 'd2')
        os.mkdir(dir1)
        os.mkdir(dir2)
        q = {"codigo": "ID1", "enunciado": "A?"}
        
        with open(os.path.join(dir1, 'lote_1.json'), 'w', encoding='utf-8') as f:
            json.dump({"questoes": [q]}, f)
        with open(os.path.join(dir2, 'lote_2.json'), 'w', encoding='utf-8') as f:
            json.dump({"questoes": [q]}, f)
            
        out1 = os.path.join(td, 'o1')
        out2 = os.path.join(td, 'o2')
        
        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out1, '--source-root', dir1, '--ids', 'ID1'])
        subprocess.check_call(['python', 'scripts/gerar-pacote-anotacao.py', '--output', out2, '--source-root', dir2, '--ids', 'ID1'])
        
        with open(os.path.join(f"{out1}-batch-1", 'content.json'), 'r', encoding='utf-8') as f:
            p1 = json.load(f)
        with open(os.path.join(f"{out2}-batch-1", 'content.json'), 'r', encoding='utf-8') as f:
            p2 = json.load(f)
            
        assert p1['questions'][0]['source_record_sha256'] == p2['questions'][0]['source_record_sha256']

def test_validar_anotacoes():
    with tempfile.TemporaryDirectory() as td:
        schema_path = 'data/editorial/schema-anotacao-v3.json'
        curr_path = 'data/editorial/curriculum-editorial-authoring-input.json'
        
        pack_path = os.path.join(td, 'content.json')
        pack_data = {
            'batch_id': 'batch-1',
            'curriculum_version': '1.0',
            'questions': [
                {'source_id': 'Q1', 'source_question_version': '1.0', 'statement': 'A corrente elétrica é medida em ampères e deve ser identificada corretamente.', 'has_image': False, 'image_inventory_status': 'NOT_APPLICABLE'},
                {'source_id': 'Q2', 'source_question_version': '1.0', 'statement': 'A corrente elétrica é medida em ampères e deve ser identificada corretamente.', 'has_image': False, 'image_inventory_status': 'NOT_APPLICABLE'}
            ]
        }
        with open(pack_path, 'w', encoding='utf-8') as f:
            json.dump(pack_data, f)
            
        def run_val(anots_data):
            apath = os.path.join(td, 'anots.json')
            with open(apath, 'w', encoding='utf-8') as f:
                json.dump(anots_data, f)
            return subprocess.run([sys.executable, 'scripts/validar-anotacoes.py', '--schema', schema_path, '--curriculum', curr_path, '--pack', pack_path, '--annotations', apath], capture_output=True, text=True)

        base_annot = {
            "annotation_version": "1.0",
            "curriculum_version": "1.0",
            "source_question_version": "1.0",
            "annotator_id": "ANNOTATOR_A",
            "in_curriculum": True,
            "primary_module": "F01",
            "acceptable_modules": [],
            "annotation_confidence": "HIGH",
            "reasoning_summary": "O enunciado pede reconhecer a corrente elétrica e sua unidade; isso corresponde ao subtema Corrente elétrica do módulo F01 de grandezas e unidades.",
            "image_status": "NOT_APPLICABLE",
            "image_required": False,
            "ambiguity": False,
            "ambiguity_reason": "",
            "supplement_used": False,
            "supplement_fields_used": [],
            "annotation_status": "ANNOTATED",
            "module_evidence": [
                {"kind": "STATEMENT", "text": "A corrente elétrica é medida em ampères"},
                {"kind": "CURRICULUM_SUBTOPIC", "module": "F01", "subtopic": "Corrente elétrica"}
            ]
        }
        
        # 1. positive
        env = {
            "batch_id": "batch-1",
            "annotator_id": "ANNOTATOR_A",
            "annotations": [
                {**base_annot, "source_id": "Q1"},
                {**base_annot, "source_id": "Q2"}
            ]
        }
        res = run_val(env)
        assert res.returncode == 0, f"Positive test failed: {res.stdout} {res.stderr}"
        
        # 2. duplicate ID
        env_dup = {**env, "annotations": [{**base_annot, "source_id": "Q1"}, {**base_annot, "source_id": "Q1"}]}
        res = run_val(env_dup)
        assert res.returncode != 0 and "duplicate" in res.stdout
        
        # 3. unknown ID
        env_unk = {**env, "annotations": [{**base_annot, "source_id": "Q1"}, {**base_annot, "source_id": "Q3"}]}
        res = run_val(env_unk)
        assert res.returncode != 0 and "unknown" in res.stdout
        
        # 4. missing ID
        env_mis = {**env, "annotations": [{**base_annot, "source_id": "Q1"}]}
        res = run_val(env_mis)
        assert res.returncode != 0 and "missing" in res.stdout
        
        # 5. primary in acceptable
        env_pia = {**env, "annotations": [
            {**base_annot, "source_id": "Q1", "primary_module": "F01", "acceptable_modules": ["F01"]},
            {**base_annot, "source_id": "Q2"}
        ]}
        res = run_val(env_pia)
        assert res.returncode != 0 and "acceptable_modules" in res.stdout
        
        # 6. version mismatch (curriculum)
        env_vm = {**env, "annotations": [
            {**base_annot, "source_id": "Q1", "curriculum_version": "2.0"},
            {**base_annot, "source_id": "Q2"}
        ]}
        res = run_val(env_vm)
        assert res.returncode != 0 and "curriculum_version mismatch" in res.stdout
        
        # 7. source question version mismatch
        env_svm = {**env, "annotations": [
            {**base_annot, "source_id": "Q1", "source_question_version": "2.0"},
            {**base_annot, "source_id": "Q2"}
        ]}
        res = run_val(env_svm)
        assert res.returncode != 0 and "source_question_version mismatch" in res.stdout

def test_reference_missing_preservation():
    # 8. reference missing preservation
    with tempfile.TemporaryDirectory() as td:
        source_dir = os.path.join(td, 'source')
        os.mkdir(source_dir)
        mock_data = {"questoes": [{"codigo": "MOCK_REF", "enunciado": "B?", "alternativas": ["c"], "imagens": ["does_not_exist.jpg"]}]}
        with open(os.path.join(source_dir, 'lote_mock.json'), 'w', encoding='utf-8') as f:
            json.dump(mock_data, f)
            
        im_manifest_path = 'data/editorial/image-manifest.json'
        backup_im = None
        if os.path.exists(im_manifest_path):
            with open(im_manifest_path, 'r', encoding='utf-8') as f:
                backup_im = f.read()
        
        try:
            with open(im_manifest_path, 'w', encoding='utf-8') as f:
                json.dump([{"source_id": "MOCK_REF", "has_image": True, "image_inventory_status": "REFERENCE_MISSING"}], f)
                
            out_dir = os.path.join(td, 'out')
            subprocess.check_call([sys.executable, 'scripts/gerar-pacote-anotacao.py', '--output', out_dir, '--source-root', source_dir, '--ids', 'MOCK_REF', '--source-mode', 'MOCK'])
            
            cfile = os.path.join(f"{out_dir}-batch-1", 'content.json')
            with open(cfile, 'r', encoding='utf-8') as f:
                pack = json.load(f)
                
            q = pack['questions'][0]
            assert q['has_image'] is True, "has_image should be True due to image-manifest"
            assert q['image_inventory_status'] == "REFERENCE_MISSING", "status should be REFERENCE_MISSING"
        finally:
            if backup_im is not None:
                with open(im_manifest_path, 'w', encoding='utf-8') as f:
                    f.write(backup_im)
            else:
                if os.path.exists(im_manifest_path):
                    os.remove(im_manifest_path)

def run_tests():
    test_curriculum()
    test_cross_process_seed()
    test_pt_hash()
    test_negative_manifest()
    test_negative_image_manifest()
    test_record_hash_independent()
    test_validar_anotacoes()
    test_reference_missing_preservation()
    print("ALL UNIT TESTS PASSED")

if __name__ == '__main__':
    run_tests()
