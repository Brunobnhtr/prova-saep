"""Gera data/editorial/curriculum-35-modules.json por EXTRACAO de fontes existentes do projeto.

Regras:
- Nenhum conteudo curricular e redigido por este script.
- Campos sem fonte no projeto ficam vazios/null e marcados como NOT_IN_PROJECT_SOURCES.
- Campos derivados (nao copiados literalmente) registram o metodo de derivacao.
- Gabaritos das ocorrencias nunca sao copiados (examples trazem so enunciado resumido).

Fontes:
  data/fase2/mapa-conteudo.json            -> code, area, tema, subtema, pre_requisitos, atividade, livros, matriz_status
  data/fase2/ocorrencias-classificadas.json -> examples (ocorrencias SAEP classificadas na Fase 2 por subtema_id)
  data/acervo-ampliado/cruzamento-35-temas.json -> dossies de apoio, observacoes editoriais, status
  <dossie>/<id>_dados.json (externo)        -> chaves de busca do dossie + cobertura em livros
"""
from pathlib import Path
import json, hashlib, collections, datetime

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/editorial/curriculum-35-modules.json'
MAPA = ROOT / 'data/fase2/mapa-conteudo.json'
OCOR = ROOT / 'data/fase2/ocorrencias-classificadas.json'
CRUZ = ROOT / 'data/acervo-ampliado/cruzamento-35-temas.json'

MISSING = 'NOT_IN_PROJECT_SOURCES'


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def file_ref(p):
    p = Path(p)
    if not p.exists():
        return {'path': str(p), 'exists': False}
    b = p.read_bytes()
    assert len(b) > 0, f'{p} vazio'
    try:
        shown = str(p.relative_to(ROOT))
    except ValueError:
        shown = str(p)
    return {'path': shown, 'exists': True, 'size_bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def preview(text, n=220):
    t = ' '.join(str(text or '').split())
    return t if len(t) <= n else t[:n].rstrip() + '...'


def main():
    mapa = load(MAPA)
    ocorrencias = load(OCOR)
    cruz = load(CRUZ)

    sub_by_id = {s['id']: s for s in mapa['subtemas']}
    cruz_by_id = {m['modulo']: m for m in cruz['modulos']}
    trilha = mapa['trilha']
    assert len(sub_by_id) == 35 and len(cruz_by_id) == 35 and len(trilha) == 35
    assert set(sub_by_id) == set(cruz_by_id) == set(trilha), 'Conjuntos de codigos divergem entre fontes'

    ex_by_mod = collections.defaultdict(list)
    for o in ocorrencias:
        if o.get('subtema_id'):
            ex_by_mod[o['subtema_id']].append(o)

    # Modulos que compartilham o mesmo dossie de apoio -> sobreposicao candidata
    dossie_users = collections.defaultdict(set)
    for code, m in cruz_by_id.items():
        for f in m.get('fontes', []):
            dossie_users[f['id_dossie']].add(code)

    external_sources = {}
    modules = []
    for order, code in enumerate(trilha, start=1):
        s = sub_by_id[code]
        c = cruz_by_id[code]

        subtopics = []
        dossiers = []
        for f in c.get('fontes', []):
            dpath = Path(f['dados'])
            external_sources[f['id_dossie']] = file_ref(dpath)
            keys, coverage = [], {}
            if dpath.exists():
                d = load(dpath)
                keys = d.get('chaves', [])
                coverage = d.get('cobertura', {})
            for k in keys:
                subtopics.append({
                    'term': k,
                    'dossier_id': f['id_dossie'],
                    'book_coverage': coverage.get(k, []),
                    'has_book_source': bool(coverage.get(k)),
                })
            dossiers.append({
                'dossier_id': f['id_dossie'],
                'dossier_theme': f.get('tema'),
                'keys_without_source': f.get('chaves_sem_fonte', []),
                'questions_md': f.get('questoes_md'),
                'questions_classified_in_dossier': f.get('questoes_classificadas'),
            })

        overlaps = sorted({u for f in c.get('fontes', []) for u in dossie_users[f['id_dossie']]} - {code})

        examples = [{
            'ref': o['uid'],
            'statement_preview': preview(o.get('enunciado')),
            'has_figure': bool(o.get('possui_figura')),
            'source_type': o.get('tipo_principal'),
        } for o in sorted(ex_by_mod.get(code, []), key=lambda x: x['uid'])]

        modules.append({
            'code': code,
            'track_order': order,
            'title': s.get('subtema'),
            'area': s.get('area'),
            'theme': s.get('tema'),
            'description': None,
            'learning_objectives': [],
            'subtopics': subtopics,
            'prerequisites': s.get('pre_requisitos', []),
            'includes': [],
            'excludes': [],
            'overlaps_with': overlaps,
            'examples': examples,
            'counterexamples': [],
            'activity_type': s.get('atividade'),
            'pedagogical_priority': s.get('prioridade_pedagogica'),
            'support_books': s.get('livros', []),
            'official_matrix_item': s.get('item_matriz_referencia'),
            'official_matrix_status': s.get('matriz_status'),
            'support_dossiers': dossiers,
            'editorial_notes': [x for x in [c.get('observacao')] if x],
            'cross_map_status': c.get('status'),
            'field_status': {
                'title': 'EXTRACTED:mapa-conteudo.subtemas[].subtema',
                'area': 'EXTRACTED:mapa-conteudo.subtemas[].area',
                'theme': 'EXTRACTED:mapa-conteudo.subtemas[].tema',
                'description': MISSING,
                'learning_objectives': MISSING,
                'subtopics': 'EXTRACTED:dossie.chaves (termos de busca do dossie; candidatos, nao validados como ementa)',
                'prerequisites': 'EXTRACTED:mapa-conteudo.subtemas[].pre_requisitos',
                'includes': MISSING,
                'excludes': MISSING,
                'overlaps_with': 'DERIVED:modulos que compartilham dossie de apoio em cruzamento-35-temas (candidato, nao validado)',
                'examples': 'EXTRACTED:ocorrencias-classificadas por subtema_id (classificacao editorial Fase 2; autoria nao verificada)',
                'counterexamples': MISSING,
            },
        })

    completeness = collections.Counter()
    for m in modules:
        for fld in ['description', 'learning_objectives', 'subtopics', 'includes', 'excludes',
                    'overlaps_with', 'examples', 'counterexamples']:
            completeness[fld] += bool(m[fld])

    payload = {
        'schema_version': 1,
        'generated_at': datetime.datetime.now().isoformat(timespec='seconds'),
        'generator': 'scripts/gerar-curriculo-35-modulos.py',
        'authority_status': 'INCOMPLETE_NOT_YET_VALID_AS_SOLE_ANNOTATION_AUTHORITY',
        'authority_notes': [
            'Os 35 codigos sao subtemas internos do projeto (docs/arquitetura/04-modelo-dados.md), nao itens da Matriz de Referencia oficial.',
            'mapa-conteudo.json registra matriz_status = [VERIFICAR] para os modulos: matriz integral e curriculo local nao confirmados.',
            'description, learning_objectives, includes, excludes e counterexamples nao existem nas fontes do projeto e nao foram redigidos.',
            'Candidatos para preencher as lacunas (exige decisao editorial, nao extracao automatica): data/extraidos/plano-eletrotecnica-ce-2016.json, data/extraidos/plano-eletrotecnica-rr-semipresencial.json, docs/01-documento-saep-2023.md.',
        ],
        'field_completeness_modules_with_data': {k: f'{v}/35' for k, v in completeness.items()},
        'sources': {
            'mapa_conteudo': file_ref(MAPA),
            'ocorrencias_classificadas': file_ref(OCOR),
            'cruzamento_35_temas': file_ref(CRUZ),
            'dossiers': external_sources,
        },
        'modules': modules,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    b = OUT.read_bytes()
    print('curriculum-35-modules.json', len(b), 'bytes', hashlib.sha256(b).hexdigest())
    print('completeness', dict(completeness))
    print('dossiers found', sum(v.get('exists', False) for v in external_sources.values()), '/', len(external_sources))


if __name__ == '__main__':
    main()

