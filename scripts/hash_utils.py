import json
import hashlib

def canonical_json_bytes(data):
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

def canonical_json_sha256(data):
    h = hashlib.sha256()
    h.update(canonical_json_bytes(data))
    return h.hexdigest()
