"""Auditoria do Blind Holdout V2.2 (300 questoes estritamente cegas).
Compara o catalogo congelado catalogo-global-v2_2.json com o ground truth editorial holdout-v2_2-labels.json.
Metodologicamente independente, auditavel e rastreavel.
"""
from pathlib import Path
import json, hashlib, collections

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

def sha256_file(p):
    b = p.read_bytes()
    assert len(b) > 0, f"Arquivo {p} tem tamanho zero!"
    return hashlib.sha256(b).hexdigest()

def main():
    cat_path = OUT / 'catalogo-global-v2_2.json'
    labels_path = OUT / 'holdout-v2_2-labels.json'
    pack_path = OUT / 'holdout-v2_2-annotation-pack.json'

    cat_sha256 = sha256_file(cat_path)
    labels_sha256 = sha256_file(labels_path)
    pack_sha256 = sha256_file(pack_path)

    catalog = json.loads(cat_path.read_text(encoding='utf-8'))['questions']
    byid_cat = {q['source_id']: q for q in catalog}

    labels = json.loads(labels_path.read_text(encoding='utf-8'))
    pack = json.loads(pack_path.read_text(encoding='utf-8'))['questions']
    pack_byid = {q['source_id']: q for q in pack}

    total = len(labels)
    assert total == 300

    strict_matches = 0
    acceptable_matches = 0
    concept_matches = 0
    family_matches = 0
    reason_matches = 0

    high_conf_total = 0
    high_conf_strict = 0
    high_conf_acceptable = 0

    detailed_results = []
    failures = []

    for sid, gt in labels.items():
        pred = byid_cat[sid]
        pack_item = pack_byid[sid]

        pred_mod = pred.get('primary_module')
        exp_mod = gt.get('expected_primary_module')
        acc_mods = gt.get('acceptable_modules', [])

        strict_ok = (pred_mod == exp_mod)
        acc_ok = (pred_mod in acc_mods) or (pred_mod == exp_mod)

        pred_concept = pred.get('primary_concept')
        exp_concept = gt.get('expected_primary_concept')
        concept_ok = (pred_concept == exp_concept)

        pred_family = pred.get('semantic_family')
        exp_family = gt.get('expected_semantic_family')
        family_ok = (pred_family == exp_family)

        pred_reason = pred.get('unclassified_reason')
        exp_reason = gt.get('expected_unclassified_reason')
        reason_ok = (pred_reason == exp_reason) if exp_mod is None else (pred_reason is None)

        conf = pred.get('theme_classification_confidence')
        if conf == 'HIGH':
            high_conf_total += 1
            if strict_ok:
                high_conf_strict += 1
            if acc_ok:
                high_conf_acceptable += 1

        if strict_ok:
            strict_matches += 1
        if acc_ok:
            acceptable_matches += 1
        if concept_ok:
            concept_matches += 1
        if family_ok:
            family_matches += 1
        if reason_ok:
            reason_matches += 1

        item_res = {
            'source_id': sid,
            'statement_preview': pred.get('statement', '')[:140],
            'theme_original': pack_item.get('original_source_theme'),
            'has_image': pred.get('has_image'),
            'expected_primary_module': exp_mod,
            'acceptable_modules': acc_mods,
            'predicted_primary_module': pred_mod,
            'strict_match': strict_ok,
            'acceptable_match': acc_ok,
            'expected_concept': exp_concept,
            'predicted_concept': pred_concept,
            'concept_match': concept_ok,
            'expected_family': exp_family,
            'predicted_family': pred_family,
            'family_match': family_ok,
            'expected_unclassified_reason': exp_reason,
            'predicted_unclassified_reason': pred_reason,
            'confidence': conf,
            'editorial_rationale': gt.get('editorial_rationale')
        }
        detailed_results.append(item_res)

        if not acc_ok:
            # Diagnose failure mode
            if exp_mod is not None and pred_mod is None:
                failure_mode = 'CONSERVATIVE_FALSE_NEGATIVE'
            elif exp_mod is None and pred_mod is not None:
                failure_mode = 'OVER_CLASSIFIED_FALSE_POSITIVE'
            else:
                failure_mode = 'MODULE_MISCLASSIFICATION'

            failures.append({
                'source_id': sid,
                'failure_mode': failure_mode,
                'statement_snippet': pred.get('statement', '')[:180],
                'expected': {
                    'primary_module': exp_mod,
                    'acceptable_modules': acc_mods,
                    'concept': exp_concept,
                    'family': exp_family,
                    'reason': exp_reason
                },
                'predicted': {
                    'primary_module': pred_mod,
                    'concept': pred_concept,
                    'family': pred_family,
                    'reason': pred_reason,
                    'confidence': conf
                },
                'editorial_rationale': gt.get('editorial_rationale')
            })

    failure_modes_count = collections.Counter(f['failure_mode'] for f in failures)

    report = {
        'version': 2.2,
        'audit_type': 'BLIND_HOLDOUT_EVALUATION',
        'sample_size': total,
        'catalogo_global_v2_2_sha256': cat_sha256,
        'holdout_labels_sha256': labels_sha256,
        'holdout_pack_sha256': pack_sha256,
        'summary_metrics': {
            'strict_module_agreement': {
                'count': strict_matches,
                'total': total,
                'rate_percent': round((strict_matches / total) * 100, 2)
            },
            'acceptable_module_agreement': {
                'count': acceptable_matches,
                'total': total,
                'rate_percent': round((acceptable_matches / total) * 100, 2)
            },
            'concept_agreement': {
                'count': concept_matches,
                'total': total,
                'rate_percent': round((concept_matches / total) * 100, 2)
            },
            'family_agreement': {
                'count': family_matches,
                'total': total,
                'rate_percent': round((family_matches / total) * 100, 2)
            },
            'unclassified_reason_agreement': {
                'count': reason_matches,
                'total': total,
                'rate_percent': round((reason_matches / total) * 100, 2)
            },
            'high_confidence_precision': {
                'high_confidence_total': high_conf_total,
                'high_strict_matches': high_conf_strict,
                'high_strict_rate_percent': round((high_conf_strict / high_conf_total) * 100, 2) if high_conf_total else 0,
                'high_acceptable_matches': high_conf_acceptable,
                'high_acceptable_rate_percent': round((high_conf_acceptable / high_conf_total) * 100, 2) if high_conf_total else 0
            }
        },
        'disagreements_total': len(failures),
        'disagreement_modes_breakdown': dict(failure_modes_count),
        'failures': failures,
        'all_evaluations': detailed_results
    }

    out_file = OUT / 'blind-audit-v2_2.json'
    out_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    audit_sha256 = sha256_file(out_file)

    print("================================================================")
    print("AUDITORIA BLIND HOLDOUT V2.2 CONCLUIDA:")
    print("================================================================")
    print(f"Tamanho da amostra cega: {total}")
    print(f"Acordo Estrito de Modulo: {strict_matches}/{total} ({report['summary_metrics']['strict_module_agreement']['rate_percent']}%)")
    print(f"Acordo Aceitavel de Modulo: {acceptable_matches}/{total} ({report['summary_metrics']['acceptable_module_agreement']['rate_percent']}%)")
    print(f"Acordo de Conceito: {concept_matches}/{total} ({report['summary_metrics']['concept_agreement']['rate_percent']}%)")
    print(f"Acordo de Familia Semantica: {family_matches}/{total} ({report['summary_metrics']['family_agreement']['rate_percent']}%)")
    print(f"Precisao em Alta Confianca (HIGH): {high_conf_acceptable}/{high_conf_total} ({report['summary_metrics']['high_confidence_precision']['high_acceptable_rate_percent']}%)")
    print(f"Total de Divergencias: {len(failures)}")
    print(f"Modos de Falha: {dict(failure_modes_count)}")
    print(f"Arquivo salvo: {out_file} (SHA256: {audit_sha256})")

if __name__ == '__main__':
    main()

