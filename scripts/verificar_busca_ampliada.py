import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
report = (root / 'docs/01-busca-ampliada.md').read_text(encoding='utf-8')
candidates = []
for line in report.splitlines():
    if line.startswith('| ['):
        cells = line.strip('|').split('|')
        match = re.search(r'\[([^\]]+)\]\((https://[^)]+)\)', cells[0])
        if match:
            candidates.append({'titulo': match[1], 'url': match[2], 'natureza': cells[1].strip(), 'acesso': cells[2].strip(), 'pdf_obtido': False})
registry = {'data': '2026-10-02', 'escopo': 'Busca ampliada em sites públicos; cobertura não exaustiva.', 'candidatos': candidates}
(root / 'data/provas/busca-ampliada/registro-buscas.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
inventory = json.loads((root / 'data/livros/inventario.json').read_text(encoding='utf-8'))
errors = []
books = inventory['livros']
for book in books:
    source = Path(book['origem'])
    if hashlib.file_digest(source.open('rb'), 'sha256').hexdigest() != book['sha256']:
        errors.append('Hash divergente: ' + book['id'])
    extracted = root / book['extracao']
    json.loads(extracted.read_text(encoding='utf-8'))
manifest = json.loads((root / 'data/provas/busca-ampliada/manifesto.json').read_text(encoding='utf-8'))
import fitz
for item in manifest['documentos']:
    if item['status'] == 'baixado':
        file = root / item['arquivo']
        if hashlib.file_digest(file.open('rb'), 'sha256').hexdigest() != item['sha256']:
            errors.append('Hash divergente: ' + item['arquivo'])
        with fitz.open(file) as pdf:
            if len(pdf) != item['paginas']:
                errors.append('Páginas divergentes: ' + item['arquivo'])
result = {'data': '2026-10-02', 'livros_verificados': len(books), 'paginas_livros': sum(b['paginas'] for b in books), 'hashes_distintos': len({b['sha256'] for b in books}), 'extracoes_json_validas': len(books), 'candidatos_registrados': len(candidates), 'pdfs_baixados_verificados': sum(d['status'] == 'baixado' for d in manifest['documentos']), 'erros': errors}
(root / 'docs/verificacao-busca-ampliada.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
if errors:
    raise SystemExit(1)
