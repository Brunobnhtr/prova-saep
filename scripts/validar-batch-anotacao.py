import argparse
import json
import os
import hashlib
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hash_utils import canonical_json_sha256

def get_file_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-dir', required=True)
    args = parser.parse_args()
    
    bd = args.batch_dir
    man_path = os.path.join(bd, 'batch-manifest.json')
    if not os.path.exists(man_path):
        print("FAIL: batch-manifest.json missing")
        sys.exit(1)
        
    with open(man_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    for file, key in [('content.json', 'content_sha256'), ('supplement.json', 'supplement_sha256')]:
        path = os.path.join(bd, file)
        if not os.path.exists(path):
            print(f"FAIL: {file} missing")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        calc_sha = canonical_json_sha256(data)
        if calc_sha != manifest[key]:
            print(f"FAIL: {file} hash mismatch. Expected {manifest[key]} got {calc_sha}")
            sys.exit(1)
            
    img_man_path = os.path.join(bd, 'images-manifest.json')
    if os.path.exists(img_man_path):
        if not manifest.get('images_manifest_sha256'):
            print("FAIL: images-manifest.json exists but not tracked in batch-manifest.json")
            sys.exit(1)
        with open(img_man_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        calc_sha = canonical_json_sha256(data)
        if calc_sha != manifest['images_manifest_sha256']:
            print("FAIL: images-manifest.json hash mismatch")
            sys.exit(1)
            
        for img in data:
            port_path = os.path.join(bd, img['portable_path'])
            if not os.path.exists(port_path):
                print(f"FAIL: Image file missing: {port_path}")
                sys.exit(1)
            f_sha = get_file_sha256(port_path)
            if f_sha != img['sha256']:
                print(f"FAIL: Image hash mismatch for {port_path}")
                sys.exit(1)
                
    curr_file = 'data/editorial/curriculum-editorial-authoring-input.json'
    if os.path.exists(curr_file):
        calc = get_file_sha256(curr_file)
        if manifest.get('curriculum_sha256') and calc != manifest['curriculum_sha256']:
            print("FAIL: curriculum_sha256 mismatch against active curriculum file")
            sys.exit(1)
            
    sm_file = 'data/editorial/source-files-manifest.json'
    if os.path.exists(sm_file):
        with open(sm_file, 'r', encoding='utf-8') as f:
            sm_data = json.load(f)
        calc = canonical_json_sha256(sm_data)
        if manifest.get('source_manifest_sha256') and calc != manifest['source_manifest_sha256']:
            print("FAIL: source_manifest_sha256 mismatch against active source manifest")
            sys.exit(1)
            
    print("MANIFEST_VALID = true")

if __name__ == '__main__':
    main()
