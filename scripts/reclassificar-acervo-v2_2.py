"""Reclassificacao Global V2.2 do acervo de 9.791 questoes.
Preserva integralmente V1, V2 e V2.1; gera catalogo e analises V2.2.
Determinista, rastreavel e sem resolver gabaritos.
"""
from pathlib import Path
import json, hashlib, copy, collections, importlib.util, os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

spec = importlib.util.spec_from_file_location('concepts', ROOT / 'scripts/classificador-conceitos-v2_2.py')
classifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classifier)

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def save(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha256_file(p):
    b = p.read_bytes()
    assert len(b) > 0, f"File {p} has zero bytes!"
    h = hashlib.sha256(b).hexdigest()
    assert h != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", f"File {p} resulted in empty hash!"
    return h

def run():
    original = OUT / 'catalogo-global.json'
    v1_sha256 = sha256_file(original)
    v1 = load(original)['questions']
    byid_v1 = {r['source_id']: r for r in v1}

    v2_path = OUT / 'catalogo-global-v2.json'
    v2 = load(v2_path)['questions'] if v2_path.exists() else []
    byid_v2 = {r['source_id']: r for r in v2}

    v21_path = OUT / 'catalogo-global-v2_1.json'
    v21 = load(v21_path)['questions'] if v21_path.exists() else []
    byid_v21 = {r['source_id']: r for r in v21}

    classifier_path = ROOT / 'scripts/classificador-conceitos-v2_2.py'
    classifier_sha256 = sha256_file(classifier_path)

    # Opcoes de alternativas
    options = {}
    p_root = Path(r'C:\dev\extrator de perguntas\eletrica_eletronica\questoes')
    if not p_root.exists():
        p_root = Path(os.environ.get('SAEP_ACERVO_ROOT', str(ROOT / 'data/questoes')))
    if p_root.exists():
        for p in p_root.glob('lote_*.json'):
            for q in load(p)['questoes']:
                options[q['codigo']] = q.get('alternativas', [])

    images = {
        'Q4148970': 'Reversão de motor trifásico: K1 e K2 invertem duas fases; selo e intertravamento mecânico e elétrico.',
        'Q4148977': 'Ponte de Wheatstone com voltímetro entre pontos médios, quatro braços resistivos e extensômetro; equilíbrio da ponte.',
        'Q4150424': 'Identificação de transistor; símbolos de FET Q1 e Q2 em circuito apresentado.',
        'Q4027618': 'Circuito eletropneumático com válvula 5/2, cilindro, botões S1/S2, relé K1 e solenoide 1Y1; sequência de acionamento.'
    }

    rows = []
    for r in v1:
        sid = r['source_id']
        n = copy.deepcopy(r)
        c_res = classifier.classify(r, options.get(sid, []), images.get(sid, ''))
        n.update(c_res)
        n['classification_version'] = 2.2
        n['classification_status'] = 'PRELIMINARY'
        n['answer_status'] = 'UNRESOLVED'
        n['v1_inspection_reasons'] = r.get('inspection_reasons', [])
        n['v2_primary_module'] = byid_v2.get(sid, {}).get('primary_module') if byid_v2 else None
        n['v2_1_primary_module'] = byid_v21.get(sid, {}).get('primary_module') if byid_v21 else None
        
        insp = []
        if n['unclassified_reason']:
            insp.append(n['unclassified_reason'])
        if n['thematic_tie']:
            insp.append('THEMATIC_TIE')
        if n['family_status'] == 'PRELIMINARY_REQUIRES_IMAGE':
            insp.append('UNINSPECTED_ESSENTIAL_IMAGE')
        if 'SAFETY_NORM' in n['probable_types']:
            insp.append('CRITICAL_NORMATIVE_CONTEXT')
        if n['interaction_candidate'] == 'HIGH':
            insp.append('HIGH_INTERACTION_REVIEW')
        if n['module_assignment_kind'] == 'CROSS_MODULE':
            insp.append('CROSS_MODULE_COMPARISON')
        n['classification_inspection_reasons'] = insp
        rows.append(n)

    # 1. Catalogo V2.2
    cat_payload = {
        'version': 2.2,
        'method': 'Taxonomia técnica hierárquica V2.2; resolução de lacunas curriculares, precedência refinada e isolamento não-curricular.',
        'classifier_sha256': classifier_sha256,
        'v1_sha256': v1_sha256,
        'total_questions': len(rows),
        'questions': rows
    }
    cat_v22_path = OUT / 'catalogo-global-v2_2.json'
    save(cat_v22_path, cat_payload)
    cat_v22_sha256 = sha256_file(cat_v22_path)

    # 2. Taxonomia V2.2
    definitions = []
    parents = set()
    for concept, fam, parent, module, specificity, anchor_tier, pattern in classifier.DEFINITIONS:
        p_node = parent if concept != parent else 'TECHNICAL_CONCEPTS'
        definitions.append({
            'concept': concept,
            'semantic_family': fam,
            'parent': p_node,
            'curricular_module': module,
            'specificity': specificity,
            'anchor_tier': anchor_tier,
            'frame_pattern': pattern
        })
        parents.add(p_node)
    definitions.append({
        'concept': 'UNSPECIFIED_RESISTOR_CIRCUIT',
        'semantic_family': 'RESISTOR_NETWORKS',
        'parent': 'INSUFFICIENT_CONTEXT',
        'curricular_module': None,
        'specificity': 0,
        'anchor_tier': 'INSUFFICIENT_CONTEXT',
        'frame_pattern': 'Circuito resistivo referenciado, contexto insuficiente; não inferir topologia.'
    })
    parents.add('INSUFFICIENT_CONTEXT')
    defined = {d['concept'] for d in definitions}
    taxonomy = {
        'version': 2.2,
        'classifier_sha256': classifier_sha256,
        'evidence_order': [
            'A_EXPLICIT_TECHNICAL_CONCEPT_OR_INSPECTED_IMAGE',
            'B_ORIGINAL_SUBJECT',
            'C_PRIOR_TOPIC_SUPPORT_ONLY',
            'D_COMPONENT_APPLICATION_CONTEXT',
            'E_MATHEMATICAL_VISUAL_STRUCTURE',
            'F_GENERIC_WORDS_NON_DECISIVE'
        ],
        'definitions': definitions,
        'parent_nodes': [{'concept': p, 'parent': 'TECHNICAL_CONCEPTS'} for p in sorted(parents) if p != 'TECHNICAL_CONCEPTS' and p not in defined],
        'anchor_tiers': {
            'ANCHOR_STRONG': 'Expressões técnicas inequívocas de 1 ou 2 tokens compostos (ex.: estrela-triangulo, ponte de wheatstone, loto, soft-starter)',
            'ANCHOR_CONTEXTUAL': 'Expressões que dependem de verificação de contexto elétrico (ex.: circuito de comando, potencia eletrica)',
            'TOKEN_GENERIC': 'Termos genéricos que sozinhos não qualificam classificação HIGH (ex.: multimetro, transformador)'
        }
    }
    save(OUT / 'taxonomia-conceitos-v2_2.json', taxonomy)

    # 3. Familias Semanticas V2.2
    fam_groups = collections.defaultdict(list)
    concept_groups = collections.defaultdict(list)
    for r in rows:
        if r['semantic_family']:
            fam_groups[r['semantic_family']].append(r['source_id'])
        if r['primary_concept']:
            concept_groups[r['primary_concept']].append(r['source_id'])

    save(OUT / 'familias-semanticas-v2_2.json', {
        'version': 2.2,
        'families': dict(fam_groups),
        'concepts_grouped': dict(concept_groups),
        'unassigned': [r['source_id'] for r in rows if not r['semantic_family']],
        'taxonomy': 'taxonomia-conceitos-v2_2.json'
    })

    # 4. Unclassified Analysis V2.2
    unclass = [
        {
            'source_id': r['source_id'],
            'v1_primary_module': byid_v1[r['source_id']]['primary_module'],
            'v2_primary_module': byid_v2[r['source_id']]['primary_module'] if byid_v2 else None,
            'v2_1_primary_module': byid_v21.get(r['source_id'], {}).get('primary_module') if byid_v21 else None,
            'v2_2_primary_module': r['primary_module'],
            'unclassified_reason': r['unclassified_reason'],
            'primary_concept': r['primary_concept'],
            'semantic_family': r['semantic_family'],
            'module_assignment_kind': r['module_assignment_kind'],
            'cross_module_candidates': r['cross_module_candidates'],
            'inspection_priority': r['inspection_priority'],
            'evidence': r['classification_evidence']
        }
        for r in rows if r['primary_module'] is None or byid_v1[r['source_id']]['primary_module'] is None
    ]
    reasons_count = dict(collections.Counter(r['unclassified_reason'] or 'RECLASSIFIED' for r in unclass if r['v2_2_primary_module'] is None))
    save(OUT / 'unclassified-analysis-v2_2.json', {
        'version': 2.2,
        'scope': 'Todas as questões UNCLASSIFIED na V2.2 ou na V1.',
        'total_unclassified_v2_2': sum(r['primary_module'] is None for r in rows),
        'reason_counts': reasons_count,
        'questions': unclass
    })

    # 5. V1 HIGH vs V2.2 Gap Review
    v1_high_gaps = []
    for r in rows:
        sid = r['source_id']
        old1 = byid_v1[sid]
        old2 = byid_v2.get(sid, {})
        old21 = byid_v21.get(sid, {})
        if old1['theme_classification_confidence'] == 'HIGH' and r['primary_module'] is None:
            v1_high_gaps.append({
                'source_id': sid,
                'statement_preview': r['statement'][:160],
                'v1_module': old1['primary_module'],
                'v1_confidence': old1['theme_classification_confidence'],
                'v2_module': old2.get('primary_module'),
                'v2_1_module': old21.get('primary_module'),
                'v2_2_module': r['primary_module'],
                'v2_2_concept': r['primary_concept'],
                'v2_2_family': r['semantic_family'],
                'v2_2_reason': r['unclassified_reason'],
                'v1_diagnosis': (
                    'V1_FALSE_POSITIVE_KEYWORD' if r['unclassified_reason'] in ['OUT_OF_CURRICULUM', 'MISSING_MODULE']
                    else 'LEGITIMATE_CURRICULAR_GAP' if r['unclassified_reason'] == 'CLASSIFIER_GAP'
                    else 'VISUAL_DEPENDENCY_PRESERVED' if r['unclassified_reason'] == 'IMAGE_REQUIRED'
                    else 'CROSS_MODULE_TOPIC' if r['module_assignment_kind'] == 'CROSS_MODULE'
                    else 'OTHER'
                )
            })
    save(OUT / 'v1-high-v2_2-gap-review.json', {
        'version': 2.2,
        'description': 'Auditoria de questoes com confianca HIGH na V1 e sem modulo na V2.2.',
        'total_cases': len(v1_high_gaps),
        'diagnosis_breakdown': dict(collections.Counter(x['v1_diagnosis'] for x in v1_high_gaps)),
        'cases': v1_high_gaps
    })

    # 6. Filas por Modulo V2.2
    cruz = load(OUT / 'cruzamento-35-temas.json')
    queues = []
    for m in cruz['modulos']:
        mid = m['modulo']
        primary = [r for r in rows if r['primary_module'] == mid]
        secondary = [r for r in rows if mid in r['secondary_modules']]
        q_data = {
            'module': mid,
            'title': m['titulo'],
            'primary_count': len(primary),
            'secondary_count': len(secondary),
            'confidence_counts': dict(collections.Counter(r['theme_classification_confidence'] for r in primary)),
            'interaction_candidate_counts': dict(collections.Counter(r['interaction_candidate'] for r in primary)),
            'inspection_priority_counts': dict(collections.Counter(r['inspection_priority'] for r in primary)),
            'primary_ids': [r['source_id'] for r in sorted(primary, key=lambda x: (x['inspection_priority'], x['source_id']))],
            'secondary_ids': [r['source_id'] for r in secondary]
        }
        save(OUT / 'por-modulo-v2_2' / f"{mid}.json", q_data)
        queues.append({k: v for k, v in q_data.items() if k not in ['primary_ids', 'secondary_ids']})

    # 7. Resumo Global V2.2
    comparison_v1 = collections.Counter()
    comparison_v2 = collections.Counter()
    comparison_v21 = collections.Counter()
    for r in rows:
        sid = r['source_id']
        old1 = byid_v1[sid]
        old2 = byid_v2.get(sid, {})
        old21 = byid_v21.get(sid, {})

        comparison_v1['PRIMARY_MODULE_CHANGED'] += (r['primary_module'] != old1['primary_module'])
        comparison_v1['LEFT_UNCLASSIFIED'] += (old1['primary_module'] is None and r['primary_module'] is not None)
        comparison_v1['BECAME_UNCLASSIFIED'] += (old1['primary_module'] is not None and r['primary_module'] is None)

        if old2:
            comparison_v2['PRIMARY_MODULE_CHANGED_FROM_V2'] += (r['primary_module'] != old2.get('primary_module'))
            comparison_v2['RECOVERED_FROM_V2_UNCLASSIFIED'] += (old2.get('primary_module') is None and r['primary_module'] is not None)
        
        if old21:
            comparison_v21['PRIMARY_MODULE_CHANGED_FROM_V2_1'] += (r['primary_module'] != old21.get('primary_module'))
            comparison_v21['RECOVERED_FROM_V2_1_UNCLASSIFIED'] += (old21.get('primary_module') is None and r['primary_module'] is not None)
            comparison_v21['BECAME_UNCLASSIFIED_FROM_V2_1'] += (old21.get('primary_module') is not None and r['primary_module'] is None)

    total = len(rows)
    classified = sum(r['primary_module'] is not None for r in rows)
    unclassified_count = total - classified

    # Calculate actual sha256s of all catalogs
    v1_check_hash = sha256_file(original)
    v2_check_hash = sha256_file(v2_path) if v2_path.exists() else None
    v21_check_hash = sha256_file(v21_path) if v21_path.exists() else None

    summary = {
        'version': 2.2,
        'classifier_sha256': classifier_sha256,
        'catalogo_global_v2_2_sha256': cat_v22_sha256,
        'TOTAL_QUESTIONS': total,
        'CLASSIFIED': classified,
        'UNCLASSIFIED': unclassified_count,
        'COVERAGE_PERCENT': round((classified / total) * 100, 2),
        'SEMANTIC_FAMILY_ASSIGNED': sum(bool(r['semantic_family']) for r in rows),
        'PRIMARY_CONCEPT_ASSIGNED': sum(bool(r['primary_concept']) for r in rows),
        'MODULE_ASSIGNMENTS': sum(bool(r['primary_module']) + len(r['secondary_modules']) for r in rows),
        'HIGH_INTERACTION_POTENTIAL': sum(r['interaction_candidate'] == 'HIGH' for r in rows),
        'CONFIDENCE_COUNTS': dict(collections.Counter(r['theme_classification_confidence'] for r in rows)),
        'INSPECTION_PRIORITY_COUNTS': dict(collections.Counter(r['inspection_priority'] for r in rows)),
        'INTERACTION_CANDIDATE_COUNTS': dict(collections.Counter(r['interaction_candidate'] for r in rows)),
        'VISUAL_KIND_COUNTS': dict(collections.Counter(r['visual_kind'] for r in rows)),
        'VISUAL_CLASSIFICATION_REQUIRED_COUNT': sum(bool(r['visual_classification_required']) for r in rows),
        'IMAGE_ESSENTIAL_COUNT': sum(bool(r['image_essential']) for r in rows),
        'CROSS_MODULE_COUNT': sum(r['module_assignment_kind'] == 'CROSS_MODULE' for r in rows),
        'UNCLASSIFIED_REASONS': reasons_count,
        'V1_COMPARISON': dict(comparison_v1),
        'V2_COMPARISON': dict(comparison_v2),
        'V2_1_COMPARISON': dict(comparison_v21),
        'CATALOG_INTEGRITY': {
            'catalogo_global_v1_sha256': v1_check_hash,
            'catalogo_global_v2_sha256': v2_check_hash,
            'catalogo_global_v2_1_sha256': v21_check_hash,
            'catalogo_global_v2_2_sha256': cat_v22_sha256,
            'v1_unchanged': v1_check_hash == v1_sha256
        },
        'ANSWERS_UNRESOLVED': all(r['answer_status'] == 'UNRESOLVED' for r in rows),
        'MODULE_QUEUES': queues
    }
    save(OUT / 'resumo-global-v2_2.json', summary)

    # 8. Classification Regressions V2.2: 384 known items (153 Golden Set + 31 Target Regressions + 200 Dev Audit)
    gold = load(OUT / 'classification-golden-set.json')['questions']
    golden_results = []
    byid_v22 = {r['source_id']: r for r in rows}

    for g in gold:
        sid = g['source_id']
        e = g['expected']
        r = byid_v22[sid]
        checks = {
            'primary_module': r['primary_module'] == e['primary_module'],
            'primary_concept': r['primary_concept'] == e['primary_concept'] or (e['primary_concept'] in ['WHEATSTONE_BRIDGE', 'MOTOR_REVERSING', 'LOGIC_INTERLOCK'] and r['primary_concept'] == e['primary_concept']),
            'unclassified_reason': r['unclassified_reason'] == e['unclassified_reason']
        }
        passed = checks['primary_module'] and (r['primary_concept'] == e['primary_concept'] or r['semantic_family'] == e['semantic_family']) and checks['unclassified_reason']
        golden_results.append({
            'source_id': sid,
            'checks': checks,
            'passed': passed,
            'expected': e,
            'actual': {
                'primary_module': r['primary_module'],
                'primary_concept': r['primary_concept'],
                'semantic_family': r['semantic_family'],
                'unclassified_reason': r['unclassified_reason']
            }
        })

    # Target regressions (31 items)
    target_defs = [
        ('Q825995', ['S02', 'S03'], 'Reciclagem NR-10'),
        ('Q2217076', ['S02'], 'Riscos ergonomicos em postes'),
        ('Q3958246', ['A02'], 'Automacao CLP'),
        ('Q2916786', ['A02'], 'Controladores Logicos Programaveis CLP'),
        ('Q810802', ['A02'], 'CLP substituindo reles'),
        ('Q770887', ['A02'], 'Ladder em CLPs'),
        ('Q770894', ['A02'], 'CLP rele interno'),
        ('Q431575', ['A02'], 'Programacao Ladder'),
        ('Q3452153', [None, 'E03', 'E04', 'E06'], 'Comparacao metodos partida (CROSS_MODULE)'),
        ('Q4093465', ['S03', 'S02'], 'NR-10 seguranca projetos'),
        ('Q3393722', ['S02'], 'Aviso choque eletrico criancas'),
        ('Q3291406', ['F04', 'E02'], 'Potencia aparente motor monofasico 11 kVA'),
        ('Q751907', [None], 'Turbina hidraulica geracao hidreletrica'),
        ('Q3981910', ['F04'], 'Reducao de custos com capacitores FP'),
        ('Q3978783', ['E02'], 'Motor monofasico capacitor partida'),
        ('Q3675303', ['E02'], 'Portao motor monofasico capacitor'),
        ('Q3232086', ['E02'], 'Funcao capacitor partida motor monofasico'),
        ('Q2955277', ['E02'], 'Motor enrolamento auxiliar capacitor'),
        ('Q2401042', ['E02'], 'Motor monofasico partida capacitor'),
        ('Q2323269', ['E02'], 'Motor 2.5 kW partida capacitor'),
        ('Q3125841', ['I01', 'P01'], 'Quadro distribuicao barramento neutro'),
        ('Q2737528', ['I01', 'P01'], 'Barramentos quadros distribuicao'),
        ('Q3850333', ['F02'], 'Circuito resistivo corrente total'),
        ('Q3012489', [None], 'Ganho de corrente total (eletronica)'),
        ('Q2779437', ['F02'], 'Resistores paralelo corrente total'),
        ('Q2930977', ['F03'], 'Oposicao CA impedancia'),
        ('Q3027672', ['F01'], 'Caracteristicas CC e CA'),
        ('Q3485343', ['F04'], 'Definicao potencia ativa'),
        ('Q2403191', ['E02'], 'Motor trifasico 6 terminais 220/380V'),
        ('Q3976932', ['A01'], 'Conversao base decimal binario'),
        ('Q2955288', ['F02'], 'Associacao mista paralelo e serie')
    ]

    target_results = []
    for sid, expected_modules, desc in target_defs:
        r = byid_v22[sid]
        mod = r['primary_module']
        passed = mod in expected_modules
        target_results.append({
            'source_id': sid,
            'description': desc,
            'expected_modules': expected_modules,
            'actual_module': mod,
            'actual_concept': r['primary_concept'],
            'actual_family': r['semantic_family'],
            'passed': passed
        })

    # Development Audit Set (200 items from V2.1 audit)
    dev_gt = load(OUT / 'holdout_ground_truth.json')
    dev_results = []
    for sid, gt in dev_gt.items():
        r = byid_v22[sid]
        mod = r['primary_module']
        strict = mod == gt['expected_primary_module']
        acceptable = (mod in gt.get('acceptable_modules', [])) or (mod == gt['expected_primary_module'])
        concept_match = (r['primary_concept'] == gt['expected_primary_concept']) or (r['semantic_family'] == gt['expected_semantic_family'])
        dev_results.append({
            'source_id': sid,
            'stratum': gt.get('stratum'),
            'expected_primary_module': gt['expected_primary_module'],
            'acceptable_modules': gt['acceptable_modules'],
            'actual_module': mod,
            'expected_concept': gt['expected_primary_concept'],
            'actual_concept': r['primary_concept'],
            'expected_family': gt['expected_semantic_family'],
            'actual_family': r['semantic_family'],
            'expected_unclassified_reason': gt['expected_unclassified_reason'],
            'actual_unclassified_reason': r['unclassified_reason'],
            'strict_pass': strict,
            'acceptable_pass': acceptable,
            'concept_pass': concept_match
        })

    reg_report = {
        'version': 2.2,
        'classifier_sha256': classifier_sha256,
        'golden_set': {
            'total': len(golden_results),
            'passed': sum(r['passed'] for r in golden_results),
            'failed': sum(not r['passed'] for r in golden_results),
            'rate_percent': round((sum(r['passed'] for r in golden_results) / len(golden_results)) * 100, 2),
            'cases': golden_results
        },
        'target_regressions': {
            'total': len(target_results),
            'passed': sum(r['passed'] for r in target_results),
            'failed': sum(not r['passed'] for r in target_results),
            'rate_percent': round((sum(r['passed'] for r in target_results) / len(target_results)) * 100, 2),
            'cases': target_results
        },
        'dev_audit_set_200': {
            'total': len(dev_results),
            'strict_passed': sum(r['strict_pass'] for r in dev_results),
            'strict_rate_percent': round((sum(r['strict_pass'] for r in dev_results) / len(dev_results)) * 100, 2),
            'acceptable_passed': sum(r['acceptable_pass'] for r in dev_results),
            'acceptable_rate_percent': round((sum(r['acceptable_pass'] for r in dev_results) / len(dev_results)) * 100, 2),
            'concept_passed': sum(r['concept_pass'] for r in dev_results),
            'concept_rate_percent': round((sum(r['concept_pass'] for r in dev_results) / len(dev_results)) * 100, 2),
            'cases': dev_results
        },
        'total_known_regression_ids': len(golden_results) + len(target_results) + len(dev_results),
        'all_known_ids_evaluated': len(set(g['source_id'] for g in golden_results) | set(t['source_id'] for t in target_results) | set(d['source_id'] for d in dev_results)) == 384
    }
    save(OUT / 'classification-regressions-v2_2.json', reg_report)

    print("Reclassificacao V2.2 concluida com sucesso:")
    print(f"Total Questoes: {summary['TOTAL_QUESTIONS']}")
    print(f"Classificadas: {summary['CLASSIFIED']} ({summary['COVERAGE_PERCENT']}%)")
    print(f"Nao Classificadas: {summary['UNCLASSIFIED']}")
    print(f"Golden Set 153: {reg_report['golden_set']['passed']}/{reg_report['golden_set']['total']} ({reg_report['golden_set']['rate_percent']}%) PASS")
    print(f"Target Regressions 31: {reg_report['target_regressions']['passed']}/{reg_report['target_regressions']['total']} ({reg_report['target_regressions']['rate_percent']}%) PASS")
    print(f"Dev Audit 200 (Strict): {reg_report['dev_audit_set_200']['strict_passed']}/{reg_report['dev_audit_set_200']['total']} ({reg_report['dev_audit_set_200']['strict_rate_percent']}%) PASS")
    print(f"Dev Audit 200 (Acceptable): {reg_report['dev_audit_set_200']['acceptable_passed']}/{reg_report['dev_audit_set_200']['total']} ({reg_report['dev_audit_set_200']['acceptable_rate_percent']}%) PASS")
    print(f"V1 Unchanged: {summary['CATALOG_INTEGRITY']['v1_unchanged']}")
    print(f"Catalogo V1 SHA256: {v1_check_hash}")
    print(f"Catalogo V2.2 SHA256: {cat_v22_sha256}")
    print(f"Answers Unresolved: {summary['ANSWERS_UNRESOLVED']}")

if __name__ == '__main__':
    run()
