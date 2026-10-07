"""Downloads públicos oficiais, validação de PDF e deduplicação SHA-256."""
from pathlib import Path
import datetime, hashlib, json, urllib.request, urllib.parse
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data/provas';DEST.mkdir(parents=True,exist_ok=True)
SOURCES=[
 ('plano-eletrotecnica-ce-2016.pdf','https://arquivos.sfiec.org.br/senai/files/files/planos_de_cursos/tecnico-eletrotecnica-barra-2016-1.pdf','plano de curso',2016,'SENAI-CE'),
 ('plano-eletrotecnica-rr-semipresencial.pdf','https://static.portaldaindustria.com.br/media/filer_public/04/1c/041c82d7-693a-4b1f-8e69-307d5cfd0680/001_plano_de_curso_tecnico_em_eletrotecnica_semipresencial_com_correcao_gramatical_1807.pdf','plano de curso',2024,'SENAI-RR / Portal da Indústria'),
 ('metodologia-senai-2019.pdf','https://sp.senaiead.senai.br/files_scorm/27120_2/Layout/Aula/docs/Livro_Msep_2019.pdf','metodologia',2019,'SENAI'),
 ('saep-sobre-ade.html','https://saep.senai.br/SobreADE/Parte1','página institucional',2025,'SENAI nacional'),
 ('saep-instrumentos.html','https://saep.senai.br/SobreADE/Parte3','página institucional',None,'SENAI nacional'),
 ('saep-ap-simulado-2018.html','https://www.ap.senai.br/noticias/sistema-do-senai-avalia-preparacao-dos-alunos-para-o-mercado-de-trabalho.html','notícia; não contém caderno',2018,'SENAI-AP'),
 ('saep-rn-aplicacao-2026.html','https://www.rn.senai.br/senai-natal-aplica-provas-saep-para-avaliar-cursos-da-instituicao/','notícia; não contém caderno',2026,'SENAI-RN'),
]

if __name__=='__main__':
    entries=[]; hashes={}
    for p in sorted(ROOT.glob('*.pdf')):
        h=hashlib.sha256(p.read_bytes()).hexdigest();hashes[h]=p.name
        entries.append({'arquivo':p.name,'origem':'workspace fornecido pelo usuário','url':None,'data_download':None,'data_inventario':'2026-10-02','ano':2026 if p.name.startswith('SIMULADO') else None,'ano_observacao':'rótulo do arquivo, não edição oficial' if p.name.startswith('SIMULADO') else 'campo ano de aplicação em branco','curso':'Técnico em Eletrotécnica','tipo':'simulado local' if p.name.startswith('SIMULADO') else 'avaliação local SisBia','sha256':h,'status':'local preservado','condicoes_uso':'Procedência e licença não comprovadas. Apenas referência pessoal/local; não incluir itens ou figuras em publicação.'})
    for name,url,kind,year,org in SOURCES:
        e={'url':url,'arquivo':None,'instituicao':org,'tipo':kind,'ano':year,'curso':'Técnico em Eletrotécnica' if kind=='plano de curso' else None,'condicoes_uso':'Acesso público oficial; licença de redistribuição não verificada. Guardar como referência local, com autoria; não tratar acesso público como licença aberta.'}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=35) as response:
                content=response.read();e['url_final']=response.url;e['content_type']=response.headers.get('Content-Type');e['http_status']=response.status
            if not content:raise ValueError('Resposta vazia')
            if org.startswith('SENAI-RR'):
                e['condicoes_uso']='Página 5 do PDF: autoriza reprodução de partes com citação da fonte. Manter atribuição ao SENAI-RR; não estender esta autorização às provas locais.'
            if name.endswith('.pdf') and not content.startswith(b'%PDF'):raise ValueError('Resposta não é PDF')
            h=hashlib.sha256(content).hexdigest();e['sha256']=h;e['bytes']=len(content)
            e['data_download']='2026-10-02'
            if h in hashes:e['status']='duplicata';e['duplicata_de']=hashes[h]
            else:
                path=DEST/name;path.write_bytes(content);hashes[h]=path.relative_to(ROOT).as_posix();e['arquivo']=hashes[h];e['status']='baixado'
                if name.endswith('.pdf'):
                    doc=pymupdf.open(path);e['paginas']=len(doc)
                    pages=[{'pagina':i+1,'texto':p.get_text(sort=True)} for i,p in enumerate(doc)]
                    out=ROOT/'data/extraidos'/path.stem
                    out.with_suffix('.json').write_text(json.dumps({'fonte':e['arquivo'],'url':url,'paginas':pages},ensure_ascii=False,indent=2),encoding='utf8')
                    out.with_suffix('.txt').write_text('\n'.join(f'=== PÁGINA {p["pagina"]} ===\n{p["texto"]}' for p in pages),encoding='utf8')
                    e['paginas_sem_texto']=[p['pagina'] for p in pages if len(p['texto'].strip())<30]
            print(name,e['status'],e.get('paginas',''))
        except Exception as err:
            e['status']='falha no download';e['erro']=str(err);e['data_tentativa']='2026-10-02';print(name,e['status'],str(err))
        entries.append(e)
    (DEST/'manifesto.json').write_text(json.dumps({'data_sessao':'2026-10-02','fuso':'America/Sao_Paulo','deduplicacao':'SHA-256 dos bytes; duplicatas não são salvas novamente','documentos':entries},ensure_ascii=False,indent=2),encoding='utf8')
