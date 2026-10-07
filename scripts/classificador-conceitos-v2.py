"""Conceitos declarativos e hierarquia contextual; não usa golden set na inferência."""
import re,unicodedata,html
def norm(s):return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFD',html.unescape(s or '').lower()) if unicodedata.category(c)!='Mn')).strip()
def has(p,s):return bool(re.search(p,s))
# concept, parent, curricular module (None means a documented gap), specificity,
# explicit technical frame. No rule for bare corrente/tensão/motor/trifásico.
DEFINITIONS=[
('MOTOR_REVERSING','MOTOR_CONTROL','E03',95,r'reversao|inversao.{0,15}(rotacao|sentido)|inver.{0,20}fases'),
('LOGIC_INTERLOCK','MOTOR_CONTROL','E03',85,r'intertravamento'),
('MOTOR_CONTROL','COMMANDS','E03',70,r'circuito.{0,35}comando|comando.{0,25}motor'),
('DIRECT_START','MOTOR_STARTING','E03',85,r'partida direta'),
('STAR_DELTA_START','MOTOR_STARTING','E04',100,r'(partida|acionamento|chave).{0,60}estrela.{0,3}triangulo|estrela.{0,3}triangulo.{0,60}(partida|acionamento)'),
('COMPENSATOR_START','MOTOR_STARTING','E04',90,r'partida compensadora|chave compensadora'),
('DAHLANDER','MOTORS','E05',95,r'dahlander'),
('FREQUENCY_DRIVE','MOTOR_DRIVES','E06',90,r'inversor.{0,25}frequencia'),
('SOFT_STARTER','MOTOR_DRIVES','E06',90,r'soft.{0,2}starter'),
('MOTOR_PROTECTION','PROTECTION','P02',92,r'(motor.{0,100}(rele termico|sobrecarga|protecao)|(sobrecarga|rele termico).{0,100}motor)'),
('MOTOR_LOCKED_ROTOR_TEST','MOTORS','E01',95,r'ensaio de rotor bloqueado|rotor bloqueado.{0,30}ensaio'),
('MOTOR_SLIP','MOTORS','E01',90,r'escorregamento|velocidade do motor.{0,180}velocidade (diminui|reduz)'),
('SYNCHRONOUS_SPEED','MOTORS','E01',80,r'(numero de polos|numero de.{0,5}polos|\d+ polos|rotacao nominal).{0,100}(frequencia|hz)|frequencia.{0,300}(polos|rotacao)|velocidade.{0,30}sincrona'),
('SYNCHRONOUS_MACHINE_EMF','MOTORS',None,95,r'reatancia sincrona|tensao induzida por fase'),
('MOTOR_EFFICIENCY','MOTORS','E01',90,r'(motor.{0,160}(eficiencia|rendimento)|(eficiencia|rendimento).{0,60}motor)'),
('INDUCTION_MOTOR','MOTORS','E01',50,r'assincron|motor.{0,15}inducao|gaiola de esquilo'),
('SYNCHRONOUS_MOTOR','MOTORS','E01',45,r'motor sincron'),
('DC_MACHINE_TORQUE','MOTORS',None,95,r'motor serie.{0,100}torque|motor.{0,20}corrente continua.{0,80}torque'),
('MOTOR_WINDING_CONNECTION','MOTORS','E02',70,r'fechamento.{0,25}motor|terminais.{0,60}(estrela|triangulo)|enrolamento.{0,40}(ligacao|estrela|triangulo)'),
('THREE_PHASE_VOLTAGE','AC_CIRCUITS','E02',75,r'tensao.{0,20}(linha|fase.fase)|tensao.{0,30}enrolamento|tensao.{0,40}carga.{0,50}submetida'),
('THREE_PHASE_POWER','ELECTRICAL_POWER','F04',70,r'(calcule|calcular|valor|determine|qual).{0,65}potencia.{0,90}trifas|trifas.{0,120}(potencia total|potencia ativa|potencia aparente)'),
('WHEATSTONE_BRIDGE','BRIDGE_CIRCUITS','F02',100,r'wheatstone|ponte.{0,20}equilibrio'),
('STRAIN_GAUGE','INDUSTRIAL_INSTRUMENTATION',None,90,r'extensometro|strain.gauge'),
('RESISTIVE_SENSOR','INDUSTRIAL_INSTRUMENTATION',None,85,r'pt.{0,2}100|termorresist|sensor.{0,30}resistiv'),
('THERMOCOUPLE','INDUSTRIAL_INSTRUMENTATION',None,80,r'termopar|termopares'),
('INSTRUMENTATION_TAGS','INDUSTRIAL_INSTRUMENTATION',None,90,r'\btic\b|identific.{0,20}sigla.{0,15}(pic|fic|lic)|padr.{0,15}isa'),
('INDUSTRIAL_TRANSMITTER','INDUSTRIAL_INSTRUMENTATION',None,80,r'transmissor.{0,40}sinais|transmissores|transdutor.{0,20}pressao'),
('ULTRASONIC_LEVEL','AUTOMATION_SENSORS','A03',95,r'nivel.{0,15}ultrasson|ultrasson.{0,30}nivel'),
('PRESENCE_SENSOR','AUTOMATION_SENSORS','A03',85,r'sensor.{0,20}presenca|circulacao de pessoas|detector.{0,15}movimento'),
('LEVEL_CONTROL','AUTOMATION_SENSORS','A03',75,r'controle de nivel|sensor de nivel'),
('FIRE_DETECTION','AUTOMATION_SENSORS','A03',85,r'alarme de incendio|detector.{0,15}(fumaca|chama)|detectores automaticos'),
('SEMICONDUCTOR_SWITCH','ANALOG_ELECTRONICS',None,92,r'transistor.{0,120}chave|chave.{0,80}transistor|chaveamento.{0,30}(transformador|corrente)|hfe.{0,10}sat'),
('TRANSISTOR_IDENTIFICATION','ANALOG_ELECTRONICS',None,88,r'tipo de transistor|transistor.{0,35}(do tipo|utilizado)'),
('TRANSISTOR_OPERATION','ANALOG_ELECTRONICS',None,75,r'transistor|\bbjt\b|\bfet\b|\bmosfet\b'),
('THYRISTOR_OPERATION','ANALOG_ELECTRONICS',None,86,r'tiristor|\bscr\b|\btriac\b'),
('RECTIFIER_OPERATION','ANALOG_ELECTRONICS',None,80,r'retificador|retifica.{0,30}(onda|tensao)|fonte.{0,35}(ac/dc|nao regulada)'),
('ACTIVE_FILTER','ANALOG_ELECTRONICS',None,85,r'filtro ativo|amplificador operacional|\bampop\b'),
('OSCILLATOR_FEEDBACK','ANALOG_ELECTRONICS',None,90,r'barkhausen|oscilacao espontan|oscilador.{0,15}realiment'),
('AMPLIFIER_GAIN','ANALOG_ELECTRONICS',None,80,r'ganho.{0,20}(potencia|db)|circuito eletronico.{0,160}ganho'),
('SEMICONDUCTOR_PHYSICS','ANALOG_ELECTRONICS',None,80,r'dopagem|portadores minoritarios|semicondutor|diodo'),
('PROTOBOARD','ANALOG_ELECTRONICS',None,80,r'protoboard'),
('INSULATION_TEST','INSULATION','M02',100,r'resistencia de isolamento|medicao.{0,20}isolacao|megohmetro|megometro|megomet|megometro|megometro'),
('CONTINUITY_TEST','MEASUREMENTS','M02',80,r'continuidade|condutores.{0,70}interligados'),
('MEASUREMENT_CONNECTION','MULTIMETER','M01',85,r'(medir|medicao|medida).{0,20}(tensao|corrente|resistencia).{0,120}(conect|terminais|serie|paralelo)|medidas.{0,70}colocado|deve ser.{0,20}colocado|instrumento.{0,70}colocado|procedimentos.{0,30}medir resistencias'),
('MULTIMETER_VOLTAGE','MULTIMETER','M01',72,r'(multimetro|voltimetro).{0,120}tensao|tensao.{0,120}(multimetro|voltimetro)'),
('MULTIMETER_CURRENT','MULTIMETER','M01',72,r'(amperimetro|multimetro).{0,100}corrente|corrente.{0,80}(amperimetro|multimetro)'),
('MULTIMETER_RESISTANCE','MULTIMETER','M01',72,r'ohmimetro|multimetro.{0,45}resistencia'),
('MULTIMETER_FUNCTION','MULTIMETER','M01',40,r'multimetro|amperimetro|voltimetro|alicate amper'),
('OSCILLOSCOPE_READING','MEASUREMENTS','M01',70,r'osciloscopio'),
('SPECTRUM_MEASUREMENT','MEASUREMENTS','M01',80,r'dominio da frequencia.{0,25}instrumento|instrumento.{0,100}dominio da frequencia'),
('CURRENT_TRANSFORMER','INDIRECT_MEASUREMENT','T02',90,r'transformador.{0,15}corrente|\bt\.?\s?c\.?\b.{0,30}secundario'),
('POTENTIAL_TRANSFORMER','INDIRECT_MEASUREMENT','T02',90,r'transformador.{0,15}potencial'),
('TRANSFORMER_THREE_PHASE','TRANSFORMERS','T01',85,r'transformador trifasico|transformador.{0,30}estrela'),
('TRANSFORMER_RATIO','TRANSFORMERS','T01',70,r'transformador.{0,130}(espiras|primario|secundario|relacao)|espiras.{0,80}transformador|relacao de transformacao'),
('TRANSFORMER_THEORY','TRANSFORMERS','T01',40,r'transformador'),
('NR10_REENERGIZATION','NR10','S01',95,r'reenergizacao|reenergizar'),
('STORED_ENERGY_DISCHARGE','NR10','S01',100,r'capacitor.{0,100}(descarreg|mantem tensao)|descarreg.{0,70}capacitor'),
('ELECTRICAL_LOCKOUT','NR10','S01',90,r'bloqueio.{0,70}(eletric|reenerg|tensao)|\bloto\b'),
('NR10_DEENERGIZATION','NR10','S01',80,r'desenergiz|ausencia de tensao|antes de iniciar.{0,80}manutencao.{0,80}isolar o circuito'),
('NR10_DOCUMENTATION','NR10','S03',92,r'prontuario|nr.{0,3}10.{0,1000}(75 kw|esquemas unifilares)'),
('VOLTAGE_CLASSIFICATION','NR10','S03',75,r'classificacao.{0,20}tensao|extra.baixa tensao|rede eletrica.{0,30}baixa tensao'),
('WORK_AT_HEIGHT','SAFETY','S02',85,r'trabalho.{0,25}altura|nr.{0,3}35|trabalhar no alto|queda.{0,20}altura'),
('EPI_EPC_SELECTION','SAFETY','S02',90,r'\bepis?\b|\bepcs?\b|protecao (individual|coletiva)|luvas isolantes'),
('WORKER_AUTHORIZATION','NR10','S02',75,r'(trabalhador|profissional).{0,50}(autoriz|habilit|qualific)|operacoes elementares'),
('WORKPLACE_ORGANIZATION','SAFETY','S02',65,r'organizacao.{0,50}ferramentas|ferramentas.{0,35}espalhadas'),
('ELECTRICAL_SAFETY','NR10','S02',30,r'nr.{0,3}10|seguranca.{0,30}eletric'),
('POWER_FACTOR_CORRECTION','POWER','F04',100,r'(capacitor|banco de capacitores).{0,140}(fator de potencia|energia reativa)|(fator de potencia).{0,150}(capacitor|corrigir|correcao)'),
('POWER_FACTOR','POWER','F04',90,r'fator de potencia'),
('ELECTRICAL_POWER','POWER','F04',65,r'(potencia (eletrica|recebida|fornecida)|qual.{0,25}potencia|valor.{0,25}potencia)|corrente total.{0,40}circuito|chuveiro.{0,100}valor da corrente'),
('ELECTRICAL_ENERGY','POWER','F04',65,r'energia.{0,30}(consumida|consumo)|\bkwh\b'),
('SOURCE_LOADING','RESISTOR_NETWORKS','F02',95,r'gerador de funcoes.{0,200}resistor|resistencia interna.{0,60}fonte'),
('KIRCHHOFF_KCL','KIRCHHOFF','F02',90,r'lei.{0,15}nos|kirchhoff.{0,35}corrente'),
('KIRCHHOFF_KVL','KIRCHHOFF','F02',90,r'lei.{0,15}malhas|kirchhoff.{0,35}tensao'),
('PARALLEL_EQUIVALENT_RESISTANCE','RESISTOR_NETWORKS','F02',65,r'associacao em paralelo|paralelo de.{0,20}resistores|resistores.{0,80}(ligados|conectados) em paralelo'),
('SERIES_EQUIVALENT_RESISTANCE','RESISTOR_NETWORKS','F02',65,r'associacao em serie|circuito (em )?serie|resistores.{0,55}(ligados|conectados) em serie'),
('MIXED_EQUIVALENT_RESISTANCE','RESISTOR_NETWORKS','F02',70,r'resistencia equivalente|associacao mista'),
('STAR_DELTA_IMPEDANCE','RESISTOR_NETWORKS','F02',92,r'circuito equivalente.{0,50}(delta|triangulo)|impedancias.{0,120}equivalente'),
('OHMS_LAW_CURRENT','OHMS_LAW','F02',65,r'(valor|calcule|determine|qual).{0,25}corrente|corrente.{0,40}(inalterada|manter)|manter.{0,15}corrente'),
('OHMS_LAW_RESISTANCE','OHMS_LAW','F02',65,r'(valor|calcule|determine|qual).{0,25}resistencia'),
('OHMS_LAW_VOLTAGE','OHMS_LAW','F02',65,r'(valor|calcule|determine|qual).{0,25}tensao|aumento de tensao'),
('OHMS_LAW','OHMS_LAW','F02',45,r'lei de ohm'),
('RESISTOR_COLOR_CODE','RESISTOR_NETWORKS','F02',85,r'resistor.{0,55}(cores|cor)|codigo de cores'),
('RC_TRANSIENT','AC_CIRCUITS','F03',95,r'constantes? de tempo|transitorio.{0,20}capac|circuito rc'),
('RLC_PHASOR','AC_CIRCUITS','F03',80,r'\brlc\b|fasor'),
('REACTANCE_IMPEDANCE','AC_CIRCUITS','F03',55,r'reatancia|impedancia'),
('FREQUENCY_PERIOD','AC_CIRCUITS','F03',55,r'frequencia|periodo|senoidal|forma.{0,3}de onda'),
('CAPACITOR_STORAGE','AC_CIRCUITS','F03',60,r'armazenar.{0,15}carga|capacitancia|capacitor'),
('INDUCTOR_STORAGE','AC_CIRCUITS','F03',60,r'indutor|indutancia'),
('ELECTRICAL_UNITS','FUNDAMENTALS','F01',65,r'unidade.{0,20}(medida|base)|sistema internacional|\bddp\b.{0,150}unidade'),
('SIGNIFICANT_FIGURES','FUNDAMENTALS','F01',90,r'algarismos significativos'),
('ELECTRICAL_QUANTITIES','FUNDAMENTALS','F01',25,r'grandeza eletrica|carga eletrica|diferenca de potencial'),
('LOAD_DEMAND_CURRENT','BUILDING_INSTALLATIONS','I01',90,r'levantamento de carga|corrente total demandada|demanda.{0,40}residencia'),
('LOAD_ALLOCATION','BUILDING_INSTALLATIONS','I01',80,r'potencia.{0,35}minima.{0,30}(atribuida|tomada)|previsao.{0,25}carga'),
('LIGHTING_CONTROL_PROTOCOL','BUILDING_INSTALLATIONS','I01',90,r'dmx512'),
('LIGHTING_SELECTION','BUILDING_INSTALLATIONS','I01',65,r'lampada|luminaria|iluminacao'),
('ELECTRICIAN_TOOLS','BUILDING_INSTALLATIONS','I01',65,r'ferramentas.{0,80}(alicate|eletricista)|alicate.{0,20}(universal|bico|corte)'),
('ELECTRICAL_CAD','ELECTRICAL_DRAWINGS','I03',80,r'\bcad\b|recursos de informatica.{0,90}instalacoes|software.{0,35}projeto eletrico'),
('ELECTRICAL_DIAGRAM_NOTATION','ELECTRICAL_DRAWINGS','I03',65,r'unifilar|multifilar|simbologia|paredes.{0,30}caixas'),
('ELECTRICAL_COMPONENT_SYMBOL','ELECTRICAL_DRAWINGS','I03',80,r'(simbolo|simbolos).{0,80}(representar|identificacao)|componente.{0,30}representado|componente.{0,40}representad'),
('WIRING_INFRASTRUCTURE','CONDUCTORS','P01',75,r'eletroduto|canaleta|rede embutida'),
('CONDUCTOR_CORRECTION','CONDUCTORS','P01',90,r'fatores de correcao|fator de correcao'),
('CONDUCTOR_AMPACITY','CONDUCTORS','P01',85,r'capacidade.{0,15}conducao|ampacidade'),
('CONDUCTOR_SIZING','CONDUCTORS','P01',60,r'dimensionamento.{0,25}(condutor|cabo)|bitola.{0,25}condutor|escolher a bitola'),
('CONDUCTOR_INSULATION','CONDUCTORS','P01',80,r'(material|materiais).{0,20}isolamento|isolacao.{0,30}(pvc|epr|xlpe)'),
('VOLTAGE_DROP','CONDUCTORS','P01',85,r'queda de tensao'),
('PROTECTION_CONDUCTOR_COORDINATION','OVERCURRENT_PROTECTION','P02',90,r'(disjuntor.{0,80}(epr|mm2)|\b(epr|mm2)\b.{0,100}disjuntor)'),
('OVERCURRENT_PROTECTION','PROTECTION','P02',55,r'disjuntor|fusivel|curto.{0,2}circuito|curtos.{0,2}circuitos|sobrecarga|protecao de ramais alimentadores'),
('FUSE_OPERATION','OVERCURRENT_PROTECTION','P02',95,r'fusivel.{0,50}descontinuidade|elo de fusao'),
('PROTECTION_SELECTIVITY','PROTECTION','P02',85,r'sele[tic]+ividade|seccione apenas o circuito defeituoso|circuito defeituoso.{0,60}demais circuitos'),
('RESIDUAL_EARTHING_COMPATIBILITY','RESIDUAL_PROTECTION','P03',95,r'diferencial.residual.{0,200}esquema de aterramento|esquema de aterramento.{0,200}diferencial.residual'),
('RESIDUAL_CURRENT_PROTECTION','RESIDUAL_PROTECTION','P03',80,r'diferencial.residual|dispositivos? dr|\bidr\b|\bddr\b|soma vetorial.{0,70}correntes'),
('LIGHTING_SWITCHING','LIGHTING_CONTROLS','I02',75,r'interruptor|lampada.{0,100}pontos de comando'),
('PHOTOELECTRIC_SWITCH','LIGHTING_CONTROLS','I02',85,r'fotocelula|rele.{0,15}foto'),
('EARTHING_SCHEME','EARTHING','P04',75,r'esquema.{0,20}aterramento|\btn.c.s\b|\btn.c\b|\btn.s\b'),
('EARTHING_ELECTRODE','EARTHING','P04',80,r'infraestrutura de aterramento|eletrodo de aterramento'),
('EARTHING_FUNCTION','EARTHING','P04',45,r'aterramento|equipotencial'),
('SPDA','ATMOSPHERIC_PROTECTION','P05',90,r'\bspda\b|sistema.{0,40}descargas atmosfericas'),
('SURGE_PROTECTION','ATMOSPHERIC_PROTECTION','P05',85,r'\bdps\b|para.raios|protecao contra surtos'),
('PV_IV_CURVE','PHOTOVOLTAICS','V01',90,r'curva iv|curva i.v|maxima potencia.{0,30}fotovolta'),
('PV_ARRAY_POWER','PHOTOVOLTAICS','V01',75,r'fotovoltaic|modulos.{0,30}wp'),
('PV_ENERGY','PHOTOVOLTAICS','V01',80,r'energia.{0,50}painel solar|painel solar.{0,120}energia'),
('RENEWABLE_SOURCES','PHOTOVOLTAICS','V01',65,r'energia renovave|energias renovave|fontes de energia renovave|fontes alternativas de energia'),
('THERMOGRAPHY','FAULT_DIAGNOSIS','D02',95,r'termograf|termovisor|ponto quente'),
('MAINTENANCE_STRATEGY','MAINTENANCE','D01',70,r'manutencao (preventiva|preditiva|corretiva)|chama.se manutencao|inspecoes sistematicas'),
('FAULT_DIAGNOSIS','FAULT_DIAGNOSIS','D02',55,r'localizacao de falhas|diagnostico.{0,20}falha|localizar.{0,15}defeito'),
('BOOLEAN_ALGEBRA','DIGITAL_LOGIC','A01',80,r'boole|karnaugh'),
('NUMBER_BASE_CONVERSION','DIGITAL_LOGIC','A01',85,r'base (decimal|octal)|hexadecimal|registrador.{0,300}(xor|and|or)'),
('LADDER_BOOLEAN','DIGITAL_LOGIC','A01',80,r'ladder.{0,120}funcao logica|funcao.{0,40}ladder'),
('LADDER_SEAL_IN','MOTOR_CONTROL','E03',95,r'contato.{0,20}selo|selo.{0,25}contato'),
('PLC_IO','PLC','A02',80,r'modulos de entrada|modulos.{0,20}saida|entradas.{0,20}saidas'),
('PLC_PROGRAMMING','PLC','A02',85,r'texto estruturado|linguagem.{0,20}\bst\b'),
('PLC_SCAN','PLC','A02',90,r'ciclo.{0,20}varredura'),
('SCADA_OPERATION','PLC','A02',75,r'supervisorio|\bscada\b'),
('CAUSE_EFFECT_LOGIC','PLC','A02',80,r'matriz de causa e efeito'),
('PLC_CONTROL','PLC','A02',45,r'controlador logico|\bclp\b'),
('AUTOMATION_ACTUATOR','PLC','A02',65,r'atuadores.{0,40}sistema de producao|atuador.{0,40}automatizado'),
('CONTACTOR_CONTROL','COMMANDS','E03',60,r'contator|comandos eletricos automaticos'),
('RELAY_OPERATION','COMMANDS','E03',65,r'rele|reles|chaves eletromecanicas'),
('PNEUMATIC_VALVE','FLUID_POWER','H01',65,r'valvula|pneumatic|hidraulic'),
('CYLINDER_FORCE','FLUID_POWER','H01',90,r'cilindro.{0,180}forca|forca.{0,70}cilindro'),
('VALVE_RETENTION','FLUID_POWER','H01',85,r'valvulas.{0,100}retorno de agua|valvula.{0,25}retencao'),
('ELECTROPNEUMATIC_SEQUENCE','FLUID_POWER','H02',80,r'eletropneumat|sequencia.{0,40}cilindro'),
('SUBSTATION_AUXILIARY_POWER','POWER_NETWORKS','R02',90,r'baterias vrla|bateria.{0,80}subestacao'),
('SUBSTATION_PROTECTION','POWER_NETWORKS','R02',80,r'subestacao.{0,100}protecao|protecao.{0,70}media tensao'),
('SUBSTATION_OPERATION','POWER_NETWORKS','R02',45,r'subestacao|barramento|seccionadora'),
('DISTRIBUTION_CONNECTION','POWER_NETWORKS','R01',70,r'ponto de entrega|ponto de conexao|acesso ao sistema de distribuicao'),
('DISTRIBUTION_TOPOLOGY','POWER_NETWORKS','R01',55,r'rede.{0,25}(radial|anel|distribuicao)|alimentador|poste'),
('INDUSTRIAL_NETWORK','AUTOMATION_COMMUNICATION',None,85,r'ethernet|csma|token ring|profibus|modbus'),
('MATERIAL_PLASTICITY','OUTSIDE_CURRICULUM',None,85,r'deformar permanentemente|plasticidade'),
('DISTRIBUTION_REGULATORY_COST','OUTSIDE_CURRICULUM',None,85,r'\berd\b|musderd'),
('ANEEL_ADMINISTRATION','OUTSIDE_CURRICULUM',None,85,r'aneel.{0,130}(pautas|assessoria|diretoria)'),
('PUMP_MECHANICAL_FAULT','OUTSIDE_CURRICULUM',None,85,r'bomba.{0,40}desgastes.{0,30}(alhetas|rotor)'),
('LORENTZ_FORCE','OUTSIDE_CURRICULUM',None,85,r'eletron.{0,100}campo magnetico'),
('AUTOMOTIVE_STARTING','OUTSIDE_CURRICULUM',None,85,r'motorista.{0,100}veiculo|veiculo automotor'),
]

def classify(record,options,image_observation=''):
    s=norm(record.get('statement'));meta=norm(' '.join(record['current_subthemes']));prior=norm(' '.join(t['title'] for t in record['prior_topics']));opt=norm(' '.join(a.get('texto','') for a in options));obs=norm(image_observation)
    signals=[]
    # Strong central concepts suppress common application-context distractors.
    for name,parent,module,specificity,p in DEFINITIONS:
        statement_match=has(p,s);image_match=bool(obs and has(p,obs));metadata_match=has(p,meta);option_match=has(p,opt)
        if not (statement_match or image_match or metadata_match):continue
        tier='A_EXPLICIT_CONCEPT' if statement_match or image_match else 'B_ORIGINAL_SUBJECT'
        score=(100 if statement_match or image_match else 30)+specificity
        if metadata_match:score+=8
        if has(p,prior):score+=3
        if option_match:score+=2
        signals.append({'concept':name,'parent':parent,'module':module,'specificity':specificity,'tier':tier,'score':score,'evidence':{'statement':statement_match,'image_observation':image_match,'original_subject':metadata_match,'prior_topic':has(p,prior),'options_support':option_match},'excerpt':(re.search(p,s).group() if statement_match else re.search(p,obs).group() if image_match else re.search(p,meta).group())})
    names={a['concept'] for a in signals}
    # Context is subordinate: diagrams of power circuitry are not power calculations.
    def suppress(concepts):
        nonlocal signals;signals=[a for a in signals if a['concept'] not in concepts]
    if names & {'MOTOR_REVERSING','LOGIC_INTERLOCK','MOTOR_CONTROL','CONTACTOR_CONTROL','DIRECT_START','STAR_DELTA_START'}:suppress({'THREE_PHASE_POWER','THREE_PHASE_VOLTAGE','INDUCTION_MOTOR','ELECTRICAL_POWER'})
    if 'WHEATSTONE_BRIDGE' in names:suppress({'SERIES_EQUIVALENT_RESISTANCE','PARALLEL_EQUIVALENT_RESISTANCE','STRAIN_GAUGE','OHMS_LAW_RESISTANCE','MULTIMETER_VOLTAGE'})
    if names & {'INSULATION_TEST','CONTINUITY_TEST'} and 'FUSE_OPERATION' not in names:suppress({'TRANSFORMER_THEORY','TRANSFORMER_RATIO','INDUCTION_MOTOR','SYNCHRONOUS_MOTOR','MULTIMETER_FUNCTION','OVERCURRENT_PROTECTION'})
    if 'FUSE_OPERATION' in names:suppress({'CONTINUITY_TEST','OVERCURRENT_PROTECTION'})
    if names & {'POWER_FACTOR','POWER_FACTOR_CORRECTION'}:suppress({'INDUCTION_MOTOR','SYNCHRONOUS_SPEED','MOTOR_EFFICIENCY','CAPACITOR_STORAGE','ELECTRICAL_POWER'})
    if names & {'RESIDUAL_CURRENT_PROTECTION','RESIDUAL_EARTHING_COMPATIBILITY'}:suppress({'OVERCURRENT_PROTECTION','EARTHING_FUNCTION'})
    if 'EPI_EPC_SELECTION' in names:suppress({'ELECTRICAL_LOCKOUT','RESIDUAL_CURRENT_PROTECTION','OVERCURRENT_PROTECTION','ELECTRICAL_SAFETY'})
    if 'NR10_DOCUMENTATION' in names:suppress({'SPDA','EARTHING_FUNCTION','ELECTRICAL_DIAGRAM_NOTATION','ELECTRICAL_SAFETY'})
    if 'THERMOGRAPHY' in names:suppress({'NR10_DEENERGIZATION','MAINTENANCE_STRATEGY'})
    if 'STORED_ENERGY_DISCHARGE' in names:suppress({'NR10_DEENERGIZATION','CAPACITOR_STORAGE','RECTIFIER_OPERATION'})
    if 'RC_TRANSIENT' in names:suppress({'SERIES_EQUIVALENT_RESISTANCE','CAPACITOR_STORAGE','OHMS_LAW_CURRENT'})
    if 'TRANSFORMER_THREE_PHASE' in names:suppress({'STAR_DELTA_START','THREE_PHASE_VOLTAGE'})
    if 'SEMICONDUCTOR_SWITCH' in names:suppress({'TRANSFORMER_THEORY','TRANSISTOR_OPERATION','RECTIFIER_OPERATION','CAPACITOR_STORAGE','PRESENCE_SENSOR','LEVEL_CONTROL'})
    if 'MOTOR_PROTECTION' in names:suppress({'INDUCTION_MOTOR','CONTACTOR_CONTROL','MOTOR_CONTROL','OVERCURRENT_PROTECTION'})
    if 'PROTECTION_CONDUCTOR_COORDINATION' in names:suppress({'CONDUCTOR_AMPACITY','CONDUCTOR_SIZING','OVERCURRENT_PROTECTION'})
    if names & {'PV_ENERGY','PV_ARRAY_POWER','PV_IV_CURVE'}:suppress({'ELECTRICAL_ENERGY','ELECTRICAL_POWER','SERIES_EQUIVALENT_RESISTANCE'})
    if 'ELECTRICAL_POWER' in names and has(r'qual.{0,45}(corrente total|potencia)|potencia eletrica (recebida|do)|valor da potencia',s):suppress({'OVERCURRENT_PROTECTION','LIGHTING_SELECTION','OHMS_LAW_CURRENT','OHMS_LAW_VOLTAGE','OHMS_LAW_RESISTANCE'})
    if names & {'MEASUREMENT_CONNECTION','MULTIMETER_VOLTAGE','MULTIMETER_CURRENT'}:suppress({'MULTIMETER_FUNCTION','LIGHTING_SELECTION','ELECTRICAL_QUANTITIES'})
    if has(r'valvula|hidraul|pneumat',s) and not has(r'nr.{0,3}10|desenergiz|reenergiz|ausencia de tensao',s):suppress({'ELECTRICAL_LOCKOUT','NR10_DEENERGIZATION','ELECTRICAL_SAFETY'})
    if 'LADDER_BOOLEAN' in names:suppress({'PLC_CONTROL','MOTOR_CONTROL'})
    if 'NUMBER_BASE_CONVERSION' in names:suppress({'PLC_CONTROL','PLC_IO'})
    if 'LOAD_ALLOCATION' in names:suppress({'CONDUCTOR_SIZING'})
    if 'CONDUCTOR_SIZING' in names and has(r'escolher a bitola',s):suppress({'CONDUCTOR_AMPACITY','VOLTAGE_DROP'})
    if 'OVERCURRENT_PROTECTION' in names and has(r'protecao de ramais',s):suppress({'DISTRIBUTION_TOPOLOGY'})
    signals.sort(key=lambda a:(-a['score'],a['concept']))
    primary=signals[0] if signals else None
    tied=bool(len(signals)>1 and signals[0]['score']==signals[1]['score'] and signals[0]['module']!=signals[1]['module'])
    concept=primary['concept'] if primary else None;module=primary['module'] if primary else None
    if concept is None and has(r'valor de r\d',s):
        concept='UNSPECIFIED_RESISTOR_CIRCUIT'
    related=[]
    for name,p,m,sp,pattern in DEFINITIONS:
        if name!=concept and has(pattern,s):related.append({'concept':name,'relationship':'CONTEXT_OR_SUPPORT','module_candidate':m})
    # Reuse is explicit and narrow; incidental equipment never creates secondary modules.
    second=[];secondary_rationale=[]
    for condition,m,rationale in [
        (concept=='WHEATSTONE_BRIDGE','M01','Ponte é técnica de medição resistiva; reutilização no estudo de instrumentos.'),
        (concept=='LOAD_DEMAND_CURRENT','F04','Requer converter potência das cargas em corrente.'),
        (concept=='ELECTRICAL_POWER' and has(r'chuveiro|residencia|tomada',s),'I01','Cálculo aplicado a cargas prediais.'),
        (concept=='CURRENT_TRANSFORMER' and has(r'amperimetro',s),'M01','Relaciona leitura do instrumento com transformação de corrente.'),
        (concept=='RESIDUAL_EARTHING_COMPATIBILITY','P04','O esquema de aterramento determina a compatibilidade da proteção residual.'),
        (concept=='LIGHTING_SWITCHING' and has(r'aterramento temporario',s),'S01','Há uma proposição adicional sobre condições de desenergização em projeto.'),
    ]:
        if condition and m!=module:second.append(m);secondary_rationale.append({'module':m,'rationale':rationale})
    # A diagram mentioned as a concept (e.g. "o diagrama unifilar representa") is not a missing asset.
    visual_reference=has(r'\bfigura\b|diagrama acima|trata.se de um circuito|valor de r\d|tipo de transistor|entre os pontos|transistor apresentado|matriz de causa e efeito|tensao entre os terminais do resistor r\d|componente.{0,45}representado em',s)
    placeholder_options=bool(options) and all(norm(a.get('texto'))==norm(a.get('letra')) for a in options)
    essential=bool(record['has_image'] or visual_reference or placeholder_options or concept=='UNSPECIFIED_RESISTOR_CIRCUIT')
    image_unseen=essential and not obs
    confidence='HIGH' if primary and primary['tier']=='A_EXPLICIT_CONCEPT' and primary['specificity']>=60 and not tied and not image_unseen else 'MEDIUM' if primary and primary['tier']=='A_EXPLICIT_CONCEPT' and not tied else 'LOW' if primary else 'UNCLASSIFIED'
    reason=None
    if not module:
        reason='OUT_OF_CURRICULUM' if primary and primary['parent']=='OUTSIDE_CURRICULUM' else 'MISSING_MODULE' if primary else 'IMAGE_REQUIRED' if essential else 'INSUFFICIENT_CONTEXT' if len(s)<80 else 'CLASSIFIER_GAP'
    types=[]
    tf=len(options)==2 and {norm(a.get('texto')) for a in options} in [{'certo','errado'},{'verdadeiro','falso'}]
    multi=has(r'assertiv|proposic|afirmativas|afirmacoes|\bi[.)\s].{0,350}\bii[.)\s]|\( \).{0,100}\( \)',s)
    if tf:types.append('TRUE_FALSE')
    if multi:types.append('MULTIPLE_PROPOSITIONS')
    quantity_question=has(r'calcule|calcular|calculo|determine|valor.{0,50}(corrente|tensao|resistencia|potencia|torque|capacitancia|escorregamento)|numero de (espiras|polos)|corrente total|correntes i\d|resistencia equivalente|qual.{0,30}potencia|quanto.{0,40}(corrente|tensao)|equivalente na base|simplificacao.{0,40}expressao|equivale a|tensao.{0,40}vale|conjugado.{0,30}reduzido',s)
    numeric=bool(re.search(r'\d',s))
    compute_family=concept in ['LOAD_DEMAND_CURRENT','SYNCHRONOUS_SPEED','STAR_DELTA_IMPEDANCE','VOLTAGE_DROP','ULTRASONIC_LEVEL','AMPLIFIER_GAIN','LORENTZ_FORCE','WHEATSTONE_BRIDGE','MOTOR_SLIP','TRANSFORMER_RATIO','CURRENT_TRANSFORMER','PV_ARRAY_POWER','ELECTRICAL_POWER','THREE_PHASE_VOLTAGE','MOTOR_PROTECTION','PROTECTION_CONDUCTOR_COORDINATION','TRANSFORMER_THREE_PHASE','DC_MACHINE_TORQUE','SYNCHRONOUS_MACHINE_EMF','LOAD_ALLOCATION','NUMBER_BASE_CONVERSION','CYLINDER_FORCE']
    calculate=not tf and ((quantity_question and numeric and concept!='MEASUREMENT_CONNECTION') or compute_family and numeric or concept=='ELECTRICAL_UNITS' and has(r'condutancia.{0,80}unidades de base',s) or concept=='BOOLEAN_ALGEBRA' and has(r'simplificacao.{0,80}expressao',s) or concept=='STAR_DELTA_START' and has(r'conjugado.{0,50}reduzido',s) or concept=='UNSPECIFIED_RESISTOR_CIRCUIT')
    # Numeric values in normative propositions are not calculations by themselves.
    if calculate and not (multi and not has(r'calcule|calcular|determine',s)):types.append('CALCULATION')
    if essential or record['has_image']:types.append('DIAGRAM')
    if has(r'grafico|curva iv|tela.{0,20}osciloscopio|formas de onda',s):types.append('GRAPH')
    sequence=has(r'ordem correta de procedimentos|sequencia.{0,40}(executad|procedimento)|ciclo.{0,20}varredura',s)
    procedure=sequence or concept in ['NR10_DEENERGIZATION','STORED_ENERGY_DISCHARGE'] and has(r'antes|ordem|pratica|procedimento|descarregar',s)
    if procedure:types.append('PROCEDURE')
    if has(r'\bnr.{0,3}\d|\bnbr\b',s):types.append('SAFETY_NORM')
    if concept in ['TRANSISTOR_IDENTIFICATION','ELECTRICAL_COMPONENT_SYMBOL'] or has(r'componente.{0,30}representado|nomes desses componentes',s):types.append('COMPONENT_IDENTIFICATION')
    if 'LADDER' in (concept or '') or has(r'ladder',s):types.append('LADDER_LOGIC')
    if primary and primary['parent'] in ['MEASUREMENTS','MULTIMETER','INDIRECT_MEASUREMENT','INSULATION']:types.append('MEASUREMENT')
    if not set(types)&{'CALCULATION','TRUE_FALSE','MULTIPLE_PROPOSITIONS','PROCEDURE'}:types.append('CONCEPTUAL')
    criteria={'requires_formula_selection':'CALCULATION' in types,'requires_data_extraction':essential and 'CALCULATION' in types,'requires_unit_conversion':bool('CALCULATION' in types and has(r'\b(kwh|kw|cv|hp|ma|mh|ms|μf|uf)\b',s)),'requires_multi_step_reasoning':concept in ['WHEATSTONE_BRIDGE','RLC_PHASOR','POWER_FACTOR_CORRECTION','MIXED_EQUIVALENT_RESISTANCE','TRANSFORMER_RATIO','LOAD_DEMAND_CURRENT','PV_ARRAY_POWER'],'has_diagram_reasoning':essential,'contains_multiple_propositions':multi,'requires_sequence':sequence,'requires_fault_diagnosis':concept in ['FAULT_DIAGNOSIS','THERMOGRAPHY']}
    richness=sum(criteria.values());potential='HIGH' if richness>=3 or multi and essential else 'MEDIUM' if richness>=1 or tf else 'LOW' if concept else 'NONE'
    formats=[]
    if 'CALCULATION' in types:formats+=['STEP_BY_STEP_CALCULATION'] if potential=='HIGH' else ['FORMULA_SELECTION']
    if tf or multi:formats+=['TRUE_FALSE_REASONING','ERROR_LOCALIZATION']
    if essential:formats+=['DIAGRAM_CLICK']
    if sequence:formats+=['SEQUENCE_ORDERING']
    if 'COMPONENT_IDENTIFICATION' in types:formats+=['COMPONENT_SELECTION']
    if criteria['requires_fault_diagnosis']:formats+=['FAULT_DIAGNOSIS']
    if criteria['requires_unit_conversion']:formats+=['UNIT_SELECTION']
    priority='P0' if record['image_status']=='IMAGE_MISSING' or not record['text_available'] or record['alternatives_count']<2 or 'SAFETY_NORM' in types else 'P1' if tied or image_unseen or potential=='HIGH' or reason in ['CLASSIFIER_GAP','IMAGE_REQUIRED'] else 'P2' if confidence in ['MEDIUM','LOW','UNCLASSIFIED'] else 'P3'
    return {'primary_concept':concept,'related_concepts':related,'primary_module':module,'secondary_modules':second,'secondary_module_rationales':secondary_rationale,'semantic_family':concept,'secondary_families':[],'family_status':'REVIEWED_IMAGE_CONTEXT' if obs else 'PRELIMINARY_REQUIRES_IMAGE' if image_unseen else 'PRELIMINARY_TECHNICAL_FRAME' if concept else 'UNASSIGNED','theme_classification_confidence':confidence if module else 'UNCLASSIFIED','concept_classification_confidence':confidence,'module_candidates':([{'module':module,'relevance':confidence,'evidence':primary}] if module else [])+[{'module':m,'relevance':'MEDIUM','rationale':r['rationale']} for m,r in zip(second,secondary_rationale)],'classification_evidence':signals[:8],'unclassified_reason':reason,'thematic_tie':tied,'probable_types':list(dict.fromkeys(types)),'probable_type':next(t for t in ['TRUE_FALSE','MULTIPLE_PROPOSITIONS','CALCULATION','PROCEDURE','DIAGRAM','CONCEPTUAL'] if t in types),'interaction_candidate':potential,'interaction_criteria':criteria,'interaction_formats':list(dict.fromkeys(formats)),'tf_level_candidate':('TF_L5' if (tf or multi) and essential else 'TF_L4' if (tf or multi) and has(r'sempre|somente|apenas|qualquer|obrigatori',s) else 'TF_L3' if multi or tf and len(s)>200 else 'TF_L2' if tf else None),'inspection_priority':priority,'image_classification_basis':'AGENT_VISUAL_OBSERVATION' if obs else 'TEXT_ONLY_NOT_VISUALLY_VERIFIED','editorial_decision':'INSPECT' if priority!='P3' or not module else 'CANDIDATE_NOT_VALIDATED'}
