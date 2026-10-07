"""Conceitos declarativos e hierarquia contextual V2.2;
Melhorias estruturais em relacao a V2.1:
- Soft-starter tem precedencia sobre mencoes genericas a CC/CA;
- Associacao de resistores tem precedencia sobre subtemas genericos de CC/CA;
- Transformador com carga resistiva e T01 (com calculo de resistencia refletida / Ohm como metodo auxiliar);
- Chaves seccionadoras restritas a contexto de subestacao/MT/AT (sem sequestrar NR-12 ou comandos de motores);
- Eletronica de audio e acustica isolada em MISSING_MODULE (sem contaminar F03);
- Cobertura geral para conversao eletromecanica (E01), manutencao industrial (D01), NBR 5410 (I01), luvas isolantes (S02), caixas de passagem e fiacao predial (I01), seguranca em instalacoes (S02), extintores em laboratorio (S02), parada de emergencia NR-12 (S02), reles temporizadores (E03), estrela trifasica (E02), religacao por distribuidora (R01), contatos indiretos e DR (P03), conceito fisico de curto-circuito (P02), caracteristicas de CA senoidal (F01);
- Ontologia explicita de conceitos tecnicos reconhecidos fora dos 35 modulos: INDUSTRIAL_NETWORK, POWER_ELECTRONICS_DC_DC, AUDIO_ELECTRONICS, ANALOG_ELECTRONICS_ADVANCED -> MISSING_MODULE;
- Transitorios RC em teoria de circuitos (carga/descarga de capacitor) direcionados para F03 (sem colidir com procedimento de seguranca/desenergizacao S01).
"""
import re, unicodedata, html

def norm(s):
    return re.sub(r'\s+', ' ', ''.join(c for c in unicodedata.normalize('NFD', html.unescape(s or '').lower()) if unicodedata.category(c) != 'Mn')).strip()

def has(p, s):
    return bool(re.search(p, s))

# (concept, semantic_family, parent, curricular_module, specificity, anchor_class, pattern)
DEFINITIONS = [
    ('MOTOR_REVERSING', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 95, 'ANCHOR_STRONG', r'reversao|inversao.{0,15}(rotacao|sentido de rotacao|giro)|inver.{0,20}fases'),
    ('LOGIC_INTERLOCK', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 85, 'ANCHOR_STRONG', r'intertravamento'),
    ('MOTOR_CONTROL', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 70, 'ANCHOR_CONTEXTUAL', r'circuito.{0,35}comando|comando.{0,25}motor'),
    ('DIRECT_START', 'MOTOR_STARTING', 'COMMANDS', 'E03', 85, 'ANCHOR_STRONG', r'partida direta'),
    ('STAR_DELTA_START', 'REDUCED_VOLTAGE_STARTING', 'COMMANDS', 'E04', 100, 'ANCHOR_STRONG', r'(partida|acionamento|chave).{0,60}estrela.{0,3}triangulo|estrela.{0,3}triangulo.{0,60}(partida|acionamento)'),
    ('COMPENSATOR_START', 'REDUCED_VOLTAGE_STARTING', 'COMMANDS', 'E04', 90, 'ANCHOR_STRONG', r'partida compensadora|chave compensadora'),
    ('MOTOR_STARTING_COMPARISON', 'MOTOR_STARTING_METHODS', 'COMMANDS', None, 98, 'ANCHOR_STRONG', r'metodos.{0,40}acionamento.{0,30}motores|partida.{0,30}(direta|estrela|soft|inversor).{0,60}(soft|inversor|compensadora|estrela)|acionamento de.{0,20}motor.{0,30}por'),
    ('DAHLANDER', 'SPECIAL_MOTORS', 'MOTORS', 'E05', 95, 'ANCHOR_STRONG', r'dahlander'),
    ('FREQUENCY_DRIVE', 'ELECTRONIC_MOTOR_DRIVES', 'COMMANDS', 'E06', 90, 'ANCHOR_STRONG', r'inversor.{0,25}frequencia'),
    ('SOFT_STARTER', 'ELECTRONIC_MOTOR_DRIVES', 'COMMANDS', 'E06', 95, 'ANCHOR_STRONG', r'soft.{0,2}starter|partida suave|chaves? eletronicas?.{0,40}(aceleracao|progressiv)|controle progressivo de acelera|sistema de partida.{0,40}chaves eletronicas'),
    ('MOTOR_PROTECTION', 'MOTOR_PROTECTION', 'PROTECTION', 'P02', 92, 'ANCHOR_STRONG', r'(motor.{0,100}(rele termico|sobrecarga|protecao)|(sobrecarga|rele termico).{0,100}motor)'),
    ('MOTOR_LOCKED_ROTOR_TEST', 'AC_MOTORS', 'MOTORS', 'E01', 95, 'ANCHOR_STRONG', r'ensaio de rotor bloqueado|rotor bloqueado.{0,30}ensaio'),
    ('MOTOR_SLIP', 'AC_MOTORS', 'MOTORS', 'E01', 90, 'ANCHOR_STRONG', r'escorregamento|velocidade do motor.{0,180}velocidade (diminui|reduz)'),
    ('SYNCHRONOUS_SPEED', 'AC_MOTORS', 'MOTORS', 'E01', 80, 'ANCHOR_STRONG', r'(numero de polos|numero de.{0,5}polos|\d+ polos|rotacao nominal).{0,100}(frequencia|hz)|frequencia.{0,300}(polos|rotacao)|velocidade.{0,30}sincrona'),
    ('SYNCHRONOUS_MACHINE_EMF', 'SYNCHRONOUS_MACHINES', 'MOTORS', None, 95, 'ANCHOR_STRONG', r'reatancia sincrona|tensao induzida por fase'),
    ('MOTOR_EFFICIENCY', 'AC_MOTORS', 'MOTORS', 'E01', 90, 'ANCHOR_STRONG', r'(motor.{0,160}(eficiencia|rendimento)|(eficiencia|rendimento).{0,60}motor)'),
    ('MOTOR_ENERGY_CONVERSION', 'AC_MOTORS', 'MOTORS', 'E01', 82, 'ANCHOR_STRONG', r'motor eletrico.{0,60}converte.{0,40}(energia mecanica|eletricidade)|conversao.{0,40}energia eletromecanica|motor eletrico.{0,40}transforma energia'),
    ('INDUCTION_MOTOR', 'AC_MOTORS', 'MOTORS', 'E01', 75, 'ANCHOR_STRONG', r'assincron|motor.{0,15}inducao|gaiola de esquilo'),
    ('SYNCHRONOUS_MOTOR', 'SYNCHRONOUS_MACHINES', 'MOTORS', 'E01', 70, 'ANCHOR_STRONG', r'motor sincron'),
    ('SINGLE_PHASE_MOTOR_CAPACITOR', 'SINGLE_PHASE_MOTORS', 'MOTORS', 'E02', 92, 'ANCHOR_STRONG', r'capacitor.{0,40}partida|partida.{0,30}capacitor|motor monofasico.{0,80}capacitor|capacitor.{0,80}motor monofasico|enrolamento auxiliar.{0,120}capacitor|motor.{0,30}fase dividida'),
    ('DC_MACHINE_TORQUE', 'DC_MACHINES', 'MOTORS', None, 95, 'ANCHOR_STRONG', r'motor serie.{0,100}torque|motor.{0,20}corrente continua.{0,80}torque'),
    ('MOTOR_WINDING_CONNECTION', 'MOTOR_CONNECTIONS', 'MOTORS', 'E02', 72, 'ANCHOR_STRONG', r'fechamento.{0,25}motor|terminais.{0,60}(estrela|triangulo)|enrolamento.{0,40}(ligacao|estrela|triangulo)|motor.{0,30}seis terminais|seis terminais.{0,30}(220|380)|placa.{0,30}(220v|380v)'),
    ('THREE_PHASE_VOLTAGE', 'THREE_PHASE_SYSTEMS', 'AC_CIRCUITS', 'E02', 82, 'ANCHOR_STRONG', r'tensao.{0,20}(linha|fase.fase)|tensao.{0,30}enrolamento|tensao.{0,40}carga.{0,50}submetida|tensao de linha|tensao de fase'),
    ('THREE_PHASE_STAR_DELTA_RELATIONS', 'THREE_PHASE_SYSTEMS', 'AC_CIRCUITS', 'E02', 85, 'ANCHOR_STRONG', r'circuito eletrico trifasico conectado em (estrela|triangulo)|ligacao em estrela.{0,50}(tensao de linha|corrente de linha|raiz de 3)'),
    ('THREE_PHASE_POWER', 'ELECTRIC_POWER_AND_ENERGY', 'ELECTRICAL_POWER', 'F04', 70, 'ANCHOR_CONTEXTUAL', r'(calcule|calcular|valor|determine|qual).{0,65}potencia.{0,90}trifas|trifas.{0,120}(potencia total|potencia ativa|potencia aparente)'),
    ('WHEATSTONE_BRIDGE', 'BRIDGE_CIRCUITS', 'BRIDGE_CIRCUITS', 'F02', 100, 'ANCHOR_STRONG', r'wheatstone|ponte.{0,20}equilibrio'),
    ('STRAIN_GAUGE', 'INSTRUMENTATION_SENSORS', 'INDUSTRIAL_INSTRUMENTATION', None, 90, 'ANCHOR_STRONG', r'extensometro|strain.gauge'),
    ('RESISTIVE_SENSOR', 'INSTRUMENTATION_SENSORS', 'INDUSTRIAL_INSTRUMENTATION', None, 85, 'ANCHOR_STRONG', r'pt.{0,2}100|termorresist|sensor.{0,30}resistiv'),
    ('THERMOCOUPLE', 'INSTRUMENTATION_SENSORS', 'INDUSTRIAL_INSTRUMENTATION', None, 80, 'ANCHOR_STRONG', r'termopar|termopares'),
    ('INSTRUMENTATION_TAGS', 'INSTRUMENTATION_STANDARDS', 'INDUSTRIAL_INSTRUMENTATION', None, 90, 'ANCHOR_STRONG', r'\btic\b|identific.{0,20}sigla.{0,15}(pic|fic|lic)|padr.{0,15}isa'),
    ('INDUSTRIAL_TRANSMITTER', 'INDUSTRIAL_TRANSMITTERS', 'INDUSTRIAL_INSTRUMENTATION', None, 80, 'ANCHOR_STRONG', r'transmissor.{0,40}sinais|transmissores|transdutor.{0,20}pressao'),
    ('ULTRASONIC_LEVEL', 'AUTOMATION_SENSORS', 'AUTOMATION_SENSORS', 'A03', 95, 'ANCHOR_STRONG', r'nivel.{0,15}ultrasson|ultrasson.{0,30}nivel'),
    ('PRESENCE_SENSOR', 'AUTOMATION_SENSORS', 'AUTOMATION_SENSORS', 'A03', 85, 'ANCHOR_STRONG', r'sensor.{0,20}presenca|circulacao de pessoas|detector.{0,15}movimento'),
    ('LEVEL_CONTROL', 'AUTOMATION_SENSORS', 'AUTOMATION_SENSORS', 'A03', 75, 'ANCHOR_CONTEXTUAL', r'controle de nivel|sensor de nivel'),
    ('FIRE_DETECTION', 'SAFETY_SYSTEMS', 'AUTOMATION_SENSORS', 'A03', 85, 'ANCHOR_STRONG', r'alarme de incendio|detector.{0,15}(fumaca|chama)|detectores automaticos'),
    ('SEMICONDUCTOR_SWITCH', 'POWER_ELECTRONICS', 'ANALOG_ELECTRONICS', None, 92, 'ANCHOR_STRONG', r'transistor.{0,120}chave|chave.{0,80}transistor|chaveamento.{0,30}(transformador|corrente)|hfe.{0,10}sat'),
    ('TRANSISTOR_IDENTIFICATION', 'TRANSISTORS', 'ANALOG_ELECTRONICS', None, 88, 'ANCHOR_STRONG', r'tipo de transistor|transistor.{0,35}(do tipo|utilizado)'),
    ('TRANSISTOR_OPERATION', 'TRANSISTORS', 'ANALOG_ELECTRONICS', None, 75, 'ANCHOR_STRONG', r'transistor|\bbjt\b|\bfet\b|\bmosfet\b'),
    ('THYRISTOR_OPERATION', 'POWER_ELECTRONICS', 'ANALOG_ELECTRONICS', None, 86, 'ANCHOR_STRONG', r'tiristor|\bscr\b|\btriac\b'),
    ('RECTIFIER_OPERATION', 'POWER_ELECTRONICS', 'ANALOG_ELECTRONICS', None, 80, 'ANCHOR_STRONG', r'retificador|retifica.{0,30}(onda|tensao)|fonte.{0,35}(ac/dc|nao regulada)'),
    ('ACTIVE_FILTER', 'OPERATIONAL_AMPLIFIERS', 'ANALOG_ELECTRONICS', None, 85, 'ANCHOR_STRONG', r'filtro ativo|amplificador operacional|\bampop\b'),
    ('OSCILLATOR_FEEDBACK', 'ANALOG_CIRCUITS', 'ANALOG_ELECTRONICS', None, 90, 'ANCHOR_STRONG', r'barkhausen|oscilacao espontan|oscilador.{0,15}realiment'),
    ('AMPLIFIER_GAIN', 'OPERATIONAL_AMPLIFIERS', 'ANALOG_ELECTRONICS', None, 85, 'ANCHOR_STRONG', r'ganho.{0,20}(potencia|db|tensao|corrente)|circuito eletronico.{0,160}ganho|ganho de corrente total'),
    ('SEMICONDUCTOR_PHYSICS', 'SEMICONDUCTORS', 'ANALOG_ELECTRONICS', None, 80, 'ANCHOR_STRONG', r'dopagem|portadores minoritarios|semicondutor|diodo'),
    ('PROTOBOARD', 'PROTOTYPING', 'ANALOG_ELECTRONICS', None, 80, 'ANCHOR_STRONG', r'protoboard'),
    ('AUDIO_ELECTRONICS', 'AUDIO_ELECTRONICS', 'ANALOG_ELECTRONICS', None, 92, 'ANCHOR_STRONG', r'amplificador de.{0,20}audio|caixa acustica|alto.falante|linha de audio|potencia de audio'),
    ('POWER_ELECTRONICS_DC_DC', 'POWER_ELECTRONICS', 'ANALOG_ELECTRONICS', None, 92, 'ANCHOR_STRONG', r'conversores?.{0,20}cc.cc|conversor.{0,20}(buck|boost)|buck.boost|\bchopper\b'),
    ('INSULATION_TEST', 'INSULATION_AND_CONTINUITY', 'INSULATION', 'M02', 100, 'ANCHOR_STRONG', r'resistencia de isolamento|medicao.{0,20}isolacao|megohmetro|megometro'),
    ('CONTINUITY_TEST', 'INSULATION_AND_CONTINUITY', 'MEASUREMENTS', 'M02', 80, 'ANCHOR_STRONG', r'continuidade|condutores.{0,70}interligados'),
    ('MEASUREMENT_CONNECTION', 'MULTIMETER_MEASUREMENTS', 'MULTIMETER', 'M01', 85, 'ANCHOR_STRONG', r'(medir|medicao|medida).{0,20}(tensao|corrente|resistencia).{0,120}(conect|terminais|serie|paralelo)|medidas.{0,70}colocado|deve ser.{0,20}colocado|instrumento.{0,70}colocado|procedimentos.{0,30}medir resistencias|espelho.{0,30}paralaxe'),
    ('MULTIMETER_VOLTAGE', 'MULTIMETER_MEASUREMENTS', 'MULTIMETER', 'M01', 75, 'ANCHOR_STRONG', r'(multimetro|voltimetro).{0,120}tensao|tensao.{0,120}(multimetro|voltimetro)'),
    ('MULTIMETER_CURRENT', 'MULTIMETER_MEASUREMENTS', 'MULTIMETER', 'M01', 75, 'ANCHOR_STRONG', r'(amperimetro|multimetro).{0,100}corrente|corrente.{0,80}(amperimetro|multimetro)'),
    ('MULTIMETER_RESISTANCE', 'MULTIMETER_MEASUREMENTS', 'MULTIMETER', 'M01', 75, 'ANCHOR_STRONG', r'ohmimetro|multimetro.{0,45}resistencia'),
    ('MULTIMETER_FUNCTION', 'MULTIMETER_MEASUREMENTS', 'MULTIMETER', 'M01', 40, 'TOKEN_GENERIC', r'multimetro|amperimetro|voltimetro|alicate amper'),
    ('OSCILLOSCOPE_READING', 'MEASUREMENT_INSTRUMENTS', 'MEASUREMENTS', 'M01', 75, 'ANCHOR_STRONG', r'osciloscopio'),
    ('SPECTRUM_MEASUREMENT', 'MEASUREMENT_INSTRUMENTS', 'MEASUREMENTS', 'M01', 80, 'ANCHOR_STRONG', r'dominio da frequencia.{0,25}instrumento|instrumento.{0,100}dominio da frequencia'),
    ('CURRENT_TRANSFORMER', 'INSTRUMENT_TRANSFORMERS', 'INDIRECT_MEASUREMENT', 'T02', 90, 'ANCHOR_STRONG', r'transformador.{0,15}corrente|\bt\.?\s?c\.?\b.{0,30}secundario'),
    ('POTENTIAL_TRANSFORMER', 'INSTRUMENT_TRANSFORMERS', 'INDIRECT_MEASUREMENT', 'T02', 90, 'ANCHOR_STRONG', r'transformador.{0,15}potencial|\bt\.?\s?p\.?\b.{0,30}secundario'),
    ('TRANSFORMER_THREE_PHASE', 'POWER_TRANSFORMERS', 'TRANSFORMERS', 'T01', 85, 'ANCHOR_STRONG', r'transformador trifasico|transformador.{0,30}estrela'),
    ('TRANSFORMER_REFLECTED_IMPEDANCE', 'POWER_TRANSFORMERS', 'TRANSFORMERS', 'T01', 88, 'ANCHOR_STRONG', r'transformador.{0,60}(alimenta.{0,30}carga|carga resistiva|impedancia refletida|resistencia da carga|lado primario.{0,30}secundario)|carga resistiva.{0,60}transformador'),
    ('TRANSFORMER_RATIO', 'POWER_TRANSFORMERS', 'TRANSFORMERS', 'T01', 75, 'ANCHOR_STRONG', r'transformador.{0,130}(espiras|primario|secundario|relacao)|espiras.{0,80}transformador|relacao de transformacao'),
    ('TRANSFORMER_THEORY', 'POWER_TRANSFORMERS', 'TRANSFORMERS', 'T01', 45, 'TOKEN_GENERIC', r'transformador|autotransformador'),
    ('NR10_REENERGIZATION', 'DEENERGIZATION_PROCEDURES', 'NR10', 'S01', 95, 'ANCHOR_STRONG', r'reenergizacao|reenergizar'),
    ('STORED_ENERGY_DISCHARGE', 'DEENERGIZATION_PROCEDURES', 'NR10', 'S01', 100, 'ANCHOR_STRONG', r'capacitor.{0,100}(descarreg|mantem tensao)|descarreg.{0,70}capacitor|energia armazenada.{0,60}(risco|seguranca|loto)'),
    ('ELECTRICAL_LOCKOUT', 'DEENERGIZATION_PROCEDURES', 'NR10', 'S01', 90, 'ANCHOR_STRONG', r'bloqueio.{0,70}(eletric|reenerg|tensao)|\bloto\b'),
    ('NR10_DEENERGIZATION', 'DEENERGIZATION_PROCEDURES', 'NR10', 'S01', 85, 'ANCHOR_STRONG', r'desenergiz|ausencia de tensao|antes de iniciar.{0,80}manutencao.{0,80}isolar o circuito|constatacao de ausencia de tensao'),
    ('NR10_DOCUMENTATION', 'SAFETY_REGULATIONS', 'NR10', 'S03', 92, 'ANCHOR_STRONG', r'prontuario|nr.{0,3}10.{0,1000}(75 kw|esquemas unifilares)|curso de reciclagem da norma nr.{0,2}10|reciclagem da norma nr.{0,2}10|nr.{0,3}10.{0,60}seguranca em projetos|seguranca em projetos.{0,60}nr.{0,2}10'),
    ('VOLTAGE_CLASSIFICATION', 'SAFETY_REGULATIONS', 'NR10', 'S03', 75, 'ANCHOR_STRONG', r'classificacao.{0,20}tensao|extra.baixa tensao|rede eletrica.{0,30}baixa tensao'),
    ('WORK_AT_HEIGHT', 'SAFETY_MEASURES', 'SAFETY', 'S02', 90, 'ANCHOR_STRONG', r'trabalho.{0,25}altura|nr.{0,3}35|trabalhar no alto|queda.{0,20}altura|riscos ergon[oó]micos.{0,100}postes'),
    ('EPI_EPC_SELECTION', 'SAFETY_MEASURES', 'SAFETY', 'S02', 90, 'ANCHOR_STRONG', r'\bepis?\b|\bepcs?\b|protecao (individual|coletiva)|luvas isolantes|luvas e capacetes|equipamentos? de protecao'),
    ('INSULATING_GLOVES', 'SAFETY_MEASURES', 'SAFETY', 'S02', 92, 'ANCHOR_STRONG', r'luvas? isolantes?|luvas? de borracha.{0,40}choque|seguranca das maos.{0,40}choque|luva de protecao tipo condutor'),
    ('WORKER_AUTHORIZATION', 'SAFETY_MEASURES', 'NR10', 'S02', 80, 'ANCHOR_STRONG', r'(trabalhador|profissional).{0,50}(autoriz|habilit|qualific)|operacoes elementares|periodo de afastamento.{0,60}reciclagem|retornar de um periodo de afastamento'),
    ('MACHINE_SAFETY_NR12', 'SAFETY_MEASURES', 'SAFETY', 'S02', 90, 'ANCHOR_STRONG', r'nr.{0,2}12|seguranca no trabalho em maquinas|dispositivos de parada de emergencia|dispositivos de partida.{0,30}acionamento e parada'),
    ('LAB_FIRE_SAFETY', 'SAFETY_MEASURES', 'SAFETY', 'S02', 85, 'ANCHOR_STRONG', r'extintores.{0,60}(laboratorio|eletrot|classe c)|sinalizacao de extintores|combate a incendio.{0,40}instalacoes eletricas'),
    ('ELECTRICAL_SAFETY_MEASURES', 'SAFETY_MEASURES', 'SAFETY', 'S02', 82, 'ANCHOR_STRONG', r'servicos executados em instalacoes eletricas.{0,60}seguranca|medidas de seguranca.{0,50}instalacoes eletricas|trabalhos em circuitos desenergizados'),
    ('WORKPLACE_ORGANIZATION', 'SAFETY_MEASURES', 'SAFETY', 'S02', 70, 'ANCHOR_CONTEXTUAL', r'organizacao.{0,50}ferramentas|ferramentas.{0,35}espalhadas'),
    ('ELECTRICAL_SAFETY', 'SAFETY_MEASURES', 'NR10', 'S02', 50, 'TOKEN_GENERIC', r'nr.{0,3}10|seguranca.{0,30}eletric|perigo de choque|risco de choque|aviso.{0,40}choque'),
    ('POWER_FACTOR_CORRECTION', 'POWER_FACTOR_MANAGEMENT', 'POWER', 'F04', 100, 'ANCHOR_STRONG', r'(capacitor|banco de capacitores).{0,140}(fator de potencia|energia reativa)|(fator de potencia).{0,150}(capacitor|corrigir|correcao)|reduzir os custos com eletricidade.{0,100}capacitor|cargas predominantes.{0,60}reduzir os custos'),
    ('POWER_FACTOR', 'POWER_FACTOR_MANAGEMENT', 'POWER', 'F04', 90, 'ANCHOR_STRONG', r'fator de potencia'),
    ('ELECTRICAL_POWER', 'ELECTRIC_POWER_AND_ENERGY', 'POWER', 'F04', 70, 'ANCHOR_CONTEXTUAL', r'(potencia (eletrica|ativa|reativa|aparente|recebida|fornecida)|qual.{0,25}potencia|valor.{0,25}potencia|triangulo de potencias|potencia ativa|potencia reativa|potencia aparente|chuveiro.{0,100}valor da corrente|(\b\d+w\b|watts).{0,350}corrente total|corrente total.{0,350}(\b\d+w\b|watts))'),
    ('ELECTRICAL_ENERGY', 'ELECTRIC_POWER_AND_ENERGY', 'POWER', 'F04', 65, 'ANCHOR_CONTEXTUAL', r'energia.{0,30}(consumida|consumo)|\bkwh\b'),
    ('SOURCE_LOADING', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 95, 'ANCHOR_STRONG', r'gerador de funcoes.{0,200}resistor|resistencia interna.{0,60}fonte'),
    ('KIRCHHOFF_KCL', 'KIRCHHOFF_LAWS', 'KIRCHHOFF', 'F02', 90, 'ANCHOR_STRONG', r'lei.{0,15}nos|kirchhoff.{0,35}corrente'),
    ('KIRCHHOFF_KVL', 'KIRCHHOFF_LAWS', 'KIRCHHOFF', 'F02', 90, 'ANCHOR_STRONG', r'lei.{0,15}malhas|kirchhoff.{0,35}tensao'),
    ('PARALLEL_EQUIVALENT_RESISTANCE', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 88, 'ANCHOR_STRONG', r'associacao em paralelo|paralelo de.{0,20}resistores|resistores.{0,80}(ligados|conectados) em paralelo'),
    ('SERIES_EQUIVALENT_RESISTANCE', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 88, 'ANCHOR_STRONG', r'associacao em serie|circuito (em )?serie|resistores.{0,55}(ligados|conectados) em serie'),
    ('RESISTOR_ASSOCIATION', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 82, 'ANCHOR_STRONG', r'associacao de resistores|conjuntos? de resistores interligados'),
    ('MIXED_EQUIVALENT_RESISTANCE', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 80, 'ANCHOR_STRONG', r'resistencia equivalente|associacao mista|associad.{0,30}paralelo.{0,120}serie|resistor.{0,30}paralelo.{0,120}serie'),
    ('STAR_DELTA_IMPEDANCE', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 92, 'ANCHOR_STRONG', r'circuito equivalente.{0,50}(delta|triangulo)|impedancias.{0,120}equivalente'),
    ('OHMS_LAW_CURRENT', 'OHMS_LAW', 'OHMS_LAW', 'F02', 65, 'ANCHOR_STRONG', r'(valor|calcule|determine|qual).{0,25}corrente|corrente.{0,40}(inalterada|manter)|manter.{0,15}corrente|qual a corrente total do circuito|a corrente total fornecida.{0,30}fonte|a corrente total no circuito'),
    ('OHMS_LAW_RESISTANCE', 'OHMS_LAW', 'OHMS_LAW', 'F02', 65, 'ANCHOR_STRONG', r'(valor|calcule|determine|qual).{0,25}resistencia'),
    ('OHMS_LAW_VOLTAGE', 'OHMS_LAW', 'OHMS_LAW', 'F02', 65, 'ANCHOR_STRONG', r'(valor|calcule|determine|qual).{0,25}tensao|aumento de tensao'),
    ('OHMS_LAW', 'OHMS_LAW', 'OHMS_LAW', 'F02', 50, 'TOKEN_GENERIC', r'lei de ohm'),
    ('RESISTOR_COLOR_CODE', 'RESISTOR_NETWORKS', 'RESISTOR_NETWORKS', 'F02', 85, 'ANCHOR_STRONG', r'resistor.{0,55}(cores|cor)|codigo de cores'),
    ('RC_TRANSIENT', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 95, 'ANCHOR_STRONG', r'constantes? de tempo|transitorio.{0,20}capac|circuito rc|carga e.{0,15}descarga de.{0,15}capacitor|circuito.{0,30}capacitor.{0,30}regime permanente'),
    ('RLC_PHASOR', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 85, 'ANCHOR_STRONG', r'\brlc\b|fasor|diagrama fasorial'),
    ('REACTANCE_IMPEDANCE', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 85, 'ANCHOR_STRONG', r'reatancia|impedancia.{0,40}(circuito|ca|ramo|complexa|equivalente|z\b|fase|fasor|indutiva|capacitiva|ohm)|oposicao.{0,50}corrente.{0,50}alternada|razao entre tensao.{0,30}corrente.{0,30}alternada'),
    ('FREQUENCY_PERIOD', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 75, 'ANCHOR_STRONG', r'(\bhz\b|frequencia.{0,25}(eletrica|sinal|rede|angular|fundamental)|periodo.{0,25}(onda|sinal|senoide|ciclo|fundamental)|\bt\s*=\s*1\s*/\s*f\b|forma.{0,3}de onda.{0,25}(senoidal|ca|alternada)|tensao.{0,15}senoidal|corrente.{0,15}senoidal)'),
    ('CAPACITOR_STORAGE', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 65, 'ANCHOR_CONTEXTUAL', r'(capacitancia|armazenar.{0,20}(carga|energia)|energia.{0,20}armazenada.{0,30}capacitor|carga.{0,20}acumulada.{0,30}capacitor|diel[eé]trico|placas.{0,20}paralelas.{0,30}capacitor|\bq\s*=\s*c\s*\.?\s*v\b)'),
    ('INDUCTOR_STORAGE', 'AC_CIRCUITS', 'AC_CIRCUITS', 'F03', 65, 'ANCHOR_CONTEXTUAL', r'indutor|indutancia|energia.{0,20}armazenada.{0,30}indutor'),
    ('DC_AC_DIFFERENCE', 'FUNDAMENTALS', 'FUNDAMENTALS', 'F01', 80, 'ANCHOR_STRONG', r'corrente.{0,15}continua.{0,30}corrente.{0,15}alternada|caracteristicas das correntes cont[ií]nua|diferenca.{0,30}(cc|ca)|(\bcc e ca\b|\bca e cc\b)'),
    ('AC_CHARACTERISTICS', 'FUNDAMENTALS', 'FUNDAMENTALS', 'F01', 80, 'ANCHOR_STRONG', r'corrente alternada \(?ca\)? e caracterizada|caracteristicas da corrente alternada|forma de onda senoidal.{0,40}(polaridade|sentido|ciclo)'),
    ('ELECTRICAL_UNITS', 'FUNDAMENTALS', 'FUNDAMENTALS', 'F01', 65, 'ANCHOR_CONTEXTUAL', r'unidade.{0,20}(medida|base)|sistema internacional|\bddp\b.{0,150}unidade|unidades de base'),
    ('SIGNIFICANT_FIGURES', 'FUNDAMENTALS', 'FUNDAMENTALS', 'F01', 90, 'ANCHOR_STRONG', r'algarismos significativos'),
    ('ELECTRICAL_QUANTITIES', 'FUNDAMENTALS', 'FUNDAMENTALS', 'F01', 30, 'TOKEN_GENERIC', r'grandeza eletrica|carga eletrica|diferenca de potencial'),
    ('LOAD_DEMAND_CURRENT', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 90, 'ANCHOR_STRONG', r'levantamento de carga|corrente total demandada|demanda.{0,40}residencia'),
    ('LOAD_ALLOCATION', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 80, 'ANCHOR_STRONG', r'potencia.{0,35}minima.{0,30}(atribuida|tomada)|previsao.{0,25}carga'),
    ('LIGHTING_CONTROL_PROTOCOL', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 90, 'ANCHOR_STRONG', r'dmx512'),
    ('LIGHTING_SELECTION', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 60, 'ANCHOR_CONTEXTUAL', r'lampada|luminaria|iluminacao'),
    ('ELECTRICIAN_TOOLS', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 65, 'ANCHOR_CONTEXTUAL', r'ferramentas.{0,80}(alicate|eletricista)|alicate.{0,20}(universal|bico|corte)'),
    ('DISTRIBUTION_BOARD', 'BUILDING_INSTALLATIONS', 'BUILDING_INSTALLATIONS', 'I01', 68, 'ANCHOR_STRONG', r'quadros? de distribuicao|barramento.{0,25}(neutro|terra|protecao|fase).{0,30}quadro|quadro geral de baixa tensao|\bqgbt\b'),
    ('NBR5410_INSTALLATIONS', 'INSTALLATION_STANDARDS', 'ELECTRICAL_INSTALLATIONS', 'I01', 88, 'ANCHOR_STRONG', r'nbr.{0,3}5410|instalac.{0,30}baixa tensao.{0,50}nbr|norma.{0,20}instalac.{0,25}baixa tensao'),
    ('OUTLET_WIRING', 'WIRING_INFRASTRUCTURE', 'ELECTRICAL_INSTALLATIONS', 'I01', 85, 'ANCHOR_STRONG', r'caixa de passagem.{0,60}condutores|reparo.{0,30}tomada|instalacao de tomada.{0,40}condutores|tomada.{0,40}fios?.{0,40}caixa'),
    ('ELECTRICAL_CAD', 'ELECTRICAL_DRAWINGS', 'ELECTRICAL_DRAWINGS', 'I03', 80, 'ANCHOR_STRONG', r'\bcad\b|recursos de informatica.{0,90}instalacoes|software.{0,35}projeto eletrico'),
    ('ELECTRICAL_DIAGRAM_NOTATION', 'ELECTRICAL_DRAWINGS', 'ELECTRICAL_DRAWINGS', 'I03', 65, 'ANCHOR_CONTEXTUAL', r'unifilar|multifilar|simbologia|paredes.{0,30}caixas'),
    ('ELECTRICAL_COMPONENT_SYMBOL', 'ELECTRICAL_DRAWINGS', 'ELECTRICAL_DRAWINGS', 'I03', 80, 'ANCHOR_STRONG', r'(simbolo|simbolos).{0,80}(representar|identificacao)|componente.{0,30}representado|componente.{0,40}representad'),
    ('WIRING_INFRASTRUCTURE', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 75, 'ANCHOR_CONTEXTUAL', r'eletroduto|canaleta|rede embutida'),
    ('CONDUCTOR_CORRECTION', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 90, 'ANCHOR_STRONG', r'fatores de correcao|fator de correcao'),
    ('CONDUCTOR_AMPACITY', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 85, 'ANCHOR_STRONG', r'capacidade.{0,15}conducao|ampacidade'),
    ('CONDUCTOR_SIZING', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 65, 'ANCHOR_CONTEXTUAL', r'dimensionamento.{0,25}(condutor|cabo)|bitola.{0,25}condutor|escolher a bitola'),
    ('CONDUCTOR_INSULATION', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 80, 'ANCHOR_STRONG', r'(material|materiais).{0,20}isolamento|isolacao.{0,30}(pvc|epr|xlpe)'),
    ('VOLTAGE_DROP', 'CONDUCTORS_AND_CABLES', 'CONDUCTORS', 'P01', 85, 'ANCHOR_STRONG', r'queda de tensao'),
    ('PROTECTION_CONDUCTOR_COORDINATION', 'OVERCURRENT_PROTECTION', 'OVERCURRENT_PROTECTION', 'P02', 90, 'ANCHOR_STRONG', r'(disjuntor.{0,80}(epr|mm2)|\b(epr|mm2)\b.{0,100}disjuntor)'),
    ('OVERCURRENT_PROTECTION', 'OVERCURRENT_PROTECTION', 'PROTECTION', 'P02', 72, 'ANCHOR_CONTEXTUAL', r'disjuntor|fusivel|curto.{0,2}circuito|curtos.{0,2}circuitos|sobrecarga|protecao de ramais alimentadores|principal funcao de um disjuntor'),
    ('SHORT_CIRCUIT_CONCEPT', 'OVERCURRENT_PROTECTION', 'PROTECTION', 'P02', 85, 'ANCHOR_STRONG', r'caminho de baixa resistencia.{0,40}corrente|curto.circuito|curtos.circuitos'),
    ('FUSE_OPERATION', 'OVERCURRENT_PROTECTION', 'OVERCURRENT_PROTECTION', 'P02', 95, 'ANCHOR_STRONG', r'fusivel.{0,50}descontinuidade|elo de fusao'),
    ('PROTECTION_SELECTIVITY', 'OVERCURRENT_PROTECTION', 'PROTECTION', 'P02', 85, 'ANCHOR_STRONG', r'sele[tic]+ividade|seccione apenas o circuito defeituoso|circuito defeituoso.{0,60}demais circuitos'),
    ('RESIDUAL_EARTHING_COMPATIBILITY', 'RESIDUAL_PROTECTION', 'RESIDUAL_PROTECTION', 'P03', 95, 'ANCHOR_STRONG', r'diferencial.residual.{0,200}esquema de aterramento|esquema de aterramento.{0,200}diferencial.residual'),
    ('RESIDUAL_CURRENT_PROTECTION', 'RESIDUAL_PROTECTION', 'RESIDUAL_PROTECTION', 'P03', 85, 'ANCHOR_STRONG', r'diferencial.residual|dispositivos? dr|\bidr\b|\bddr\b|soma vetorial.{0,70}correntes'),
    ('INDIRECT_CONTACT_PROTECTION', 'RESIDUAL_PROTECTION', 'PROTECTION', 'P03', 88, 'ANCHOR_STRONG', r'contatos? indiretos?|protecao contra contatos indiretos|esquemas? de aterramento.{0,60}(dispositivo diferencial|dr\b|seccionamento automatico)'),
    ('LIGHTING_SWITCHING', 'LIGHTING_CONTROLS', 'LIGHTING_CONTROLS', 'I02', 75, 'ANCHOR_CONTEXTUAL', r'interruptor|lampada.{0,100}pontos de comando'),
    ('PHOTOELECTRIC_SWITCH', 'LIGHTING_CONTROLS', 'LIGHTING_CONTROLS', 'I02', 85, 'ANCHOR_STRONG', r'fotocelula|rele.{0,15}foto'),
    ('EARTHING_SCHEME', 'EARTHING_SYSTEMS', 'EARTHING', 'P04', 80, 'ANCHOR_STRONG', r'esquema.{0,20}aterramento|\btn.c.s\b|\btn.c\b|\btn.s\b|\btt\b|\bit\b'),
    ('EARTHING_ELECTRODE', 'EARTHING_SYSTEMS', 'EARTHING', 'P04', 80, 'ANCHOR_STRONG', r'infraestrutura de aterramento|eletrodo de aterramento'),
    ('EARTHING_FUNCTION', 'EARTHING_SYSTEMS', 'EARTHING', 'P04', 45, 'TOKEN_GENERIC', r'aterramento|equipotencial'),
    ('SPDA', 'SURGE_AND_LIGHTNING_PROTECTION', 'ATMOSPHERIC_PROTECTION', 'P05', 90, 'ANCHOR_STRONG', r'\bspda\b|sistema.{0,40}descargas atmosfericas'),
    ('SURGE_PROTECTION', 'SURGE_AND_LIGHTNING_PROTECTION', 'ATMOSPHERIC_PROTECTION', 'P05', 85, 'ANCHOR_STRONG', r'\bdps\b|para.raios|protecao contra surtos'),
    ('PV_IV_CURVE', 'PHOTOVOLTAIC_SYSTEMS', 'PHOTOVOLTAICS', 'V01', 90, 'ANCHOR_STRONG', r'curva iv|curva i.v|maxima potencia.{0,30}fotovolta'),
    ('PV_ARRAY_POWER', 'PHOTOVOLTAIC_SYSTEMS', 'PHOTOVOLTAICS', 'V01', 75, 'ANCHOR_STRONG', r'fotovoltaic|modulos.{0,30}wp'),
    ('PV_ENERGY', 'PHOTOVOLTAIC_SYSTEMS', 'PHOTOVOLTAICS', 'V01', 80, 'ANCHOR_STRONG', r'energia.{0,50}painel solar|painel solar.{0,120}energia'),
    ('RENEWABLE_SOURCES', 'PHOTOVOLTAIC_SYSTEMS', 'PHOTOVOLTAICS', 'V01', 65, 'ANCHOR_CONTEXTUAL', r'energia renovave|energias renovave|fontes de energia renovave|fontes alternativas de energia'),
    ('THERMOGRAPHY', 'MAINTENANCE_AND_DIAGNOSIS', 'FAULT_DIAGNOSIS', 'D02', 95, 'ANCHOR_STRONG', r'termograf|termovisor|ponto quente'),
    ('MAINTENANCE_STRATEGY', 'MAINTENANCE_AND_DIAGNOSIS', 'MAINTENANCE', 'D01', 85, 'ANCHOR_STRONG', r'manutencao (preventiva|preditiva|corretiva)|chama.se manutencao|inspecoes sistematicas|manutencao preventiva.{0,40}corretiva|manutencao preditiva.{0,40}preventiva|tipos de manutencao.{0,40}(eletrica|industrial)|estrategia de manutencao'),
    ('MAINTENANCE_TYPES', 'MAINTENANCE_AND_DIAGNOSIS', 'MAINTENANCE', 'D01', 75, 'ANCHOR_CONTEXTUAL', r'manutencao de rotina|planos? de manutencao|manutencao programada'),
    ('MOTOR_MAINTENANCE', 'MAINTENANCE_AND_DIAGNOSIS', 'MAINTENANCE', 'D01', 82, 'ANCHOR_STRONG', r'manutencao de motores|manutencao preventiva.{0,40}motor|inspecao periodica.{0,40}motor eletrico'),
    ('INSTRUMENT_MAINTENANCE', 'MAINTENANCE_AND_DIAGNOSIS', 'MAINTENANCE', 'D01', 82, 'ANCHOR_STRONG', r'manutencao de equipamentos.{0,40}laborat|calibracao de instrumentos|manutencao.{0,30}instrumentos de medicao'),
    ('FAULT_DIAGNOSIS', 'MAINTENANCE_AND_DIAGNOSIS', 'FAULT_DIAGNOSIS', 'D02', 55, 'ANCHOR_CONTEXTUAL', r'localizacao de falhas|diagnostico.{0,20}falha|localizar.{0,15}defeito'),
    ('BOOLEAN_ALGEBRA', 'DIGITAL_LOGIC', 'DIGITAL_LOGIC', 'A01', 80, 'ANCHOR_STRONG', r'boole|karnaugh|portas? logicas?'),
    ('NUMBER_BASE_CONVERSION', 'DIGITAL_LOGIC', 'DIGITAL_LOGIC', 'A01', 85, 'ANCHOR_STRONG', r'base (decimal|octal)|hexadecimal|registrador.{0,300}(xor|and|or)|sistema.{0,15}numeracao|converter.{0,30}binario'),
    ('LADDER_BOOLEAN', 'DIGITAL_LOGIC', 'DIGITAL_LOGIC', 'A01', 80, 'ANCHOR_STRONG', r'ladder.{0,120}funcao logica|funcao.{0,40}ladder'),
    ('LADDER_SEAL_IN', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 95, 'ANCHOR_STRONG', r'contato.{0,20}selo|selo.{0,25}contato'),
    ('TIMER_RELAY', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 88, 'ANCHOR_STRONG', r'rele temporizador|temporizador|tempos predeterminados.{0,40}(ligar|desligar)|programar.{0,20}ligar e desligar automaticamente'),
    ('PLC_LADDER', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 92, 'ANCHOR_STRONG', r'linguagem.{0,15}ladder|grafica ladder|diagrama ladder|programacao.{0,20}ladder'),
    ('PLC_INTERNAL_RELAY', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 90, 'ANCHOR_STRONG', r'rele.{0,20}(interno|auxiliar|marca).{0,40}(clp|ladder)|(clp|ladder).{0,40}rele.{0,20}(interno|auxiliar)'),
    ('PLC_IO', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 88, 'ANCHOR_STRONG', r'modulos de entrada|modulos.{0,20}saida|entradas.{0,20}saidas'),
    ('PLC_PROGRAMMING', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 85, 'ANCHOR_STRONG', r'texto estruturado|linguagem.{0,20}\bst\b|instrucoes de programacao.{0,30}clp'),
    ('PLC_SCAN', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 90, 'ANCHOR_STRONG', r'ciclo.{0,20}varredura'),
    ('SCADA_OPERATION', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 75, 'ANCHOR_STRONG', r'supervisorio|\bscada\b'),
    ('CAUSE_EFFECT_LOGIC', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 80, 'ANCHOR_STRONG', r'matriz de causa e efeito'),
    ('PLC_CONTROL', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 82, 'ANCHOR_STRONG', r'controlador logico|\bclp\b|controladores logicos|automacao industrial.{0,80}clp'),
    ('AUTOMATION_ACTUATOR', 'PROGRAMMABLE_CONTROLLERS', 'PLC', 'A02', 65, 'ANCHOR_CONTEXTUAL', r'atuadores.{0,40}sistema de producao|atuador.{0,40}automatizado'),
    ('CONTACTOR_CONTROL', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 65, 'ANCHOR_CONTEXTUAL', r'contator|comandos eletricos automaticos'),
    ('RELAY_OPERATION', 'MOTOR_CONTROL', 'COMMANDS', 'E03', 65, 'ANCHOR_CONTEXTUAL', r'rele|reles|chaves eletromecanicas'),
    ('PNEUMATIC_VALVE', 'FLUID_POWER', 'FLUID_POWER', 'H01', 75, 'ANCHOR_STRONG', r'valvula.{0,30}(direcional|pneumatica|hidraulica|solenoide|bloqueio|retencao|reguladora|3/2|5/2|5/3|4/2|4/3)|circuito.{0,20}(pneumatico|hidraulico|eletropneumatico)|atuador.{0,20}(pneumatico|hidraulico)|cilindro.{0,20}(pneumatico|hidraulico)|simbologia.{0,20}pneumatica|ar comprimido.{0,30}(pressao|valvula|cilindro)'),
    ('CYLINDER_FORCE', 'FLUID_POWER', 'FLUID_POWER', 'H01', 90, 'ANCHOR_STRONG', r'cilindro.{0,180}forca|forca.{0,70}cilindro'),
    ('VALVE_RETENTION', 'FLUID_POWER', 'FLUID_POWER', 'H01', 85, 'ANCHOR_STRONG', r'valvulas.{0,100}retorno de agua|valvula.{0,25}retencao'),
    ('ELECTROPNEUMATIC_SEQUENCE', 'ELECTROPNEUMATICS', 'FLUID_POWER', 'H02', 80, 'ANCHOR_STRONG', r'eletropneumat|sequencia.{0,40}cilindro'),
    ('SUBSTATION_AUXILIARY_POWER', 'SUBSTATIONS', 'POWER_NETWORKS', 'R02', 90, 'ANCHOR_STRONG', r'baterias vrla|bateria.{0,80}subestacao'),
    ('SUBSTATION_PROTECTION', 'SUBSTATIONS', 'POWER_NETWORKS', 'R02', 80, 'ANCHOR_STRONG', r'subestacao.{0,100}protecao|protecao.{0,70}media tensao'),
    ('SUBSTATION_OPERATION', 'SUBSTATIONS', 'POWER_NETWORKS', 'R02', 75, 'ANCHOR_STRONG', r'subestacao|chave seccionadora.{0,60}(alta tensao|media tensao|subestacao|blindad|abertura sob carga)|seccionadora.{0,60}(subestacao|linha de distribuicao)|patio de subestacao|bay de entrada'),
    ('DISTRIBUTION_CONNECTION', 'DISTRIBUTION_NETWORKS', 'POWER_NETWORKS', 'R01', 70, 'ANCHOR_STRONG', r'ponto de entrega|ponto de conexao|acesso ao sistema de distribuicao'),
    ('DISTRIBUTION_REGULATION', 'DISTRIBUTION_NETWORKS', 'POWER_NETWORKS', 'R01', 85, 'ANCHOR_STRONG', r'distribuidora de energia.{0,60}(unidade consumidora|religacao|restabelecer|prazos?)|regulacao.{0,40}distribuicao de energia'),
    ('DISTRIBUTION_TOPOLOGY', 'DISTRIBUTION_NETWORKS', 'POWER_NETWORKS', 'R01', 70, 'ANCHOR_STRONG', r'rede.{0,25}(radial|anel|distribuicao)|alimentador|rede aerea|poste.{0,25}(distribuicao|concessionaria|rede eletrica)|cruzeta|isolador de suspensao'),
    ('INDUSTRIAL_NETWORK', 'COMMUNICATION_NETWORKS', 'INDUSTRIAL_AUTOMATION', None, 92, 'ANCHOR_STRONG', r'redes? industriais?|profibus|modbus|fieldbus|devicenet|ethernet industrial|csma|token ring|padrao ethernet'),
    ('MATERIAL_PLASTICITY', 'MATERIALS_SCIENCE', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'deformar permanentemente|plasticidade'),
    ('DISTRIBUTION_REGULATORY_COST', 'REGULATORY_FRAMEWORK', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'\berd\b|musderd'),
    ('ANEEL_ADMINISTRATION', 'REGULATORY_FRAMEWORK', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'aneel.{0,130}(pautas|assessoria|diretoria)'),
    ('PUMP_MECHANICAL_FAULT', 'MECHANICAL_FAULTS', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'bomba.{0,40}desgastes.{0,30}(alhetas|rotor)'),
    ('HYDROELECTRIC_GENERATION', 'POWER_GENERATION', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'geracao hidreletrica|turbina hidraulica|kaplan|francis|pelton'),
    ('LORENTZ_FORCE', 'THEORETICAL_PHYSICS', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'eletron.{0,100}campo magnetico'),
    ('AUTOMOTIVE_STARTING', 'AUTOMOTIVE', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'motorista.{0,100}veiculo|veiculo automotor'),
    ('WELDING_TECHNOLOGY', 'WELDING', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'eletrodos? revestidos?|norma aws|soldagem|bisel|junta soldada'),
    ('HEAVY_MACHINERY_DIESEL', 'AUTOMOTIVE', 'OUTSIDE_CURRICULUM', None, 85, 'ANCHOR_STRONG', r'maquina pesada.{0,40}motor a diesel|motor a diesel.{0,40}maquina pesada'),
]

FAMILY_MAP = {c: f for c, f, p, m, sp, ac, pat in DEFINITIONS}

def classify(record, options, image_observation=''):
    s = norm(record.get('statement'))
    meta = norm(' '.join(record.get('current_subthemes', [])))
    prior = norm(' '.join(t['title'] for t in record.get('prior_topics', [])))
    opt = norm(' '.join(a.get('texto', '') for a in options))
    obs = norm(image_observation)

    signals = []
    for name, fam, parent, module, specificity, anchor_class, p in DEFINITIONS:
        stmt_match = has(p, s)
        obs_match = bool(obs and has(p, obs))
        meta_match = has(p, meta)
        opt_match = has(p, opt)

        if not (stmt_match or obs_match or meta_match):
            continue

        tier = 'A_EXPLICIT_CONCEPT' if stmt_match or obs_match else 'B_ORIGINAL_SUBJECT'
        score = (100 if stmt_match or obs_match else 30) + specificity
        if meta_match:
            score += 8
        if has(p, prior):
            score += 3
        if opt_match:
            score += 2

        signals.append({
            'concept': name,
            'semantic_family': fam,
            'parent': parent,
            'module': module,
            'specificity': specificity,
            'anchor_class': anchor_class,
            'tier': tier,
            'score': score,
            'evidence': {
                'statement': stmt_match,
                'image_observation': obs_match,
                'original_subject': meta_match,
                'prior_topic': has(p, prior),
                'options_support': opt_match
            },
            'excerpt': (re.search(p, s).group() if stmt_match else re.search(p, obs).group() if obs_match else re.search(p, meta).group())
        })

    names = {a['concept'] for a in signals}

    def suppress(concepts):
        nonlocal signals
        signals = [a for a in signals if a['concept'] not in concepts]

    # Domain Guardrails and Precedence Rules V2.2
    
    # Soft starter and electronic drives beat generic CC/CA and generic power
    if names & {'SOFT_STARTER', 'FREQUENCY_DRIVE'}:
        suppress({'DC_AC_DIFFERENCE', 'ELECTRICAL_POWER', 'SUBSTATION_OPERATION'})

    # Resistor networks beat generic DC/AC subthemes
    if names & {'PARALLEL_EQUIVALENT_RESISTANCE', 'SERIES_EQUIVALENT_RESISTANCE', 'MIXED_EQUIVALENT_RESISTANCE', 'RESISTOR_ASSOCIATION', 'WHEATSTONE_BRIDGE'}:
        suppress({'DC_AC_DIFFERENCE'})

    # Transformer feeding load beats auxiliary Ohm's law calculation
    if names & {'TRANSFORMER_REFLECTED_IMPEDANCE', 'TRANSFORMER_RATIO', 'TRANSFORMER_THREE_PHASE'} and not has(r'megometro|megohmetro|resistencia de isolamento|transformador de corrente|transformador de potencial|\btc\b|\btp\b', s):
        suppress({'OHMS_LAW_RESISTANCE', 'OHMS_LAW_CURRENT', 'OHMS_LAW_VOLTAGE', 'OHMS_LAW', 'SUBSTATION_OPERATION'})

    # Machine safety (NR-12) or electrical safety beats substation operation
    if names & {'MACHINE_SAFETY_NR12', 'ELECTRICAL_SAFETY', 'EPI_EPC_SELECTION', 'INSULATING_GLOVES', 'WORKER_AUTHORIZATION', 'WORK_AT_HEIGHT', 'ELECTRICAL_SAFETY_MEASURES', 'LAB_FIRE_SAFETY'} or has(r'nr.{0,2}12|seguranca no trabalho em maquinas', s):
        suppress({'SUBSTATION_OPERATION', 'DISTRIBUTION_TOPOLOGY'})

    # Motor control and starting methods suppress substation operation
    if names & {'STAR_DELTA_START', 'DIRECT_START', 'SOFT_STARTER', 'FREQUENCY_DRIVE', 'COMPENSATOR_START', 'MOTOR_CONTROL', 'RELAY_OPERATION', 'TIMER_RELAY'}:
        suppress({'SUBSTATION_OPERATION'})

    # Audio electronics is recognized as outside curriculum and suppresses generic AC impedance
    if 'AUDIO_ELECTRONICS' in names or has(r'amplificador de audio|caixa acustica|alto.falante', s):
        suppress({'REACTANCE_IMPEDANCE', 'ELECTRICAL_POWER'})

    # Circuit theory RC transient beats NR-10 stored energy discharge
    if 'RC_TRANSIENT' in names and not has(r'nr.{0,2}10|desenergiz|reenergiz|seguranca do trabalho|loto', s):
        suppress({'STORED_ENERGY_DISCHARGE'})

    if names & {'MOTOR_REVERSING', 'LOGIC_INTERLOCK', 'MOTOR_CONTROL', 'CONTACTOR_CONTROL', 'DIRECT_START', 'STAR_DELTA_START'}:
        suppress({'THREE_PHASE_POWER', 'THREE_PHASE_VOLTAGE', 'INDUCTION_MOTOR', 'ELECTRICAL_POWER'})

    if 'WHEATSTONE_BRIDGE' in names:
        suppress({'SERIES_EQUIVALENT_RESISTANCE', 'PARALLEL_EQUIVALENT_RESISTANCE', 'STRAIN_GAUGE', 'OHMS_LAW_RESISTANCE', 'MULTIMETER_VOLTAGE'})

    if names & {'INSULATION_TEST', 'CONTINUITY_TEST'} and 'FUSE_OPERATION' not in names:
        suppress({'TRANSFORMER_THEORY', 'TRANSFORMER_RATIO', 'INDUCTION_MOTOR', 'SYNCHRONOUS_MOTOR', 'MULTIMETER_FUNCTION', 'OVERCURRENT_PROTECTION'})

    if 'FUSE_OPERATION' in names:
        suppress({'CONTINUITY_TEST', 'OVERCURRENT_PROTECTION'})

    if names & {'POWER_FACTOR', 'POWER_FACTOR_CORRECTION'}:
        suppress({'INDUCTION_MOTOR', 'SYNCHRONOUS_SPEED', 'MOTOR_EFFICIENCY', 'CAPACITOR_STORAGE', 'ELECTRICAL_POWER'})

    if names & {'RESIDUAL_CURRENT_PROTECTION', 'RESIDUAL_EARTHING_COMPATIBILITY', 'INDIRECT_CONTACT_PROTECTION'}:
        suppress({'OVERCURRENT_PROTECTION', 'EARTHING_FUNCTION'})

    # Specific protection and conductor sizing concepts outrank generic NBR 5410
    if names & {'RESIDUAL_CURRENT_PROTECTION', 'RESIDUAL_EARTHING_COMPATIBILITY', 'INDIRECT_CONTACT_PROTECTION', 'EARTHING_SCHEME', 'EARTHING_ELECTRODE', 'SPDA', 'SURGE_PROTECTION', 'CONDUCTOR_AMPACITY', 'CONDUCTOR_SIZING', 'VOLTAGE_DROP', 'OVERCURRENT_PROTECTION'}:
        suppress({'NBR5410_INSTALLATIONS'})

    if names & {'EPI_EPC_SELECTION', 'INSULATING_GLOVES'}:
        suppress({'ELECTRICAL_LOCKOUT', 'RESIDUAL_CURRENT_PROTECTION', 'OVERCURRENT_PROTECTION', 'ELECTRICAL_SAFETY', 'MAINTENANCE_STRATEGY'})

    if 'NR10_DOCUMENTATION' in names:
        suppress({'SPDA', 'EARTHING_FUNCTION', 'ELECTRICAL_DIAGRAM_NOTATION', 'ELECTRICAL_SAFETY', 'FREQUENCY_PERIOD'})

    if 'THERMOGRAPHY' in names:
        suppress({'NR10_DEENERGIZATION', 'MAINTENANCE_STRATEGY'})

    if 'STORED_ENERGY_DISCHARGE' in names:
        suppress({'NR10_DEENERGIZATION', 'CAPACITOR_STORAGE', 'RECTIFIER_OPERATION'})

    if 'RC_TRANSIENT' in names:
        suppress({'SERIES_EQUIVALENT_RESISTANCE', 'CAPACITOR_STORAGE', 'OHMS_LAW_CURRENT'})

    if 'TRANSFORMER_THREE_PHASE' in names:
        suppress({'STAR_DELTA_START', 'THREE_PHASE_VOLTAGE'})

    if 'SEMICONDUCTOR_SWITCH' in names:
        suppress({'TRANSFORMER_THEORY', 'TRANSISTOR_OPERATION', 'RECTIFIER_OPERATION', 'CAPACITOR_STORAGE', 'PRESENCE_SENSOR', 'LEVEL_CONTROL'})

    if 'MOTOR_PROTECTION' in names:
        suppress({'INDUCTION_MOTOR', 'CONTACTOR_CONTROL', 'MOTOR_CONTROL', 'OVERCURRENT_PROTECTION'})

    if 'PROTECTION_CONDUCTOR_COORDINATION' in names:
        suppress({'CONDUCTOR_AMPACITY', 'CONDUCTOR_SIZING', 'OVERCURRENT_PROTECTION'})

    if names & {'PV_ENERGY', 'PV_ARRAY_POWER', 'PV_IV_CURVE'}:
        suppress({'ELECTRICAL_ENERGY', 'ELECTRICAL_POWER', 'SERIES_EQUIVALENT_RESISTANCE'})

    # CLP / Ladder dominates over electro-mechanical commands
    if names & {'PLC_CONTROL', 'PLC_LADDER', 'PLC_INTERNAL_RELAY', 'PLC_IO', 'PLC_SCAN', 'PLC_PROGRAMMING', 'CAUSE_EFFECT_LOGIC'}:
        suppress({'RELAY_OPERATION', 'CONTACTOR_CONTROL', 'MOTOR_CONTROL', 'FREQUENCY_PERIOD'})

    if names & {'PLC_IO', 'PLC_INTERNAL_RELAY', 'PLC_LADDER', 'PLC_SCAN', 'PLC_PROGRAMMING', 'CAUSE_EFFECT_LOGIC'}:
        suppress({'PLC_CONTROL'})

    # NR-10 / Safety dominates over incidental hardware and periods
    if names & {'NR10_DEENERGIZATION', 'NR10_REENERGIZATION', 'NR10_DOCUMENTATION', 'VOLTAGE_CLASSIFICATION', 'WORK_AT_HEIGHT', 'EPI_EPC_SELECTION', 'INSULATING_GLOVES', 'WORKER_AUTHORIZATION', 'ELECTRICAL_SAFETY', 'STORED_ENERGY_DISCHARGE', 'ELECTRICAL_LOCKOUT', 'ELECTRICAL_SAFETY_MEASURES', 'LAB_FIRE_SAFETY'}:
        if has(r'perigo|risco|crianca|escola|seguranca.{0,20}trabalho|nr.{0,2}10|choque', s):
            suppress({'LIGHTING_SWITCHING'})
        suppress({'FREQUENCY_PERIOD', 'DISTRIBUTION_TOPOLOGY', 'SUBSTATION_OPERATION'})

    if has(r'ergonom|nr.{0,3}17|nr.{0,3}35|trabalho.{0,20}altura|seguranca do trabalho|postura|membros superiores|queda de altura', s):
        suppress({'DISTRIBUTION_TOPOLOGY', 'SUBSTATION_OPERATION'})

    if 'SINGLE_PHASE_MOTOR_CAPACITOR' in names or has(r'motor monofasico.{0,60}capacitor|capacitor de partida', s):
        suppress({'CAPACITOR_STORAGE', 'ELECTRICAL_POWER'})

    if 'POWER_FACTOR_CORRECTION' in names or has(r'reduzir.{0,30}custos.{0,50}capacitor|cargas predominantes.{0,60}reduzir', s):
        suppress({'CAPACITOR_STORAGE', 'ELECTRICAL_POWER'})

    if 'OVERCURRENT_PROTECTION' in names and has(r'disjuntor.{0,40}quadro|principal funcao de um disjuntor', s):
        suppress({'DISTRIBUTION_BOARD'})

    if has(r'quadro de distribuicao|barramento.{0,20}neutro|qgbt|instalac(ao|oes) predia(l|is)|caixa de passagem', s):
        suppress({'SUBSTATION_OPERATION', 'SUBSTATION_PROTECTION'})

    if 'MOTOR_STARTING_COMPARISON' in names:
        suppress({'STAR_DELTA_START', 'DIRECT_START', 'SOFT_STARTER', 'FREQUENCY_DRIVE', 'COMPENSATOR_START'})

    if has(r'geracao hidreletrica|turbina hidraulica|kaplan|francis|pelton|saneamento|estacao elevatoria|reservatorio', s):
        suppress({'PNEUMATIC_VALVE', 'VALVE_RETENTION', 'CYLINDER_FORCE'})

    if names & {'OHMS_LAW_CURRENT', 'OHMS_LAW_RESISTANCE', 'OHMS_LAW_VOLTAGE', 'PARALLEL_EQUIVALENT_RESISTANCE', 'SERIES_EQUIVALENT_RESISTANCE', 'MIXED_EQUIVALENT_RESISTANCE', 'RESISTOR_ASSOCIATION'} and not has(r'potencia|watts|\bva\b|\bvar\b|\b\d+w\b|chuveiro|ventilador', s):
        suppress({'ELECTRICAL_POWER'})

    if 'ELECTRICAL_POWER' in names and has(r'chuveiro|ventilador|\b\d+w\b|potencia eletrica|lampada de \d+w', s):
        suppress({'OHMS_LAW_CURRENT', 'OHMS_LAW_VOLTAGE', 'OHMS_LAW_RESISTANCE', 'LIGHTING_SELECTION', 'OVERCURRENT_PROTECTION'})

    if 'AMPLIFIER_GAIN' in names:
        suppress({'ELECTRICAL_POWER'})

    if 'ELECTRICAL_POWER' in names and has(r'qual.{0,45}(potencia|potencia ativa|potencia aparente)|potencia eletrica (recebida|do)|valor da potencia', s):
        suppress({'OVERCURRENT_PROTECTION', 'LIGHTING_SELECTION', 'OHMS_LAW_CURRENT', 'OHMS_LAW_VOLTAGE', 'OHMS_LAW_RESISTANCE'})

    if names & {'MEASUREMENT_CONNECTION', 'MULTIMETER_VOLTAGE', 'MULTIMETER_CURRENT'}:
        suppress({'MULTIMETER_FUNCTION', 'LIGHTING_SELECTION', 'ELECTRICAL_QUANTITIES'})

    if has(r'valvula|hidraul|pneumat', s) and not has(r'nr.{0,3}10|desenergiz|reenergiz|ausencia de tensao', s):
        suppress({'ELECTRICAL_LOCKOUT', 'NR10_DEENERGIZATION', 'ELECTRICAL_SAFETY'})

    if 'LADDER_BOOLEAN' in names:
        suppress({'PLC_CONTROL', 'MOTOR_CONTROL'})

    if 'NUMBER_BASE_CONVERSION' in names:
        suppress({'PLC_CONTROL', 'PLC_IO'})

    if 'LOAD_ALLOCATION' in names:
        suppress({'CONDUCTOR_SIZING'})

    if 'CONDUCTOR_SIZING' in names and has(r'escolher a bitola', s):
        suppress({'CONDUCTOR_AMPACITY', 'VOLTAGE_DROP'})

    if 'OVERCURRENT_PROTECTION' in names and has(r'protecao de ramais', s):
        suppress({'DISTRIBUTION_TOPOLOGY'})

    signals.sort(key=lambda a: (-a['score'], a['concept']))
    primary = signals[0] if signals else None
    tied = bool(len(signals) > 1 and signals[0]['score'] == signals[1]['score'] and signals[0]['module'] != signals[1]['module'])

    concept = primary['concept'] if primary else None
    module = primary['module'] if primary else None
    family = primary['semantic_family'] if primary else None

    if concept is None and has(r'valor de r\d', s):
        concept = 'UNSPECIFIED_RESISTOR_CIRCUIT'
        family = 'RESISTOR_NETWORKS'

    # Related concepts derived from surviving signals
    related = []
    surviving_concepts = {a['concept'] for a in signals[1:]}
    for name, fam, p, m, sp, ac, pattern in DEFINITIONS:
        if name != concept:
            if name in surviving_concepts:
                rel = 'APPLICATION_CONTEXT' if p in ['COMMANDS', 'PROTECTION', 'MEASUREMENTS'] else 'CROSS_MODULE' if m != module and m is not None else 'SUPPORTING'
                related.append({'concept': name, 'semantic_family': fam, 'relationship': rel, 'module_candidate': m})
            elif has(pattern, s) and name not in names:
                related.append({'concept': name, 'semantic_family': fam, 'relationship': 'SUPPORTING', 'module_candidate': m})

    # Cross-module handling
    assignment_kind = 'SINGLE_MODULE'
    cross_candidates = []
    if concept == 'MOTOR_STARTING_COMPARISON':
        assignment_kind = 'CROSS_MODULE'
        module = None
        cross_candidates = ['E03', 'E04', 'E06']
    elif module is None and primary:
        assignment_kind = 'MISSING_MODULE' if primary['parent'] != 'OUTSIDE_CURRICULUM' else 'OUT_OF_CURRICULUM'

    # Secondary modules
    second = []
    secondary_rationale = []
    for cond, m, rat in [
        (concept == 'WHEATSTONE_BRIDGE', 'M01', 'Ponte é técnica de medição resistiva; reutilização no estudo de instrumentos.'),
        (concept == 'LOAD_DEMAND_CURRENT', 'F04', 'Requer converter potência das cargas em corrente.'),
        (concept == 'ELECTRICAL_POWER' and has(r'chuveiro|residencia|tomada', s), 'I01', 'Cálculo aplicado a cargas prediais.'),
        (concept == 'CURRENT_TRANSFORMER' and has(r'amperimetro', s), 'M01', 'Relaciona leitura do instrumento com transformação de corrente.'),
        (concept == 'RESIDUAL_EARTHING_COMPATIBILITY', 'P04', 'O esquema de aterramento determina a compatibilidade da proteção residual.'),
        (concept == 'LIGHTING_SWITCHING' and has(r'aterramento temporario', s), 'S01', 'Há uma proposição adicional sobre condições de desenergização em projeto.'),
        (concept == 'MOTOR_STARTING_COMPARISON', 'E03', 'Métodos de acionamento abrangem comandos diretos.'),
        (concept == 'MOTOR_STARTING_COMPARISON', 'E04', 'Métodos de acionamento abrangem partida estrela-triângulo e compensadora.'),
        (concept == 'MOTOR_STARTING_COMPARISON', 'E06', 'Métodos de acionamento abrangem soft-starter e inversores de frequência.')
    ]:
        if cond and m != module and m not in second:
            second.append(m)
            secondary_rationale.append({'module': m, 'rationale': rat})

    # IMAGE HANDLING
    has_img = bool(record.get('has_image'))
    img_status = record.get('image_status', 'IMAGE_OPTIONAL')

    visual_ref = has(r'\bfigura\b|diagrama acima|trata.se de um circuito|valor de r\d|tipo de transistor|entre os pontos|transistor apresentado|matriz de causa e efeito|tensao entre os terminais do resistor r\d|componente.{0,45}representado em|circuito ilustrado|grafico acima|forma de onda apresentada', s)
    placeholder_opts = bool(options) and all(norm(a.get('texto')) == norm(a.get('letra')) for a in options)
    text_depends_on_image = visual_ref or placeholder_opts or concept == 'UNSPECIFIED_RESISTOR_CIRCUIT'

    image_essential = (img_status == 'IMAGE_ESSENTIAL') or (has_img and text_depends_on_image) or (concept == 'UNSPECIFIED_RESISTOR_CIRCUIT')
    visual_classification_required = image_essential or (img_status == 'IMAGE_MISSING' and text_depends_on_image)
    image_unseen = visual_classification_required and not obs

    # Visual kind classification
    visual_kind = None
    if has_img:
        if has(r'grafico|curva|tela.{0,20}osciloscopio', s):
            visual_kind = 'GRAPH'
        elif has(r'tabela|quadro\b', s):
            visual_kind = 'TABLE'
        elif has(r'unifilar|multifilar|ladder|esquema|diagrama|circuito', s):
            visual_kind = 'SCHEMATIC'
        elif has(r'simbolo|simbologia', s):
            visual_kind = 'SYMBOL'
        elif has(r'display|mostrador|escala.{0,20}multimetro', s):
            visual_kind = 'INSTRUMENT_DISPLAY'
        elif has(r'foto|fotografia|aparencia', s):
            visual_kind = 'PHOTO'
        else:
            visual_kind = 'DIAGRAM'

    # CALIBRATED CONFIDENCE
    if not primary:
        confidence = 'UNCLASSIFIED'
    elif img_status == 'IMAGE_MISSING' and text_depends_on_image:
        confidence = 'LOW'
    elif image_unseen or tied:
        confidence = 'LOW' if tied else 'MEDIUM'
    elif primary['tier'] == 'A_EXPLICIT_CONCEPT':
        if primary['anchor_class'] == 'ANCHOR_STRONG' and primary['specificity'] >= 70:
            confidence = 'HIGH'
        elif primary['anchor_class'] == 'ANCHOR_CONTEXTUAL' and (primary['evidence']['original_subject'] or primary['evidence']['options_support']):
            confidence = 'HIGH'
        elif primary['anchor_class'] == 'TOKEN_GENERIC':
            confidence = 'MEDIUM'
        else:
            confidence = 'MEDIUM'
    elif primary['tier'] == 'B_ORIGINAL_SUBJECT':
        confidence = 'MEDIUM' if primary['anchor_class'] in ['ANCHOR_STRONG', 'ANCHOR_CONTEXTUAL'] else 'LOW'
    else:
        confidence = 'LOW'

    reason = None
    if not module:
        if concept == 'MOTOR_STARTING_COMPARISON':
            reason = 'CROSS_MODULE'
        elif primary and primary['parent'] == 'OUTSIDE_CURRICULUM':
            reason = 'OUT_OF_CURRICULUM'
        elif primary:
            reason = 'MISSING_MODULE'
        elif visual_classification_required:
            reason = 'IMAGE_REQUIRED'
        elif len(s) < 80:
            reason = 'INSUFFICIENT_CONTEXT'
        else:
            reason = 'CLASSIFIER_GAP'

    types = []
    tf = len(options) == 2 and {norm(a.get('texto')) for a in options} in [{'certo', 'errado'}, {'verdadeiro', 'falso'}]
    multi = has(r'assertiv|proposic|afirmativas|afirmacoes|\bi[.)\s].{0,350}\bii[.)\s]|\( \).{0,100}\( \)', s)
    if tf:
        types.append('TRUE_FALSE')
    if multi:
        types.append('MULTIPLE_PROPOSITIONS')

    quantity_question = has(r'calcule|calcular|calculo|determine|valor.{0,50}(corrente|tensao|resistencia|potencia|torque|capacitancia|escorregamento)|numero de (espiras|polos)|corrente total|correntes i\d|resistencia equivalente|qual.{0,30}potencia|quanto.{0,40}(corrente|tensao)|equivalente na base|simplificacao.{0,40}expressao|equivale a|tensao.{0,40}vale|conjugado.{0,30}reduzido', s)
    numeric = bool(re.search(r'\d', s))
    compute_family = concept in [
        'LOAD_DEMAND_CURRENT', 'SYNCHRONOUS_SPEED', 'STAR_DELTA_IMPEDANCE', 'VOLTAGE_DROP', 'ULTRASONIC_LEVEL',
        'AMPLIFIER_GAIN', 'LORENTZ_FORCE', 'WHEATSTONE_BRIDGE', 'MOTOR_SLIP', 'TRANSFORMER_RATIO', 'CURRENT_TRANSFORMER',
        'PV_ARRAY_POWER', 'ELECTRICAL_POWER', 'THREE_PHASE_VOLTAGE', 'MOTOR_PROTECTION', 'PROTECTION_CONDUCTOR_COORDINATION',
        'TRANSFORMER_THREE_PHASE', 'TRANSFORMER_REFLECTED_IMPEDANCE', 'DC_MACHINE_TORQUE', 'SYNCHRONOUS_MACHINE_EMF', 'LOAD_ALLOCATION', 'NUMBER_BASE_CONVERSION',
        'CYLINDER_FORCE'
    ]
    calculate = not tf and (
        (quantity_question and numeric and concept != 'MEASUREMENT_CONNECTION') or
        (compute_family and numeric) or
        (concept == 'ELECTRICAL_UNITS' and has(r'condutancia.{0,80}unidades de base', s)) or
        (concept == 'BOOLEAN_ALGEBRA' and has(r'simplificacao.{0,80}expressao', s)) or
        (concept == 'STAR_DELTA_START' and has(r'conjugado.{0,50}reduzido', s)) or
        (concept == 'UNSPECIFIED_RESISTOR_CIRCUIT')
    )
    if calculate and not (multi and not has(r'calcule|calcular|determine', s)):
        types.append('CALCULATION')

    if visual_kind in ['SCHEMATIC', 'DIAGRAM'] or has(r'diagrama|esquema|circuito unifilar|circuito multifilar|linguagem ladder', s):
        types.append('DIAGRAM')
    if visual_kind == 'GRAPH' or has(r'grafico|curva iv|tela.{0,20}osciloscopio|formas de onda', s):
        types.append('GRAPH')

    sequence = has(r'ordem correta de procedimentos|sequencia.{0,40}(executad|procedimento)|ciclo.{0,20}varredura', s)
    procedure = sequence or (concept in ['NR10_DEENERGIZATION', 'STORED_ENERGY_DISCHARGE'] and has(r'antes|ordem|pratica|procedimento|descarregar', s))
    if procedure:
        types.append('PROCEDURE')
    if has(r'\bnr.{0,3}\d|\bnbr\b', s):
        types.append('SAFETY_NORM')
    if concept in ['TRANSISTOR_IDENTIFICATION', 'ELECTRICAL_COMPONENT_SYMBOL'] or has(r'componente.{0,30}representado|nomes desses componentes', s):
        types.append('COMPONENT_IDENTIFICATION')
    if 'LADDER' in (concept or '') or has(r'ladder', s):
        types.append('LADDER_LOGIC')
    if primary and primary['parent'] in ['MEASUREMENTS', 'MULTIMETER', 'INDIRECT_MEASUREMENT', 'INSULATION']:
        types.append('MEASUREMENT')
    if not set(types) & {'CALCULATION', 'TRUE_FALSE', 'MULTIPLE_PROPOSITIONS', 'PROCEDURE'}:
        types.append('CONCEPTUAL')

    criteria = {
        'requires_formula_selection': 'CALCULATION' in types,
        'requires_data_extraction': image_essential and 'CALCULATION' in types,
        'requires_unit_conversion': bool('CALCULATION' in types and has(r'\b(kwh|kw|cv|hp|ma|mh|ms|μf|uf)\b', s)),
        'requires_multi_step_reasoning': concept in ['WHEATSTONE_BRIDGE', 'RLC_PHASOR', 'POWER_FACTOR_CORRECTION', 'MIXED_EQUIVALENT_RESISTANCE', 'TRANSFORMER_RATIO', 'LOAD_DEMAND_CURRENT', 'PV_ARRAY_POWER', 'TRANSFORMER_REFLECTED_IMPEDANCE'],
        'has_diagram_reasoning': bool(image_essential and visual_kind in ['SCHEMATIC', 'DIAGRAM', 'GRAPH']),
        'contains_multiple_propositions': multi,
        'requires_sequence': sequence,
        'requires_fault_diagnosis': concept in ['FAULT_DIAGNOSIS', 'THERMOGRAPHY']
    }
    richness = sum(criteria.values())
    potential = 'HIGH' if richness >= 3 or (multi and image_essential and visual_kind in ['SCHEMATIC', 'DIAGRAM']) else 'MEDIUM' if richness >= 1 or tf else 'LOW' if concept else 'NONE'

    formats = []
    if 'CALCULATION' in types:
        formats += ['STEP_BY_STEP_CALCULATION'] if potential == 'HIGH' else ['FORMULA_SELECTION']
    if tf or multi:
        formats += ['TRUE_FALSE_REASONING', 'ERROR_LOCALIZATION']
    if image_essential and visual_kind in ['SCHEMATIC', 'DIAGRAM']:
        formats += ['DIAGRAM_CLICK']
    if sequence:
        formats += ['SEQUENCE_ORDERING']
    if 'COMPONENT_IDENTIFICATION' in types:
        formats += ['COMPONENT_SELECTION']
    if criteria['requires_fault_diagnosis']:
        formats += ['FAULT_DIAGNOSIS']
    if criteria['requires_unit_conversion']:
        formats += ['UNIT_SELECTION']

    priority = (
        'P0' if record.get('image_status') == 'IMAGE_MISSING' or not record.get('text_available', True) or record.get('alternatives_count', 4) < 2 or 'SAFETY_NORM' in types
        else 'P1' if tied or image_unseen or potential == 'HIGH' or reason in ['CLASSIFIER_GAP', 'IMAGE_REQUIRED', 'MISSING_MODULE']
        else 'P2' if confidence in ['MEDIUM', 'LOW', 'UNCLASSIFIED']
        else 'P3'
    )

    family_status = (
        'REVIEWED_IMAGE_CONTEXT' if obs
        else 'PRELIMINARY_REQUIRES_IMAGE' if image_unseen
        else 'PRELIMINARY_TECHNICAL_FRAME' if concept
        else 'UNASSIGNED'
    )

    return {
        'primary_concept': concept,
        'related_concepts': related,
        'primary_module': module,
        'secondary_modules': second,
        'secondary_module_rationales': secondary_rationale,
        'module_assignment_kind': assignment_kind,
        'cross_module_candidates': cross_candidates,
        'semantic_family': family,
        'secondary_families': [],
        'family_status': family_status,
        'theme_classification_confidence': confidence if module else 'UNCLASSIFIED',
        'concept_classification_confidence': confidence,
        'module_candidates': ([{'module': module, 'relevance': confidence, 'evidence': primary}] if module else []) + [{'module': m, 'relevance': 'MEDIUM', 'rationale': r['rationale']} for m, r in zip(second, secondary_rationale)],
        'classification_evidence': signals[:8],
        'unclassified_reason': reason,
        'thematic_tie': tied,
        'visual_kind': visual_kind,
        'visual_classification_required': visual_classification_required,
        'image_essential': image_essential,
        'probable_types': list(dict.fromkeys(types)),
        'probable_type': next(t for t in ['TRUE_FALSE', 'MULTIPLE_PROPOSITIONS', 'CALCULATION', 'PROCEDURE', 'DIAGRAM', 'CONCEPTUAL'] if t in types),
        'interaction_candidate': potential,
        'interaction_criteria': criteria,
        'interaction_formats': list(dict.fromkeys(formats)),
        'tf_level_candidate': ('TF_L5' if (tf or multi) and image_essential else 'TF_L4' if (tf or multi) and has(r'sempre|somente|apenas|qualquer|obrigatori', s) else 'TF_L3' if multi or (tf and len(s) > 200) else 'TF_L2' if tf else None),
        'inspection_priority': priority,
        'image_classification_basis': 'AGENT_VISUAL_OBSERVATION' if obs else 'TEXT_ONLY_NOT_VISUALLY_VERIFIED',
        'editorial_decision': 'INSPECT' if priority != 'P3' or not module else 'CANDIDATE_NOT_VALIDATED'
    }
