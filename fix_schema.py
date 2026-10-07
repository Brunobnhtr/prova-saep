import json
with open('data/editorial/curriculum-35-modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)
module_codes = [m['code'] for m in modules]

with open('data/editorial/schema-anotacao-v3.json', 'r', encoding='utf-8') as f:
    schema = json.load(f)

schema['properties']['acceptable_modules']['items']['enum'] = module_codes
schema['properties']['primary_module']['enum'] = module_codes + [None]

with open('data/editorial/schema-anotacao-v3.json', 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
