"""Anotações editoriais do agente após leitura dos 150 enunciados e alternativas.
Não chama o classificador, não copia previsões; não resolve alternativas.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/acervo-ampliado'
# index | expected module (- = no module) | central concept | question experience
# C conceptual; N calculation; T true/false; D diagram; P procedure; M propositions.
ANNOTATIONS='''
0 E03 MOTOR_REVERSING D
1 F02 WHEATSTONE_BRIDGE N,D
2 - TRANSISTOR_IDENTIFICATION D
3 E01 INDUCTION_MOTOR C
4 S01 NR10_DEENERGIZATION P
5 S01 NR10_DEENERGIZATION C
6 S01 STORED_ENERGY_DISCHARGE P
7 - MATERIAL_PLASTICITY C
8 S02 EPI_EPC_SELECTION C
9 S02 EPI_EPC_SELECTION C
10 S02 EPI_EPC_SELECTION M
11 S02 EPI_EPC_SELECTION C
12 F03 CAPACITOR_STORAGE C
13 F01 ELECTRICAL_UNITS N
14 I01 LOAD_DEMAND_CURRENT N
15 P01 WIRING_INFRASTRUCTURE C
16 M01 MULTIMETER_FUNCTION C
17 M01 MULTIMETER_CURRENT T
18 M01 MULTIMETER_VOLTAGE C
19 F02 SOURCE_LOADING T
20 F02 KIRCHHOFF_KVL C
21 F02 PARALLEL_EQUIVALENT_RESISTANCE N
22 M01 MEASUREMENT_CONNECTION D
23 F03 RC_TRANSIENT N
24 F02 STAR_DELTA_IMPEDANCE N
25 E01 SYNCHRONOUS_SPEED N
26 E01 SYNCHRONOUS_SPEED N
27 - SYNCHRONOUS_MACHINE_EMF N
28 F04 POWER_FACTOR C
29 F04 POWER_FACTOR_CORRECTION N
30 F04 ELECTRICAL_POWER N
31 I03 ELECTRICAL_CAD C
32 I03 ELECTRICAL_DIAGRAM_NOTATION C
33 - INSTRUMENTATION_TAGS C
34 I03 ELECTRICAL_DIAGRAM_NOTATION D
35 I03 ELECTRICAL_COMPONENT_SYMBOL D
36 S02 WORK_AT_HEIGHT C
37 E02 THREE_PHASE_VOLTAGE N
38 P02 OVERCURRENT_PROTECTION C
39 - DISTRIBUTION_REGULATORY_COST N
40 - INDUSTRIAL_TRANSMITTER C
41 A01 BOOLEAN_ALGEBRA C
42 A01 BOOLEAN_ALGEBRA N
43 A01 NUMBER_BASE_CONVERSION N
44 A01 LADDER_BOOLEAN D
45 E01 SYNCHRONOUS_SPEED N
46 E01 MOTOR_SLIP N
47 E01 MOTOR_SLIP C
48 E01 MOTOR_SLIP T
49 T01 TRANSFORMER_RATIO N
50 T01 TRANSFORMER_RATIO N
51 - SEMICONDUCTOR_SWITCH D,T
52 A02 AUTOMATION_ACTUATOR C
53 T02 CURRENT_TRANSFORMER N
54 T02 CURRENT_TRANSFORMER N
55 R02 SUBSTATION_AUXILIARY_POWER C
56 - PROTOBOARD C
57 R02 SUBSTATION_PROTECTION T
58 - INDUSTRIAL_NETWORK T
59 P01 VOLTAGE_DROP N
60 R01 DISTRIBUTION_CONNECTION C
61 I01 LIGHTING_SELECTION C
62 F04 ELECTRICAL_POWER N
63 I01 LIGHTING_CONTROL_PROTOCOL C
64 - ANEEL_ADMINISTRATION T
65 I01 LOAD_ALLOCATION N
66 P01 CONDUCTOR_AMPACITY C
67 P01 CONDUCTOR_CORRECTION C
68 P01 CONDUCTOR_SIZING M
69 P02 PROTECTION_CONDUCTOR_COORDINATION N
70 F04 ELECTRICAL_POWER N
71 P02 OVERCURRENT_PROTECTION C
72 P03 RESIDUAL_CURRENT_PROTECTION C
73 I02 LIGHTING_SWITCHING C
74 I02 LIGHTING_SWITCHING C
75 I03 ELECTRICAL_COMPONENT_SYMBOL C
76 I02 LIGHTING_SWITCHING M
77 P03 RESIDUAL_CURRENT_PROTECTION C
78 P03 RESIDUAL_CURRENT_PROTECTION C
79 P03 RESIDUAL_CURRENT_PROTECTION C
80 P03 RESIDUAL_EARTHING_COMPATIBILITY C
81 M02 CONTINUITY_TEST C
82 P02 FUSE_OPERATION C
83 M02 INSULATION_TEST T
84 S03 NR10_DOCUMENTATION C
85 V01 PV_ENERGY N
86 V01 PV_ARRAY_POWER N
87 V01 PV_IV_CURVE C
88 V01 RENEWABLE_SOURCES C
89 D02 THERMOGRAPHY C
90 D01 MAINTENANCE_STRATEGY C
91 M01 MEASUREMENT_CONNECTION C
92 D01 MAINTENANCE_STRATEGY C
93 D02 THERMOGRAPHY T
94 M01 MEASUREMENT_CONNECTION C
95 E01 MOTOR_LOCKED_ROTOR_TEST C
96 E02 THREE_PHASE_VOLTAGE N
97 P02 MOTOR_PROTECTION N
98 R01 DISTRIBUTION_CONNECTION C
99 E03 DIRECT_START C
100 E03 LOGIC_INTERLOCK D
101 P02 MOTOR_PROTECTION C
102 E03 RELAY_OPERATION C
103 A01 NUMBER_BASE_CONVERSION N
104 A02 PLC_IO T
105 A02 PLC_PROGRAMMING C
106 A02 SCADA_OPERATION C
107 E06 FREQUENCY_DRIVE C
108 E06 FREQUENCY_DRIVE C
109 E06 SOFT_STARTER C
110 E06 FREQUENCY_DRIVE C
111 E04 STAR_DELTA_START N
112 E04 STAR_DELTA_START C
113 E04 STAR_DELTA_START C
114 T01 TRANSFORMER_THREE_PHASE N
115 A03 PRESENCE_SENSOR C
116 A03 ULTRASONIC_LEVEL N
117 A03 FIRE_DETECTION C
118 - PUMP_MECHANICAL_FAULT C
119 E05 DAHLANDER T
120 P04 EARTHING_SCHEME C
121 P04 EARTHING_ELECTRODE C
122 P04 EARTHING_FUNCTION C
123 P01 CONDUCTOR_INSULATION C
124 P05 SURGE_PROTECTION T
125 P05 SPDA T
126 P05 SURGE_PROTECTION C
127 S03 NR10_DOCUMENTATION C
128 F03 INDUCTOR_STORAGE T
129 - TRANSISTOR_OPERATION C
130 - SEMICONDUCTOR_SWITCH M
131 - TRANSISTOR_IDENTIFICATION D
132 I01 ELECTRICIAN_TOOLS C
133 S02 WORKPLACE_ORGANIZATION T
134 - THYRISTOR_OPERATION C
135 - SEMICONDUCTOR_PHYSICS T
136 - RECTIFIER_OPERATION D,M
137 - DC_MACHINE_TORQUE N
138 - OSCILLATOR_FEEDBACK D
139 - UNSPECIFIED_RESISTOR_CIRCUIT D,N
140 - THYRISTOR_OPERATION C
141 - LORENTZ_FORCE N
142 - TRANSISTOR_OPERATION C
143 - ACTIVE_FILTER D
144 - AMPLIFIER_GAIN N
145 A02 CAUSE_EFFECT_LOGIC D
146 - AMPLIFIER_GAIN N
147 F01 SIGNIFICANT_FIGURES C
148 S01 NR10_DEENERGIZATION P
149 - SEMICONDUCTOR_SWITCH C
'''
TYPE={'C':'CONCEPTUAL','N':'CALCULATION','T':'TRUE_FALSE','D':'DIAGRAM','P':'PROCEDURE','M':'MULTIPLE_PROPOSITIONS'}
rows=json.loads((OUT/'amostra-classificacao-revisao.json').read_text(encoding='utf-8'))['questions'];gold=[]
for line in ANNOTATIONS.strip().splitlines():
 i,m,f,t=line.split();r=rows[int(i)];primary=None if m=='-' else m
 missing=f in ['TRANSISTOR_IDENTIFICATION','TRANSISTOR_OPERATION','SEMICONDUCTOR_SWITCH','INSTRUMENTATION_TAGS','INDUSTRIAL_TRANSMITTER','PROTOBOARD','INDUSTRIAL_NETWORK','SYNCHRONOUS_MACHINE_EMF','THYRISTOR_OPERATION','SEMICONDUCTOR_PHYSICS','RECTIFIER_OPERATION','DC_MACHINE_TORQUE','OSCILLATOR_FEEDBACK','ACTIVE_FILTER','AMPLIFIER_GAIN']
 reason='MISSING_MODULE' if not primary and missing else 'IMAGE_REQUIRED' if f=='UNSPECIFIED_RESISTOR_CIRCUIT' else 'OUT_OF_CURRICULUM' if not primary else None
 secondary={'Q4148977':['M01'],'Q3200234':['F04'],'Q3915223':['I01'],'Q2447327':['I01'],'Q3200229':['I01'],'Q1066325':['S01'],'Q533336':['P04'],'Q3976912':['M01']}.get(r['source_id'],[])
 note=f'O objeto da pergunta é {f}; a posição curricular esperada é {primary or reason}. Enunciado e todas as alternativas lidos; menções de contexto não justificam outros módulos por si só.'
 if int(i)==0:note='Imagem inspecionada: K1/K2 invertem fases, com contatos de selo e intertravamento; avaliar funcionamento/reversão, não calcular potência trifásica.'
 if int(i)==1:note='Imagem inspecionada: ponte de quatro braços, voltímetro entre pontos médios, extensômetro e condição de equilíbrio. F02 para cálculo de ponte; M01 como reutilização em medição.'
 if int(i)==2:note='Imagem inspecionada e opções lidas: identificar família do transistor. Não existe módulo de eletrônica de componentes na trilha de 35; reconhecer conceito, manter MISSING_MODULE.'
 if int(i)==3:note='Pergunta a máquina assíncrona; alternativas discriminam classes de máquinas. E01 cobre operação/velocidade de motor; corrente alternada é apenas contexto.'
 gold.append({'source_id':r['source_id'],'sample_stratum':r['stratum'],'expected':{'primary_module':primary,'secondary_modules':secondary,'primary_concept':f,'semantic_family':f,'probable_types':[TYPE[x] for x in t.split(',')],'unclassified_reason':reason},'review':{'reviewer':'AGENT_EDITORIAL','basis':'STATEMENT_AND_ALL_OPTIONS_PLUS_IMAGE' if int(i) in [0,1,2] else 'STATEMENT_AND_ALL_OPTIONS','rationale':note,'answer_resolved':False,'limitations':'Sem revisão humana independente; casos que referem imagens ausentes têm apenas classificação temática pelo texto, não interpretação técnica da figura.'}})
assert len(gold)==150 and len({r['source_id'] for r in gold})==150
# Complemento dirigido, também lido pelo agente, para cobrir H01/H02 após detectar lacuna na amostra inicial.
for sid,module,family,types,basis,rationale in [
 ('Q431574','H01','CYLINDER_FORCE',['CALCULATION'],'STATEMENT_AND_ALL_OPTIONS','Pede força de um cilindro pneumático em função de pressão e área; motor citado é o equipamento substituído.'),
 ('Q402437','H01','VALVE_RETENTION',['CONCEPTUAL'],'STATEMENT_AND_ALL_OPTIONS','Identifica válvula pela função de impedir retorno no circuito hidráulico; não se trata de bloqueio elétrico.'),
 ('Q4027618','H02','ELECTROPNEUMATIC_SEQUENCE',['DIAGRAM'],'STATEMENT_AND_ALL_OPTIONS_PLUS_IMAGE','Imagem inspecionada: comando elétrico energiza relé e solenoide de válvula 5/2 que atua em cilindro; condição de acionamento eletropneumático.')]:
 gold.append({'source_id':sid,'sample_stratum':'TARGETED_COVERAGE:'+module,'expected':{'primary_module':module,'secondary_modules':[],'primary_concept':family,'semantic_family':family,'probable_types':types,'unclassified_reason':None},'review':{'reviewer':'AGENT_EDITORIAL','basis':basis,'rationale':rationale,'answer_resolved':False,'limitations':'Revisão de classificação pelo agente; sem revisão humana independente.'}})
for r in gold:
 r['expected']['probable_type']=next(t for t in ['TRUE_FALSE','MULTIPLE_PROPOSITIONS','CALCULATION','PROCEDURE','DIAGRAM','CONCEPTUAL'] if t in r['expected']['probable_types'])
save={'version':1,'scope':'Referência editorial independente das previsões, mas usada no desenvolvimento V2; não é holdout nem certificação de precisão. Não copiar expectativas para o classificador.','selection_bias':'150 itens estratificados pela V1, curtos e majoritariamente sem imagem, mais três casos dirigidos de H01/H02; 153 itens com exemplos dos 35 módulos esperados, além de lacunas/fora do currículo. Amostra não probabilística.','questions':gold}
(OUT/'classification-golden-set.json').write_text(json.dumps(save,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('153 expectativas editoriais gravadas; nenhum gabarito resolvido.')
