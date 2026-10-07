import json
with open('data/acervo-ampliado/catalogo-global-v2_2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    if q.get('alternatives_count', 0) > 0 and len(q.get('alternativas', [])) == 0 and len(q.get('alternatives', [])) == 0:
        print(f"ID: {q['source_id']}, count: {q.get('alternatives_count')}")
        break
