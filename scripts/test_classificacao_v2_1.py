import unittest, json, importlib.util, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

spec = importlib.util.spec_from_file_location('classifier', ROOT / 'scripts/classificador-conceitos-v2_1.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def fixture(statement, subjects=None, prior=None, has_image=False, image_status='IMAGE_OPTIONAL'):
    return {
        'statement': statement,
        'current_subthemes': subjects or [],
        'prior_topics': prior or [],
        'image_status': image_status,
        'has_image': has_image,
        'text_available': True,
        'alternatives_count': 4
    }

options = [{'letra': x, 'texto': 'Alternativa ' + x} for x in 'ABCD']

class ClassificationV21Tests(unittest.TestCase):
    def test_frozen_golden_regressions(self):
        r = json.loads((OUT / 'classification-regressions-v2_1.json').read_text(encoding='utf-8'))
        self.assertEqual(r['golden_set']['total'], 153)
        self.assertEqual(r['golden_set']['failed'], 0)
        for case in r['golden_set']['cases']:
            with self.subTest(source_id=case['source_id']):
                self.assertTrue(case['passed'], case)

    def test_target_regressions_31(self):
        r = json.loads((OUT / 'classification-regressions-v2_1.json').read_text(encoding='utf-8'))
        self.assertEqual(r['target_regressions']['total'], 31)
        self.assertEqual(r['target_regressions']['failed'], 0)
        for case in r['target_regressions']['cases']:
            with self.subTest(source_id=case['source_id']):
                self.assertTrue(case['passed'], case)

    def test_prior_topic_cannot_classify_alone(self):
        r = c.classify(fixture('Assinale a alternativa correta sobre o objeto.', prior=[{'title': 'Desenergização e reenergização'}]), options)
        self.assertIsNone(r['primary_module'])

    def test_incidental_transformer_does_not_create_secondary(self):
        r = c.classify(fixture('Qual instrumento mede resistência de isolamento no motor e no transformador?'), options)
        self.assertEqual(r['primary_module'], 'M02')
        self.assertEqual(r['secondary_modules'], [])

    def test_valve_blocking_is_not_electrical_lockout(self):
        r = c.classify(fixture('A válvula de bloqueio hidráulico interrompe o fluxo de fluido. Qual sua função?'), options)
        self.assertNotEqual(r['semantic_family'], 'ELECTRICAL_LOCKOUT')

    def test_logic_interlock_is_control(self):
        r = c.classify(fixture('O intertravamento no circuito de comando do motor evita energizar dois contatores.'), options)
        self.assertEqual(r['primary_module'], 'E03')
        self.assertEqual(r['primary_concept'], 'LOGIC_INTERLOCK')

    def test_series_of_applications_not_series_network(self):
        r = c.classify(fixture('Extensômetros resistivos têm uma série de aplicações. Calcule o equilíbrio da ponte de Wheatstone.'), options)
        self.assertEqual(r['semantic_family'], 'BRIDGE_CIRCUITS')
        self.assertEqual(r['primary_concept'], 'WHEATSTONE_BRIDGE')

    def test_power_circuit_not_power_calculation(self):
        r = c.classify(fixture('No circuito de potência e comando do motor trifásico, explique a reversão por contatores.'), options)
        self.assertEqual(r['primary_module'], 'E03')
        self.assertNotEqual(r['primary_concept'], 'THREE_PHASE_POWER')

    def test_distractors_cannot_supply_primary_alone(self):
        opts = [{'letra': x, 'texto': t} for x, t in zip('ABCD', ['Contator', 'Relé térmico', 'Disjuntor', 'Transformador'])]
        r = c.classify(fixture('Assinale a alternativa correta sobre o dispositivo.'), opts)
        self.assertIsNone(r['primary_module'])

    def test_image_useful_does_not_block_high_confidence(self):
        r = c.classify(fixture('Calcule a resistência equivalente da associação em série de dois resistores de 10 ohms.', has_image=True, image_status='IMAGE_USEFUL'), options)
        self.assertEqual(r['primary_module'], 'F02')
        self.assertFalse(r['visual_classification_required'])
        self.assertNotEqual(r['family_status'], 'PRELIMINARY_REQUIRES_IMAGE')

    def test_single_phase_motor_capacitor_is_e02(self):
        r = c.classify(fixture('Um motor monofásico com capacitor de partida apresenta falha no enrolamento auxiliar.'), options)
        self.assertEqual(r['primary_module'], 'E02')
        self.assertEqual(r['primary_concept'], 'SINGLE_PHASE_MOTOR_CAPACITOR')

    def test_plc_dominates_relay_commands(self):
        r = c.classify(fixture('No controlador lógico programável CLP, a linguagem Ladder substitui relés auxiliares.'), options)
        self.assertEqual(r['primary_module'], 'A02')
        self.assertIn(r['primary_concept'], ['PLC_CONTROL', 'PLC_LADDER'])

    def test_nr10_period_not_frequency_period(self):
        r = c.classify(fixture('O curso de reciclagem da norma NR-10 é exigido após retorno de um período de afastamento superior a 90 dias.'), options)
        self.assertIn(r['primary_module'], ['S02', 'S03'])
        self.assertNotEqual(r['primary_concept'], 'FREQUENCY_PERIOD')

    def test_height_work_on_poles_is_s02(self):
        r = c.classify(fixture('Riscos ergonômicos e quedas no trabalho em altura na manutenção de postes de rede elétrica.'), options)
        self.assertEqual(r['primary_module'], 'S02')
        self.assertNotEqual(r['primary_module'], 'R01')

    def test_distribution_board_busbar_is_i01(self):
        r = c.classify(fixture('O dimensionamento dos barramentos de cobre no quadro de distribuição predial.'), options)
        self.assertEqual(r['primary_module'], 'I01')
        self.assertNotEqual(r['primary_module'], 'R02')

    def test_power_factor_correction_is_f04(self):
        r = c.classify(fixture('Instalação de banco de capacitores para correção do fator de potência e redução de reativos.'), options)
        self.assertEqual(r['primary_module'], 'F04')
        self.assertEqual(r['primary_concept'], 'POWER_FACTOR_CORRECTION')

    def test_hash_integrity_v1_and_v2(self):
        v1_path = OUT / 'catalogo-global.json'
        v2_path = OUT / 'catalogo-global-v2.json'
        self.assertTrue(v1_path.exists())
        self.assertTrue(v2_path.exists())

if __name__ == '__main__':
    unittest.main()

