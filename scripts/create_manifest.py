import os
import json
import hashlib
import glob

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def detect_encoding_and_load(path):
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            return 'utf-8-sig', data
    except Exception:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return 'utf-8', data

def create_manifest():
    source_root = r"C:\dev\extrator de perguntas\eletrica_eletronica\questoes"
    manifest = []
    
    files = glob.glob(os.path.join(source_root, "lote_*.json"))
    files.sort()
    
    for f in files:
        enc, data = detect_encoding_and_load(f)
        q_list = data.get('questoes', [])
        q_count = len(q_list)
        first_id = q_list[0].get('codigo') if q_count > 0 else None
        last_id = q_list[-1].get('codigo') if q_count > 0 else None
        
        manifest.append({
            "relative_path": os.path.basename(f),
            "filename": os.path.basename(f),
            "size_bytes": os.path.getsize(f),
            "sha256": get_file_sha256(f),
            "encoding_detected": enc,
            "question_count": q_count,
            "first_source_id": first_id,
            "last_source_id": last_id
        })
        
    with open('data/editorial/source-files-manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

if __name__ == '__main__':
    create_manifest()
