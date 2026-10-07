"""Extração do simulado fornecido pelo usuário; não atribui respostas."""
from pathlib import Path
import hashlib, json, re
from difflib import SequenceMatcher
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'616470170-ELETROTECNICA-II-1-SIMULADO-2022-2-prova.pdf'
out=ROOT/'data/extraidos/simulado-2022-2'
out.mkdir(parents=True,exist_ok=True)
doc=pymupdf.open(source)
pages=[re.sub(r'Pagina\s+\d+\s+de\s+\d+','',p.get_text(sort=True)) for p in doc]
body=''; offsets=[]
for i,t in enumerate(pages): offsets.append((len(body),i+1)); body+=t+'\n'
matches=list(re.finditer(r'SAEP_(\d+)\b',body))
items=[]
for i,m in enumerate(matches):
    end=matches[i+1].start() if i+1<len(matches) else len(body)
    raw=body[m.end():end].strip()
    metadata=re.match(r'Cruzamento:\s*(.*?)\s*Dificuldade do item:\s*(Fácil|Médio|Difícil)',raw,re.S)
    cross=metadata[1].strip() if metadata else None
    difficulty=metadata[2] if metadata else None
    content=raw[metadata.end():].strip() if metadata else raw
    alternatives=list(re.finditer(r'(?m)^\s*([A-E])(?:\)|\s*$)',content))
    if len(alternatives)>5 and [a[1] for a in alternatives[-5:]]==list('ABCDE'):
        alternatives=alternatives[-5:]  # Não confundir a unidade A) ao fim de uma linha com alternativa.
    stem=content[:alternatives[0].start()].strip() if alternatives else content
    options=[{'letra':a[1],'texto':content[a.end():alternatives[j+1].start() if j+1<len(alternatives) else len(content)].strip()} for j,a in enumerate(alternatives)]
    first=max(p for off,p in offsets if off<=m.start())
    last=max(p for off,p in offsets if off<end)
    images=[]
    for pn in range(first,last+1):
        page=doc[pn-1]; y0=0; y1=page.rect.height
        if pn==first:
            boxes=page.search_for(m[0]); y0=boxes[0].y0 if boxes else 0
        if i+1<len(matches) and pn==last:
            boxes=page.search_for(matches[i+1][0]); y1=boxes[0].y0 if boxes else y1
        for k,im in enumerate(page.get_image_info()):
            box=pymupdf.Rect(im['bbox'])
            if y0<=box.y0<y1 and box.width>10 and box.height>10:
                dest=out/'figuras'/f'p{pn:02d}-imagem{k+1:02d}.png';dest.parent.mkdir(exist_ok=True)
                page.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=box).save(dest)
                images.append({'pagina':pn,'arquivo':dest.relative_to(ROOT).as_posix(),'descricao':'[VERIFICAR] descrição e alternativas gráficas pendentes'})
    items.append({'id':m[0],'ordem':i+1,'paginas':list(range(first,last+1)),'cruzamento_impresso':cross,'dificuldade_impressa':difficulty,'enunciado':stem,'alternativas':options,'figuras':images,'gabarito':None})
old=[]
for file in (ROOT/'data/extraidos').glob('*.json'):
    d=json.loads(file.read_text(encoding='utf-8'))
    if isinstance(d,dict):
        old.extend({'arquivo':file.name,**x} for x in d.get('itens',[]) if isinstance(x,dict) and 'enunciado' in x)
normalize=lambda s:re.sub(r'\W+','',s.lower())
sameids=sorted({x['id'] for x in items}&{x.get('id') for x in old})
similar=[]
for x in items:
    best=max(((SequenceMatcher(None,normalize(x['enunciado']),normalize(y['enunciado'])).ratio(),y) for y in old),key=lambda pair:pair[0],default=None)
    if best and best[0]>=0.75:
        similar.append({'id':x['id'],'candidato_anterior':best[1].get('id',best[1].get('ordem')),'arquivo':best[1]['arquivo'],'similaridade':round(best[0],3),'status':'[VERIFICAR] comparação textual não certifica duplicata'})
data={'arquivo_origem':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'paginas':len(doc),'curso':'Técnico em Eletrotécnica','natureza':'Simulado conforme cabeçalho; não comprovado como prova nacional aplicada','versao_itinerario':'V6','versao_matriz':1,'periodo_aplicacao_matriz':2021,'titulo_periodo':'2022.2','gabarito_status':'Não localizado no texto; não inferido de formatação ou figuras','numero_itens':len(items),'itens':items,'ids_compartilhados_pdfs_anteriores':sameids,'similaridades_candidatas':similar,'comparacao_docx_2023':'Pendente; coleção com segmentação provisória','paginas_texto':[{'pagina':i+1,'texto':t} for i,t in enumerate(pages)]}
(out/'simulado.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'texto.txt').write_text('\n'.join(f'=== PÁGINA {i+1} ===\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
check={'itens':len(items),'ids_distintos':len({x['id'] for x in items}),'alternativas_incompletas':[x['id'] for x in items if [a['letra'] for a in x['alternativas']]!=list('ABCDE')],'metadados_ausentes':[x['id'] for x in items if not x['cruzamento_impresso'] or not x['dificuldade_impressa']],'figuras':sum(len(x['figuras']) for x in items),'ids_compartilhados':sameids,'similaridades_candidatas':similar,'sha256':data['sha256']}
(ROOT/'docs/verificacao-simulado-2022.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(check,ensure_ascii=False))
doc[0].get_pixmap(matrix=pymupdf.Matrix(1,1)).save(ROOT/'tmp/pdfs/simulado-2022-capa.png')
