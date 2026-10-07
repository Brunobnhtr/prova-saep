import json
import os

with open('data/editorial/curriculum-35-modules.json', 'r', encoding='utf-8') as f:
    skeleton = json.load(f)

editorial = []

for m in skeleton:
    mod = {
        "code": m['code'],
        "title": {
            "value": m['title'],
            "origin": "SOURCE_DERIVED"
        },
        "description": {
            "value": f"Editorial draft description for {m['code']}.",
            "origin": "EDITORIALLY_AUTHORED"
        },
        "learning_objectives": [
            {
                "value": f"Objective 1 for {m['code']}",
                "origin": "EDITORIALLY_AUTHORED"
            }
        ],
        "subtopics": [
            {
                "value": f"{m['code']}.1 Draft subtopic",
                "origin": "EDITORIALLY_AUTHORED"
            }
        ],
        "prerequisites": {
            "value": m['prerequisites'],
            "origin": "SOURCE_DERIVED"
        },
        "includes": [
            {
                "value": f"Core topics of {m['code']}",
                "origin": "EDITORIALLY_AUTHORED"
            }
        ],
        "excludes": [
            {
                "value": f"Topics belonging to neighboring modules",
                "origin": "EDITORIALLY_AUTHORED"
            }
        ],
        "overlaps_with": [],
        "classification_examples": [
            {
                "value": f"Sample question directly addressing {m['code']}.",
                "module": m['code'],
                "origin": "EDITORIALLY_AUTHORED"
            }
        ],
        "classification_counterexamples": []
    }
    
    # Generate some draft overlaps if F02/F03 etc.
    if m['code'] == 'F02':
        mod['overlaps_with'].append({
            "module": "F03",
            "boundary_rule": {
                "value": "resistores puramente ôhmicos e CC -> F02; reatância/impedância/fase/RLC CA -> F03",
                "origin": "EDITORIALLY_AUTHORED"
            }
        })
        mod['classification_counterexamples'].append({
            "value": "Calcule a impedância de um circuito RLC série em 60 Hz.",
            "points_to": "F03",
            "origin": "EDITORIALLY_AUTHORED"
        })
    elif m['code'] == 'S01':
        mod['overlaps_with'].append({
            "module": "S02",
            "boundary_rule": {
                "value": "Desenergização/reenergização (bloqueio, teste de tensão) -> S01; Zonas de risco, altura, EPI -> S02",
                "origin": "EDITORIALLY_AUTHORED"
            }
        })

    editorial.append(mod)

with open('data/editorial/curriculum-35-modules-editorial-v1.json', 'w', encoding='utf-8') as f:
    json.dump(editorial, f, ensure_ascii=False, indent=2)

print("Generated curriculum-35-modules-editorial-v1.json")
