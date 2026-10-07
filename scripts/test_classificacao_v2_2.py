import unittest, json, importlib.util, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

spec = importlib.util.spec_from_file_location('c22', ROOT / 'scripts/classificador-conceitos-v2_2.py')
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

class ClassificationV22Tests(unittest.TestCase):
    # Integrity and Hash Invariants
    def test_file_size_and_hashes_not_empty(self):
        EMPTY_SHA = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        for fname in ['catalogo-global.json', 'catalogo-global-v2.json', 'catalogo-global-v2_1.json']:
            p = OUT / fname
            self.assertTrue(p.exists(), f"File {fname} must exist")
            b = p.read_bytes()
            self.assertGreater(len(b), 1000, f"File {fname} must have real content")
            h = hashlib.sha256(b).hexdigest()
            self.assertNotEqual(h, EMPTY_SHA, f"File {fname} cannot have empty hash")

    # Domain Tests for the 24 fixed areas
    def test_soft_starter_beats_generic_cc_ca(self):
        r = c.classify(fixture('Sistema de partida de motores CC e CA que utiliza a tecnologia de chaves eletrônicas, assegura o controle progressivo de aceleração e desaceleração.'), options)
        self.assertEqual(r['primary_module'], 'E06')
        self.assertEqual(r['primary_concept'], 'SOFT_STARTER')

    def test_resistor_network_beats_cc_ca_subtheme(self):
        r = c.classify(fixture('Em um circuito é possível organizar conjuntos de resistores interligados, chamada associação de resistores.', subjects=['Circuitos de Corrente Contínua e de Corrente Alternada']), options)
        self.assertEqual(r['primary_module'], 'F02')
        self.assertIn(r['primary_concept'], ['RESISTOR_ASSOCIATION', 'MIXED_EQUIVALENT_RESISTANCE'])

    def test_transformer_with_load_beats_auxiliary_ohm_formula(self):
        r = c.classify(fixture('Um transformador ideal alimenta uma carga resistiva, conforme indicado na figura. O valor rms da tensão da fonte é 200 V e a potência é 400 W.'), options)
        self.assertEqual(r['primary_module'], 'T01')
        self.assertEqual(r['primary_concept'], 'TRANSFORMER_REFLECTED_IMPEDANCE')

    def test_machine_safety_nr12_with_switch_not_substation(self):
        r = c.classify(fixture('A norma de segurança no trabalho em máquinas e equipamentos (NR-12) define medidas de proteção para chaves seccionadoras e dispositivos de parada.', subjects=['Chaves Seccionadoras']), options)
        self.assertEqual(r['primary_module'], 'S02')
        self.assertNotEqual(r['primary_module'], 'R02')

    def test_motor_starting_schematic_not_substation(self):
        r = c.classify(fixture('Trata-se de um acionamento de motor elétrico por chave de partida.', subjects=['Chaves Seccionadoras']), options)
        self.assertNotEqual(r['primary_module'], 'R02')

    def test_audio_impedance_is_missing_module_not_f03(self):
        r = c.classify(fixture('Um amplificador de potência de áudio alimenta uma caixa acústica com um alto-falante de impedância 8 ohms.'), options)
        self.assertIsNone(r['primary_module'])
        self.assertEqual(r['unclassified_reason'], 'MISSING_MODULE')
        self.assertEqual(r['primary_concept'], 'AUDIO_ELECTRONICS')

    def test_nbr5410_installation_standard_is_i01(self):
        r = c.classify(fixture('A NBR 5410 regulamenta as instalações elétricas de baixa tensão no tocante aos requisitos gerais de instalação predial.'), options)
        self.assertEqual(r['primary_module'], 'I01')

    def test_insulating_gloves_is_safety(self):
        r = c.classify(fixture('Garantem a segurança das mãos contra choques e queimaduras. Podem ser luvas isolantes de borracha.'), options)
        self.assertEqual(r['primary_module'], 'S02')

    def test_emergency_stop_nr12_is_safety(self):
        r = c.classify(fixture('A NR-12 trata dos dispositivos de partida, acionamento e parada de emergência em máquinas.'), options)
        self.assertEqual(r['primary_module'], 'S02')

    def test_relay_timer_is_e03(self):
        r = c.classify(fixture('O dispositivo que possibilita programar, ligar e desligar automaticamente circuitos elétricos em tempos predeterminados é o relé temporizador.'), options)
        self.assertEqual(r['primary_module'], 'E03')
        self.assertEqual(r['primary_concept'], 'TIMER_RELAY')

    def test_short_circuit_concept_is_p02(self):
        r = c.classify(fixture('Se houver um caminho de baixa resistência por onde flui corrente elétrica anormalmente elevada, isso resultará em curto-circuito.'), options)
        self.assertEqual(r['primary_module'], 'P02')

    def test_industrial_networks_is_missing_module(self):
        r = c.classify(fixture('As redes industriais de comunicação como Profibus e Fieldbus transmitem dados entre controladores e dispositivos de campo.'), options)
        self.assertIsNone(r['primary_module'])
        self.assertEqual(r['unclassified_reason'], 'MISSING_MODULE')
        self.assertEqual(r['primary_concept'], 'INDUSTRIAL_NETWORK')

    def test_dc_dc_converters_is_missing_module(self):
        r = c.classify(fixture('Com relação aos conversores estáticos CC-CC do tipo Buck e Boost, analise as afirmativas.'), options)
        self.assertIsNone(r['primary_module'])
        self.assertEqual(r['unclassified_reason'], 'MISSING_MODULE')
        self.assertEqual(r['primary_concept'], 'POWER_ELECTRONICS_DC_DC')

    def test_rc_transient_is_f03(self):
        r = c.classify(fixture('O circuito apresenta uma fonte conectada a um resistor e capacitor para carga e descarga de um capacitor com constante de tempo.'), options)
        self.assertEqual(r['primary_module'], 'F03')
        self.assertEqual(r['primary_concept'], 'RC_TRANSIENT')

    def test_three_phase_star_relations_is_e02(self):
        r = c.classify(fixture('Sobre um circuito elétrico trifásico conectado em estrela, determine a relação entre tensão de linha e tensão de fase.'), options)
        self.assertEqual(r['primary_module'], 'E02')

    def test_motor_energy_conversion_is_e01(self):
        r = c.classify(fixture('O motor elétrico converte energia elétrica em energia mecânica por meio do campo magnético girante.'), options)
        self.assertEqual(r['primary_module'], 'E01')

    def test_distribution_regulation_is_r01(self):
        r = c.classify(fixture('A distribuidora de energia elétrica deve restabelecer o fornecimento para a unidade consumidora rural dentro dos prazos regulatórios.'), options)
        self.assertEqual(r['primary_module'], 'R01')

    def test_indirect_contact_dr_is_p03(self):
        r = c.classify(fixture('Para proteger os usuários contra contatos indiretos, utiliza-se dispositivo diferencial-residual (DR) em esquemas de aterramento.'), options)
        self.assertEqual(r['primary_module'], 'P03')

    def test_ac_waveform_characteristics_is_f01(self):
        r = c.classify(fixture('A corrente alternada (CA) é caracterizada por inversão periódica do sentido e forma de onda senoidal.'), options)
        self.assertEqual(r['primary_module'], 'F01')

if __name__ == '__main__':
    unittest.main()
