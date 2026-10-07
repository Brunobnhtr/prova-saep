# Curriculum Editorial V1 — Fronteiras de Classificação

Base GitHub: `Brunobnhtr/prova-saep@3d9eeba0cee4dec8106b7eac3dae5221c7822b75`

Este documento é uma **autoria editorial para classificação**. `code`, `title` e `prerequisites` vêm do esqueleto source-derived; descrições, limites e exemplos foram redigidos editorialmente para reduzir ambiguidade entre módulos. Não substitui norma técnica vigente nem deve ser usado como instrução operacional de campo.

## Regras globais

- Classificar pela **competência necessária para resolver a questão**, não por palavra isolada.
- Termos genéricos como `corrente`, `frequência`, `bloqueio`, `potência`, `inversor`, `sensor` ou `diagrama` não bastam para decidir o módulo.
- Quando um conceito de outro módulo aparece apenas como dado intermediário, priorizar o objetivo final da questão.
- Se duas competências forem indispensáveis, definir uma primária pelo objetivo final e registrar a outra como overlap aceitável apenas durante a anotação.
- Questões dependentes de imagem sem referência válida devem permanecer marcadas como `IMAGE_REQUIRED`/`REFERENCE_MISSING`; não inferir conteúdo visual ausente.
- Módulos com `normative_review_required=true` exigem revisão normativa antes de transformar regras editoriais em conteúdo didático normativo.

## Fronteiras críticas de alta prioridade

- **F01 × F02:** Unidade/conversão e reconhecimento de grandeza → F01; relação V-I-R, resistores e resistência equivalente → F02.
- **F02 × F03:** Circuito resistivo/CC → F02; reatância, impedância, fase, RLC ou frequência alterando comportamento → F03.
- **F03 × F04:** Impedância/reatância/onda → F03; potência ativa/reativa/aparente, energia, FP ou rendimento → F04.
- **S01 × H01:** `bloqueio` só é S01 quando impede reenergização elétrica; válvula de bloqueio fluídica é H01.
- **S01 × S02 × S03:** Desenergização/reenergização → S01; pessoas/EPI/EPC/altura/zonas → S02; classe de tensão/documentação → S03.
- **M01 × M02:** Seleção/escala/leitura de instrumento → M01; continuidade e resistência de isolamento → M02.
- **I01 × I02 × I03:** Previsão de cargas/pontos → I01; comando de iluminação/sensores prediais → I02; representação/simbologia/CAD → I03.
- **P01 × P02 × P03:** Condutor/ampacidade/queda → P01; sobrecorrente/curto/disjuntor/fusível → P02; diferencial residual/DR → P03.
- **P04 × P05:** Esquemas de aterramento/equipotencialização → P04; SPDA/captação/descida/DPS/surtos → P05.
- **E01 × E02:** Placa/dados nominais → E01; bobinas/terminais/fechamento → E02.
- **E02 × E04:** Estrela/triângulo como fechamento permanente → E02; transição temporizada para partida → E04.
- **E03 × A01/A02:** Contatores/botoeiras e comando eletromecânico → E03; Ladder como lógica/CLP → A01/A02.
- **E05 × E06:** Duas velocidades por polos/Dahlander → E05; variação eletrônica por frequência → E06.
- **T01 × T02:** Transformador de potência/relação de espiras → T01; TC/TP/relés/medição indireta → T02.
- **R01 × R02:** Rede de distribuição e topologia externa → R01; equipamentos/barramentos/operação de subestação → R02.
- **A01 × A02 × A03:** Booleanos/Ladder elementar → A01; sequência de I/O/temporizadores → A02; escolha/princípio do sensor → A03.
- **H01 × H02:** Componente/símbolo fluídico → H01; sequência e diagnóstico eletropneumático → H02.
- **D01 × D02:** Estratégia/tipo de manutenção → D01; localizar causa/falha por sintomas/termografia/conexões → D02.
- **F04 × V01:** Potência/energia genérica → F04; arranjo, geração e eficiência fotovoltaica → V01.
- **E06 × V01:** Inversor de frequência de motor → E06; inversor fotovoltaico → V01.

## Módulos e regras editoriais

### Fundamentos F01–F04

#### F01 — Circuitos CC/CA - Unidades e grandezas CC/CA

Fundamentos de grandezas elétricas e suas unidades em corrente contínua e alternada, com foco em reconhecer, converter e interpretar tensão, corrente, resistência, frequência, potência e energia sem aprofundar os métodos de cálculo próprios dos módulos posteriores.

**Inclui:** Identificação de unidade correta; Conversão mA↔A, kV↔V, kW↔W, Wh↔kWh; Leitura conceitual de grandezas sem cálculo específico; Diferença entre CC e CA em nível introdutório.

**Exclui/desvia para:** Lei de Ohm e associação de resistores → F02; Reatância, impedância, fase e formas de onda → F03; Cálculo de potência, energia ou fator de potência → F04; Seleção/uso de instrumentos → M01.

**Regras de fronteira:**

- Se o núcleo da questão é reconhecer ou converter grandezas/unidades, classificar F01.
- Se a questão usa V, I e R para determinar uma incógnita, priorizar F02.
- Se frequência é apenas uma unidade/dado nominal, F01; se altera comportamento reativo ou forma de onda, F03.
- Se potência/energia são apenas unidades, F01; se há cálculo ou eficiência/fator de potência, F04.

#### F02 — Circuitos CC/CA - Lei de Ohm e associação de resistores

Análise de circuitos resistivos por Lei de Ohm e associação de resistores, incluindo relações entre tensão, corrente e resistência e obtenção de resistências equivalentes em série, paralelo e associações mistas.

**Inclui:** Cálculos V-I-R; Resistência equivalente; Distribuição de tensão/corrente em resistores; Malhas e nós quando o problema é essencialmente resistivo.

**Exclui/desvia para:** Reatância e impedância RLC → F03; Potência e energia → F04; Dimensionamento de seção de condutor por ampacidade/queda → P01; Medição com multímetro → M01.

**Regras de fronteira:**

- Circuito puramente resistivo e relação V-I-R → F02.
- Se indutor/capacitor/fasor/ângulo de fase forem determinantes, usar F03.
- Se o objetivo final é potência, energia ou fator de potência, usar F04 mesmo que Lei de Ohm seja etapa intermediária.
- Se resistência do condutor é usada para dimensionamento de instalação, considerar P01.

#### F03 — Circuitos CC/CA - Frequência, formas de onda e reatância

Comportamento de sinais e circuitos em corrente alternada, abrangendo frequência, período, formas de onda, fase, reatâncias e impedância de elementos R, L e C.

**Inclui:** Problemas em que frequência altera XL/XC; Impedância complexa; Relação de fase; Leitura/interpretação de ondas CA.

**Exclui/desvia para:** Unidades/conversões sem análise de circuito → F01; Circuitos puramente resistivos → F02; Potência ativa/reativa/aparente e FP → F04; Parametrização de frequência em inversores → E06.

**Regras de fronteira:**

- Menção isolada a 60 Hz não torna a questão F03; frequência deve ser objeto do raciocínio.
- RLC, reatância, impedância ou defasagem determinantes → F03.
- Potência/fator de potência como objetivo → F04.
- Frequência de saída/ajuste de acionamento eletrônico → E06.

#### F04 — Energia e eficiência - Potência, energia e fator de potência

Potência e energia elétrica em CC e CA, incluindo potência ativa, reativa e aparente, fator de potência, consumo, rendimento e relações de eficiência energética.

**Inclui:** Cálculo de consumo; Demanda de potência simples quando não é projeto predial; FP e compensação conceitual; Eficiência/rendimento energético.

**Exclui/desvia para:** Unidades apenas → F01; Impedância/reatância sem objetivo de potência → F03; Previsão de cargas de instalação predial → I01; Dados nominais de motor quando foco é placa/motor → E01; Produção/arranjo fotovoltaico → V01.

**Regras de fronteira:**

- Se a incógnita/decisão central é W, VA, var, Wh, kWh, FP ou rendimento, F04.
- Se potência aparece como dado de placa para reconhecer motor, E01.
- Se soma de cargas atende projeto de tomadas/iluminação, I01.
- Se potência/energia é específica de gerador/arranjo FV, V01.

### Instrumentação M01–M02

#### M01 — Instrumentos - Multímetro, alicate e seleção de escala

Seleção, princípio de uso e interpretação de instrumentos elétricos portáteis, especialmente multímetro e alicate amperímetro, com foco em grandeza, função, escala e leitura.

**Inclui:** Escolha de instrumento; Interpretação de escala; Erro por função/faixa inadequada; Comparação multímetro × alicate.

**Exclui/desvia para:** Ensaios de continuidade e isolamento como objetivo → M02; Grandezas/unidades sem instrumento → F01; TC/TP e medição indireta em SEP → T02.

**Regras de fronteira:**

- Instrumento portátil e seleção de função/escala → M01.
- Teste de continuidade ou megômetro/isolação como objetivo → M02.
- Medição indireta por transformadores de instrumento → T02.

#### M02 — Instrumentos - Continuidade e resistência de isolamento

Ensaios de continuidade elétrica e resistência de isolamento aplicados à verificação de condutores, circuitos, enrolamentos e equipamentos, com interpretação de resultados.

**Inclui:** Ensaios elétricos de continuidade/isolamento; Detecção de interrupção por continuidade; Verificação de condição de isolação.

**Exclui/desvia para:** Seleção geral de multímetro → M01; Estratégia de manutenção preventiva/preditiva → D01; Termografia e localização ampla de falhas → D02.

**Regras de fronteira:**

- Se a pergunta é como/por que interpretar continuidade ou isolação, M02.
- Se o ensaio aparece apenas como ferramenta dentro de plano de manutenção, D01 pode ser primário.
- Se o foco é localizar/diagnosticar falha por sintomas/termografia, D02.

### Segurança S01–S03

#### S01 — Segurança em eletricidade - Desenergização e reenergização

Princípios e sequência conceitual de controle de energia elétrica para colocar instalações em condição segura de trabalho e posteriormente restabelecer a energia, incluindo impedimento de reenergização e verificação de ausência de tensão.

**Inclui:** Sequência de desenergização/reenergização; LOTO em contexto elétrico; Verificação de estado desenergizado.

**Exclui/desvia para:** Válvulas de bloqueio hidráulico/pneumático → H01; EPI, qualificação, trabalho em altura e zonas → S02; Prontuário/documentação e classificação de tensão → S03; Aterramento permanente de instalação → P04.

**Regras de fronteira:**

- A palavra 'bloqueio' só indica S01 quando se refere a impedir reenergização/energia elétrica.
- Bloqueio de válvula ou atuador não é S01.
- EPI/treinamento/zona de risco sem sequência de desenergização → S02.
- Documentação e categorias de tensão → S03.

#### S02 — Segurança em eletricidade - Qualificação, EPI, altura e zonas de risco

Requisitos de pessoas, proteção individual/coletiva, trabalho em altura e delimitação de zonas de risco em atividades elétricas, tratados em nível curricular e normativo.

**Inclui:** Questões sobre trabalhador e proteção; EPI/EPC; altura; zonas de aproximação.

**Exclui/desvia para:** Sequência de desenergização → S01; Classificação de tensão e documentos → S03; Proteções por DR → P03; Manutenção como estratégia → D01.

**Regras de fronteira:**

- Pessoa/EPI/EPC/zona/altura → S02.
- Procedimento de retirar e restabelecer energia → S01.
- Prontuário, diagramas obrigatórios ou classe de tensão → S03.
- Dispositivo diferencial residual como tecnologia de proteção → P03.

#### S03 — Segurança em eletricidade - Classificação de tensão e documentação

Classificação de instalações por níveis de tensão e documentação técnica/de segurança associada à organização de serviços elétricos.

**Inclui:** Questões cujo objeto é documentação/registro de segurança; Classificação de tensão.

**Exclui/desvia para:** Desenho/simbologia do diagrama → I03; Sequência de desenergização → S01; EPI/qualificação → S02.

**Regras de fronteira:**

- Se a pergunta é sobre conteúdo/finalidade/exigência documental, S03.
- Se pede interpretar ou desenhar símbolo/diagrama, I03.
- Se o valor de tensão é apenas grandeza física, F01; se define classe/categoria de instalação, S03.

### Instalações I01–I03

#### I01 — Instalações prediais - Tomadas, iluminação e previsão de cargas

Planejamento básico de instalações elétricas prediais quanto a pontos de iluminação, tomadas e previsão de cargas, incluindo organização de circuitos em nível de projeto.

**Inclui:** Soma/previsão de potência de cargas prediais; Quantidade/posição funcional de tomadas e iluminação.

**Exclui/desvia para:** Comando de interruptores/sensores → I02; Representação gráfica/CAD → I03; Dimensionamento de condutor → P01; Proteção de circuito → P02; Potência geral não vinculada a projeto predial → F04.

**Regras de fronteira:**

- Carga predial/quantidade de pontos → I01.
- Como acionar a lâmpada/sensor → I02.
- Como representar em planta/diagrama → I03.
- Bitola/correção → P01; disjuntor/fusível → P02.

#### I02 — Instalações prediais - Interruptores, sensores e relé fotocélula

Comandos usuais de instalações prediais para iluminação e cargas simples, incluindo interruptores, sensores e relés fotocélula.

**Inclui:** Questões de acionamento predial; Seleção funcional entre interruptor/sensor/fotocélula.

**Exclui/desvia para:** Previsão de cargas → I01; Simbologia/desenho → I03; Sensores industriais/alarme/nível → A03; Comando de motores → E03.

**Regras de fronteira:**

- Comando de iluminação predial → I02.
- Sensor de nível/processo/alarme integrado a automação → A03.
- Contator/selo/reversão de motor → E03.

#### I03 — Projetos elétricos - Simbologia, unifilar, multifilar e CAD

Representação gráfica de instalações e sistemas elétricos por símbolos, diagramas unifilares/multifilares, plantas e ferramentas CAD.

**Inclui:** Identificação de símbolo; Tipo de diagrama; Leitura de desenho quando foco é representação.

**Exclui/desvia para:** Conteúdo funcional do circuito predial → I01/I02; Ladder/CLP → A01/A02; Simbologia pneumática/hidráulica → H01; Documentação de segurança → S03.

**Regras de fronteira:**

- Símbolo/representação elétrica → I03.
- Símbolo pneumático/hidráulico → H01.
- Ladder como linguagem lógica → A01.
- Diagrama citado apenas como documento obrigatório → S03.

### Dimensionamento e proteção P01–P05

#### P01 — Dimensionamento - Condutores, instalação e fatores de correção

Dimensionamento de condutores em instalações elétricas considerando seção, método de instalação, capacidade de condução, queda de tensão e fatores de correção fornecidos.

**Inclui:** Bitola/seção; ampacidade; fatores de correção; queda de tensão aplicada ao cabo.

**Exclui/desvia para:** Lei de Ohm de resistor abstrato → F02; Previsão de cargas → I01; Dimensionamento de disjuntor/fusível → P02; Condutor de proteção/aterramento quando foco é esquema de aterramento → P04.

**Regras de fronteira:**

- Se o produto final é escolher/verificar seção de cabo, P01.
- Se o produto final é proteção contra sobrecorrente, P02.
- Queda de tensão pode ser P01 quando critério de dimensionamento.

#### P02 — Dimensionamento - Disjuntores, fusíveis, curvas e curto-circuito

Proteção de circuitos contra sobrecorrentes e curto-circuitos por disjuntores e fusíveis, incluindo características, curvas de atuação e coordenação básica.

**Inclui:** Proteção por sobrecorrente; dimensionamento/seleção de disjuntor/fusível; curvas.

**Exclui/desvia para:** Proteção diferencial residual → P03; Dimensionamento do cabo → P01; Relés de proteção/SEP → T02; Comando de motor por contatores → E03.

**Regras de fronteira:**

- Sobrecorrente/curto/disjuntor/fusível → P02.
- Fuga à terra/proteção diferencial de pessoas → P03.
- Relé de proteção associado a TC/TP/SEP → T02.

#### P03 — Proteção de pessoas - DR, IDR, DDR e coordenação de funções

Proteção adicional de pessoas e instalações por dispositivos diferenciais residuais, distinguindo funções de DR/IDR/DDR e sua coordenação com proteção de sobrecorrente.

**Inclui:** Questões sobre fuga à terra e corrente residual; funções diferenciais.

**Exclui/desvia para:** Disjuntor/fusível de sobrecorrente → P02; Esquema de aterramento → P04; EPI e zonas de risco → S02.

**Regras de fronteira:**

- Se a grandeza central é corrente residual/diferença entre ida e retorno, P03.
- Se sobrecorrente/curto é central, P02.
- Aterramento pode complementar proteção, mas topologia TT/TN/IT é P04.

#### P04 — Aterramento e SPDA - Esquemas de aterramento e equipotencialização

Esquemas de aterramento das instalações e equipotencialização, com foco nas funções de condutores de proteção, massas e topologias usuais de aterramento.

**Inclui:** Topologia do aterramento da instalação; equipotencialização; condutor PE.

**Exclui/desvia para:** SPDA, captação, descida e DPS → P05; DR como dispositivo → P03; Aterramento temporário de desenergização → S01.

**Regras de fronteira:**

- Esquema permanente TT/TN/IT/equipotencialização → P04.
- Aterramento temporário como etapa de segurança → S01.
- Sistema externo de proteção contra descargas/DPS → P05.

#### P05 — Aterramento e SPDA - Captação, descida, aterramento e DPS

Proteção contra descargas atmosféricas e surtos, abrangendo captação, condutores de descida, subsistema de aterramento e dispositivos de proteção contra surtos.

**Inclui:** SPDA; para-raios/captores em contexto técnico; DPS; coordenação conceitual contra surtos.

**Exclui/desvia para:** Esquemas TT/TN/IT e equipotencialização geral → P04; Disjuntores/fusíveis → P02; Proteção diferencial → P03.

**Regras de fronteira:**

- Se o problema é descarga atmosférica/surto/captação/descida/DPS, P05.
- Se trata da topologia de aterramento da instalação sem SPDA/surto, P04.

### Motores e acionamentos E01–E06

#### E01 — Motores elétricos - Placa, potência, corrente e velocidade

Características nominais e desempenho básico de motores elétricos, com leitura de placa e interpretação de potência, corrente, tensão, velocidade, rendimento e dados de identificação.

**Inclui:** Leitura de placa; dados nominais; reconhecimento de tipo de motor.

**Exclui/desvia para:** Ligação de bobinas/fechamentos → E02; Circuitos de partida/comando → E03-E06; Potência genérica sem contexto de motor → F04; Diagnóstico de motor → D02.

**Regras de fronteira:**

- Placa e parâmetros nominais do motor → E01.
- Como conectar enrolamentos → E02.
- Como partir/reverter/controlar → E03-E06.
- Falha/diagnóstico → D02.

#### E02 — Motores elétricos - Bobinas, fechamentos e ligação monofásica/trifásica

Constituição elétrica e conexão de enrolamentos de motores, incluindo terminais, bobinas, fechamentos e ligações monofásicas/trifásicas.

**Inclui:** Conexão física/lógica dos enrolamentos; identificação de terminais.

**Exclui/desvia para:** Partida estrela-triângulo como estratégia de partida → E04; Comando/reversão/selagem → E03; Dahlander → E05; Placa/dados nominais → E01.

**Regras de fronteira:**

- Fechamento estático dos enrolamentos → E02.
- Sequência temporizada estrela-triângulo para partida → E04.
- Duas velocidades por reconexão Dahlander → E05.
- Contatores, selo e intertravamento → E03.

#### E03 — Comandos e partidas - Direta, reversão, selo e intertravamento

Comandos elétricos clássicos para partida direta e reversão de motores, com contatores, botoeiras, selo, intertravamento e elementos de proteção/comando.

**Inclui:** Ladder eletromecânico de motores; contatores para partida direta/reversão.

**Exclui/desvia para:** Lógica Ladder de CLP → A01/A02; Estrela-triângulo → E04; Dahlander → E05; Inversor/soft-starter → E06; Disjuntor/fusível como proteção de circuito → P02.

**Regras de fronteira:**

- Contatores/botoeiras/selo/reversão convencional → E03.
- Se o diagrama é programa de CLP, A01/A02.
- Se técnica de partida específica é estrela-triângulo ou compensadora, E04.
- Se eletrônico parametrizável, E06.

#### E04 — Comandos e partidas - Estrela-triângulo e compensadora

Partidas de motores por estrela-triângulo e compensadora, incluindo finalidade de redução da corrente de partida e sequência funcional dos elementos.

**Inclui:** Circuitos e sequência de estrela-triângulo; partida compensadora.

**Exclui/desvia para:** Fechamento estrela/triângulo estático → E02; Partida direta/reversão → E03; Dahlander → E05; Soft-starter/inversor → E06.

**Regras de fronteira:**

- Estrela/triângulo apenas como fechamento nominal → E02.
- Mudança automática estrela→triângulo para partir → E04.
- Controle eletrônico de rampa → E06.

#### E05 — Comandos e partidas - Dahlander e duas velocidades

Comandos de motores de duas velocidades, especialmente ligação Dahlander, com identificação das configurações de polos e lógica básica de seleção/intertravamento de velocidades.

**Inclui:** Questões que citam explicitamente Dahlander; duas velocidades por reconexão de enrolamentos/polos.

**Exclui/desvia para:** Fechamento comum de motor → E02; Partida/reversão comum → E03; Controle de velocidade por inversor → E06.

**Regras de fronteira:**

- Duas velocidades por polos/enrolamentos Dahlander → E05.
- Velocidade variável por frequência eletrônica → E06.
- Apenas estrela/triângulo de tensão → E02/E04 conforme contexto.

#### E06 — Acionamentos - Inversor, soft-starter e parametrização

Acionamentos eletrônicos de motores por inversores de frequência e soft-starters, incluindo funções, parâmetros, rampas e controle básico de velocidade/partida.

**Inclui:** Parametrização de acionamento; controle eletrônico de velocidade; partida suave.

**Exclui/desvia para:** Frequência/reatância de circuito CA → F03; Partida convencional com contatores → E03/E04; Dahlander → E05.

**Regras de fronteira:**

- Se frequência é parâmetro de um inversor para controlar motor, E06.
- Se frequência é propriedade de senoide/circuito reativo, F03.
- Soft-starter sempre permanece E06, não E04.

### Transformadores e SEP T01–T02

#### T01 — Transformadores - Relação de transformação e proteções

Fundamentos de transformadores de potência/distribuição, com relação de transformação, grandezas de primário/secundário, perdas/rendimento e proteções associadas em nível técnico.

**Inclui:** Cálculos de transformação; identificação funcional de transformadores de potência/distribuição.

**Exclui/desvia para:** TC e TP para medição/proteção → T02; Potência genérica → F04; Equipamentos de subestação como conjunto → R02.

**Regras de fronteira:**

- Transformador para transferência de energia e relação N/V/I → T01.
- Transformador de instrumento para medição/relé → T02.
- Questão centrada na operação/conjunto da subestação → R02.

#### T02 — Medição e proteção em SEP - TC, TP, relés e medição indireta

Medição e proteção indireta em sistemas elétricos de potência por transformadores de corrente e potencial, relés e cadeias de medição/proteção.

**Inclui:** TC/TP; relés de proteção de SEP; medição indireta.

**Exclui/desvia para:** Transformador de potência → T01; Multímetro/alicate → M01; Disjuntor/fusível de instalação → P02; Operação global da subestação → R02.

**Regras de fronteira:**

- TC/TP como sensores de corrente/tensão para instrumento/relé → T02.
- Transformador transferindo potência → T01.
- Equipamento de subestação sem foco no princípio de medição/proteção → R02.

### Redes e subestações R01–R02

#### R01 — Redes de distribuição - Estruturas, postes, alimentadores e topologias

Elementos e topologias de redes de distribuição, incluindo estruturas, postes, alimentadores, ramais e configurações radiais ou em anel em nível técnico.

**Inclui:** Questões de arquitetura física/topológica da rede de distribuição.

**Exclui/desvia para:** Equipamentos/barramentos de subestação → R02; Transformadores como princípio → T01; Segurança/zona de trabalho → S02.

**Regras de fronteira:**

- Rede externa entre subestações/cargas e sua topologia → R01.
- Pátio, barramentos e equipamentos de subestação → R02.
- Transformador isolado e relação elétrica → T01.

#### R02 — Subestações - Equipamentos, barramentos e operação

Constituição e operação funcional de subestações, incluindo equipamentos de manobra/proteção, barramentos, transformadores e arranjos básicos.

**Inclui:** Identificação de equipamento de subestação; arranjo de barramentos; operação de subestação em nível conceitual.

**Exclui/desvia para:** Topologia de rede externa → R01; TC/TP/relés como princípio → T02; Transformador como relação de transformação → T01; Sequência normativa de desenergização do trabalhador → S01.

**Regras de fronteira:**

- Se a questão trata do equipamento como parte do arranjo/operação da subestação, R02.
- Se o foco é relação de TC/TP ou relé, T02.
- Se o foco é relação de transformação do transformador, T01.

### Automação A01–A03

#### A01 — CLP e lógica - Booleanos, binário, tabela verdade e Ladder

Fundamentos de lógica digital e linguagem Ladder, incluindo booleanos, binário, tabelas verdade e interpretação de contatos/bobinas como expressões lógicas.

**Inclui:** Lógica pura; leitura de rung; equivalência entre expressão booleana e Ladder.

**Exclui/desvia para:** Sequenciamento com I/O de CLP → A02; Comandos eletromecânicos de motor → E03; Sensores físicos → A03.

**Regras de fronteira:**

- Se o objetivo é lógica/expressão/tabela verdade/Ladder elementar, A01.
- Se há estados, etapas, temporização, I/O e sequência de processo, A02.
- Ladder desenhado como circuito eletromecânico de contatores sem CLP pode ser E03.

#### A02 — CLP e lógica - Entradas, saídas e controle sequencial

Aplicação de CLP ao controle sequencial por entradas, saídas, memórias, temporizadores e contadores, com foco em lógica de processo e estados.

**Inclui:** Programas Ladder de CLP com sequência; I/O endereçado; temporização/contagem em automação.

**Exclui/desvia para:** Lógica booleana elementar → A01; Sensor/dispositivo de campo como objeto → A03; Circuito convencional de contatores → E03; Sequência eletropneumática centrada em atuadores/válvulas → H02.

**Regras de fronteira:**

- Programa de CLP e sequência de I/O → A02.
- Só símbolo/princípio de sensor → A03.
- Sequência cujo desafio principal é pneumático/eletropneumático → H02.

#### A03 — Sensores - Sensores de presença, alarme e nível

Sensores e dispositivos de detecção usados em automação e instalações, com foco em presença, proximidade, alarme e nível, seus princípios e aplicações.

**Inclui:** Identificação/seleção de sensores industriais; detecção de nível/presença/alarme.

**Exclui/desvia para:** Relé fotocélula e sensor de iluminação predial → I02; Programação do CLP usando sensor → A02; Instrumentação analógica especializada fora da taxonomia → possível gap/out-of-curriculum.

**Regras de fronteira:**

- Se a pergunta é qual sensor/princípio usar, A03.
- Se o sensor é apenas uma entrada e o núcleo é a sequência do CLP, A02.
- Fotocélula de iluminação predial pode ser I02.

### Pneumática/hidráulica H01–H02

#### H01 — Pneumática e hidráulica - Válvulas, atuadores e simbologia

Fundamentos de pneumática e hidráulica relativos a válvulas, atuadores e simbologia de circuitos fluídicos.

**Inclui:** Identificação de símbolo fluídico; função de válvula/atuador.

**Exclui/desvia para:** Bloqueio elétrico de reenergização → S01; Sequência eletropneumática → H02; Simbologia elétrica → I03.

**Regras de fronteira:**

- 'Válvula de bloqueio' é H01, não S01.
- Componente/símbolo fluídico isolado → H01.
- Sequência de cilindros, selo e diagnóstico eletropneumático → H02.

#### H02 — Pneumática e hidráulica - Sequências, selo e diagnóstico eletropneumático

Análise de sequências e comandos eletropneumáticos/eletro-hidráulicos, integrando válvulas, atuadores, contatos, selo e diagnóstico de funcionamento.

**Inclui:** Questões de sequência fluídica; diagnóstico de circuito eletropneumático.

**Exclui/desvia para:** Componente/simbologia isolado → H01; Comando de motor convencional → E03; Programa de CLP como núcleo → A02.

**Regras de fronteira:**

- Se o desafio é a ordem/movimento dos atuadores fluídicos, H02.
- Se só identifica a válvula/cilindro, H01.
- Se a mesma sequência é tratada prioritariamente como programa de CLP, A02 pode ser primário.

### Manutenção D01–D02

#### D01 — Manutenção e diagnóstico - Preventiva, preditiva, corretiva e inspeções

Gestão técnica da manutenção por estratégias preventiva, preditiva e corretiva, inspeções e planejamento básico, com foco em selecionar a abordagem adequada ao contexto de falha/equipamento.

**Inclui:** Classificação de tipos de manutenção; escolha da estratégia; planejamento básico.

**Exclui/desvia para:** Termografia/localização concreta de falha → D02; Teste de continuidade/isolação como técnica → M02; Segurança/desenergização → S01/S02.

**Regras de fronteira:**

- Se a pergunta é 'qual estratégia/tipo de manutenção', D01.
- Se pergunta 'onde/qual falha' usando sintomas, termografia ou conexão, D02.
- Se técnica específica de continuidade/isolação é objeto do conhecimento, M02.

#### D02 — Manutenção e diagnóstico - Termografia, conexões e localização de falhas

Diagnóstico e localização de falhas elétricas por inspeção técnica, termografia, análise de conexões e interpretação de sintomas/medições.

**Inclui:** Questões que pedem causa/local da falha; termogramas; conexões anormais.

**Exclui/desvia para:** Classificação preventiva/preditiva/corretiva → D01; Continuidade/isolamento como ensaio específico → M02; Defeito de lógica em CLP → A02; Defeito de sequência eletropneumática → H02.

**Regras de fronteira:**

- Falha física/elétrica localizada por sintoma, temperatura ou conexão → D02.
- Tipo de manutenção → D01.
- Se a questão é puramente sobre como funciona o ensaio de isolação, M02.

### Fotovoltaica V01

#### V01 — Energia solar fotovoltaica - Arranjos, potência e eficiência

Fundamentos de sistemas fotovoltaicos, incluindo módulos, arranjos série/paralelo, grandezas elétricas, potência, eficiência e blocos funcionais básicos do sistema.

**Inclui:** Questões explicitamente de geração solar FV; configuração de strings; potência/eficiência FV.

**Exclui/desvia para:** Potência/energia genérica → F04; Dimensionamento de condutores não específico ao arranjo → P01; Inversor de motor → E06; Proteção contra surtos/SPDA → P05.

**Regras de fronteira:**

- Se a fonte/arranjo fotovoltaico é essencial ao problema, V01.
- Se é apenas cálculo genérico de energia sem contexto FV, F04.
- 'Inversor' de sistema FV é V01; inversor de frequência para motor é E06.

