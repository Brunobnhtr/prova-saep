import json
import argparse
import random
import hashlib
import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hash_utils import canonical_json_sha256

class SourceFidelityError(Exception):
    pass

def stable_seed(seed_text):
    digest = hashlib.sha256(seed_text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")

def get_file_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def get_content_sha256(data):
    return canonical_json_sha256(data)

def get_record_canonical_sha256(q_record):
    clean_record = {k: v for k, v in q_record.items() if not k.startswith('_')}
    return canonical_json_sha256(clean_record)

def load_original_sources(source_root, strict, report_path=None):
    if not source_root or not os.path.exists(source_root):
        if strict:
            raise Exception(f"Strict mode: source_root {source_root} not found.")
        return {}
    
    questions = {}
    collisions = []
    
    report = {
        'source_root': source_root,
        'files_discovered': 0,
        'files_loaded': 0,
        'files_failed': 0,
        'records_loaded': 0,
        'unique_ids': 0,
        'collisions': 0,
        'parse_errors': [],
        'encoding_per_file': {},
        'cardinality_counts': {2: 0, 4: 0, 5: 0}
    }
    
    for root, _, files in os.walk(source_root):
        for file in files:
            if not file.startswith('lote_') or not file.endswith('.json'):
                continue
            report['files_discovered'] += 1
            path = os.path.join(root, file)
            
            loaded = False
            try:
                with open(path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                report['encoding_per_file'][file] = 'utf-8-sig'
                loaded = True
            except Exception as e:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    report['encoding_per_file'][file] = 'utf-8'
                    loaded = True
                except Exception as e2:
                    report['parse_errors'].append(f"Failed to parse {path}: {e2}")
                    report['files_failed'] += 1
                    if strict:
                        raise Exception(f"Failed to parse {path}: {e2}")
                    
            if loaded:
                questions_found = 0
                if isinstance(data, dict) and 'questoes' in data:
                    for q in data['questoes']:
                        if 'codigo' in q:
                            qid = q['codigo']
                            if qid in questions:
                                collisions.append((qid, questions[qid]['_source_file'], path))
                                report['collisions'] += 1
                                if strict:
                                    raise Exception(f"SOURCE_ID_COLLISION: {qid} in {questions[qid]['_source_file']} and {path}")
                            else:
                                q['_source_file'] = path
                                questions[qid] = q
                                questions_found += 1
                                
                                alts = q.get('alternativas', [])
                                cnt = len(alts)
                                if cnt not in report['cardinality_counts']:
                                    report['cardinality_counts'][cnt] = 0
                                report['cardinality_counts'][cnt] += 1
                
                if questions_found > 0:
                    report['files_loaded'] += 1
                    report['records_loaded'] += questions_found
    
    report['unique_ids'] = len(questions)
    if report_path:
        os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
    return questions

def get_image_format(path):
    ext = path.split('.')[-1].lower() if '.' in path else 'unknown'
    return ext

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', help='List of IDs to include')
    parser.add_argument('--sample-size', type=int, help='Random sample size')
    parser.add_argument('--seed', type=str, help='Seed string for sampling')
    parser.add_argument('--output', required=True, help='Output prefix / directory')
    parser.add_argument('--source-root', default=os.environ.get('SAEP_ACERVO_ROOT'), help='Root path to original lots')
    parser.add_argument('--curriculum', default='data/editorial/curriculum-editorial-authoring-input.json', help='Curriculum path')
    parser.add_argument('--strict-editorial', action='store_true', help='Fail on broken images or missing source root')
    parser.add_argument('--report-path', default=None, help='Path to save load report')
    parser.add_argument('--source-mode', choices=['REAL', 'MOCK'], default='REAL', help='Source mode (REAL or MOCK)')
    args = parser.parse_args()

    if args.strict_editorial and (not args.source_root or not os.path.exists(args.source_root)):
        raise Exception("source root required in strict editorial mode")

    report_path = args.report_path
    if not report_path:
        report_path = f"{args.output}-source-load-report.json"

    original_sources = load_original_sources(args.source_root, strict=args.strict_editorial, report_path=report_path)
    
    available_ids = list(original_sources.keys())
    available_ids.sort()
    
    selected_ids = []
    if args.ids:
        selected_ids = [i for i in args.ids if i in available_ids]
        if not selected_ids and args.source_mode == 'MOCK': # MOCK behavior for dry-run without real lots
            selected_ids = args.ids
    elif args.sample_size:
        rng = random.Random(stable_seed(args.seed)) if args.seed else random.Random()
        if args.sample_size > len(available_ids):
            selected_ids = available_ids
        else:
            rng.shuffle(available_ids)
            selected_ids = available_ids[:args.sample_size]

    curr_sha = get_file_sha256(args.curriculum) if os.path.exists(args.curriculum) else "dummy_sha"
    
    manifest_path = 'data/editorial/source-files-manifest.json'
    source_manifest_sha = None
    if args.source_mode != 'MOCK':
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as mf:
                source_manifest_sha = canonical_json_sha256(json.load(mf))
    
    # Load image manifest
    image_manifest_path = 'data/editorial/image-manifest.json'
    image_manifest_data = {}
    if os.path.exists(image_manifest_path):
        with open(image_manifest_path, 'r', encoding='utf-8') as f:
            try:
                manifest_list = json.load(f)
                for item in manifest_list:
                    image_manifest_data[item.get('source_id')] = item
            except:
                pass
    
    batch_index = 1
    out_dir = Path(args.output)
    if not out_dir.exists():
        out_dir = Path(f"{args.output}-batch-{batch_index}")
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)
    
    pack_a = {
        'batch_id': out_dir.name,
        'source_mode': args.source_mode,
        'sample_seed': args.seed,
        'question_ids': selected_ids,
        'curriculum_version': '1.0',
        'curriculum_sha256': curr_sha,
        'source_manifest_sha256': source_manifest_sha,
        'questions': []
    }
    
    pack_b = {
        'batch_id': out_dir.name,
        'questions': []
    }
    
    images_manifest = []

    for qid in selected_ids:
        orig_q = original_sources.get(qid, {})
        if not orig_q and args.strict_editorial and args.source_mode != 'MOCK':
            raise Exception(f"Question {qid} not found in strict mode")

        statement = orig_q.get('enunciado', 'MOCK STATEMENT')
        alternatives = orig_q.get('alternativas', ['A','B'])
        
        orig_img_refs = orig_q.get('imagens', [])
        exported_img_refs = []
        
        for idx, ref in enumerate(orig_img_refs):
            img_path = ref.get('path', ref) if isinstance(ref, dict) else ref
            if not isinstance(img_path, str): continue
            
            basename = os.path.basename(img_path)
            fname = f"{qid}_{idx}_{basename}"
            target_path = img_dir / fname
            
            search_paths = [img_path]
            if not os.path.isabs(img_path) and args.source_root:
                search_paths.append(os.path.join(args.source_root, img_path))
            
            found_path = None
            for sp in search_paths:
                if os.path.exists(sp):
                    found_path = sp
                    break
            
            if found_path:
                shutil.copy2(found_path, target_path)
                try:
                    with Image.open(target_path) as img:
                        img.verify()
                    is_loadable = True
                except Exception:
                    is_loadable = False

                if not is_loadable and args.strict_editorial:
                    raise Exception(f"Image {found_path} is corrupt or unloadable")

                img_sha = get_file_sha256(target_path)
                images_manifest.append({
                    'source_id': qid,
                    'source_path': img_path,
                    'portable_path': f"images/{fname}",
                    'sha256': img_sha,
                    'size_bytes': os.path.getsize(target_path),
                    'format': get_image_format(fname),
                    'loadable': is_loadable
                })
                exported_img_refs.append(f"images/{fname}")
            else:
                if args.strict_editorial:
                    raise Exception(f"Missing image {img_path} for {qid}")
                exported_img_refs.append({ "error": "missing_image", "original_path": img_path })

        source_file = orig_q.get('_source_file', 'unknown')
        
        img_info = image_manifest_data.get(qid, {})
        has_image = img_info.get('has_image', len(exported_img_refs) > 0)
        image_inventory_status = img_info.get('image_inventory_status', 'AVAILABLE' if len(exported_img_refs) > 0 else 'NOT_APPLICABLE')

        pack_a['questions'].append({
            'source_id': qid,
            'source_file': os.path.basename(source_file),
            'source_file_sha256': get_file_sha256(source_file),
            'source_record_sha256': get_record_canonical_sha256(orig_q) if orig_q else None,
            'statement': statement,
            'alternatives': alternatives,
            'alternatives_count_source': len(alternatives),
            'alternatives_count_exported': len(alternatives),
            'image_refs': exported_img_refs,
            'has_image': has_image,
            'image_inventory_status': image_inventory_status,
            'source_question_version': '1.0'
        })
        
        pack_b['questions'].append({
            'source_id': qid,
            'current_theme': orig_q.get('assunto', ''),
            'prior_topics': [],
            'source_origin': source_file,
        })
        
    with open(out_dir / "content.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(pack_a, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        
    with open(out_dir / "supplement.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(pack_b, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        
    if images_manifest:
        with open(out_dir / "images-manifest.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(images_manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        
    manifest = {
        'batch_id': out_dir.name,
        'created_at': datetime.now().isoformat(),
        'source_mode': args.source_mode,
        'sample_seed': args.seed,
        'curriculum_version': '1.0',
        'curriculum_sha256': curr_sha,
        'source_manifest_sha256': source_manifest_sha,
        'question_ids': selected_ids,
        'content_sha256': get_content_sha256(pack_a),
        'supplement_sha256': get_content_sha256(pack_b),
        'images_manifest_sha256': get_content_sha256(images_manifest) if images_manifest else None
    }
    
    with open(out_dir / "batch-manifest.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

if __name__ == '__main__':
    main()
