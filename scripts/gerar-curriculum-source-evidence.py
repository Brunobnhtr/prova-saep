import json
import os
import re

evidence = []

source_files = [
    "data/extraidos/plano-eletrotecnica-ce-2016.txt",
    "data/extraidos/plano-eletrotecnica-rr-semipresencial.txt"
]

modules = {
    "F01": ["Eletricidade Básica", "Grandezas fundamentais", "corrente", "tensão"],
    "F02": ["Circuitos de Corrente Contínua", "Ohm", "Kirchhoff", "associação"],
    "F03": ["Circuitos de Corrente Alternada", "impedância", "reatância", "fasores"],
    "F04": ["Eletromagnetismo", "campo magnético", "indução", "Faraday"]
}

for sf in source_files:
    if not os.path.exists(sf): continue
    with open(sf, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for mod, terms in modules.items():
            for term in terms:
                if term.lower() in line_lower:
                    evidence.append({
                        "module": mod,
                        "source_file": sf,
                        "line": i + 1,
                        "matched_text": line.strip()[:200],
                        "kind": "MODULE_DEFINITION" if "objetivo" in line_lower or "ementa" in line_lower else "PREREQUISITE_REFERENCE"
                    })
                    break

with open('data/editorial/curriculum-source-evidence.json', 'w', encoding='utf-8') as f:
    json.dump(evidence, f, ensure_ascii=False, indent=2)
