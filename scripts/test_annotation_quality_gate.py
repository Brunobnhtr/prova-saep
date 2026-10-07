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
        pp=os.path.join(td,'content.json'); ap=os.path.join(td,'ann.json')
        json.dump(pack, open(pp,'w',encoding='utf-8'), ensure_ascii=False)
        json.dump(env, open(ap,'w',encoding='utf-8'), ensure_ascii=False)
        cmd=[sys.executable,VALIDATOR,'--schema',SCHEMA,'--curriculum',AUTHORING,'--editorial-curriculum',EDITORIAL,'--pack',pp,'--annotations',ap]
        if extra: cmd += extra
        return subprocess.run(cmd,capture_output=True,text=True)


def ann(reason, evid, subtopic='Corrente elétrica'):
    return {
      'source_id':'Q1','annotation_version':'1.1','curriculum_version':'1.0','source_question_version':'1.0',
      'annotator_id':'ANNOTATOR_B','in_curriculum':True,'primary_module':'F01','acceptable_modules':[],
      'annotation_confidence':'HIGH','reasoning_summary':reason,'image_status':'NOT_APPLICABLE','image_required':False,
      'ambiguity':False,'ambiguity_reason':'','supplement_used':False,'supplement_fields_used':[],
      'annotation_status':'ANNOTATED','module_evidence':[
        {'kind':'STATEMENT','text':evid},
        {'kind':'CURRICULUM_SUBTOPIC','module':'F01','subtopic':subtopic}
      ]
    }

PACK={'batch_id':'q','curriculum_version':'1.0','questions':[{'source_id':'Q1','source_question_version':'1.0','statement':'A corrente elétrica é medida em ampères e deve ser identificada corretamente.','has_image':False,'image_inventory_status':'NOT_APPLICABLE'}]}


def test_positive():
    a=ann('O enunciado pede reconhecer a corrente elétrica e sua unidade; isso corresponde ao subtema Corrente elétrica do módulo F01 de grandezas e unidades.','A corrente elétrica é medida em ampères')
    r=run(PACK,{'batch_id':'q','annotator_id':'ANNOTATOR_B','annotations':[a]})
    assert r.returncode==0, r.stdout+r.stderr
    assert 'SEMANTIC_BINDING_VALID = true' in r.stdout


def test_random_template_rejected():
    a=ann('A questão aborda diretamente o conceito central deste módulo, exigindo cálculos específicos e análise do circuito.','A corrente elétrica é medida em ampères')
    r=run(PACK,{'batch_id':'q','annotator_id':'ANNOTATOR_B','annotations':[a]})
    assert r.returncode!=0 and 'GENERIC_REASONING_TEMPLATE' in r.stdout


def test_missing_subtopic_rejected():
    a=ann('O enunciado pede reconhecer a corrente elétrica e sua unidade; isso corresponde ao módulo F01 de grandezas e unidades.','A corrente elétrica é medida em ampères')
    a['module_evidence']=[a['module_evidence'][0]]
    r=run(PACK,{'batch_id':'q','annotator_id':'ANNOTATOR_B','annotations':[a]})
    assert r.returncode!=0 and 'CURRICULUM_SUBTOPIC' in r.stdout


def test_wrong_subtopic_rejected():
    a=ann('O enunciado pede reconhecer a corrente elétrica e sua unidade; isso corresponde ao módulo F01 de grandezas e unidades.','A corrente elétrica é medida em ampères','Subtópico inventado')
    r=run(PACK,{'batch_id':'q','annotator_id':'ANNOTATOR_B','annotations':[a]})
    assert r.returncode!=0 and 'UNKNOWN_CURRICULUM_SUBTOPIC' in r.stdout


def test_reason_not_linked_to_statement_rejected():
    a=ann('Este conteúdo pertence ao Sistema Internacional e prefixos porque trata apenas de conversões e nomenclatura geral de unidades técnicas.','A corrente elétrica é medida em ampères')
    r=run(PACK,{'batch_id':'q','annotator_id':'ANNOTATOR_B','annotations':[a]})
    assert r.returncode!=0 and 'REASONING_NOT_LINKED_TO_STATEMENT' in r.stdout


def run_tests():
    test_positive(); test_random_template_rejected(); test_missing_subtopic_rejected(); test_wrong_subtopic_rejected(); test_reason_not_linked_to_statement_rejected()
    print('ANNOTATION QUALITY V4.1.3 TESTS PASSED')

if __name__=='__main__': run_tests()
