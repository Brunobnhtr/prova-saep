"""Coleta suplementar: somente downloads públicos, sem cookies/login."""
from pathlib import Path
import hashlib,json,urllib.request
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data/provas/busca-ampliada';DEST.mkdir(parents=True,exist_ok=True)
SOURCES=[
 ('plano-operacional-pratica-2024.pdf','https://drive.usercontent.google.com/download?id=1r7I6sIACTLTMKS9PUSwh1enzNU1BHPz8&export=download','plano operacional da prova prática; não é caderno','https://drive.google.com/file/d/1r7I6sIACTLTMKS9PUSwh1enzNU1BHPz8/view'),
 ('pesquisa-preparacao-saep-ifes.pdf','https://repositorio.ifes.edu.br/bitstreams/326a7fe8-4568-4059-9b5b-40bd6354508a/download','pesquisa acadêmica sobre preparação para SAEP; verificar anexos',None),
]
entries=[]
for name,url,kind,page in SOURCES:
    e={'url':url,'pagina_origem':page,'tipo':kind,'data_tentativa':'2026-10-02','condicoes_uso':'Documento público; licença de redistribuição ainda não verificada. Referência pessoal/local.'}
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=30) as response:
            content=response.read();e['http_status']=response.status;e['content_type']=response.headers.get('Content-Type')
        if not content.startswith(b'%PDF'):raise ValueError('Resposta não é PDF; não salvar HTML como PDF nem contornar desafio de acesso.')
        doc=pymupdf.open(stream=content,filetype='pdf')
        e.update({'arquivo':(DEST/name).relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),'paginas':len(doc),'data_download':'2026-10-02','status':'baixado'})
        (DEST/name).write_bytes(content)
        out=ROOT/'data/extraidos/busca-ampliada';out.mkdir(exist_ok=True)
        pages=[{'pagina':n+1,'texto':p.get_text(sort=True)} for n,p in enumerate(doc)]
        (out/(Path(name).stem+'.json')).write_text(json.dumps({'fonte':e['arquivo'],'paginas':pages},ensure_ascii=False,indent=2),encoding='utf8')
        (out/(Path(name).stem+'.txt')).write_text('\n'.join(f'=== PÁGINA {p["pagina"]} ===\n{p["texto"]}' for p in pages),encoding='utf8')
    except Exception as err:e.update({'status':'download não obtido','erro':str(err)})
    print(name,e['status'],e.get('paginas',e.get('erro')))
    entries.append(e)
(DEST/'manifesto.json').write_text(json.dumps({'data':'2026-10-02','escopo':'busca suplementar em qualquer domínio público autorizada pelo usuário','documentos':entries},ensure_ascii=False,indent=2),encoding='utf8')
