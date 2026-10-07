"""Validacao estrutural rigorosa e verificacao de invariantes da Classificacao V2.2.
Verifica integridade de hashes, conservacao de IDs (9.791), estado de gabaritos (UNRESOLVED)
e consistencia de todas as saidas e artefatos.
"""
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'
SCRIPTS = ROOT / 'scripts'

EMPTY_HASH = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

def file_info(p):
    assert p.exists(), f"Arquivo nao encontrado: {p}"
    b = p.read_bytes()
    sz = len(b)
    assert sz > 0, f"Arquivo {p} possui 0 bytes!"
    h = hashlib.sha256(b).hexdigest()
    assert h != EMPTY_HASH, f"Arquivo {p} resultou no hash de string vazia!"
    return {'path': str(p.relative_to(ROOT)), 'size_bytes': sz, 'sha256': h}

def main():
    tracked_files = [
        OUT / 'catalogo-global.json',
        OUT / 'catalogo-global-v2.json',
        OUT / 'catalogo-global-v2_1.json',
        OUT / 'catalogo-global-v2_2.json',
        OUT / 'resumo-global-v2_2.json',
        OUT / 'taxonomia-conceitos-v2_2.json',
        OUT / 'familias-semanticas-v2_2.json',
        OUT / 'unclassified-analysis-v2_2.json',
        OUT / 'v1-high-v2_2-gap-review.json',
        OUT / 'classification-regressions-v2_2.json',
        OUT / 'holdout-v2_2-annotation-pack.json',
        OUT / 'holdout-v2_2-meta.json',
        OUT / 'holdout-v2_2-labels.json',
        OUT / 'blind-audit-v2_2.json',
        SCRIPTS / 'classificador-conceitos-v2_2.py',
        SCRIPTS / 'reclassificar-acervo-v2_2.py',
        SCRIPTS / 'test_classificacao_v2_2.py',
        SCRIPTS / 'amostrar-holdout-v2_2.py',
        SCRIPTS / 'anotar-blind-holdout-v2_2.py',
        SCRIPTS / 'auditar-blind-holdout-v2_2.py'
    ]

    file_manifest = {}
    for f in tracked_files:
        info = file_info(f)
        file_manifest[f.name] = info

    # 1. Checagem de ID conservation (9791 em todos os catalogos)
    v1_q = json.loads((OUT / 'catalogo-global.json').read_text(encoding='utf-8-sig'))['questions']
    v2_q = json.loads((OUT / 'catalogo-global-v2.json').read_text(encoding='utf-8-sig'))['questions']
    v21_q = json.loads((OUT / 'catalogo-global-v2_1.json').read_text(encoding='utf-8-sig'))['questions']
    v22_q = json.loads((OUT / 'catalogo-global-v2_2.json').read_text(encoding='utf-8-sig'))['questions']

    assert len(v1_q) == 9791, f"V1 count {len(v1_q)} != 9791"
    assert len(v2_q) == 9791, f"V2 count {len(v2_q)} != 9791"
    assert len(v21_q) == 9791, f"V2.1 count {len(v21_q)} != 9791"
    assert len(v22_q) == 9791, f"V2.2 count {len(v22_q)} != 9791"

    v1_ids = [q['source_id'] for q in v1_q]
    v2_ids = [q['source_id'] for q in v2_q]
    v21_ids = [q['source_id'] for q in v21_q]
    v22_ids = [q['source_id'] for q in v22_q]

    assert v1_ids == v2_ids == v21_ids == v22_ids, "Ordem de IDs diverge entre catalogos!"

    # 2. Invariante de integridade V1
    v1_hash_direct = file_manifest['catalogo-global.json']['sha256']
    assert v1_hash_direct == '84172aadab440c65532b75bc8caf21ea8e5a5d844d6173cfd90e87bb22ed49a6', f"V1 SHA alterado: {v1_hash_direct}"

    # 3. Invariante de gabaritos UNRESOLVED
    assert all(q.get('answer_status') == 'UNRESOLVED' for q in v22_q), "Existe questao com resposta resolvida em V2.2!"

    # 4. Invariante de isolamento do blind holdout
    gold_set_ids = {q['source_id'] for q in json.loads((OUT / 'classification-golden-set.json').read_text(encoding='utf-8-sig'))['questions']}
    # Carregar regression report
    reg_report = json.loads((OUT / 'classification-regressions-v2_2.json').read_text(encoding='utf-8'))
    holdout_labels = json.loads((OUT / 'holdout-v2_2-labels.json').read_text(encoding='utf-8'))
    holdout_ids = set(holdout_labels.keys())
    assert len(holdout_ids) == 300, f"Holdout count {len(holdout_ids)} != 300"

    gold_ids = {c['source_id'] for c in reg_report['golden_set']['cases']}
    target_ids = {c['source_id'] for c in reg_report['target_regressions']['cases']}
    dev_audit_ids = {c['source_id'] for c in reg_report['dev_audit_set_200']['cases']}
    total_known_384 = gold_ids | target_ids | dev_audit_ids
    assert len(total_known_384) == 384, f"Total de IDs conhecidos de regressao deve ser 384, obtido {len(total_known_384)}"

    overlap = holdout_ids & total_known_384
    assert len(overlap) == 0, f"Infeccao metodologica detectada: {len(overlap)} questoes do holdout estao nos 384 conhecidos: {overlap}"

    # 5. Carregar resultados de regressao e auditoria
    audit_report = json.loads((OUT / 'blind-audit-v2_2.json').read_text(encoding='utf-8'))
    summary_v22 = json.loads((OUT / 'resumo-global-v2_2.json').read_text(encoding='utf-8'))

    validation = {
        'version': 2.2,
        'status': 'VALIDATED_CONSISTENT',
        'invariants': {
            'total_questions_exact': len(v22_q) == 9791,
            'id_sequence_conserved': True,
            'v1_intact': v1_hash_direct == '84172aadab440c65532b75bc8caf21ea8e5a5d844d6173cfd90e87bb22ed49a6',
            'no_empty_hashes': True,
            'answers_unresolved': True,
            'holdout_blind_contamination_zero': len(overlap) == 0
        },
        'catalog_metrics': {
            'total_questions': summary_v22['TOTAL_QUESTIONS'],
            'classified': summary_v22['CLASSIFIED'],
            'unclassified': summary_v22['UNCLASSIFIED'],
            'coverage_percent': summary_v22['COVERAGE_PERCENT']
        },
        'regression_metrics': {
            'golden_set_153': f"{reg_report['golden_set']['passed']}/{reg_report['golden_set']['total']} ({reg_report['golden_set']['rate_percent']}%)",
            'target_regressions_31': f"{reg_report['target_regressions']['passed']}/{reg_report['target_regressions']['total']} ({reg_report['target_regressions']['rate_percent']}%)",
            'dev_audit_200_strict': f"{reg_report['dev_audit_set_200']['strict_passed']}/{reg_report['dev_audit_set_200']['total']} ({reg_report['dev_audit_set_200']['strict_rate_percent']}%)",
            'dev_audit_200_acceptable': f"{reg_report['dev_audit_set_200']['acceptable_passed']}/{reg_report['dev_audit_set_200']['total']} ({reg_report['dev_audit_set_200']['acceptable_rate_percent']}%)"
        },
        'blind_holdout_metrics': {
            'sample_size': 300,
            'strict_agreement': f"{audit_report['summary_metrics']['strict_module_agreement']['count']}/300 ({audit_report['summary_metrics']['strict_module_agreement']['rate_percent']}%)",
            'acceptable_agreement': f"{audit_report['summary_metrics']['acceptable_module_agreement']['count']}/300 ({audit_report['summary_metrics']['acceptable_module_agreement']['rate_percent']}%)",
            'concept_agreement': f"{audit_report['summary_metrics']['concept_agreement']['count']}/300 ({audit_report['summary_metrics']['concept_agreement']['rate_percent']}%)",
            'family_agreement': f"{audit_report['summary_metrics']['family_agreement']['count']}/300 ({audit_report['summary_metrics']['family_agreement']['rate_percent']}%)",
            'high_confidence_precision': f"{audit_report['summary_metrics']['high_confidence_precision']['high_acceptable_matches']}/{audit_report['summary_metrics']['high_confidence_precision']['high_confidence_total']} ({audit_report['summary_metrics']['high_confidence_precision']['high_acceptable_rate_percent']}%)"
        },
        'file_manifest': file_manifest
    }

    out_path = OUT / 'validacao-classificacao-v2_2.json'
    out_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    val_sha = file_info(out_path)['sha256']

    print("================================================================")
    print("VALIDACAO ESTRUTURAL V2.2 COMPLETA:")
    print("================================================================")
    print("Todas as invariantes foram verificadas e aprovadas:")
    print(f"- Total Questoes: {len(v22_q)} (Exato 9.791 preservado)")
    print(f"- Integridade V1: Intacta ({v1_hash_direct})")
    print(f"- Gabaritos: 100% UNRESOLVED")
    print(f"- Blind Holdout: 300 questoes estritamente isoladas dos 384 conhecidos (Contaminacao: 0)")
    print(f"- Golden Set 153: {validation['regression_metrics']['golden_set_153']}")
    print(f"- Target Regressions 31: {validation['regression_metrics']['target_regressions_31']}")
    print(f"- Dev Audit 200: {validation['regression_metrics']['dev_audit_200_acceptable']}")
    print(f"- Blind Holdout 300: {validation['blind_holdout_metrics']['acceptable_agreement']}")
    print(f"- Validacao salva em: {out_path} (SHA256: {val_sha})")

if __name__ == '__main__':
    main()
