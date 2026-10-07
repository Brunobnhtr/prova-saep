import unittest,json,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/acervo-ampliado'
spec=importlib.util.spec_from_file_location('classifier',ROOT/'scripts/classificador-conceitos-v2.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
def fixture(statement,subjects=None,prior=None):
 return {'statement':statement,'current_subthemes':subjects or [],'prior_topics':prior or [],'image_status':'IMAGE_OPTIONAL','has_image':False,'text_available':True,'alternatives_count':4}
options=[{'letra':x,'texto':'Alternativa '+x} for x in 'ABCD']
class ClassificationTests(unittest.TestCase):
 def test_frozen_golden_regressions(self):
  r=json.loads((OUT/'classification-regressions.json').read_text(encoding='utf-8'))
  self.assertEqual(r['golden_size'],153)
  for case in r['cases']:
   with self.subTest(source_id=case['source_id']):self.assertTrue(case['passed'],case)
 def test_prior_topic_cannot_classify_alone(self):
  r=c.classify(fixture('Assinale a alternativa correta sobre o objeto.',prior=[{'title':'Desenergização e reenergização'}]),options)
  self.assertIsNone(r['primary_module'])
 def test_incidental_transformer_does_not_create_secondary(self):
  r=c.classify(fixture('Qual instrumento mede resistência de isolamento no motor e no transformador?'),options)
  self.assertEqual(r['primary_module'],'M02');self.assertEqual(r['secondary_modules'],[])
 def test_valve_blocking_is_not_electrical_lockout(self):
  r=c.classify(fixture('A válvula de bloqueio hidráulico interrompe o fluxo. Qual sua função?'),options)
  self.assertEqual(r['primary_module'],'H01');self.assertNotEqual(r['semantic_family'],'ELECTRICAL_LOCKOUT')
 def test_logic_interlock_is_control(self):
  r=c.classify(fixture('O intertravamento no circuito de comando do motor evita energizar dois contatores.'),options)
  self.assertEqual(r['primary_module'],'E03');self.assertEqual(r['primary_concept'],'LOGIC_INTERLOCK')
 def test_series_of_applications_not_series_network(self):
  r=c.classify(fixture('Extensômetros resistivos têm uma série de aplicações. Calcule o equilíbrio da ponte de Wheatstone.'),options)
  self.assertEqual(r['semantic_family'],'WHEATSTONE_BRIDGE')
 def test_power_circuit_not_power_calculation(self):
  r=c.classify(fixture('No circuito de potência e comando do motor trifásico, explique a reversão por contatores.'),options)
  self.assertEqual(r['primary_module'],'E03');self.assertNotEqual(r['primary_concept'],'THREE_PHASE_POWER')
 def test_distractors_cannot_supply_primary_alone(self):
  opts=[{'letra':x,'texto':t} for x,t in zip('ABCD',['Contator','Relé térmico','Disjuntor','Transformador'])]
  r=c.classify(fixture('Assinale a alternativa correta sobre o dispositivo.'),opts)
  self.assertIsNone(r['primary_module'])
 def test_trivial_calculation_not_automatic_high_interaction(self):
  r=c.classify(fixture('Calcule a potência elétrica de uma carga de 12 V e 2 A.'),options)
  self.assertIn('CALCULATION',r['probable_types']);self.assertNotEqual(r['interaction_candidate'],'HIGH')
 def test_explicit_transistor_concept_with_curricular_gap(self):
  r=c.classify(fixture('Qual tipo de transistor está apresentado na figura?',subjects=['Transistores']),options)
  self.assertEqual(r['primary_concept'],'TRANSISTOR_IDENTIFICATION');self.assertIsNone(r['primary_module']);self.assertEqual(r['unclassified_reason'],'MISSING_MODULE');self.assertNotEqual(r['concept_classification_confidence'],'HIGH')
 def test_v1_v2_integrity(self):
  r=json.loads((OUT/'validacao-classificacao-v2.json').read_text(encoding='utf-8'))
  self.assertEqual(r['failed'],0)
if __name__=='__main__':unittest.main()
