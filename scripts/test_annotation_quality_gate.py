import json
import os
import subprocess
import sys
import tempfile

VALIDATOR = 'scripts/validar-anotacoes.py'
SCHEMA = 'data/editorial/schema-anotacao-v3.json'
AUTHORING = 'data/editorial/curriculum-editorial-authoring-input.json'
EDITORIAL = 'data/editorial/curriculum-35-modules-editorial-v1.json'


def run(pack, env, extra=None):
    with tempfile.TemporaryDirectory() as td:
        pp = os.path.join(td, 'content.json')
        ap = os.path.join(td, 'ann.json')
        with open(pp, 'w', encoding='utf-8') as f:
            json.dump(pack, f, ensure_ascii=False)
        with open(ap, 'w', encoding='utf-8') as f:
            json.dump(env, f, ensure_ascii=False)
        cmd = [
            sys.executable,
            VALIDATOR,
            '--schema', SCHEMA,
            '--curriculum', AUTHORING,
            '--editorial-curriculum', EDITORIAL,
            '--pack', pp,
            '--annotations', ap,
        ]
        if extra:
            cmd += extra
        return subprocess.run(cmd, capture_output=True, text=True)


def ann(source_id='Q1', reason=None, evid=None, subtopic='Corrente elétrica', annotator='ANNOTATOR_B'):
    reason = reason or (
        'O enunciado pede reconhecer a corrente elétrica e sua unidade; '
        'isso corresponde ao subtema Corrente elétrica do módulo F01 de grandezas e unidades.'
    )
    evid = evid or 'A corrente elétrica é medida em ampères'
    return {
        'source_id': source_id,
        'annotation_version': '1.1',
        'curriculum_version': '1.0',
        'source_question_version': '1.0',
        'annotator_id': annotator,
        'in_curriculum': True,
        'primary_module': 'F01',
        'acceptable_modules': [],
        'annotation_confidence': 'HIGH',
        'reasoning_summary': reason,
        'image_status': 'NOT_APPLICABLE',
        'image_required': False,
        'ambiguity': False,
        'ambiguity_reason': '',
        'supplement_used': False,
        'supplement_fields_used': [],
        'annotation_status': 'ANNOTATED',
        'module_evidence': [
            {'kind': 'STATEMENT', 'text': evid},
            {'kind': 'CURRICULUM_SUBTOPIC', 'module': 'F01', 'subtopic': subtopic},
        ],
    }


def pack(n=1):
    return {
        'batch_id': 'quality-test',
        'curriculum_version': '1.0',
        'questions': [
            {
                'source_id': f'Q{i}',
                'source_question_version': '1.0',
                'statement': 'A corrente elétrica é medida em ampères e deve ser identificada corretamente.',
                'has_image': False,
                'image_inventory_status': 'NOT_APPLICABLE',
            }
            for i in range(1, n + 1)
        ],
    }


def env(items):
    return {'batch_id': 'quality-test', 'annotator_id': 'ANNOTATOR_B', 'annotations': items}


def assert_fail(res, *needles):
    assert res.returncode != 0, res.stdout + res.stderr
    assert any(n in res.stdout for n in needles), res.stdout + res.stderr


def test_positive():
    res = run(pack(1), env([ann()]))
    assert res.returncode == 0, res.stdout + res.stderr
    assert 'ANNOTATION_QUALITY_VALID = true' in res.stdout
    assert 'SEMANTIC_BINDING_VALID = true' in res.stdout


def test_placeholder_reasoning_rejected():
    a = ann(reason='Auto generated reasoning.')
    assert_fail(run(pack(1), env([a])), 'reasoning_summary too short', 'PLACEHOLDER_REASONING')


def test_placeholder_evidence_rejected():
    a = ann(evid='evidence')
    assert_fail(run(pack(1), env([a])), 'STATEMENT_EVIDENCE_TOO_SHORT', 'PLACEHOLDER_EVIDENCE')


def test_ungrounded_statement_evidence_rejected():
    a = ann(evid='texto que não existe de forma alguma no enunciado original')
    assert_fail(run(pack(1), env([a])), 'STATEMENT_EVIDENCE_NOT_GROUNDED')


def test_repeated_reasoning_template_rejected():
    p = pack(3)
    reason = (
        'A corrente elétrica indicada no enunciado corresponde ao subtema Corrente elétrica '
        'do módulo F01 de grandezas e unidades, portanto esta classificação é a adequada.'
    )
    items = [ann(source_id=f'Q{i}', reason=reason) for i in range(1, 4)]
    assert_fail(run(p, env(items)), 'REPEATED_REASONING_TEMPLATE')


def test_generic_reasoning_template_rejected():
    a = ann(reason='A questão aborda diretamente o conceito central deste módulo, exigindo cálculos específicos e análise do circuito.')
    assert_fail(run(pack(1), env([a])), 'GENERIC_REASONING_TEMPLATE')


def test_missing_subtopic_rejected():
    a = ann()
    a['module_evidence'] = [a['module_evidence'][0]]
    assert_fail(run(pack(1), env([a])), 'CURRICULUM_SUBTOPIC')


def test_wrong_subtopic_rejected():
    a = ann(subtopic='Subtópico inventado')
    assert_fail(run(pack(1), env([a])), 'UNKNOWN_CURRICULUM_SUBTOPIC')


def test_reason_not_linked_to_statement_rejected():
    a = ann(reason='Este conteúdo pertence ao Sistema Internacional e prefixos porque trata apenas de conversões e nomenclatura geral de unidades técnicas.')
    assert_fail(run(pack(1), env([a])), 'REASONING_NOT_LINKED_TO_STATEMENT')


def test_reason_not_linked_to_curriculum_rejected():
    a = ann(reason='A corrente elétrica aparece no enunciado, mas o raciocínio discute exclusivamente manutenção preventiva e inspeção periódica de equipamentos.')
    assert_fail(run(pack(1), env([a])), 'REASONING_NOT_LINKED_TO_CURRICULUM')


def run_tests():
    test_positive()
    test_placeholder_reasoning_rejected()
    test_placeholder_evidence_rejected()
    test_ungrounded_statement_evidence_rejected()
    test_repeated_reasoning_template_rejected()
    test_generic_reasoning_template_rejected()
    test_missing_subtopic_rejected()
    test_wrong_subtopic_rejected()
    test_reason_not_linked_to_statement_rejected()
    test_reason_not_linked_to_curriculum_rejected()
    print('ANNOTATION QUALITY V4.1.3.1 TESTS PASSED')


if __name__ == '__main__':
    run_tests()
