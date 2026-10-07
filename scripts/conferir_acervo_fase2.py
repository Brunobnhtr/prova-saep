from pathlib import Path
import json,re,hashlib
from difflib import SequenceMatcher
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'data/fase2';out.mkdir(parents=True,exist_ok=True)
docxfile=ROOT/'data/extraidos/questoes-saep-2023/colecao.json'
d=json.loads(docxfile.read_text(encoding='utf-8'))
pdf=pymupdf.open(ROOT/'tmp/pdfs/colecao-2023-conferencia.pdf')
text=''; offsets=[]
for i,p in enumerate(pdf): offsets.append((len(text),i+1));text+=p.get_text(sort=True)+'\n'
markers=[]; expected=1
for m in re.finditer(r'(?m)^[ \t]*(\d{1,2})\)[ \t]*',text):
    if int(m[1])==expected:
        markers.append(m);expected+=1
assert expected==81 and len(d['itens'])==80
for i,x in enumerate(d['itens']):
    end=markers[i+1].start() if i<79 else len(text)
    raw=text[markers[i].end():end].strip()
    am=list(re.finditer(r'(?m)^\s*\(?([A-Ea-e])(?:\)|\s*[-–])\s*',raw))
    if len(am)>=5 and [a[1].upper() for a in am[-5:]]==list('ABCDE'):
        am=am[-5:]
        x['enunciado']=raw[:am[0].start()].strip()
        x['alternativas']=[{'letra':a[1].upper(),'texto':raw[a.end():am[j+1].start() if j<4 else len(raw)].strip()} for j,a in enumerate(am)]
        x['metodo_alternativas']='A-E conferidas no PDF renderizado pelo Word'
    else:
        x['enunciado']=raw
        x['alternativas']=[{'letra':l,'texto':None,'origem':'Alternativa gráfica no arquivo; usar figura vinculada'} for l in 'ABCDE']
        x['metodo_alternativas']='Alternativas gráficas A-E conferidas visualmente; sem transcrição de circuitos'
    x['numero_documento']=i+1
    x['paginas']=list(range(max(p for off,p in offsets if off<=markers[i].start()),max(p for off,p in offsets if off<end)+1))
    if 'gráficas' in x['metodo_alternativas']:
        # Guarda também a página composta: figuras agrupadas podem não aparecer como blip no parágrafo.
        folder=out/'figuras-conferencia';folder.mkdir(exist_ok=True)
        for pn in x['paginas']:
            dest=folder/f'c23-item{i+1:02d}-p{pn:02d}.png'
            pdf[pn-1].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(dest)
            x['figuras'].append(dest.relative_to(ROOT).as_posix())
d['paginas_conferidas']=len(pdf);d['conferencia']='Word em modo somente leitura; 80 números sequenciais; origem preservada; anotações não certificadas como gabarito'
(out/'colecao-2023-conferida.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
allitems=[]
for label,path in [('A1','data/extraidos/avaliacoes.json'),('A2','data/extraidos/avaliacoes-2.json'),('S26','data/extraidos/simulado-2026.json'),('S22','data/extraidos/simulado-2022-2/simulado.json'),('C23','data/fase2/colecao-2023-conferida.json')]:
    source=json.loads((ROOT/path).read_text(encoding='utf-8'))
    for x in source['itens']:allitems.append({**x,'fonte':label,'referencia':path,'uid':label+':'+x['id']})
norm=lambda s:re.sub(r'\W+','',s.lower())
groups={}
for x in allitems:
    key=x['id'] if x['id'].startswith('SAEP_') else 'TEXTO:'+norm(x['enunciado'])
    groups.setdefault(key,[]).append(x)
representatives=[xs[0] for xs in groups.values()]
candidates=[]
for i,x in enumerate(representatives):
    if x['fonte']!='C23':continue
    tokens=set(re.findall(r'\w+',x['enunciado'].lower()))
    for y in representatives[:i]:
        other=set(re.findall(r'\w+',y['enunciado'].lower()))
        j=len(tokens&other)/max(1,len(tokens|other))
        if j<.42:continue
        score=SequenceMatcher(None,norm(x['enunciado']),norm(y['enunciado']),autojunk=False).ratio()
        if score>=.64:candidates.append({'a':x['uid'],'b':y['uid'],'similaridade':round(score,3),'a_texto':x['enunciado'][:160],'b_texto':y['enunciado'][:160]})
(out/'candidatos-duplicatas.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'ocorrencias.json').write_text(json.dumps(allitems,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ocorrencias':len(allitems),'grupos_preliminares':len(groups),'candidatos':candidates,'docx_graficas':[x['ordem'] for x in d['itens'] if 'gráficas' in x['metodo_alternativas']]},ensure_ascii=False))
