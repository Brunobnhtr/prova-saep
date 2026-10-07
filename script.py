import json
with open('data/editorial/curriculum-35-modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)

md = '# Curriculum 35 Modules Audit\n\n'
md += '| Module | Title | Objectives | Subtopics | Prerequisites | Sources | Gaps |\n'
md += '|---|---|---:|---:|---:|---:|---|\n'

for m in modules:
    gaps = 'DOCUMENTATION_GAP' if m.get('needs_editorial_definition') else 'OK'
    md += f"| {m['code']} | {m['title']} | {len(m['learning_objectives'])} | {len(m['subtopics'])} | {len(m['prerequisites'])} | {len(m['source_refs'])} | {gaps} |\n"

with open('docs/curriculum-35-modules-audit.md', 'w', encoding='utf-8') as f:
    f.write(md)
