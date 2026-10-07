from pathlib import Path
import json,re,hashlib,html,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
base=Path(r'C:\dev\extrator de perguntas');target=Path('data/acervo-ampliado');target.mkdir(parents=True,exist_ok=True)
questions=[];errors=[]
for p in sorted((base/'eletrica_eletronica/questoes').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf-8-sig'));qs=d.get('questoes',[])
 if d.get('total')!=len(qs):errors.append({'arquivo':str(p),'problema':'total divergente'})
 questions.extend(qs)
ids=collections.Counter(q.get('codigo') for q in questions);images_missing=[];html_gaps=[];hashes=collections.defaultdict(list)
for q in questions:
 for image in q.get('imagens',[]):
  path=image.get('caminho') or ('imagens/'+image['arquivo'] if image.get('arquivo') else None)
  if path is None or not (base/'eletrica_eletronica'/path).is_file():images_missing.append({'codigo':q['codigo'],'caminho':path,'estado':image.get('erro')})
 n_html=len(re.findall(r'<img\b',(q.get('enunciado_html') or ''),re.I))
 if n_html>len(q.get('imagens',[])):html_gaps.append({'codigo':q['codigo'],'imagens_html':n_html,'imagens_salvas':len(q.get('imagens',[]))})
 signature={'texto':re.sub(r'\s+',' ',html.unescape((q.get('enunciado') or ''))).strip().casefold(),'alternativas':[(a.get('letra'),re.sub(r'\s+',' ',(a.get('texto') or '')).strip().casefold()) for a in q.get('alternativas',[])],'imagens':[i.get('url_original') for i in q.get('imagens',[])]}
 hashes[hashlib.sha256(json.dumps(signature,sort_keys=True,ensure_ascii=False).encode()).hexdigest()].append(q['codigo'])
dossiers=[]
for p in sorted((base/'livros senai/dossies').glob('*/*_dados.json')):
 d=json.loads(p.read_text(encoding='utf-8-sig'));cov=d.get('cobertura',{});fig=list((p.parent/'figuras').glob('*.png'))
 dossiers.append({'id':d['id'],'tema':d['tema'],'pasta':str(p.parent),'dados':str(p),'fontes_pdf':[str(f) for f in p.parent.glob('*.pdf')],'textos':[str(f) for f in p.parent.glob('*_texto.md')],'figuras':len(fig),'fontes':len(d.get('blocos',[])),'chaves_sem_fonte':[k for k,v in cov.items() if not v],'paginas_sem_texto':len(d.get('paginas_sem_texto',[]))})
mds=[]
for p in (base/'livros senai/questoes').rglob('*.md'):
 txt=p.read_text(encoding='utf-8-sig');m=re.match(r'#\s+(\d+\.\d+)\s+(.+)',txt)
 if m:mds.append({'id':m.group(1),'tema':m.group(2),'arquivo':str(p),'questoes_markdown':len(re.findall(r'^### \d+\.',txt,re.M))})
index=json.loads((base/'eletrica_eletronica/_index.json').read_text(encoding='utf-8-sig'));failure=json.loads((base/'eletrica_eletronica/_erros.json').read_text(encoding='utf-8-sig'))
summary={'data':'2026-10-06','raiz':str(base),'dossies':len(dossiers),'figuras_dossies':sum(d['figuras'] for d in dossiers),'questoes_ocorrencias':len(questions),'questoes_ids_distintos':len(ids),'ids_repetidos':[i for i,c in ids.items() if c>1],'index_total':index['total'],'index_ids_coincidem':set(ids)=={q['codigo'] for q in index['questoes']},'enunciados_ausentes':sum(not (q.get('enunciado') or '').strip() for q in questions),'gabaritos_presentes':sum(q.get('gabarito') is not None for q in questions),'gabaritos_ausentes':sum(q.get('gabarito') is None for q in questions),'alternativas_por_quantidade':dict(collections.Counter(len(q.get('alternativas',[])) for q in questions)),'imagens_arquivo':sum(1 for f in (base/'eletrica_eletronica/imagens').iterdir() if f.is_file()),'referencias_imagens_ausentes':images_missing,'questoes_com_mais_imgs_html_que_salvas':html_gaps,'erros_registrados':failure['total'],'duplicatas_conteudo_candidatas':[v for v in hashes.values() if len(v)>1],'questoes_por_tema_md':len(mds),'questoes_soma_por_tema':sum(d['questoes_markdown'] for d in mds),'dossies_com_lacunas':sum(bool(d['chaves_sem_fonte']) for d in dossiers),'observacao':'Metadados e verificacao estrutural. Classificacao, gabaritos e pertinencia tecnica nao foram certificados. Identidade diferente nao garante enunciado distinto.'}
(target/'inventario.json').write_text(json.dumps({'resumo':summary,'dossies':dossiers,'questoes_por_tema':mds,'inconsistencias_lotes':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2)[:5500]);print('Salvo:',target/'inventario.json')
