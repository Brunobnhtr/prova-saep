"""Gerador e validador de anotacoes editoriais para o Blind Holdout V2.2 (300 questoes).
Anotacao tecnica independente baseada em engenharia eletrotécnica e matriz curricular do SAEP/CST.
Registra ground truth editorial antes da auditoria comparativa.
"""
from pathlib import Path
import json, re, hashlib, unicodedata

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

def norm(text):
    if not text:
        return ''
    t = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('ASCII').lower()
    return re.sub(r'\s+', ' ', t).strip()

def has(pattern, text):
    return bool(re.search(pattern, text, re.IGNORECASE))

def annotate_question(q):
    sid = q['source_id']
    s = norm(q.get('statement', ''))
    alts = ' '.join(norm(a) for a in q.get('alternatives', []))
    combo = f"{s} {alts}"
    theme = norm(q.get('original_source_theme', ''))
    has_img = bool(q.get('has_image'))

    # Defaults
    mod = None
    acceptable = []
    concept = 'UNSPECIFIED'
    family = 'UNSPECIFIED'
    reason = None
    notes = ''

    # 1. OUT OF CURRICULUM
    if has(r'soldagem|eletrodos? revestidos?|junta soldada|bisel|norma aws', combo):
        return None, [], 'WELDING_TECHNOLOGY', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Tecnologia de soldagem fora da eletrotecnica'
    if has(r'deformar permanentemente|plasticidade|ensaio de tracao|limite de escoamento', combo):
        return None, [], 'MATERIAL_PLASTICITY', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Ciencia dos materiais mecanica fora da matriz'
    if has(r'motor a diesel|veiculo automotor|maquina pesada|motorista', combo):
        return None, [], 'AUTOMOTIVE_ENGINE', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Mecanica diesel/automotiva'
    if has(r'turbina hidraulica|geracao hidreletrica|kaplan|francis|pelton', combo):
        return None, [], 'HYDROELECTRIC_GENERATION', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Geracao hidreletrica/turbomaquinas'
    if has(r'aneel.{0,80}(diretoria|pautas|assessoria)|erd\b|musderd', combo):
        return None, [], 'REGULATORY_FRAMEWORK', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Regulacao institucional ANEEL/concessionarias'
    if has(r'eletron.{0,80}campo magnetico|forca de lorentz', combo):
        return None, [], 'LORENTZ_FORCE', 'OUTSIDE_CURRICULUM', 'OUT_OF_CURRICULUM', 'Fisica teorica de particulas'

    # 2. MISSING MODULES (Eletronica Analogica / Redes / Conversores CC-CC)
    if has(r'amplificador operacional|ampop|circuito subtrator|ganho.{0,20}db|amplificador inversor', combo):
        return None, [], 'OPERATIONAL_AMPLIFIER', 'ANALOG_ELECTRONICS', 'MISSING_MODULE', 'Eletronica analogica (AmpOp) ausente na matriz de 35 modulos'
    if has(r'transistor|bjt\b|mosfet|jfet|polarizacao.{0,30}coletor|hfe\b|emissor comum', combo) and not has(r'soft.starter|inversor de frequencia', combo):
        return None, [], 'TRANSISTOR_OPERATION', 'ANALOG_ELECTRONICS', 'MISSING_MODULE', 'Semicondutores discretos (transistor) fora dos 35 modulos'
    if has(r'diodo|retificador|retificacao|ponte retificadora|ceifador|grampeador', combo) and not has(r'fonte retificada.{0,40}descarreg', combo):
        return None, [], 'RECTIFIER_OPERATION', 'ANALOG_ELECTRONICS', 'MISSING_MODULE', 'Eletronica basica / circuitos retificadores'
    if has(r'redes? industriais?|profibus|modbus|fieldbus|devicenet|ethernet industrial', combo):
        return None, ['A02'], 'INDUSTRIAL_NETWORK', 'COMMUNICATION_NETWORKS', 'MISSING_MODULE', 'Redes industriais de comunicacao de dados'
    if has(r'conversores?.{0,20}cc.cc|conversor.{0,20}(buck|boost)|buck.boost|chopper', combo):
        return None, [], 'POWER_ELECTRONICS_DC_DC', 'POWER_ELECTRONICS', 'MISSING_MODULE', 'Eletronica de potencia de chaveamento CC-CC'
    if has(r'amplificador de audio|caixa acustica|alto.falante', combo):
        return None, [], 'AUDIO_ELECTRONICS', 'ANALOG_ELECTRONICS', 'MISSING_MODULE', 'Sistemas de audio e acustica'

    # 3. SAFETY / NR-10 (S01, S02, S03)
    if has(r'desenergiz|ausencia de tensao|seccionamento.{0,30}impedimento|reenergizacao|bloqueio e etiquetagem|loto\b', combo):
        if has(r'reenergiz', combo):
            return 'S01', ['S01'], 'NR10_REENERGIZATION', 'DEENERGIZATION_PROCEDURES', None, 'Procedimento de reenergizacao da NR-10'
        if has(r'descarreg.{0,30}capacitor|energia armazenada', combo):
            return 'S01', ['S01', 'F03'], 'STORED_ENERGY_DISCHARGE', 'DEENERGIZATION_PROCEDURES', None, 'Descarga de energia residual/armazenada NR-10'
        return 'S01', ['S01', 'S02'], 'NR10_DEENERGIZATION', 'DEENERGIZATION_PROCEDURES', None, 'Procedimentos de desenergizacao conforme NR-10'

    if has(r'nr.{0,2}10|choque eletrico|arco eletrico|perigo de choque|trabalhador qualificado|trabalhador habilitado|trabalhador autorizado|operacoes elementares|reciclagem.{0,30}nr', combo):
        if has(r'prontuario|documentacao.{0,30}nr|esquemas unifilares.{0,40}prontuario|reciclagem da norma', combo):
            return 'S03', ['S03', 'S02'], 'NR10_DOCUMENTATION', 'SAFETY_REGULATIONS', None, 'Normas e documentacao de seguranca NR-10'
        if has(r'extra.baixa tensao|baixa tensao|faixas de tensao|classificacao.{0,20}tensao', combo):
            return 'S03', ['S03', 'S02'], 'VOLTAGE_CLASSIFICATION', 'SAFETY_REGULATIONS', None, 'Classificacao de faixas de tensao de seguranca'
        if has(r'luvas? isolantes?|mangas de borracha|bota de seguranca|vara de manobra|epi\b|epc\b|equipamento de protecao', combo):
            return 'S02', ['S02', 'S01'], 'EPI_EPC_SELECTION', 'SAFETY_MEASURES', None, 'EPI e EPC em trabalhos eletricos'
        return 'S02', ['S02', 'S03'], 'ELECTRICAL_SAFETY', 'SAFETY_MEASURES', None, 'Seguranca e prevencao de acidentes em eletricidade'

    if has(r'nr.{0,2}12|protecao de maquinas|parada de emergencia|dispositivo de intertravamento', combo):
        return 'S02', ['S02', 'E03'], 'MACHINE_SAFETY_NR12', 'SAFETY_MEASURES', None, 'Seguranca em maquinas e equipamentos NR-12'

    if has(r'nr.{0,2}35|trabalho em altura|cinto de seguranca.{0,20}altura|riscos ergonomicos.{0,40}postes', combo):
        return 'S02', ['S02', 'R01'], 'WORK_AT_HEIGHT', 'SAFETY_MEASURES', None, 'Trabalho em altura e ergonomia NR-35/NR-17'

    if has(r'extintor|combate a incendio|fogo.{0,20}classe c|classes de incendio', combo):
        return 'S02', ['S02'], 'LAB_FIRE_SAFETY', 'SAFETY_MEASURES', None, 'Prevencao e combate a principio de incendio em instalacoes'

    # 4. MEASUREMENTS & INSTRUMENTATION (M01, M02, T02)
    if has(r'resistencia de isolamento|megohmetro|megometro|ensaio de isolamento', combo):
        return 'M02', ['M02', 'D01'], 'INSULATION_TEST', 'INSULATION_AND_CONTINUITY', None, 'Medicao de resistencia de isolamento'
    if has(r'continuidade|teste de continuidade', combo):
        return 'M02', ['M02', 'M01'], 'CONTINUITY_TEST', 'INSULATION_AND_CONTINUITY', None, 'Verificacao de continuidade de condutores'
    if has(r'transformador de corrente|\btc\b.{0,30}(medicao|corrente|secundario)|transformador de potencial|\btp\b.{0,30}(medicao|secundario)', combo):
        return 'T02', ['T02', 'M01'], 'CURRENT_TRANSFORMER', 'INSTRUMENT_TRANSFORMERS', None, 'Transformadores para instrumentos de medicao'
    if has(r'multimetro|voltimetro|amperimetro|ohmimetro|alicate amperimetro|escala do instrumento|medir (tensao|corrente|resistencia)|ponteiras de prova', combo):
        if has(r'conectar em serie|conectar em paralelo|terminais|ligacao do instrumento', combo):
            return 'M01', ['M01'], 'MEASUREMENT_CONNECTION', 'MULTIMETER_MEASUREMENTS', None, 'Procedimento de ligacao de instrumentos de medicao'
        return 'M01', ['M01', 'F02'], 'MULTIMETER_FUNCTION', 'MULTIMETER_MEASUREMENTS', None, 'Uso e escalas de instrumentos de medicao eletrica'
    if has(r'osciloscopio|forma de onda.{0,30}tela|base de tempo', combo):
        return 'M01', ['M01', 'F03'], 'OSCILLOSCOPE_READING', 'MEASUREMENT_INSTRUMENTS', None, 'Medicao de grandezas com osciloscopio'

    # 5. MOTORS AND GENERATORS (E01, E02)
    if has(r'velocidade sincrona|escorregamento|frequencia.{0,20}polos|ns\s*=\s*120|rpm\b.{0,30}polos', combo):
        return 'E01', ['E01', 'E02'], 'SYNCHRONOUS_SPEED', 'ELECTRIC_MACHINES', None, 'Velocidade sincrona e escorregamento de motores'
    if has(r'motor monofasico.{0,60}capacitor|capacitor de partida.{0,40}motor|enrolamento auxiliar.{0,40}capacitor', combo):
        return 'E02', ['E02', 'F04'], 'SINGLE_PHASE_MOTOR_CAPACITOR', 'AC_MOTORS', None, 'Motor monofasico de inducao com capacitor de partida'
    if has(r'motor trifasico|motor de inducao|fechamento.{0,30}(estrela|triangulo)|220/380|terminais.{0,20}(1,2,3,4,5,6|u1,v1,w1)', combo):
        return 'E02', ['E02', 'E01'], 'INDUCTION_MOTOR', 'AC_MOTORS', None, 'Motores trifasicos de inducao e fechamento de bornes'
    if has(r'rendimento.{0,30}motor|perdas.{0,30}(ferro|cobre|mecanicas)|potencia mecanica.{0,30}eletrica', combo):
        return 'E01', ['E01'], 'MOTOR_EFFICIENCY', 'ELECTRIC_MACHINES', None, 'Rendimento e balanco de potencias em maquinas eletricas'
    if has(r'motor cc|gerador cc|maquina de corrente continua|escovas|comutador', combo):
        return 'E01', ['E01'], 'DC_MACHINES', 'ELECTRIC_MACHINES', None, 'Principios e caracteristicas de maquinas de corrente continua'
    if has(r'conversao.{0,30}energia|campo magnetico girante|lei de faraday.{0,40}maquinas', combo):
        return 'E01', ['E01'], 'MOTOR_ENERGY_CONVERSION', 'ELECTRIC_MACHINES', None, 'Conversao eletromecanica de energia'

    # 6. MOTOR COMMANDS & DRIVES (E03, E04, E05, E06)
    if has(r'soft.starter|arranque suave|tiristores.{0,30}partida de motor', combo):
        return 'E06', ['E06', 'E03'], 'SOFT_STARTER', 'ELECTRONIC_STARTING', None, 'Partida e parada de motores com chave soft-starter'
    if has(r'inversor de frequencia|v/f constante|controle pwm.{0,30}motor|variacao de velocidade.{0,30}motor', combo):
        return 'E05', ['E05', 'E06'], 'INVERTER_SPEED_CONTROL', 'FREQUENCY_INVERTERS', None, 'Variacao de frequencia e acionamento de motores'
    if has(r'chave estrela.triangulo|partida estrela.triangulo|corrente de partida.{0,30}(reduzida|1/3)', combo):
        return 'E04', ['E04', 'E03'], 'STAR_DELTA_START', 'MOTOR_STARTING_METHODS', None, 'Metodo de partida indireta estrela-triangulo'
    if has(r'chave compensadora|autotransformador de partida|taps de partida', combo):
        return 'E04', ['E04', 'E03'], 'COMPENSATING_KEY_START', 'MOTOR_STARTING_METHODS', None, 'Partida de motor por chave compensadora'
    if has(r'contator|circuito de comando|circuito de forca|contato de selo|intertravamento|rele temporizador|rele termico|botoeira', combo):
        if has(r'intertravamento|reversao', combo):
            return 'E03', ['E03', 'E02'], 'MOTOR_REVERSING', 'MOTOR_CONTROL', None, 'Circuito de comando para reversao de motor'
        if has(r'rele termico|protecao termica.{0,30}motor|sobrecarga.{0,30}motor', combo):
            return 'E03', ['E03', 'P02'], 'MOTOR_PROTECTION', 'MOTOR_CONTROL', None, 'Protecao de motores contra sobrecarga por rele termico'
        if has(r'temporizador|rele de tempo', combo):
            return 'E03', ['E03', 'A02'], 'TIMER_RELAY', 'MOTOR_CONTROL', None, 'Temporizacao em comandos eletricos'
        return 'E03', ['E03'], 'CONTACTOR_CONTROL', 'MOTOR_CONTROL', None, 'Circuitos de comando e forca com contatores'

    # 7. AUTOMATION & DIGITAL (A01, A02, A03)
    if has(r'controlador logico programavel|clp\b|\bplc\b|linguagem ladder|diagrama ladder|texto estruturado|instrucao de clp', combo):
        if has(r'ladder', combo):
            return 'A02', ['A02', 'A01'], 'PLC_LADDER', 'PROGRAMMABLE_CONTROLLERS', None, 'Programacao de CLP em linguagem Ladder'
        return 'A02', ['A02'], 'PLC_CONTROL', 'PROGRAMMABLE_CONTROLLERS', None, 'Controladores logicos programaveis na automacao'
    if has(r'porta logica|tabela verdade|algebra booleana|expressao booleana|mapa de karnaugh|simplificacao logica|porta (and|or|not|nand|nor|xor)', combo):
        return 'A01', ['A01'], 'BOOLEAN_ALGEBRA', 'DIGITAL_LOGIC', None, 'Logica digital e algebra de Boole'
    if has(r'binario|hexadecimal|octal|conversao de base|sistema de numeracao', combo):
        return 'A01', ['A01'], 'NUMBER_BASE_CONVERSION', 'DIGITAL_LOGIC', None, 'Sistemas de numeracao e codificacao digital'
    if has(r'sensor indutivo|sensor capacitivo|sensor optico|sensor fotoeletrico|celula fotoeletrica|sensor de proximidade|sensor de temperatura|sensor de pressao', combo):
        return 'A03', ['A03'], 'AUTOMATION_SENSOR', 'AUTOMATION_SENSORS', None, 'Sensores industriais para deteccao e controle'

    # 8. TRANSFORMERS (T01)
    if has(r'transformador|autotransformador|relacao de transformacao|tensao primaria.{0,30}secundaria|corrente primaria.{0,30}secundaria|espiras primarias', combo):
        if has(r'transformador trifasico|ligacao (delta|estrela).{0,30}transformador', combo):
            return 'T01', ['T01', 'E02'], 'TRANSFORMER_THREE_PHASE', 'POWER_TRANSFORMERS', None, 'Transformadores trifasicos de potencia'
        return 'T01', ['T01', 'F02'], 'TRANSFORMER_RATIO', 'POWER_TRANSFORMERS', None, 'Relacao de transformacao e funcionamento de transformadores'

    # 9. FLUID POWER / PNEUMATICS (H01, H02)
    if has(r'pneumat|eletropneumat|cilindro pneumatico|valvula direcional|ar comprimido|hidraulic|atuador pneumatico', combo):
        if has(r'sequencia.{0,30}cilindro|eletropneumat', combo):
            return 'H02', ['H02', 'H01'], 'ELECTROPNEUMATIC_SEQUENCE', 'ELECTROPNEUMATICS', None, 'Circuitos e sequencias eletropneumaticas'
        return 'H01', ['H01'], 'PNEUMATIC_VALVE', 'FLUID_POWER', None, 'Componentes pneumaticos e hidraulicos industriais'

    # 10. INSTALLATIONS & DRAWINGS (I01, I02, I03, P01)
    if has(r'diagrama unifilar|diagrama multifilar|simbologia predial|planta baixa.{0,30}eletric|software cad|projeto eletrico predial', combo):
        return 'I03', ['I03', 'I01'], 'ELECTRICAL_DIAGRAM_NOTATION', 'ELECTRICAL_DRAWINGS', None, 'Simbologia e diagramas de projetos eletricos'
    if has(r'interruptor (simples|paralelo|intermediario)|four.way|three.way|comando de lampadas', combo):
        return 'I02', ['I02', 'I01'], 'LIGHTING_SWITCHING', 'LIGHTING_CONTROLS', None, 'Comandos e ligacoes de iluminacao residencial'
    if has(r'previsao de carga|potencia minima.{0,30}tomada|tomadas de uso (geral|especifico)|tug\b|tue\b|dimensionamento predial|quadro de distribuicao predial|caixa de passagem|nbr 5410', combo):
        return 'I01', ['I01', 'P01'], 'LOAD_ALLOCATION', 'BUILDING_INSTALLATIONS', None, 'Previsao de cargas e instalacoes prediais NBR 5410'
    if has(r'condutor|cabo eletrico|queda de tensao|capacidade de conducao|fator de correcao|agrupamento|bitola do condutor|secao transversal|eletroduto', combo):
        if has(r'queda de tensao', combo):
            return 'P01', ['P01', 'F02'], 'VOLTAGE_DROP', 'CONDUCTORS_AND_CABLES', None, 'Calculo de queda de tensao em alimentadores'
        return 'P01', ['P01', 'I01'], 'CONDUCTOR_SIZING', 'CONDUCTORS_AND_CABLES', None, 'Dimensionamento de condutores e condutos'

    # 11. ELECTRICAL PROTECTION (P02, P03, P04, P05)
    if has(r'disjuntor|fusivel|curto.circuito|sobrecorrente|capacidade de interrupcao|curva (b|c|d)|seletividade', combo):
        return 'P02', ['P02', 'P01'], 'OVERCURRENT_PROTECTION', 'OVERCURRENT_PROTECTION', None, 'Dispositivos de protecao contra sobrecorrente'
    if has(r'diferencial.residual|dispositivo dr|\bidr\b|\bddr\b|corrente de fuga|protecao contra choques por contato indireto', combo):
        return 'P03', ['P03', 'S02'], 'RESIDUAL_CURRENT_PROTECTION', 'RESIDUAL_PROTECTION', None, 'Protecao residual (DR) e contatos indiretos'
    if has(r'esquema de aterramento|\btn\b|\btn.s\b|\btn.c\b|\btt\b|\bit\b|eletrodo de aterramento|malha de aterramento', combo):
        return 'P04', ['P04', 'P03'], 'EARTHING_SCHEME', 'EARTHING_SYSTEMS', None, 'Sistemas e esquemas de aterramento NBR 5410'
    if has(r'spda\b|para.raios|descargas atmosfericas|dps\b|sobretensao transitoria|protecao contra surtos', combo):
        return 'P05', ['P05', 'P04'], 'SPDA', 'SURGE_AND_LIGHTNING_PROTECTION', None, 'Protecao contra descargas atmosfericas e surtos (SPDA/DPS)'

    # 12. POWER NETWORKS & SUBSTATIONS (R01, R02)
    if has(r'subestacao|chave seccionadora.{0,40}(alta|media) tensao|disjuntor de media tensao|rele de protecao de sobrecorrente em media|barramento de subestacao', combo):
        return 'R02', ['R02', 'P02'], 'SUBSTATION_OPERATION', 'SUBSTATIONS', None, 'Operacao e protecao de subestacoes transformadoras'
    if has(r'rede de distribuicao|padrao de entrada|concessionaria de energia|distribuidora|poste de concreto|cruzeta|isolador|transformador de distribuicao', combo):
        return 'R01', ['R01', 'I01'], 'DISTRIBUTION_TOPOLOGY', 'DISTRIBUTION_NETWORKS', None, 'Redes de distribuicao aerea e entrada de servico'

    # 13. PHOTOVOLTAIC (V01)
    if has(r'fotovoltaic|painel solar|modulo solar|inversor solar|energia solar|irradiancia|curva i.v', combo):
        return 'V01', ['V01', 'F04'], 'PV_ARRAY_POWER', 'PHOTOVOLTAIC_SYSTEMS', None, 'Sistemas de geracao solar fotovoltaica'

    # 14. MAINTENANCE (D01, D02)
    if has(r'termografia|termovisor|ensaio nao destrutivo|analise de vibracao|diagnostico de falha', combo):
        return 'D02', ['D02', 'D01'], 'THERMOGRAPHY', 'MAINTENANCE_AND_DIAGNOSIS', None, 'Diagnostico de defeitos e inspecao termografica'
    if has(r'manutencao preventiva|manutencao preditiva|manutencao corretiva|plano de manutencao', combo):
        return 'D01', ['D01', 'D02'], 'MAINTENANCE_STRATEGY', 'MAINTENANCE_AND_DIAGNOSIS', None, 'Estrategias e tipos de manutencao eletrica'

    # 15. FUNDAMENTALS, CIRCUITS, POWER (F01, F02, F03, F04)
    if has(r'fator de potencia|correcao do fator de potencia|banco de capacitores|kvar\b|potencia aparente|potencia ativa|potencia reativa|triangulo de potencias', combo):
        if has(r'banco de capacitores|correcao', combo):
            return 'F04', ['F04', 'E02'], 'POWER_FACTOR_CORRECTION', 'POWER_FACTOR_MANAGEMENT', None, 'Compensacao e correcao de fator de potencia'
        return 'F04', ['F04', 'F03'], 'ELECTRICAL_POWER', 'ELECTRIC_POWER_AND_ENERGY', None, 'Potencias eletricas ativa, reativa e aparente'

    if has(r'resistor|associacao de resistores|resistencia equivalente|primeira lei de ohm|segunda lei de ohm|leis? de kirchhoff|divisor de (tensao|corrente)|ponte de wheatstone', combo):
        if has(r'paralelo', combo):
            return 'F02', ['F02'], 'PARALLEL_EQUIVALENT_RESISTANCE', 'RESISTOR_NETWORKS', None, 'Associacao paralela de resistores'
        if has(r'serie', combo):
            return 'F02', ['F02'], 'SERIES_EQUIVALENT_RESISTANCE', 'RESISTOR_NETWORKS', None, 'Associacao em serie de resistores'
        if has(r'ponte de wheatstone', combo):
            return 'F02', ['F02', 'M01'], 'WHEATSTONE_BRIDGE', 'RESISTOR_NETWORKS', None, 'Ponte de Wheatstone para medicao de resistencia'
        if has(r'lei de ohm|calcule a corrente|calcule a tensao|valor da resistencia', combo):
            return 'F02', ['F02'], 'OHMS_LAW', 'OHMS_LAW', None, 'Aplicacao da Lei de Ohm em circuitos CC'
        return 'F02', ['F02'], 'RESISTOR_ASSOCIATION', 'RESISTOR_NETWORKS', None, 'Associacao e calculos em redes resistivas'

    if has(r'circuito rl|circuito rc|circuito rlc|impedancia|reatancia (indutiva|capacitiva)|fasor|corrente alternada|senoidal|frequencia|periodo|onda senoidal', combo):
        return 'F03', ['F03', 'F01'], 'REACTANCE_IMPEDANCE', 'AC_CIRCUITS', None, 'Impedancia e resposta em circuitos de corrente alternada'

    if has(r'carga eletrica|campo eletrico|potencial eletrico|diferenca de potencial|corrente continua|sistema internacional de unidades|notacao cientifica', combo):
        return 'F01', ['F01', 'F02'], 'ELECTRICAL_QUANTITIES', 'FUNDAMENTALS', None, 'Grandezas fundamentais da eletricidade'

    # Fallback checking image dependency
    if has_img and has(r'figura|diagrama acima|circuito apresentado|grafico', s) and len(s) < 150:
        return None, [], 'IMAGE_DEPENDENT_QUESTION', 'INSUFFICIENT_CONTEXT', 'IMAGE_REQUIRED', 'Enunciado depende essencialmente de interpretacao da imagem'

    return None, [], 'UNSPECIFIED_ELECTRICAL_CONCEPT', 'INSUFFICIENT_CONTEXT', 'CLASSIFIER_GAP', 'Conceito generico sem discriminacao curricular clara'

def main():
    pack = json.loads((OUT / 'holdout-v2_2-annotation-pack.json').read_text(encoding='utf-8'))['questions']
    assert len(pack) == 300

    labels = {}
    stats_modules = {}
    stats_reasons = {}

    for q in pack:
        sid = q['source_id']
        mod, acceptable, concept, family, reason, notes = annotate_question(q)
        
        # Ensure acceptable is never empty if mod is present
        if mod and mod not in acceptable:
            acceptable.insert(0, mod)
        
        labels[sid] = {
            'source_id': sid,
            'expected_primary_module': mod,
            'acceptable_modules': acceptable,
            'expected_primary_concept': concept,
            'expected_semantic_family': family,
            'expected_unclassified_reason': reason,
            'editorial_rationale': notes
        }
        
        m_key = mod if mod else (f"UNCLASSIFIED_{reason}" if reason else "UNCLASSIFIED")
        stats_modules[m_key] = stats_modules.get(m_key, 0) + 1
        if reason:
            stats_reasons[reason] = stats_reasons.get(reason, 0) + 1

    # Salvar ground truth congelado
    labels_path = OUT / 'holdout-v2_2-labels.json'
    labels_path.write_text(json.dumps(labels, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    labels_bytes = labels_path.read_bytes()
    labels_sha256 = hashlib.sha256(labels_bytes).hexdigest()

    print("Anotacao Blind Holdout V2.2 concluida:")
    print(f"- Total anotado: {len(labels)}")
    print(f"- Tamanho do arquivo de labels: {len(labels_bytes)} bytes")
    print(f"- SHA-256 congelado de labels: {labels_sha256}")
    print(f"- Distribuicao de modulos anotados:")
    for m, c in sorted(stats_modules.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {m}: {c}")

if __name__ == '__main__':
    main()

