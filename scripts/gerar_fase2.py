"""Mapa editorial rastreável; não inventa códigos da Matriz de Referência."""
from pathlib import Path
import json,re,csv,collections

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/fase2';OUT.mkdir(exist_ok=True)
# id | área | tema | subtema | pré-requisitos | atividade | livros
SPEC='''F01|Fundamentos|Circuitos CC/CA|Unidades e grandezas CC/CA||explicação e cálculo|013,015
F02|Fundamentos|Circuitos CC/CA|Lei de Ohm e associação de resistores|F01|cálculo passo a passo e circuito virtual|013
F03|Fundamentos|Circuitos CC/CA|Frequência, formas de onda e reatância|F01,F02|laboratório de formas de onda e cálculo|015
F04|Fundamentos|Energia e eficiência|Potência, energia e fator de potência|F01,F02,F03|cálculo e painel de cargas|011,015
M01|Medições|Instrumentos|Multímetro, alicate e seleção de escala|F01|instrumento virtual e diagnóstico|013,015
M02|Medições|Instrumentos|Continuidade e resistência de isolamento|M01,S01|multímetro e megômetro virtuais|007,058
S01|Segurança|Segurança em eletricidade|Desenergização e reenergização||sequência normativa e cenário de decisão|076
S02|Segurança|Segurança em eletricidade|Qualificação, EPI, altura e zonas de risco|S01|norma e análise de cenário|075,076
S03|Segurança|Segurança em eletricidade|Classificação de tensão e documentação|F01,S01|norma e leitura de prontuário|076
I01|Instalações|Instalações prediais|Tomadas, iluminação e previsão de cargas|F04,S01|planta interativa e cálculo|044,045,072
I02|Instalações|Instalações prediais|Interruptores, sensores e relé fotocélula|I01,M01|ligação em diagrama e diagnóstico|044,034
I03|Instalações|Projetos elétricos|Simbologia, unifilar, multifilar e CAD|F01|leitura de planta e desenho|049,072
P01|Proteção|Dimensionamento|Condutores, instalação e fatores de correção|F04,I01,S01|cálculo com tabela e comparação|045,071
P02|Proteção|Dimensionamento|Disjuntores, fusíveis, curvas e curto-circuito|P01|cálculo e leitura de curvas|042,043
P03|Proteção|Proteção de pessoas|DR, IDR, DDR e coordenação de funções|S01,I01|comparação de dispositivos e circuito|044,076
P04|Proteção|Aterramento e SPDA|Esquemas de aterramento e equipotencialização|S01,I03|diagrama interativo|044,076
P05|Proteção|Aterramento e SPDA|Captação, descida, aterramento e DPS|P04|identificação de subsistemas e norma|045,076
E01|Máquinas|Motores elétricos|Placa, potência, corrente e velocidade|F04,M01|placa interativa e cálculo|006,007
E02|Máquinas|Motores elétricos|Bobinas, fechamentos e ligação monofásica/trifásica|E01,M02|laboratório de terminais|006,007
E03|Máquinas|Comandos e partidas|Direta, reversão, selo e intertravamento|E02,P02|diagrama de força e comando|007,060
E04|Máquinas|Comandos e partidas|Estrela-triângulo e compensadora|E03|laboratório e escolha de componentes|007,006
E05|Máquinas|Comandos e partidas|Dahlander e duas velocidades|E03|diagrama e comparação de velocidades|007,006
E06|Máquinas|Acionamentos|Inversor, soft-starter e parametrização|E03,F03|painel virtual e diagnóstico|006
T01|Máquinas|Transformadores|Relação de transformação e proteções|F03,F04|cálculo e diagrama|037,015
T02|Potência|Medição e proteção em SEP|TC, TP, relés e medição indireta|T01,M01,S01|diagrama e cálculo|037,070
R01|Potência|Redes de distribuição|Estruturas, postes, alimentadores e topologias|I03,S02|leitura de estruturas e projeto|032,062
R02|Potência|Subestações|Equipamentos, barramentos e operação|R01,T02|diagrama unifilar e cenário|037,059,070
A01|Automação|CLP e lógica|Booleanos, binário, tabela verdade e Ladder|F01|lógica interativa|021,031
A02|Automação|CLP e lógica|Entradas, saídas e controle sequencial|A01,E03|laboratório de CLP|031,005
A03|Automação|Sensores|Sensores de presença, alarme e nível|A02,I02|seleção e diagrama|034,047
H01|Automação|Pneumática e hidráulica|Válvulas, atuadores e simbologia|I03|identificação de componentes|001,003
H02|Automação|Pneumática e hidráulica|Sequências, selo e diagnóstico eletropneumático|H01,E03,A01|laboratório de sequência|001,003
D01|Manutenção|Manutenção e diagnóstico|Preventiva, preditiva, corretiva e inspeções|S01|classificação de cenários e planejamento|055,058
D02|Manutenção|Manutenção e diagnóstico|Termografia, conexões e localização de falhas|D01,M02|diagnóstico visual|055,058
V01|Energia|Energia solar fotovoltaica|Arranjos, potência e eficiência|F04,P01|cálculo e arranjo virtual|011,070'''
subs=[]
for line in SPEC.splitlines():
    id,area,theme,name,pre,activity,books=line.split('|')
    subs.append({'id':id,'area':area,'tema':theme,'subtema':name,'pre_requisitos':pre.split(',') if pre else [],'atividade':activity,'livros':['livro-'+s for s in books.split(',')],'item_matriz_referencia':None,'matriz_status':'[VERIFICAR] matriz integral e currículo local não confirmados'})
index={x['id']:x for x in subs}
oldgroups={
'F01':'76953 77855 77410','F02':'76385 77764','F03':'77777','M01':'78272 77411 77686 77409','M02':'78454',
'S01':'78307 78432','S02':'76147','S03':'76652 77014','I03':'78294','P01':'77412 77862 77772 77683 78480','P04':'76980','P05':'77743',
'E03':'78437','E04':'76314 77817','E06':'77578 76352 77568 76121','E01':'77437','P02':'77736','T01':'77826','R01':'77825 77400 77408 77795 77534',
'A01':'78287 77858 76509 76885','A02':'76648 78273','D01':'76206','D02':'78348'}
assignment={'SAEP_'+id:sub for sub,ids in oldgroups.items() for id in ids.split()}
s26='S01 F02 V01 S02 V01 P05 I02 I03 R02 M01 M02 E06 A02 P05 A02 H01 V01 P03 I03 P01 P01 P01 M01 P05 F01 T01 R01 A01 E01 H01 P01 P03 A02 H02 F04 D02 D02 M01 A02 M01 R01'.split()
s22='S01 F04 F03 M02 T01 P02 M02 T02 H01 H01 M01 S01 E02 I01 R02 H01 E03 P02 D02 H02 R02 R02 M02 F02 F04 E06 I02 I03 I03 M01 I03 R02 S03 S03 S02 R02 R02 I02 P03 T02'.split()
c23='P03 E02 D01 S01 F04 E03 P05 E04 M01 F04 I01 A02 A01 A02 H02 F02 H02 P04 E06 A03 M02 H01 I02 P04 P02 M01 H02 M01 P05 S02 M01 P02 D01 E01 D02 T02 P01 P03 R02 E01 D02 T01 H02 A03 P02 E03 P02 I01 P02 P05 I02 P01 R01 S02 I02 H02 P01 S02 A03 R01 D01 S01 F01 I01 H02 D01 E03 H01 P05 E05 I03 H02 I01 M01 E06 E04 T02 A03 R02 I02'.split()
assert len(s26)==41 and len(s22)==40 and len(c23)==80
items=json.loads((OUT/'ocorrencias.json').read_text(encoding='utf-8'))
for x in items:
    if x['fonte']=='S26':sub=s26[x['ordem']-1]
    elif x['fonte']=='S22':sub=s22[x['ordem']-1]
    elif x['fonte']=='C23':sub=c23[x['ordem']-1]
    else:sub=assignment[x['id']]
    x['subtema_id']=sub
    if x.get('dificuldade_impressa'):
        weight={'Fácil':1,'Médio':2,'Difícil':3}[x['dificuldade_impressa']]; origin='rótulo impresso no simulado; não psicometria validada'
    else:
        # Estimativa transparente de esforço instrucional para ordenar a criação de conteúdo.
        type=x.get('tipo_principal','')
        weight=3 if type=='leitura de diagrama' or sub in ['E04','E05','E06','H02','P01','P02','R02','A02'] else 2 if type=='cálculo' or sub in ['F02','F03','F04','E01','T01','T02','V01'] else 1
        origin='estimativa editorial de esforço; sem respostas de alunos'
    x['dificuldade_peso']=weight;x['dificuldade_origem']=origin
    key=x['id'] if x['id'].startswith('SAEP_') else 'TEXTO:'+re.sub(r'\W+','',x['enunciado'].lower())
    if x['fonte']=='C23' and x['ordem'] in [3,61]:key='EDITORIAL:C23-3-61'
    x['grupo_deduplicacao']=key
groups=collections.defaultdict(list)
for x in items:groups[x['grupo_deduplicacao']].append(x)
assert len(items)==241 and len(groups)==206
for g,xs in groups.items():assert len({x['subtema_id'] for x in xs})==1,(g,xs)
books=json.loads((ROOT/'data/livros/inventario.json').read_text(encoding='utf-8'))['livros'];bookindex={b['id']:b for b in books}
for s in subs:
    matches=[x for x in items if x['subtema_id']==s['id']]
    gs={x['grupo_deduplicacao'] for x in matches}
    s['frequencia_por_documento']={f:sum(x['fonte']==f for x in matches) for f in ['A1','A2','S26','S22','C23']}
    s['ocorrencias']=len(matches);s['frequencia_distinta_conservadora']=len(gs)
    difficulty=[max(x['dificuldade_peso'] for x in groups[g]) for g in gs]
    s['dificuldade_media']=round(sum(difficulty)/len(difficulty),2) if difficulty else 0
    s['prioridade_frequencia_x_dificuldade']=sum(difficulty)
    s['prioridade_pedagogica']='obrigatória antes de laboratórios' if s['id'] in ['S01','S02'] else 'pré-requisito' if s['id'] in ['F01','F02','F03','F04','M01','I03'] else 'conforme escore'
    s['meta_questoes_originais']=max(8,min(24,4+2*len(gs)))
    s['meta_composicao']='Aproximadamente metade contextualizadas e metade por etapas; norma/diagnóstico usam decisões, sem cálculo artificial.'
    s['ocorrencias_refs']=[x['uid'] for x in matches]
    s['cruzamentos_impressos_s22']=sorted({x['cruzamento_impresso'] for x in matches if x.get('cruzamento_impresso')})
    s['fontes_livros']=[{'id':b,'nome':bookindex[b]['nome'],'origem':bookindex[b]['origem'],'sumario_paginas':bookindex[b]['sumario_paginas'],'status':'livro de apoio selecionado por assunto; capítulo e versão técnica serão conferidos ao produzir o módulo'} for b in s['livros']]
ordered=[];remaining=set(index)
while remaining:
    ready=[index[id] for id in remaining if set(index[id]['pre_requisitos'])<=set(ordered)]
    assert ready,'Ciclo de pré-requisitos'
    ready.sort(key=lambda x:(x['id'] not in ['S01','S02','F01','F02','F03','F04','M01'], -x['prioridade_frequencia_x_dificuldade'],x['id']))
    ordered.append(ready[0]['id']);remaining.remove(ready[0]['id'])
data={'data':'2026-10-02','metodo':'Classificação editorial manual de cada ocorrência, um subtema principal; prioridades sobre grupos conservadores; mapas oficiais ausentes não preenchidos.','documentos':{'A1':'avaliações.pdf','A2':'avaliações 2.pdf','S26':'SIMULADO 2026.pdf','S22':'simulado Eletrotécnica 2022.2','C23':'coleção Questões SAEP 2023 DOCX'},'ocorrencias':len(items),'grupos_distintos_conservadores':len(groups),'trilha':ordered,'subtemas':subs}
(OUT/'mapa-conteudo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'ocorrencias-classificadas.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'indice-deduplicado.json').write_text(json.dumps([{'grupo':g,'subtema_id':xs[0]['subtema_id'],'ocorrencias':[{'uid':x['uid'],'arquivo_dados':x['referencia'],'paginas':x.get('paginas',[])} for x in xs]} for g,xs in groups.items()],ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'matriz-cobertura.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f,delimiter=';');writer.writerow(['id','area','tema','subtema','A1','A2','S26','S22','C23','distintos','dificuldade','prioridade','meta_questoes'])
    for s in subs:writer.writerow([s['id'],s['area'],s['tema'],s['subtema'],*s['frequencia_por_documento'].values(),s['frequencia_distinta_conservadora'],s['dificuldade_media'],s['prioridade_frequencia_x_dificuldade'],s['meta_questoes_originais']])
lines=['# Fase 2 - Matriz de cobertura e prioridades','', 'As colunas contam ocorrências por documento. A coluna distintos elimina 33 IDs compartilhados A1/A2, a repetição 10/23 de S26 e a repetição 3/61 de C23. Mesma situação com comando ou alternativas diferentes permanece separada. Frequência nesta coleção não é probabilidade de cair na prova.','', '| ID | Área / tema / subtema | A1 | A2 | S26 | S22 | C23 | Distintos | Dificuldade média | F × D | Meta |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for s in subs:lines.append('| '+ ' | '.join(map(str,[s['id'],s['area']+' / '+s['tema']+' / '+s['subtema'],*s['frequencia_por_documento'].values(),s['frequencia_distinta_conservadora'],s['dificuldade_media'],s['prioridade_frequencia_x_dificuldade'],s['meta_questoes_originais']]))+' |')
lines+=['',f'Totais: 40 + 40 + 41 + 40 + 80 = 241 ocorrências; 206 grupos conservadores; {sum(s["meta_questoes_originais"] for s in subs)} questões originais planejadas, ainda não produzidas.','', 'A1/A2: avaliações sem ano confirmado; S26: simulado 2026; S22: simulado 2022.2; C23: coleção em DOCX, 2023 no nome. Dificuldade: pesos 1/2/3, rótulos impressos em S22 e estimativas editoriais nos demais. A prioridade soma o maior peso de cada grupo do subtema: frequência distinta × dificuldade média não arredondada. Não usa dificuldade de aluno ainda desconhecida.','', 'Taxonomia, pré-requisitos, tipos de atividade, fontes e cruzamentos impressos estão em `data/fase2/mapa-conteudo.json`. O campo item_matriz_referencia permanece null: [VERIFICAR]. Cada ocorrência tem classificação e origem em `ocorrencias-classificadas.json`.']
(ROOT/'docs/02-matriz-cobertura.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
lines=['# Fase 2 - Trilha de estudo e metas','', 'Ordem obtida dos pré-requisitos; entre conteúdos liberados, prioriza segurança, fundamentos e escore de frequência × dificuldade. Não há datas fixas porque disponibilidade e data da prova não foram informadas. Estude em blocos de 25 a 40 minutos e ajuste pelo desempenho.','', 'Cada subtema seguirá explicação curta → atividade → perguntas por etapas → revisão dos erros. Critério provisório de avanço: resolver 8 de 10 itens originais novos sem dica e explicar o raciocínio; segurança requer completar o procedimento do cenário sem pular etapas. Isso é meta pedagógica, não nota mínima oficial do SAEP.','', '| Ordem | Subtema | Pré-requisitos | Atividade principal | Questões originais | Livros de apoio |','|---:|---|---|---|---:|---|']
for i,id in enumerate(ordered,1):
    s=index[id];lines.append(f'| {i} | {id} - {s["subtema"]} | {", ".join(s["pre_requisitos"]) or "nenhum"} | {s["atividade"]} | {s["meta_questoes_originais"]} | '+ '; '.join(b['id']+' '+b['nome'].replace('.pdf','') for b in s['fontes_livros'])+' |')
lines+=['','## Revisão e uso das fontes','','Retome os erros na próxima sessão, depois em aproximadamente 3 e 7 dias; ajuste os intervalos após observar retenção. Ainda não é decisão do algoritmo da plataforma. Cálculos terão quatro alternativas em cada etapa conforme pedido; mini-simulados devem preservar o perfil de quatro ou cinco alternativas da fonte escolhida, sem misturá-los sem informar.','', 'Para cada meta, distribuir inicialmente cerca de metade em itens contextualizados e metade em etapas. Subtemas gráficos devem incluir diagramas próprios; normativos devem citar edição e trecho verificados. Metas não autorizam gerar ou publicar cópias de questões reais. Os cinco PDFs criados para upload no Scribd não foram contados como provas nem fontes de frequência.','', 'Livros estão identificados no inventário; páginas de sumário e caminhos constam no JSON. A seleção é de apoio, sem prometer revisão integral ou pertinência de todas as páginas. Valores de catálogo, normas e modelos de motores de 9/12 pontas precisam de conferência específica antes da implementação.','', 'O MVP de motores continua previsto para a Fase 4. Antes dele, inserir revisão curta de segurança, instrumentos, circuitos, placa e comandos. A trilha de estudo completa e a ordem de implementação do MVP são planos diferentes.']
(ROOT/'docs/02-trilha-estudo.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
checks={'ocorrencias':len(items),'grupos_conservadores':len(groups),'subtemas':len(subs),'soma_frequencias':sum(s['ocorrencias'] for s in subs),'soma_distintos':sum(s['frequencia_distinta_conservadora'] for s in subs),'sem_classificacao':[],'trilha_sem_ciclos':True,'metas_total':sum(s['meta_questoes_originais'] for s in subs),'todos_livros_referenciados_existem':all((ROOT/b['extracao']).exists() for b in books),'matriz_integral_confirmada':False}
(ROOT/'docs/verificacao-fase2.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False));print('TOP',[(s['id'],s['prioridade_frequencia_x_dificuldade']) for s in sorted(subs,key=lambda s:-s['prioridade_frequencia_x_dificuldade'])[:8]])
