"""Inventário e extração de livros fornecidos pelo usuário, sem mover originais."""
from pathlib import Path
import hashlib,json,re
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'C:\dev\extrator de perguntas\livros senai\meus_livros')
OUT=ROOT/'data/livros';OUT.mkdir(parents=True,exist_ok=True)
entries=[]
for index,path in enumerate(sorted(SOURCE.rglob('*.pdf')),1):
    e={'id':f'livro-{index:03d}','nome':path.name,'origem':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'condicoes_uso':'Fornecido pelo usuário para referência pessoal/local; autorização de publicação não confirmada.'}
    try:
        doc=pymupdf.open(path)
        pages=[{'pagina':n+1,'texto':p.get_text(sort=True)} for n,p in enumerate(doc)]
        e['paginas']=len(doc);e['paginas_sem_texto']=[p['pagina'] for p in pages if len(p['texto'].strip())<30]
        first='\n'.join(p['texto'] for p in pages[:10])
        e['senai_nas_paginas_iniciais']=bool(re.search(r'SENAI',first,re.I))
        e['anos_mencionados_inicio']=sorted(set(re.findall(r'\b(?:19|20)\d{2}\b',first)))
        e['sumario_paginas']=[p['pagina'] for p in pages[:25] if re.search(r'sum[aá]rio',p['texto'],re.I)]
        dest=OUT/(e['id']+'.json')
        dest.write_text(json.dumps({'fonte':str(path),'sha256':e['sha256'],'paginas':pages},ensure_ascii=False,indent=2),encoding='utf8')
        e['extracao']=dest.relative_to(ROOT).as_posix();e['status']='texto extraído; revisão técnica não realizada'
    except Exception as error:e['status']='falha';e['erro']=str(error)
    entries.append(e)
hashes={}
for e in entries:hashes.setdefault(e['sha256'],[]).append(e['id'])
result={'data':'2026-10-02','pasta_origem':str(SOURCE),'livros':entries,'duplicatas_binarias':[v for v in hashes.values() if len(v)>1],'observacao':'Livros de cursos relacionados são apoio; não alteram o curso alvo Técnico em Eletrotécnica.'}
(OUT/'inventario.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# Livros SENAI fornecidos pelo usuário','',f'Pasta: `{SOURCE}`. Originais preservados, sem cópia dos PDFs.','',f'{len(entries)} PDFs; {sum(e.get("paginas",0) for e in entries)} páginas; {sum(len(e.get("paginas_sem_texto",[])) for e in entries)} páginas com menos de 30 caracteres extraídos.','', '| Livro | Páginas | Páginas com pouco texto | Extração |','|---|---:|---:|---|']
for e in entries:lines.append(f'| {e["nome"]} | {e.get("paginas","?")} | {len(e.get("paginas_sem_texto",[]))} | {e.get("extracao",e["status"])} |')
lines+=['','Anos listados no JSON são menções textuais, não necessariamente edição. Páginas com pouco texto podem ser capas, figuras ou páginas digitalizadas; não afirmar que todo livro esteja integralmente transcrito. Direitos de publicação e edição técnica ainda precisam ser conferidos. Livros de automação, mecatrônica e eletrônica serão usados apenas conforme pertinência ao curso alvo.']
(ROOT/'docs/01-inventario-livros.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(json.dumps({'arquivos':len(entries),'paginas':sum(e.get('paginas',0) for e in entries),'falhas':sum(e['status']=='falha' for e in entries),'duplicatas_binarias':result['duplicatas_binarias'],'paginas_pouco_texto':sum(len(e.get('paginas_sem_texto',[])) for e in entries)},ensure_ascii=False))
