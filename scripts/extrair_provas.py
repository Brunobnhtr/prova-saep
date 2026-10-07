"""Extração local reproduzível; não acessa URLs embutidas nos PDFs."""
from pathlib import Path
import hashlib, json, re, collections
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/extraidos'
OUT.mkdir(parents=True, exist_ok=True)

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# Classificação editorial após leitura dos itens. Tema/tipo principal, não Matriz oficial.
GROUPS = {
 'Segurança e NR-10': '76147 78307 76652 77014 78432',
 'Circuitos CC/CA e grandezas': '76953 76385 77410 77777 77855 77764',
 'Manutenção e diagnóstico': '76206 78348',
 'Motores, comandos e acionamentos': '77578 77817 76121 76352 77437 76314 77568 77736 78437',
 'Medições elétricas': '77411 78272 78454 77409 77686',
 'Redes de distribuição e SEP': '77795 77825 77408 77534 77400',
 'Projetos e CAD': '78294',
 'CLP, lógica e automação': '76509 76885 78273 78287 76648 77858',
 'Proteção e dimensionamento': '77772 77683 77862 78480 77412',
 'Transformadores': '77826',
 'Aterramento e SPDA': '76980 77743',
}
THEMES = {i:t for t,ids in GROUPS.items() for i in ids.split()}
CALC = set('76385 77825 77683 77826 77437 76314 78480 77736 77412'.split())
DIAGRAM = set('77795 76509 77408 77777 78273 77400 77764 78437 77858'.split())
NORM = set('76147 78307 76652 77014 78432 77772 77862 77743'.split())
SIMTHEME = {
 1:'Segurança e NR-10',2:'Circuitos CC/CA e grandezas',3:'Energia solar fotovoltaica',4:'Segurança e NR-10',5:'Energia solar fotovoltaica',6:'Aterramento e SPDA',7:'Instalações prediais',8:'Projetos e CAD',9:'Redes de distribuição e SEP',10:'Medições elétricas',11:'Medições elétricas',12:'Motores, comandos e acionamentos',13:'CLP, lógica e automação',14:'Aterramento e SPDA',15:'CLP, lógica e automação',16:'Pneumática e eletropneumática',17:'Energia solar fotovoltaica',18:'Proteção e dimensionamento',19:'Projetos e CAD',20:'Proteção e dimensionamento',21:'Proteção e dimensionamento',22:'Proteção e dimensionamento',23:'Medições elétricas',24:'Aterramento e SPDA',25:'Circuitos CC/CA e grandezas',26:'Transformadores',27:'Redes de distribuição e SEP',28:'CLP, lógica e automação',29:'Motores, comandos e acionamentos',30:'Pneumática e eletropneumática',31:'Proteção e dimensionamento',32:'Proteção e dimensionamento',33:'CLP, lógica e automação',34:'Pneumática e eletropneumática',35:'Circuitos CC/CA e grandezas',36:'Manutenção e diagnóstico',37:'Manutenção e diagnóstico',38:'Circuitos CC/CA e grandezas',39:'CLP, lógica e automação',40:'Medições elétricas',41:'Redes de distribuição e SEP'}
SIMCALC={2,3,5,17,20,21,22,28,29,31,35}
SIMDIAG={1,7,8,9,12,13,14,15,16,19,26,27,30,33,34,41}
SIMNORM={4,6,18,24,32}

def clean(s):
    s=re.sub(r'https://forms\.cloud\.microsoft/[^\s]+', '[URL DO FORMULÁRIO OMITIDA]', s)
    s=re.sub(r'Pagina\s+1\s+de\s+1', '', s)
    return s.strip()

def figures(doc, ranges, folder):
    folder.mkdir(parents=True, exist_ok=True)
    result=[]
    for page_no,y0,y1 in ranges:
        page=doc[page_no-1]
        for k,im in enumerate(page.get_image_info()):
            box=fitz.Rect(im['bbox'])
            if box.y0 < y0 or box.y0 >= y1:
                continue
            if 'avaliacoes' in folder.name and box.y1<90:
                continue  # Logotipos no cabeçalho, sem excluir diagramas que começam no topo.
            if box.width<10 or box.height<10:
                continue
            path=folder/f'p{page_no:02d}-imagem{k+1:02d}.png'
            page.get_pixmap(matrix=fitz.Matrix(2,2),clip=box).save(path)
            result.append({'pagina':page_no,'bbox':list(box),'arquivo':path.relative_to(ROOT).as_posix(),'descricao':'[VERIFICAR] Transcrição e descrição acessível da figura pendentes.'})
    return result

def extract_eval(filename, slug):
    doc=fitz.open(ROOT/filename)
    pages=[clean(p.get_text(sort=True)) for p in doc]
    body=''; boundaries=[]
    for n,s in enumerate(pages):
        boundaries.append((len(body),n+1)); body+=s+'\n'
    body_items=body.split('FOLHA DE RESPOSTA')[0]
    keys=dict(re.findall(r'SAEP_(\d+)\s+([A-D])\b',body.split('GABARITO',1)[1]))
    matches=list(re.finditer(r'SAEP_(\d+)\.',body_items))
    items=[]
    for idx,m in enumerate(matches):
        end=matches[idx+1].start() if idx+1<len(matches) else len(body_items)
        raw=body_items[m.end():end]
        stem,alts=raw.split('Alternativas',1)
        am=list(re.finditer(r'\b([A-D])\.\s*\(\s*\)',alts))
        options=[{'letra':a.group(1),'texto':alts[a.end():am[j+1].start() if j+1<len(am) else len(alts)].strip()} for j,a in enumerate(am)]
        startpage=max(n for off,n in boundaries if off<=m.start())
        endpage=max(n for off,n in boundaries if off<end)
        ranges=[]
        for pn in range(startpage,endpage+1):
            y0=0;y1=doc[pn-1].rect.height
            if pn==startpage: y0=doc[pn-1].search_for(m.group(0))[0].y0
            if idx+1<len(matches) and pn==endpage:
                boxes=doc[pn-1].search_for(matches[idx+1].group(0))
                if boxes: y1=boxes[0].y0
            ranges.append((pn,y0,y1))
        id=m.group(1)
        imgs=figures(doc,ranges,OUT/'figuras'/slug)
        items.append({'id':'SAEP_'+id,'ordem':idx+1,'paginas':list(range(startpage,endpage+1)), 'enunciado':stem.strip(),'alternativas':options,'gabarito':{'resposta':keys[id],'origem':'extraído do gabarito do PDF','validacao_tecnica':'[VERIFICAR] Não equivale a revisão técnica.'},'tema_principal':THEMES[id], 'tipo_principal':'cálculo' if id in CALC else 'leitura de diagrama' if id in DIAGRAM else 'norma e segurança' if id in NORM else 'conceitual','figuras':imgs,'possui_figura':bool(imgs),'classificacao':'editorial; não é cruzamento da Matriz de Referência'})
    data={'schema_versao':1,'arquivo_origem':filename,'curso':'Técnico em Eletrotécnica','curso_evidencia':'DADOS DA AVALIAÇÃO, última página','ano_aplicacao':None,'ano_status':'não informado; campo em branco','versao_matriz':1,'versao_itinerario':2022,'paginas':len(doc),'numero_itens':len(items),'gabarito_paginas':[n+1 for n,s in enumerate(pages) if 'GABARITO' in s or (n==len(pages)-1)],'metodo':'PyMuPDF, texto ordenado por página; figuras rasterizadas dos retângulos de imagens; sem OCR','itens':items,'paginas_texto':[{'pagina':n+1,'texto':s} for n,s in enumerate(pages)]}
    save(OUT/(slug+'.json'),data)
    (OUT/(slug+'.txt')).write_text('\n'.join(f'=== PÁGINA {n+1} ===\n{s}' for n,s in enumerate(pages)),encoding='utf-8')
    return data

def extract_sim():
    filename='SIMULADO 2026.pdf';doc=fitz.open(ROOT/filename); entries=[]
    for pn,page in enumerate(doc):
        blocks=page.get_text('dict')['blocks']; markers=[]
        for b in blocks:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip()
                if re.fullmatch(r'\d{1,2}',text) and 125<line['bbox'][0]<130:
                    markers.append((int(text),line['bbox'][1]))
        markers.sort(key=lambda x:x[1])
        for j,(num,y0) in enumerate(markers):
            y1=markers[j+1][1] if j+1<len(markers) else page.rect.height-40
            question=[]; altlines=[]
            for b in blocks:
                for line in b.get('lines',[]):
                    if not y0+5<line['bbox'][1]<y1: continue
                    text=''.join(s['text'] for s in line['spans']).strip()
                    size=max(s['size'] for s in line['spans'])
                    if not text or 'Microsoft' in text:continue
                    if size>7.4: question.append((line['bbox'][1],text))
                    else: altlines.append((line['bbox'][1],text))
            alts=[];last=None
            for y,t in sorted(altlines):
                if last is None or y-last>14:alts.append(t)
                else:alts[-1]+=' '+t
                last=y
            if alts==['A B','C D']:
                alts=['A','B','C','D']
            imgs=figures(doc,[(pn+1,y0,y1)],OUT/'figuras'/'simulado-2026')
            entries.append({'id':f'SIM2026_{num:02d}','ordem':num,'paginas':[pn+1],'enunciado':'\n'.join(t for y,t in sorted(question)),'alternativas':[{'letra':chr(65+k),'texto':t} for k,t in enumerate(alts)],'letras_atribuidas_por_ordem':True,'gabarito':{'resposta':None,'origem':'não encontrado no documento','validacao_tecnica':'[VERIFICAR] Não inferir gabarito.'},'tema_principal':SIMTHEME[num],'tipo_principal':'cálculo' if num in SIMCALC else 'leitura de diagrama' if num in SIMDIAG else 'norma e segurança' if num in SIMNORM else 'conceitual','figuras':imgs,'possui_figura':bool(imgs),'classificacao':'editorial; não é cruzamento da Matriz de Referência'})
    entries.sort(key=lambda x:x['ordem'])
    pages=[clean(p.get_text(sort=True)) for p in doc]
    data={'schema_versao':1,'arquivo_origem':filename,'curso':'Técnico em Eletrotécnica','curso_evidencia':'contexto dos enunciados, sem ficha formal de curso','ano_aplicacao':None,'ano_rotulo':2026,'data_impressao':'2026-05-20 08:43','ano_status':'2026 no nome e cabeçalho de impressão; edição oficial não comprovada','paginas':len(doc),'numero_itens':len(entries),'metodo':'PyMuPDF, linhas por coordenadas e tamanho de fonte; sem OCR','itens':entries,'paginas_texto':[{'pagina':n+1,'texto':s} for n,s in enumerate(pages)]}
    save(OUT/'simulado-2026.json',data)
    (OUT/'SIMULADO 2026.txt').write_text('\n'.join(f'=== PÁGINA {n+1} ===\n{s}' for n,s in enumerate(pages)),encoding='utf-8')
    return data

if __name__=='__main__':
    docs=[extract_eval('avaliações.pdf','avaliacoes'),extract_eval('avaliações 2.pdf','avaliacoes-2'),extract_sim()]
    # Apagar somente as duas extrações iniciais redundantes, sem tocar PDFs.
    for name in ['avaliações.txt','avaliações 2.txt']:
        p=OUT/name
        if p.exists():p.unlink()
    summary={'documentos':[],'duplicatas_por_id':[]}
    ids=collections.defaultdict(list)
    for d in docs:
        summary['documentos'].append({'arquivo':d['arquivo_origem'],'itens':d['numero_itens'],'temas':dict(collections.Counter(i['tema_principal'] for i in d['itens'])),'tipos':dict(collections.Counter(i['tipo_principal'] for i in d['itens'])),'itens_com_figura':sum(i['possui_figura'] for i in d['itens'])})
        for i in d['itens']:ids[i['id']].append({'arquivo':d['arquivo_origem'],'ordem':i['ordem'],'resposta':i['gabarito']['resposta']})
    summary['duplicatas_por_id']=[{'id':k,'ocorrencias':v} for k,v in ids.items() if len(v)>1]
    summary['total_ocorrencias']=sum(d['numero_itens'] for d in docs)
    summary['ids_distintos']=len(ids)
    normalized=collections.defaultdict(list)
    for d in docs:
        for i in d['itens']:
            normalized[re.sub(r'\W','',i['enunciado'].lower())].append({'arquivo':d['arquivo_origem'],'id':i['id']})
    summary['duplicatas_por_enunciado']=[v for v in normalized.values() if len(v)>1]
    # Índice de estudo deduplicado por ID e pela repetição exata do simulado.
    seen=set(); unique=[]
    for d in docs:
        for i in d['itens']:
            identity=i['id'] if i['id'].startswith('SAEP_') else re.sub(r'\W','',i['enunciado'].lower())
            if identity in seen:continue
            seen.add(identity); unique.append({'id':i['id'],'arquivo':d['arquivo_origem'],'tema_principal':i['tema_principal'],'tipo_principal':i['tipo_principal']})
    summary['itens_unicos_conservador']=len(unique)
    save(OUT/'indice-deduplicado.json',{'criterio':'ID SAEP; enunciado normalizado para itens sem ID SAEP. Não elimina semelhanças apenas temáticas.','itens':unique})
    save(OUT/'resumo.json',summary)
    for d in docs:
        bad=[(i['id'],len(i['alternativas'])) for i in d['itens'] if len(i['alternativas'])!=4]
        print(d['arquivo_origem'],d['numero_itens'],'alternativas fora do padrão:',bad)
