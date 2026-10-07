"""Importa a coleção fornecida pelo usuário sem alterar o DOCX original."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import hashlib, json, re, collections

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / '754180435-Questoes-SAEP-2023.docx'
out = ROOT / 'data/extraidos/questoes-saep-2023'
out.mkdir(parents=True, exist_ok=True)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{' + ns['w'] + '}'
with ZipFile(source) as z:
    numbering = ET.fromstring(z.read('word/numbering.xml'))
    abstract = {x.get(W+'abstractNumId'): x for x in numbering.findall('w:abstractNum', ns)}
    nums = {x.get(W+'numId'): x.find('w:abstractNumId',ns).get(W+'val') for x in numbering.findall('w:num',ns)}
    rels = {x.get('Id'): x.get('Target') for x in ET.fromstring(z.read('word/_rels/document.xml.rels')) if x.get('TargetMode') != 'External'}
    paragraphs = []
    for i,p in enumerate(ET.fromstring(z.read('word/document.xml')).findall('.//w:body/w:p',ns)):
        text = ''.join(x.text or '' for x in p.findall('.//w:t',ns)).strip()
        num = p.find('w:pPr/w:numPr/w:numId',ns)
        fmt = None
        if num is not None:
            level = p.find('w:pPr/w:numPr/w:ilvl',ns)
            lvl = level.get(W+'val') if level is not None else '0'
            node = abstract[nums[num.get(W+'val')]].find("w:lvl[@w:ilvl='"+lvl+"']/w:numFmt",ns)
            fmt = node.get(W+'val') if node is not None else None
        images = []
        for blip in p.findall('.//a:blip',ns):
            target = rels.get(blip.get('{'+ns['r']+'}embed'))
            if target and target.startswith('media/'):
                dest = out / 'figuras' / Path(target).name
                dest.parent.mkdir(exist_ok=True)
                dest.write_bytes(z.read('word/'+target))
                images.append(dest.relative_to(ROOT).as_posix())
        for embedded in p.findall('.//{urn:schemas-microsoft-com:vml}imagedata'):
            target=rels.get(embedded.get('{'+ns['r']+'}id'))
            if target and target.startswith('media/'):
                dest=out/'figuras'/Path(target).name
                dest.parent.mkdir(exist_ok=True)
                dest.write_bytes(z.read('word/'+target))
                images.append(dest.relative_to(ROOT).as_posix())
        paragraphs.append({'indice': i, 'texto': text, 'formato_lista': fmt, 'figuras': images})
    # Número explícito ou lista decimal com enunciado longo; listas de procedimentos ficam dentro do item.
    starts = [i for i,p in enumerate(paragraphs) if re.match(r'^\d{1,3}\)\s*',p['texto']) or (p['formato_lista']=='decimal' and (len(p['texto'])>120 or i==100) and i not in (160,161,163))]
    items=[]
    for k,start in enumerate(starts):
        segment=paragraphs[start:starts[k+1] if k+1<len(starts) else len(paragraphs)]
        meaningful=[p for p in segment if p['texto']]
        options=[p for p in meaningful if p['indice'] != start and p['formato_lista'] in ('lowerLetter','upperLetter')]
        method='numeração alfabética OOXML'
        if len(options)!=5:
            inline = next((p for p in meaningful if re.search(r'A\).*B\).*C\)',p['texto'])),None)
            if inline:
                matches=list(re.finditer(r'([A-E])\)',inline['texto']))
                options=[{'indice':inline['indice'],'texto':inline['texto'][m.end():matches[j+1].start() if j+1<len(matches) else len(inline['texto'])].strip()} for j,m in enumerate(matches)]
                method='alternativas A-E no mesmo parágrafo'
            elif len(meaningful) >= 7:
                options=meaningful[-5:]
                method='últimos cinco parágrafos textuais; [VERIFICAR] segmentação visual'
            else:
                options=[]
                method='[VERIFICAR] alternativas em figuras ou segmentação incompleta; não inferidas'
        option_indices={p['indice'] for p in options}
        stem='\n'.join(p['texto'] for p in meaningful if p['indice'] not in option_indices)
        explicit=re.match(r'^(\d{1,3})\)\s*',stem)
        items.append({'id':f'COLECAO2023_{k+1:03d}', 'ordem':k+1, 'numero_explicito':int(explicit[1]) if explicit else None, 'enunciado':re.sub(r'^\d{1,3}\)\s*','',stem), 'alternativas':[{'letra':chr(65+j),'texto':p['texto']} for j,p in enumerate(options)], 'metodo_alternativas':method, 'figuras':list(dict.fromkeys(f for p in segment for f in p['figuras'])), 'paragrafos_origem':[p['indice'] for p in segment], 'gabarito':None})
    media=[n for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')]
    for name in media:
        dest=out/'figuras'/Path(name).name
        dest.parent.mkdir(exist_ok=True)
        dest.write_bytes(z.read(name))
    app=ET.fromstring(z.read('docProps/app.xml'))
    pages=app.find('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Pages')
data={'arquivo_origem':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'procedencia':'Arquivo fornecido pelo usuário; candidato Scribd 754180435; autenticidade e aplicação oficial não confirmadas.', 'ano_aplicacao':None,'ano_nome_arquivo':2023,'paginas_metadados_word':int(pages.text),'paginas_status':'Metadado armazenado, não conferido por renderização.', 'numero_itens':len(items),'arquivos_media':len(media),'gabarito_status':'Não localizado no texto; destaques e imagens não validados como respostas.', 'itens':items, 'paragrafos':paragraphs}
(out/'colecao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'texto.txt').write_text('\n'.join(p['texto'] for p in paragraphs),encoding='utf-8')
print(json.dumps({'itens':len(items),'numeros_explicitos_divergentes':[(x['ordem'],x['numero_explicito']) for x in items if x['numero_explicito'] and x['numero_explicito']!=x['ordem']], 'alternativas_metodos':dict(collections.Counter(x['metodo_alternativas'] for x in items)), 'media':len(media)},ensure_ascii=False))
