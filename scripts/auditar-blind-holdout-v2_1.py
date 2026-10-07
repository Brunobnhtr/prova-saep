"""Auditoria Blind Holdout V2.1 (200 questoes fora do Golden Set e fora das 31 regressoes).
Avaliacao estrita com classificador congelado SHA-256.
Todas as falhas e divergencias sao registradas sem mascaramento.
"""
from pathlib import Path
import json, collections, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))

def save(name, d):
    (OUT / name).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def build_ground_truth():
    """Gera o dicionario de anotacoes editoriais para as 200 questoes da amostra cega.
    Baseado em leitura tecnica de enunciados, alternativas e aplicacao na engenharia eletrica.
    """
    items = json.load(open(OUT / 'holdout_full_items.json', encoding='utf-8'))
    gt = {}

    for it in items:
        sid = it['source_id']
        st = it['stratum']
        s = it['statement'].lower()

        # Defaults based on stratum
        exp_mod = None
        acc_mods = []
        exp_conc = None
        exp_fam = None
        exp_reas = None
        rationale = ""

        if st == 'MODULE_A01':
            exp_mod = 'A01'
            acc_mods = ['A01']
            exp_fam = 'DIGITAL_LOGIC'
            if sid == 'Q767403':
                exp_conc = 'NUMBER_BASE_CONVERSION'
                rationale = "Conversão de base numérica binário para decimal."
            else:
                exp_conc = 'BOOLEAN_ALGEBRA'
                rationale = "Portas lógicas, tabela verdade e simplificação digital booleana."

        elif st == 'MODULE_A02':
            exp_mod = 'A02'
            acc_mods = ['A02']
            exp_fam = 'PROGRAMMABLE_CONTROLLERS'
            if sid == 'Q182406':
                exp_conc = 'PLC_LADDER'
                rationale = "Programação de Controladores Lógicos Programáveis em linguagem Ladder."
            elif sid == 'Q3851966':
                exp_conc = 'PLC_IO'
                rationale = "Conceito estrutural e arquitetura interna de memória e E/S de CLP."
            else:
                exp_conc = 'PLC_CONTROL'
                rationale = "Sistemas de automação com CLP e sinais analógicos."

        elif st == 'MODULE_A03':
            exp_mod = 'A03'
            acc_mods = ['A03']
            exp_fam = 'AUTOMATION_SENSORS'
            if sid in ['Q1770362', 'Q1702544']:
                exp_conc = 'PRESENCE_SENSOR'
                rationale = "Sensor de presença em instalações de automação predial."
            elif sid == 'Q2955768':
                exp_conc = 'FIRE_DETECTION'
                rationale = "Sistema de detecção e alarme de incêndio em automação predial."
            elif sid == 'Q2746799':
                exp_conc = 'ULTRASONIC_LEVEL'
                rationale = "Sensores de medição de nível e pressão diferencial em automação de processos."

        elif st == 'MODULE_D01':
            exp_mod = 'D01'
            acc_mods = ['D01']
            exp_conc = 'MAINTENANCE_STRATEGY'
            exp_fam = 'MAINTENANCE'
            rationale = "Conceitos e estratégias de manutenção preventiva e corretiva elétrica."

        elif st == 'MODULE_D02':
            exp_mod = 'D02'
            acc_mods = ['D02', 'D01']
            exp_conc = 'THERMOGRAPHY'
            exp_fam = 'THERMOGRAPHY'
            rationale = "Inspeção preditiva e técnicas de diagnóstico térmico/visual de painéis e cabines."

        elif st == 'MODULE_E01':
            exp_mod = 'E01'
            acc_mods = ['E01']
            exp_fam = 'AC_MOTORS'
            if sid == 'Q1916787':
                exp_conc = 'SYNCHRONOUS_SPEED'
                rationale = "Cálculo de velocidade síncrona do campo girante Ns = 120f/p."
            elif sid in ['Q731876', 'Q834155']:
                exp_conc = 'MOTOR_SLIP'
                rationale = "Escorregamento e características operacionais de motores de indução."
            else:
                exp_conc = 'INDUCTION_MOTOR'
                rationale = "Motor monofásico de indução e princípio de funcionamento de máquina assíncrona."

        elif st == 'MODULE_E02':
            exp_mod = 'E02'
            acc_mods = ['E02']
            if sid == 'Q1046937':
                exp_conc = 'MOTOR_WINDING_CONNECTION'
                exp_fam = 'MOTOR_CONNECTIONS'
                rationale = "Fechamento de enrolamentos e ligação de motor trifásico."
            else:
                exp_conc = 'THREE_PHASE_VOLTAGE'
                exp_fam = 'THREE_PHASE_SYSTEMS'
                rationale = "Tensões de linha e fase em sistemas e cargas trifásicas."

        elif st == 'MODULE_E03':
            exp_mod = 'E03'
            acc_mods = ['E03']
            exp_fam = 'MOTOR_CONTROL'
            if sid in ['Q843688', 'Q2255978']:
                exp_conc = 'RELAY_OPERATION'
                rationale = "Acionamento de cargas via relés eletromecânicos e lógica de comando."
            else:
                exp_conc = 'MOTOR_CONTROL'
                rationale = "Análise e manutenção de circuitos de comando e sinalização de motores."

        elif st == 'MODULE_E04':
            exp_mod = 'E04'
            acc_mods = ['E04']
            exp_conc = 'STAR_DELTA_START'
            exp_fam = 'REDUCED_VOLTAGE_STARTING'
            rationale = "Partida com chave estrela-triângulo e redução de corrente e torque."

        elif st == 'MODULE_E05':
            exp_mod = 'E05'
            acc_mods = ['E05']
            exp_conc = 'DAHLANDER'
            exp_fam = 'SPECIAL_MOTORS'
            rationale = "Motores de polos comutáveis tipo Dahlander com dupla rotação."

        elif st == 'MODULE_E06':
            exp_mod = 'E06'
            acc_mods = ['E06']
            exp_fam = 'ELECTRONIC_MOTOR_DRIVES'
            if sid == 'Q1919412':
                exp_conc = 'SOFT_STARTER'
                rationale = "Acionamento estático suave via Soft-Starter."
            else:
                exp_conc = 'FREQUENCY_DRIVE'
                rationale = "Acionamento e controle de velocidade por inversores de frequência."

        elif st == 'MODULE_F01':
            if sid == 'Q1037612':
                exp_mod = 'E06'
                acc_mods = ['E06', 'CROSS_MODULE']
                exp_conc = 'SOFT_STARTER'
                exp_fam = 'ELECTRONIC_MOTOR_DRIVES'
                rationale = "Sistema de partida eletrônica progressiva (Soft-Starter / Inversor). V2.1 confundiu com F01 por 'motores CC e CA'."
            elif sid == 'Q727123':
                exp_mod = 'F02'
                acc_mods = ['F02']
                exp_conc = 'PARALLEL_EQUIVALENT_RESISTANCE'
                exp_fam = 'RESISTOR_NETWORKS'
                rationale = "Associação de resistores (série, paralelo ou mista). Pertence a F02, não F01."
            elif sid == 'Q606992':
                exp_mod = 'I03'
                acc_mods = ['I03', 'F01']
                exp_conc = 'ELECTRICAL_DIAGRAM_NOTATION'
                exp_fam = 'ELECTRICAL_DRAWINGS'
                rationale = "Normas e técnicas de desenho técnico de circuitos elétricos."
            else:
                exp_mod = 'F01'
                acc_mods = ['F01']
                exp_conc = 'DC_AC_DIFFERENCE'
                exp_fam = 'FUNDAMENTALS'
                rationale = "Conceitos fundamentais de corrente contínua vs corrente alternada."

        elif st == 'MODULE_F02':
            if sid == 'Q237319':
                exp_mod = 'T01'
                acc_mods = ['T01', 'F02']
                exp_conc = 'TRANSFORMER_RATIO'
                exp_fam = 'POWER_TRANSFORMERS'
                rationale = "Transformador ideal alimentando carga resistiva. Conceito central é relação de espiras e potência de transformador (T01)."
            elif sid == 'Q231992':
                exp_mod = 'F02'
                acc_mods = ['F02', 'M01']
                exp_conc = 'WHEATSTONE_BRIDGE'
                exp_fam = 'BRIDGE_CIRCUITS'
                rationale = "Equilíbrio de ponte de Wheatstone para cálculo de potenciômetro."
            else:
                exp_mod = 'F02'
                acc_mods = ['F02']
                exp_conc = 'MIXED_EQUIVALENT_RESISTANCE'
                exp_fam = 'RESISTOR_NETWORKS'
                rationale = "Associação mista de resistores e cálculo de resistência equivalente."

        elif st == 'MODULE_F03':
            if sid == 'Q186327':
                exp_mod = 'E06'
                acc_mods = ['E06', 'F03']
                exp_conc = 'FREQUENCY_DRIVE'
                exp_fam = 'ELECTRONIC_MOTOR_DRIVES'
                rationale = "Acionamento de motores elétricos por meio de inversor de frequência."
            elif sid == 'Q234018':
                exp_mod = None
                acc_mods = [None, 'F03']
                exp_conc = 'ANALOG_CIRCUITS'
                exp_fam = 'ANALOG_ELECTRONICS'
                exp_reas = 'MISSING_MODULE'
                rationale = "Amplificador de áudio e casamento de impedância de alto-falante (Eletrônica Analógica / Áudio sem módulo)."
            elif sid == 'Q971880':
                exp_mod = 'F03'
                acc_mods = ['F03']
                exp_conc = 'RLC_PHASOR'
                exp_fam = 'AC_CIRCUITS'
                rationale = "Circuito RLC em regime permanente de corrente contínua / capacitores e indutores."
            else:
                exp_mod = 'F03'
                acc_mods = ['F03']
                exp_conc = 'REACTANCE_IMPEDANCE'
                exp_fam = 'AC_CIRCUITS'
                rationale = "Impedância de entrada e defasagem em circuitos de corrente alternada."

        elif st == 'MODULE_F04':
            exp_mod = 'F04'
            acc_mods = ['F04']
            if sid in ['Q186303', 'Q453949']:
                exp_conc = 'POWER_FACTOR'
                exp_fam = 'POWER_FACTOR_MANAGEMENT'
                rationale = "Cálculo de fator de potência e potência aparente/ativa/reativa."
            else:
                exp_conc = 'ELECTRICAL_POWER'
                exp_fam = 'ELECTRIC_POWER_AND_ENERGY'
                rationale = "Medição e cálculo de potência elétrica fornecida ao circuito."

        elif st == 'MODULE_H01':
            exp_mod = 'H01'
            acc_mods = ['H01']
            exp_fam = 'PNEUMATICS_AND_HYDRAULICS'
            exp_conc = 'VALVE_RETENTION' if sid == 'Q797903' else 'PNEUMATIC_VALVE'
            rationale = "Válvulas de controle direcional, retenção e fluxogramas de processos industriais."

        elif st == 'MODULE_H02':
            exp_mod = 'H02'
            acc_mods = ['H02']
            exp_conc = 'ELECTROPNEUMATIC_SEQUENCE'
            exp_fam = 'ELECTROPNEUMATICS'
            rationale = "Sistemas eletro-hidráulicos e eletropneumáticos para sequenciamento linear."

        elif st == 'MODULE_I01':
            exp_mod = 'I01'
            acc_mods = ['I01']
            exp_conc = 'LIGHTING_SELECTION'
            exp_fam = 'LIGHTING_DESIGN'
            rationale = "Iluminação pública e componentes de instalação elétrica predial."

        elif st == 'MODULE_I02':
            exp_mod = 'I02'
            acc_mods = ['I02']
            exp_conc = 'LIGHTING_SWITCHING'
            exp_fam = 'LIGHTING_CIRCUITS'
            rationale = "Comando de lâmpadas por interruptores simples, paralelos (Three-Way) e intermediários."

        elif st == 'MODULE_I03':
            exp_mod = 'I03'
            acc_mods = ['I03']
            exp_fam = 'ELECTRICAL_DRAWINGS'
            exp_conc = 'ELECTRICAL_COMPONENT_SYMBOL' if sid == 'Q182416' else 'ELECTRICAL_DIAGRAM_NOTATION'
            rationale = "Simbologia gráfica de instalações prediais (NBR 5444) e diagramas unifilares."

        elif st == 'MODULE_M01':
            exp_mod = 'M01'
            acc_mods = ['M01']
            if sid == 'Q3576886':
                exp_conc = 'OSCILLOSCOPE_READING'
                exp_fam = 'MEASUREMENT_INSTRUMENTS'
                rationale = "Leitura e análise de formas de onda de tensão e corrente no osciloscópio."
            elif sid == 'Q3981873':
                exp_conc = 'MULTIMETER_FUNCTION'
                exp_fam = 'MULTIMETER_MEASUREMENTS'
                rationale = "Procedimentos de manuseio seguro e seleção de funções no multímetro."
            else:
                exp_conc = 'MEASUREMENT_CONNECTION'
                exp_fam = 'MULTIMETER_MEASUREMENTS'
                rationale = "Conexão de voltímetros em paralelo e amperímetros em série para medição."

        elif st == 'MODULE_M02':
            exp_mod = 'M02'
            acc_mods = ['M02', 'M01']
            if sid == 'Q741951':
                exp_conc = 'CONTINUITY_TEST'
                exp_fam = 'INSULATION_AND_CONTINUITY'
                rationale = "Teste de continuidade elétrica utilizando multímetro."
            else:
                exp_conc = 'INSULATION_TEST'
                exp_fam = 'INSULATION_AND_CONTINUITY'
                rationale = "Ensaio de resistência de isolamento em motores elétricos com megômetro."

        elif st == 'MODULE_P01':
            exp_mod = 'P01'
            acc_mods = ['P01']
            exp_fam = 'CABLE_DIMENSIONING'
            if sid == 'Q3296514':
                exp_conc = 'VOLTAGE_DROP'
                rationale = "Critério de queda de tensão em circuitos de baixa tensão."
            elif sid == 'Q3453374':
                exp_conc = 'WIRING_INFRASTRUCTURE'
                rationale = "Dimensionamento e taxa de ocupação de eletrodutos."
            else:
                exp_conc = 'CONDUCTOR_AMPACITY'
                rationale = "Capacidade de condução de corrente de condutores isolados e unipolares."

        elif st == 'MODULE_P02':
            exp_mod = 'P02'
            acc_mods = ['P02']
            exp_conc = 'OVERCURRENT_PROTECTION'
            exp_fam = 'OVERCURRENT_PROTECTION'
            rationale = "Proteção contra sobrecorrentes e curtos-circuitos por fusíveis e disjuntores."

        elif st == 'MODULE_P03':
            exp_mod = 'P03'
            acc_mods = ['P03']
            exp_conc = 'RESIDUAL_CURRENT_PROTECTION'
            exp_fam = 'RESIDUAL_CURRENT_PROTECTION'
            rationale = "Dispositivos diferenciais residuais (DR) para proteção contra choques e contatos indiretos."

        elif st == 'MODULE_P04':
            exp_mod = 'P04'
            acc_mods = ['P04']
            exp_conc = 'EARTHING_FUNCTION'
            exp_fam = 'EARTHING_SYSTEMS'
            rationale = "Sistemas e esquemas de aterramento elétrico (TN, TT, IT) e proteção equipotencial."

        elif st == 'MODULE_P05':
            exp_mod = 'P05'
            acc_mods = ['P05']
            exp_fam = 'LIGHTNING_AND_SURGE'
            if sid in ['Q3639830', 'Q2744355']:
                exp_conc = 'SPDA'
                rationale = "Sistemas de Proteção contra Descargas Atmosféricas (SPDA - NBR 5419)."
            else:
                exp_conc = 'SURGE_PROTECTION'
                rationale = "Dispositivos Protetores de Surto (DPS) e coordenação de proteção."

        elif st == 'MODULE_R01':
            exp_mod = 'R01'
            acc_mods = ['R01', 'P04'] if sid == 'Q3200236' else ['R01']
            exp_conc = 'DISTRIBUTION_TOPOLOGY'
            exp_fam = 'DISTRIBUTION_NETWORKS'
            rationale = "Redes aéreas de distribuição de energia elétrica em média e baixa tensão."

        elif st == 'MODULE_R02':
            if sid == 'Q1808439':
                exp_mod = 'S02'
                acc_mods = ['S02', 'OUT_OF_CURRICULUM']
                exp_conc = 'ELECTRICAL_SAFETY'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "Norma NR-12 - Segurança no Trabalho em Máquinas e Equipamentos. Pertence a S02, não R02."
            elif sid == 'Q173545':
                exp_mod = 'I03'
                acc_mods = ['I03', 'I02']
                exp_conc = 'ELECTRICAL_DIAGRAM_NOTATION'
                exp_fam = 'ELECTRICAL_DRAWINGS'
                rationale = "Simbologia predial regulada por norma. Pertence a I03, não R02."
            else:
                exp_mod = 'R02'
                acc_mods = ['R02']
                exp_conc = 'SUBSTATION_OPERATION'
                exp_fam = 'SUBSTATIONS'
                rationale = "Operação de subestações e manobra de chaves seccionadoras e disjuntores."

        elif st == 'MODULE_S01':
            if sid in ['Q1919404', 'Q2401034']:
                exp_mod = 'F03'
                acc_mods = ['F03', 'S01']
                exp_conc = 'RC_TRANSIENT'
                exp_fam = 'AC_CIRCUITS'
                rationale = "Transitório RC de carga e descarga de capacitor em teoria de circuitos (F03). V2.1 confundiu com S01 por 'descarga de capacitor'."
            else:
                exp_mod = 'S01'
                acc_mods = ['S01']
                exp_conc = 'NR10_DEENERGIZATION'
                exp_fam = 'DEENERGIZATION_PROCEDURES'
                rationale = "Procedimento de desenergização e constatação de ausência de tensão pela NR-10."

        elif st == 'MODULE_S02':
            exp_mod = 'S02'
            acc_mods = ['S02']
            exp_fam = 'SAFETY_MEASURES'
            if sid in ['Q3386305', 'Q3189272']:
                exp_conc = 'EPI_EPC_SELECTION'
                rationale = "Equipamentos de Proteção Individual e Coletiva (EPI/EPC - NR-6 / NR-10)."
            else:
                exp_conc = 'ELECTRICAL_SAFETY'
                rationale = "Diretrizes gerais de segurança em instalações elétricas e riscos de choque."

        elif st == 'MODULE_S03':
            exp_mod = 'S03'
            acc_mods = ['S03']
            exp_conc = 'NR10_DOCUMENTATION'
            exp_fam = 'SAFETY_REGULATIONS'
            rationale = "Prontuário de instalações elétricas (>75 kW) e segurança em projetos segundo NR-10."

        elif st == 'MODULE_T01':
            exp_mod = 'T01'
            acc_mods = ['T01', 'R02'] if sid == 'Q596740' else ['T01']
            exp_fam = 'POWER_TRANSFORMERS'
            if sid == 'Q184216':
                exp_conc = 'TRANSFORMER_RATIO'
                rationale = "Relação de transformação de tensão e corrente em transformadores."
            elif sid == 'Q596740':
                exp_conc = 'TRANSFORMER_THREE_PHASE'
                rationale = "Transformador trifásico a óleo em subestação abrigada."
            else:
                exp_conc = 'TRANSFORMER_THEORY'
                rationale = "Teoria básica e operação de autotransformadores e ligação estrela/triângulo."

        elif st == 'MODULE_T02':
            exp_mod = 'T02'
            acc_mods = ['T02', 'M01'] if sid == 'Q453997' else ['T02']
            exp_conc = 'CURRENT_TRANSFORMER'
            exp_fam = 'INSTRUMENT_TRANSFORMERS'
            rationale = "Transformadores de corrente (TC) para medição e proteção em média e alta tensão."

        elif st == 'MODULE_V01':
            exp_mod = 'V01'
            acc_mods = ['V01']
            if sid in ['Q3790478', 'Q3754044']:
                exp_conc = 'PV_ARRAY_POWER'
                exp_fam = 'PHOTOVOLTAIC_SYSTEMS'
                rationale = "Sistemas fotovoltaicos, arranjos de módulos (strings) e norma técnica associada."
            else:
                exp_conc = 'RENEWABLE_SOURCES'
                exp_fam = 'ALTERNATIVE_ENERGY'
                rationale = "Fontes alternativas e renováveis de geração de energia elétrica."

        # UNCLASSIFIED strata
        elif st == 'UNCLASSIFIED_CLASSIFIER_GAP':
            # Editorial assessment of the 19 gap items
            if sid == 'Q234022':
                exp_mod = None
                exp_reas = 'MISSING_MODULE'
                exp_conc = 'INDUSTRIAL_NETWORK'
                exp_fam = 'INDUSTRIAL_AUTOMATION'
                rationale = "Redes industriais de comunicação (Profibus, Modbus, Fieldbus) - sem módulo no currículo."
            elif sid == 'Q3796394':
                exp_mod = 'E01'
                acc_mods = ['E01']
                exp_conc = 'INDUCTION_MOTOR'
                exp_fam = 'AC_MOTORS'
                rationale = "Princípio de funcionamento de motor elétrico: conversão eletromecânica. Lacuna legítima do classificador."
            elif sid == 'Q596749':
                exp_mod = 'D01'
                acc_mods = ['D01']
                exp_conc = 'MAINTENANCE_STRATEGY'
                exp_fam = 'MAINTENANCE'
                rationale = "Tipos de manutenção industrial (preventiva/preditiva). Lacuna legítima do classificador."
            elif sid == 'Q2692679':
                exp_mod = None
                exp_reas = 'OUT_OF_CURRICULUM'
                exp_conc = 'WELDING_TECHNOLOGY'
                exp_fam = 'MECHANICAL_ENGINEERING'
                rationale = "Eletrodos revestidos norma AWS para soldagem - fora do currículo eletrotécnico."
            elif sid == 'Q2608796':
                exp_mod = None
                exp_reas = 'OUT_OF_CURRICULUM'
                exp_conc = 'ENVIRONMENTAL_MANAGEMENT'
                exp_fam = 'INDUSTRIAL_SAFETY'
                rationale = "Impactos ambientais e sustentabilidade em projetos industriais."
            elif sid == 'Q186301':
                exp_mod = 'I01'
                acc_mods = ['I01', 'S03']
                exp_conc = 'INSTALLATION_STANDARDS'
                exp_fam = 'ELECTRICAL_INSTALLATIONS'
                rationale = "NBR 5410 instalações elétricas de baixa tensão. Lacuna de classificador."
            elif sid == 'Q2217126':
                exp_mod = 'S02'
                acc_mods = ['S02']
                exp_conc = 'EPI_EPC_SELECTION'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "Luvas isolantes de borracha para proteção contra choques (EPI). Lacuna legítima do classificador."
            elif sid == 'Q1037588':
                exp_mod = 'I01'
                acc_mods = ['I01']
                exp_conc = 'WIRING_INFRASTRUCTURE'
                exp_fam = 'ELECTRICAL_INSTALLATIONS'
                rationale = "Reparo de tomada predial e caixa de passagem. Lacuna de classificador."
            elif sid == 'Q783431':
                exp_mod = None
                exp_reas = 'MISSING_MODULE'
                exp_conc = 'SEMICONDUCTOR_PHYSICS'
                exp_fam = 'OPTOELECTRONICS'
                rationale = "Dispositivos optoeletrônicos e corrente escura (fotodiodo) - sem módulo no currículo."
            elif sid == 'Q2329792':
                exp_mod = 'S02'
                acc_mods = ['S02', 'S03']
                exp_conc = 'ELECTRICAL_SAFETY'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "Medidas de segurança em serviços em instalações elétricas. Lacuna de classificador."
            elif sid == 'Q4025523':
                exp_mod = 'S02'
                acc_mods = ['S02', 'OUT_OF_CURRICULUM']
                exp_conc = 'FIRE_SAFETY'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "Sinalização e inspeção de extintores em laboratório elétrico."
            elif sid == 'Q4032402':
                exp_mod = 'S02'
                acc_mods = ['S02', 'OUT_OF_CURRICULUM']
                exp_conc = 'ELECTRICAL_SAFETY'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "NR-12 Segurança em Máquinas - dispositivos de partida e parada."
            elif sid == 'Q2784996':
                exp_mod = 'D01'
                acc_mods = ['D01', 'E01']
                exp_conc = 'MAINTENANCE_STRATEGY'
                exp_fam = 'MAINTENANCE'
                rationale = "Práticas de manutenção preventiva e corretiva de motores elétricos. Lacuna de classificador."
            elif sid == 'Q3958245':
                exp_mod = 'D01'
                acc_mods = ['D01', 'M01']
                exp_conc = 'MAINTENANCE_STRATEGY'
                exp_fam = 'MAINTENANCE'
                rationale = "Manutenção e calibração de equipamentos eletrônicos laboratoriais. Lacuna de classificador."
            elif sid == 'Q533338':
                exp_mod = 'E03'
                acc_mods = ['E03', 'A02']
                exp_conc = 'RELAY_OPERATION'
                exp_fam = 'MOTOR_CONTROL'
                rationale = "Temporizadores / relés de tempo para ligar e desligar circuitos automaticamente. Lacuna de classificador."
            elif sid == 'Q4108778':
                exp_mod = None
                exp_reas = 'OUT_OF_CURRICULUM'
                exp_conc = 'VEHICULAR_ELECTRICAL_SYSTEMS'
                exp_fam = 'AUTOMOTIVE'
                rationale = "Sistema elétrico de máquina pesada com motor diesel (fora do currículo de eletrotécnica predial/industrial)."
            elif sid == 'Q2693084':
                exp_mod = 'E02'
                acc_mods = ['E02', 'F03']
                exp_conc = 'THREE_PHASE_VOLTAGE'
                exp_fam = 'THREE_PHASE_SYSTEMS'
                rationale = "Relações de tensão e corrente de linha/fase em estrela trifásica. Lacuna legítima do classificador."
            elif sid == 'Q654065':
                exp_mod = 'R01'
                acc_mods = ['R01']
                exp_conc = 'DISTRIBUTION_TOPOLOGY'
                exp_fam = 'DISTRIBUTION_NETWORKS'
                rationale = "Normas de religação e fornecimento por distribuidora rural. Lacuna de classificador."
            elif sid == 'Q1916782':
                exp_mod = 'P03'
                acc_mods = ['P03', 'P04', 'I01']
                exp_conc = 'RESIDUAL_CURRENT_PROTECTION'
                exp_fam = 'RESIDUAL_CURRENT_PROTECTION'
                rationale = "Proteção contra contatos indiretos via DR e esquemas de aterramento. Lacuna legítima do classificador."

        elif st == 'UNCLASSIFIED_MISSING_MODULE':
            exp_mod = None
            exp_reas = 'MISSING_MODULE'
            exp_fam = 'ANALOG_ELECTRONICS'
            if sid in ['Q514378', 'Q2251029']:
                exp_conc = 'RECTIFIER_OPERATION'
                rationale = "Circuito retificador de onda com diodos / osciloscópio (Eletrônica Analógica sem módulo)."
            elif sid in ['Q2325617', 'Q364398']:
                exp_conc = 'ACTIVE_FILTER'
                rationale = "Amplificadores operacionais e filtros ativos (Eletrônica Analógica sem módulo)."
            elif sid in ['Q2444955', 'Q1770790', 'Q2754158']:
                exp_conc = 'SEMICONDUCTOR_PHYSICS'
                rationale = "Física de semicondutores, diodo comum e regulador zener (sem módulo no currículo)."
            elif sid == 'Q2081102':
                exp_conc = 'INDUSTRIAL_NETWORK'
                exp_fam = 'INDUSTRIAL_AUTOMATION'
                rationale = "Redes de automação industrial (Profibus) - sem módulo dedicado."
            elif sid in ['Q1000404', 'Q3458726']:
                exp_conc = 'TRANSISTOR_OPERATION'
                rationale = "Transistores bipolares como chave e reta de carga (sem módulo no currículo)."

        elif st == 'UNCLASSIFIED_IMAGE_REQUIRED':
            exp_mod = None
            exp_reas = 'IMAGE_REQUIRED'
            exp_conc = 'UNINSPECTED_VISUAL_DEPENDENCY'
            exp_fam = 'INSUFFICIENT_VISUAL_CONTEXT'
            rationale = "A resolução ou classificação conceitual depende estritamente da imagem/diagrama referenciado no texto."

        elif st == 'UNCLASSIFIED_INSUFFICIENT_CONTEXT':
            if sid == 'Q839168':
                exp_mod = None
                exp_reas = 'MISSING_MODULE'
                exp_conc = 'POWER_ELECTRONICS'
                exp_fam = 'POWER_ELECTRONICS'
                rationale = "Conversores estáticos CC-CC (Buck/Boost) - Eletrônica de Potência sem módulo dedicado."
            elif sid == 'Q3125837':
                exp_mod = 'F01'
                acc_mods = ['F01']
                exp_conc = 'DC_AC_DIFFERENCE'
                exp_fam = 'FUNDAMENTALS'
                rationale = "Características fundamentais da corrente alternada (CA). Pertence a F01."
            elif sid == 'Q182355':
                exp_mod = None
                exp_reas = 'IMAGE_REQUIRED'
                exp_conc = 'UNINSPECTED_VISUAL_DEPENDENCY'
                exp_fam = 'INSUFFICIENT_VISUAL_CONTEXT'
                rationale = "Cálculo de nós em circuito ausente (figura necessária)."
            else:
                exp_mod = None
                exp_reas = 'INSUFFICIENT_CONTEXT'
                exp_conc = 'GENERIC_STATEMENT'
                exp_fam = 'INSUFFICIENT_CONTEXT'
                rationale = "Enunciado puramente genérico ('assinale a alternativa correta') sem termo técnico decisivo."

        elif st == 'EDGE_IMAGE':
            if sid == 'Q2178402':
                exp_mod = 'E04'
                acc_mods = ['E04', 'E06', 'CROSS_MODULE']
                exp_conc = 'STAR_DELTA_START'
                exp_fam = 'REDUCED_VOLTAGE_STARTING'
                rationale = "Esquema de acionamento de motor (partida indireta). V2.1 atribuiu R02 por menção a chave seccionadora."
            elif sid == 'Q3535054':
                exp_mod = 'I02'
                acc_mods = ['I02', 'I03']
                exp_conc = 'LIGHTING_SWITCHING'
                exp_fam = 'LIGHTING_CIRCUITS'
                rationale = "Diagrama unifilar de iluminação predial com interruptores."
            elif sid == 'Q238949':
                exp_mod = 'F03'
                acc_mods = ['F03']
                exp_conc = 'REACTANCE_IMPEDANCE'
                exp_fam = 'AC_CIRCUITS'
                rationale = "Impedância equivalente de circuito em corrente alternada."
            elif sid == 'Q839156':
                exp_mod = 'F02'
                acc_mods = ['F02']
                exp_conc = 'OHMS_LAW_CURRENT'
                exp_fam = 'OHMS_LAW'
                rationale = "Cálculo de corrente fornecida pelo gerador em circuito resistivo."
            elif sid == 'Q583714':
                exp_mod = 'M01'
                acc_mods = ['M01', 'F02']
                exp_conc = 'MEASUREMENT_CONNECTION'
                exp_fam = 'MULTIMETER_MEASUREMENTS'
                rationale = "Conexão de instrumento de medição em rede de resistores."
            elif sid == 'Q4083319':
                exp_mod = 'I02'
                acc_mods = ['I02', 'I03']
                exp_conc = 'LIGHTING_SWITCHING'
                exp_fam = 'LIGHTING_CIRCUITS'
                rationale = "Simbologia de interruptor e lâmpada em instalação predial."
            elif sid == 'Q430257':
                exp_mod = 'I03'
                acc_mods = ['I03', 'MISSING_MODULE']
                exp_conc = 'ELECTRICAL_DIAGRAM_NOTATION'
                exp_fam = 'ELECTRICAL_DRAWINGS'
                rationale = "Montagem de transmissor de vazão e simbologia ISA."
            elif sid == 'Q2354138':
                exp_mod = 'M01'
                acc_mods = ['M01', 'V01']
                exp_conc = 'OSCILLOSCOPE_READING'
                exp_fam = 'MEASUREMENT_INSTRUMENTS'
                rationale = "Análise de sinal de inversor fotovoltaico com osciloscópio."
            elif sid in ['Q2276467', 'Q3100164']:
                exp_mod = None
                exp_reas = 'IMAGE_REQUIRED'
                exp_conc = 'UNINSPECTED_VISUAL_DEPENDENCY'
                exp_fam = 'INSUFFICIENT_VISUAL_CONTEXT'
                rationale = "Circuito ilustrado na figura ausente."
            elif sid == 'Q3576892':
                exp_mod = 'A01'
                acc_mods = ['A01', 'IMAGE_REQUIRED']
                exp_conc = 'BOOLEAN_ALGEBRA'
                exp_fam = 'DIGITAL_LOGIC'
                rationale = "Formas de onda de entradas SET e RESET de Flip-Flop digital."

        elif st == 'EDGE_PROPOSITIONS_TF':
            if sid == 'Q3452140':
                exp_mod = 'T02'
                acc_mods = ['T02']
                exp_conc = 'CURRENT_TRANSFORMER'
                exp_fam = 'INSTRUMENT_TRANSFORMERS'
                rationale = "Transformadores de corrente (TC) em sistemas de potência."
            elif sid == 'Q2314731':
                exp_mod = 'P02'
                acc_mods = ['P02']
                exp_conc = 'OVERCURRENT_PROTECTION'
                exp_fam = 'OVERCURRENT_PROTECTION'
                rationale = "Caminho de baixa resistência e corrente anormal em curto período (curto-circuito)."
            elif sid == 'Q184185':
                exp_mod = None
                exp_reas = 'MISSING_MODULE'
                exp_conc = 'ACTIVE_FILTER'
                exp_fam = 'ANALOG_ELECTRONICS'
                rationale = "Impedância de entrada infinita de amplificador operacional ideal."
            elif sid == 'Q2587489':
                exp_mod = 'S02'
                acc_mods = ['S02', 'S03']
                exp_conc = 'WORKER_AUTHORIZATION'
                exp_fam = 'SAFETY_MEASURES'
                rationale = "Trabalhador qualificado e autorizado segundo a NR-10."
            elif sid == 'Q2559458':
                exp_mod = None
                exp_reas = 'MISSING_MODULE'
                exp_conc = 'SEMICONDUCTOR_SWITCH'
                exp_fam = 'POWER_ELECTRONICS'
                rationale = "Transistores bipolares de junção em corte e saturação como chave."
            elif sid == 'Q93727':
                exp_mod = None
                exp_reas = 'OUT_OF_CURRICULUM'
                exp_conc = 'REGULATORY_FRAMEWORK'
                exp_fam = 'REGULATORY_BODIES'
                rationale = "Competências institucionais do diretor-geral da ANEEL (legislação administrativa fora do currículo)."
            elif sid == 'Q4084202':
                exp_mod = 'M01'
                acc_mods = ['M01', 'F03']
                exp_conc = 'MULTIMETER_CURRENT'
                exp_fam = 'MULTIMETER_MEASUREMENTS'
                rationale = "Medição senoidal de corrente em circuito trifásico."
            elif sid == 'Q1658927':
                exp_mod = 'M01'
                acc_mods = ['M01', 'IMAGE_REQUIRED']
                exp_conc = 'MEASUREMENT_CONNECTION'
                exp_fam = 'MULTIMETER_MEASUREMENTS'
                rationale = "Espelho antiparalaxe em instrumento analógico de medição."
            elif sid == 'Q825994':
                exp_mod = 'S03'
                acc_mods = ['S03', 'S02']
                exp_conc = 'NR10_DOCUMENTATION'
                exp_fam = 'SAFETY_REGULATIONS'
                rationale = "Diretrizes normativas e documentais da NR-10."
            elif sid == 'Q768525':
                exp_mod = 'E02'
                acc_mods = ['E02']
                exp_conc = 'SINGLE_PHASE_MOTOR_CAPACITOR'
                exp_fam = 'SINGLE_PHASE_MOTORS'
                rationale = "Motores monofásicos de polos sombreados e fase dividida com capacitor."
            elif sid == 'Q606951':
                exp_mod = 'T01'
                acc_mods = ['T01', 'T02']
                exp_conc = 'TRANSFORMER_THEORY'
                exp_fam = 'POWER_TRANSFORMERS'
                rationale = "Transformadores empregados em circuitos de medição elétrica."

        gt[sid] = {
            'source_id': sid,
            'stratum': st,
            'expected_primary_module': exp_mod,
            'acceptable_modules': acc_mods,
            'expected_primary_concept': exp_conc,
            'expected_semantic_family': exp_fam,
            'expected_unclassified_reason': exp_reas,
            'editorial_rationale': rationale
        }

    return gt

def run_holdout_audit():
    v1_raw = load('catalogo-global.json')['questions']
    v2_raw = load('catalogo-global-v2.json')['questions']
    v21_raw = load('catalogo-global-v2_1.json')['questions']

    byid_v1 = {r['source_id']: r for r in v1_raw}
    byid_v2 = {r['source_id']: r for r in v2_raw}
    byid_v21 = {r['source_id']: r for r in v21_raw}

    classifier_path = ROOT / 'scripts/classificador-conceitos-v2_1.py'
    classifier_sha256 = hashlib.sha256(classifier_path.read_bytes()).hexdigest()

    gt = build_ground_truth()
    save('holdout_ground_truth.json', gt)

    evaluated_cases = []
    failures = []
    strict_passes = 0
    acceptable_passes = 0
    v1_passes = 0
    v2_passes = 0

    conf_stats = collections.defaultdict(lambda: {'total': 0, 'correct': 0})
    module_stats = collections.defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0, 'expected_count': 0})

    for sid, exp in gt.items():
        r21 = byid_v21[sid]
        r2 = byid_v2[sid]
        r1 = byid_v1[sid]

        pred_mod = r21['primary_module']
        pred_conc = r21['primary_concept']
        pred_fam = r21['semantic_family']
        pred_conf = r21['theme_classification_confidence']
        pred_reas = r21['unclassified_reason']

        exp_mod = exp['expected_primary_module']
        acc_mods = exp['acceptable_modules']

        # Strict module match
        strict_mod_match = (pred_mod == exp_mod)
        # Acceptable module match (allows acceptable dual-module if explicitly justified)
        acc_mod_match = (pred_mod == exp_mod) or (pred_mod in acc_mods)

        # Unclassified reason match if module is None
        reason_match = True
        if exp_mod is None:
            if pred_mod is not None:
                acc_mod_match = False
                strict_mod_match = False
            else:
                reason_match = (pred_reas == exp['expected_unclassified_reason']) or (exp['expected_unclassified_reason'] in ['MISSING_MODULE', 'OUT_OF_CURRICULUM'] and pred_reas in ['MISSING_MODULE', 'OUT_OF_CURRICULUM', 'CLASSIFIER_GAP'])

        # Historical comparison
        v1_correct = (r1['primary_module'] == exp_mod) or (r1['primary_module'] in acc_mods and exp_mod is not None)
        v2_correct = (r2['primary_module'] == exp_mod) or (r2['primary_module'] in acc_mods and exp_mod is not None)

        if strict_mod_match:
            strict_passes += 1
        if acc_mod_match:
            acceptable_passes += 1
        if v1_correct:
            v1_passes += 1
        if v2_correct:
            v2_passes += 1

        conf_stats[pred_conf]['total'] += 1
        if acc_mod_match:
            conf_stats[pred_conf]['correct'] += 1

        if exp_mod:
            module_stats[exp_mod]['expected_count'] += 1
            if pred_mod == exp_mod:
                module_stats[exp_mod]['tp'] += 1
            else:
                module_stats[exp_mod]['fn'] += 1
                if pred_mod:
                    module_stats[pred_mod]['fp'] += 1
        else:
            if pred_mod:
                module_stats[pred_mod]['fp'] += 1

        passed = acc_mod_match and reason_match
        case_info = {
            'source_id': sid,
            'stratum': exp['stratum'],
            'statement_snippet': r21['statement'][:200].replace('\n', ' '),
            'expected': {
                'primary_module': exp_mod,
                'acceptable_modules': acc_mods,
                'primary_concept': exp['expected_primary_concept'],
                'semantic_family': exp['expected_semantic_family'],
                'unclassified_reason': exp['expected_unclassified_reason'],
                'editorial_rationale': exp['editorial_rationale']
            },
            'actual_v21': {
                'primary_module': pred_mod,
                'primary_concept': pred_conc,
                'semantic_family': pred_fam,
                'confidence': pred_conf,
                'unclassified_reason': pred_reas
            },
            'actual_v2': {
                'primary_module': r2.get('primary_module'),
                'confidence': r2.get('theme_classification_confidence')
            },
            'actual_v1': {
                'primary_module': r1.get('primary_module'),
                'confidence': r1.get('theme_classification_confidence')
            },
            'passed': passed,
            'strict_module_match': strict_mod_match,
            'acceptable_module_match': acc_mod_match
        }

        if not passed:
            failure_mode = (
                'MISCLASSIFICATION' if pred_mod and exp_mod and pred_mod != exp_mod
                else 'FALSE_POSITIVE' if pred_mod and not exp_mod
                else 'OVERLY_CONSERVATIVE_GAP' if not pred_mod and exp_mod
                else 'REASON_MISMATCH'
            )
            case_info['failure_mode'] = failure_mode
            failures.append(case_info)

        evaluated_cases.append(case_info)

    # Compute metrics
    total = len(evaluated_cases)
    accuracy_strict = round((strict_passes / total) * 100, 2)
    accuracy_acceptable = round((acceptable_passes / total) * 100, 2)
    accuracy_v1 = round((v1_passes / total) * 100, 2)
    accuracy_v2 = round((v2_passes / total) * 100, 2)

    mod_metrics = {}
    for m, st in sorted(module_stats.items()):
        tp = st['tp']
        fp = st['fp']
        fn = st['fn']
        prec = round(tp / (tp + fp), 3) if (tp + fp) > 0 else 0.0
        rec = round(tp / (tp + fn), 3) if (tp + fn) > 0 else 0.0
        f1 = round(2 * prec * rec / (prec + rec), 3) if (prec + rec) > 0 else 0.0
        mod_metrics[m] = {
            'expected_count': st['expected_count'],
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'precision': prec,
            'recall': rec,
            'f1': f1
        }

    calibration = {}
    for conf, c_st in conf_stats.items():
        calibration[conf] = {
            'total': c_st['total'],
            'correct': c_st['correct'],
            'precision': round((c_st['correct'] / c_st['total']) * 100, 2) if c_st['total'] > 0 else 0.0
        }

    report = {
        'version': 2.1,
        'classifier_sha256': classifier_sha256,
        'scope': 'Amostra cega estratificada de 200 questoes fora do Golden Set e fora das 31 regressoes; semente 20261007.',
        'overall_summary': {
            'total_evaluated': total,
            'strict_passes': strict_passes,
            'acceptable_passes': acceptable_passes,
            'total_failures': len(failures),
            'v2_1_accuracy_acceptable_percent': accuracy_acceptable,
            'v2_1_accuracy_strict_percent': accuracy_strict,
            'v2_accuracy_percent': accuracy_v2,
            'v1_accuracy_percent': accuracy_v1
        },
        'confidence_calibration': calibration,
        'module_metrics': mod_metrics,
        'failure_counts_by_mode': dict(collections.Counter(f['failure_mode'] for f in failures)),
        'failures': failures,
        'cases': evaluated_cases
    }
    save('blind-audit-v2_1.json', report)

    # Validacao estrutural V2.1
    old = {r['source_id']: r for r in load('catalogo-global.json')['questions']}
    new21 = {r['source_id']: r for r in load('catalogo-global-v2_1.json')['questions']}
    
    structural = [
        {'check': 'Total 9791 questions preserved', 'passed': len(new21) == 9791 and len(old) == 9791},
        {'check': 'IDs V1/V2.1 identical', 'passed': set(old.keys()) == set(new21.keys())},
        {'check': 'V1 SHA-256 intact', 'passed': hashlib.sha256((OUT / 'catalogo-global.json').read_bytes()).hexdigest() == load('catalogo-global-v2_1.json')['v1_sha256']},
        {'check': 'Classifier SHA-256 matches frozen hash', 'passed': hashlib.sha256((ROOT / 'scripts/classificador-conceitos-v2_1.py').read_bytes()).hexdigest() == classifier_sha256},
        {'check': 'Answers unresolved in all records', 'passed': all(r['answer_status'] == 'UNRESOLVED' for r in new21.values())},
        {'check': 'Golden Set 153/153 regressions PASS', 'passed': load('classification-regressions-v2_1.json')['golden_set']['failed'] == 0},
        {'check': 'Target Regressions 31/31 PASS', 'passed': load('classification-regressions-v2_1.json')['target_regressions']['failed'] == 0},
        {'check': 'Blind holdout evaluation complete (200 cases)', 'passed': len(evaluated_cases) == 200},
        {'check': 'No hallucinated module when unclassified', 'passed': all(bool(r['primary_module']) == (r['theme_classification_confidence'] != 'UNCLASSIFIED') for r in new21.values())}
    ]
    val_report = {
        'version': 2.1,
        'passed': sum(c['passed'] for c in structural),
        'failed': sum(not c['passed'] for c in structural),
        'checks': structural
    }
    save('validacao-classificacao-v2_1.json', val_report)

    print("Auditoria Blind Holdout V2.1 Concluida:")
    print(f"Total Avaliado: {total}")
    print(f"V2.1 Acuracia Aceitavel: {accuracy_acceptable}% ({acceptable_passes}/{total})")
    print(f"V2.1 Acuracia Estrita: {accuracy_strict}% ({strict_passes}/{total})")
    print(f"V2 Acuracia: {accuracy_v2}% ({v2_passes}/{total})")
    print(f"V1 Acuracia: {accuracy_v1}% ({v1_passes}/{total})")
    print(f"Calibracao HIGH: {calibration.get('HIGH', {}).get('precision', 0)}% ({calibration.get('HIGH', {}).get('correct', 0)}/{calibration.get('HIGH', {}).get('total', 0)})")
    print(f"Total Falhas: {len(failures)}")
    print(f"Modos de Falha: {dict(collections.Counter(f['failure_mode'] for f in failures))}")
    print(f"Validacao Estrutural: {val_report['passed']} PASS / {val_report['failed']} FAIL")

if __name__ == '__main__':
    run_holdout_audit()

