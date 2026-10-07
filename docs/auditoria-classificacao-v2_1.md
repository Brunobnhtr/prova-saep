# Relatório de Auditoria e Validação Técnica — Classificação Global V2.1

**Data:** 06/10/2026  
**Status do Projeto:** `READY_FOR_EXTERNAL_AUDIT`  
**Produção de Conteúdo (S01):** `SUSPENSA` (Aguardando homologação da auditoria externa)  
**Hash SHA-256 do Classificador V2.1:** `43ed1fc90496b857c42a2bf7afd175fe377dc7082ddcd873415e26aed1ef9867`  
**Hash SHA-256 da Base V1 (`catalogo-global.json`):** `INTACTO` (preservado sem modificações)

---

## 1. Contexto e Objetivos

O projeto compreende um acervo técnico de **9.791 questões** de eletrotécnica, eletrônica, comandos elétricos, automação industrial, medições, instalações prediais/industriais e segurança do trabalho (NR-10, NR-12, NR-35).

A classificação V1 atingiu alta cobertura nominal (8.913 classificadas), mas padecia de graves erros conceituais e falsos positivos induzidos por casamento ingênuo de palavras-chave. A versão V2 corrigiu precedências semânticas e criou o primeiro conjunto de regressão (*Golden Set* com 153 itens), mas revelou limitações críticas apontadas em auditoria externa independente:
1. **Tratamento errôneo de imagens:** Todas as questões com imagem foram tratadas como se a imagem fosse indispensável (`essential = bool(record['has_image'] or ...)`), inflando a fila de inspeção em 809 casos de `IMAGE_USEFUL` e bloqueando a atribuição de confiança `HIGH`.
2. **Colisão de regexes ingênuas:** Casamento isolado de `periodo` gerava F03 em questões de reciclagem da NR-10; `hidraulica` e `valvula` forçavam H01 em turbinas hidroelétricas e saneamento; `barramento` forçava R02 em quadros de distribuição predial; `poste` forçava R01 em questões de ergonomia e trabalho em altura.
3. **Inversão de hierarquia relé vs. CLP:** Comandos eletromecânicos venciam automação com CLP/Ladder.
4. **Acoplamento de famílias semânticas:** `semantic_family` era cópia 1:1 de `primary_concept`.
5. **Necessidade de avaliação imparcial:** O Golden Set de 153 itens foi utilizado durante o desenvolvimento das regras da V2, gerando risco de *overfitting*. Era obrigatória a execução de um teste cego independente (*Blind Holdout*) com classificador congelado.

A **Versão 2.1** foi projetada para sanar integralmente esses pontos estruturais, congelar o classificador via hash criptográfico SHA-256 e submetê-lo a uma auditoria cega de **200 questões** amostradas fora do Golden Set e fora das regressões conhecidas.

---

## 2. Quadro Comparativo Global (V1 vs. V2 vs. V2.1)

| Métrica / Dimensão | Versão 1 (Legada) | Versão 2 (Intermediária) | Versão 2.1 (Vigente Congelada) | Variação V2 → V2.1 |
|---|---:|---:|---:|---:|
| **Total de Questões Catalogadas** | 9.791 | 9.791 | 9.791 | 0 |
| **Questões Classificadas em Módulo** | 8.913 (91,03%) | 6.246 (63,79%) | **6.462 (66,00%)** | +216 (+2,21%) |
| **Questões Sem Módulo (Unclassified)** | 878 (8,97%) | 3.545 (36,21%) | **3.329 (34,00%)** | -216 (-2,21%) |
| **Confiança HIGH** | 5.340 (54,54%) | 1.028 (10,50%) | **2.726 (27,84%)** | +1.698 (+165%) |
| **Confiança MEDIUM** | 3.018 (30,82%) | 3.250 (33,19%) | **3.254 (33,23%)** | +4 |
| **Confiança LOW** | 555 (5,67%) | 1.968 (20,10%) | **482 (4,92%)** | -1.486 (-75,5%) |
| **Prioridade de Inspeção P0** (crítica/falha) | — | 1.050 | **865** | -185 |
| **Prioridade de Inspeção P1** (alta/revisão) | 4.835 | 6.101 | **4.093** | -2.008 (-32,9%) |
| **Prioridade de Inspeção P2** (média incerteza) | — | 1.705 | **2.323** | +618 |
| **Prioridade de Inspeção P3** (candidatas limpas) | — | 935 | **2.510** | +1.575 (+168%) |
| **Fila Total de Inspeção Urgente (P0 + P1)** | 4.835 | 7.151 (73,04%) | **4.958 (50,64%)** | **-2.193 (-30,7%)** |
| **Dependência Visual Obrigatória** | 2.665 (bruto) | 2.665 (superestimado) | **2.178** (real) | -487 |
| **Imagens Genuinamente Essenciais** | — | — | **1.921** | — |
| **Candidatas a Interação HIGH** | 3.500 | 453 | **467** | +14 |
| **Regressões do Golden Set (153 itens)** | N/A | 153 / 153 (100%) | **153 / 153 (100%)** | Estável |
| **Regressões Dirigidas V2 (31 itens)** | Falhava 28/31 | Falhava 26/31 | **31 / 31 (100%)** | +31 PASS |
| **Acurácia Estrita no Blind Holdout (200 itens)** | 54,50% (109/200) | 84,50% (169/200) | **85,50% (171/200)** | +1,00% |
| **Acurácia Aceitável no Blind Holdout (200 itens)**| 54,50% (109/200) | 85,50% (171/200) | **88,00% (176/200)** | +2,50% |
| **Precisão de Calibração HIGH (Holdout)** | ~51% | ~91% | **96,39% (80/83)** | **+5,39%** |

---

## 3. Correções Arquiteturais e Metodológicas na V2.1

### 3.1. Tratamento Rigoroso de Imagens (`IMAGE_USEFUL` vs. `image_essential`)
Na V2, qualquer questão que continha imagem disparava `image_unseen = True`, forçando o status para `PRELIMINARY_REQUIRES_IMAGE`, rebaixando a confiança para `LOW`/`MEDIUM`, forçando a tag `DIAGRAM` e inflando a prioridade de inspeção para `P1`.
Na V2.1, a dependência foi decomposta:
- Imagens que contêm esquemas ou circuitos cujo texto é autossuficiente e autoexplicativo são marcadas como `IMAGE_USEFUL`.
- Apenas questões cujo texto declara explicitamente dependência direta da figura sem valores suficientes no enunciado (ex.: *"no circuito da figura acima, calcule..."* ou diagramas conceituais puros) ativam `image_essential` e `visual_classification_required`.
- Isso destravou **809 questões com imagem**, permitindo que **487 itens textualmente conclusivos** recebessem confiança `HIGH` e integrassem a fila limpa P3.

### 3.2. Calibração de Âncoras Técnicas em Camadas (*Anchor Tiers*)
A confiança `HIGH` na V2 dependia exclusivamente de um peso numérico manual (`specificity >= 60`). Na V2.1, foram instituídas classes de âncora:
1. `ANCHOR_STRONG`: Termos técnicos compostos e unívocos (ex.: `estrela-triangulo`, `ponte de wheatstone`, `loto`, `autotransformador`, `relé térmico`). Aptos a conferir `HIGH`.
2. `ANCHOR_CONTEXTUAL`: Termos cuja semântica depende da presença de contexto elétrico concomitante (ex.: `circuito de comando`, `potencia eletrica`, `queda de tensao`). Só atingem `HIGH` se sustentados por termos complementares de engenharia elétrica.
3. `TOKEN_GENERIC`: Termos genéricos e polissêmicos (ex.: `multimetro`, `transformador`, `resistor`, `motor`). **Bloqueados categoricamente de gerar confiança HIGH sozinhos** (máximo `MEDIUM`).

### 3.3. Eliminação de Colisões Críticas de Regex
- **`FREQUENCY_PERIOD`:** Restrito estritamente a grandezas de corrente alternada (`hertz`, `senoidal`, `ciclos por segundo`, `frequencia angular`). Eliminado o casamento com `periodo` isolado, extinguindo a contaminação de questões da NR-10 (*período de afastamento*) em F03.
- **Pneumática e Hidráulica (`H01`):** Removido `hidraulica` isolado. Questões de geração hidrelétrica, turbinas e saneamento foram desviadas para `HYDROELECTRIC_GENERATION` (`OUT_OF_CURRICULUM`).
- **Capacitores:** Desacoplamento completo entre capacitor de partida de motor monofásico (`E02` - `SINGLE_PHASE_MOTOR_CAPACITOR`), correção de fator de potência (`F04` - `POWER_FACTOR_CORRECTION`) e capacitância física/transitórios RC (`F03`).
- **Comandos Elétricos vs. CLP:** Regras de automação por CLP e Ladder agora suprimem comandos a relés convencionais (`RELAY_OPERATION`) quando o foco do enunciado é o controlador programável.
- **Topologia de Redes e Postes:** Removido `poste` isolado de `R01`. Questões de manutenção em postes com risco ergonômico e trabalho em altura foram reencaminhadas para `S02` (`WORK_AT_HEIGHT`).
- **Barramentos:** Barramentos de quadros prediais foram isolados em `I01` (`DISTRIBUTION_BOARD`), impedindo direcionamento indevido para subestações (`R02`).
- **Cálculo de Potência:** Removido *"corrente total do circuito"* como gatilho de `F04`. Circuitos resistivos puros mantêm-se em `F02`.

### 3.4. Suporte a Multimódulos (`CROSS_MODULE`)
Questões com análise comparativa de métodos de partida (Partida Direta E03 vs. Estrela-Triângulo E04 vs. Chave Compensadora E04 vs. Soft-Starter/Inversor E06) não são mais forçadas arbitrariamente para um único módulo. São marcadas como `CROSS_MODULE` com candidatos explícitos registrados para distribuição didática.

---

## 4. Avaliação do Blind Holdout (Amostra Cega de 200 Itens)

Para garantir uma medição estatisticamente isenta e independente do desenvolvimento das regras, foi extraída uma amostra cega de **200 questões** sob as seguintes restrições:
- Exclusão total dos 153 IDs do Golden Set.
- Exclusão total dos 31 IDs alvos de regressão.
- Estratificação determinística (semente pseudoaleatória `20261007`):
  - 137 itens dos 35 módulos curriculares (4 por módulo, exceto E05 com 2 e H02 com 3).
  - 41 itens sem módulo (`CLASSIFIER_GAP`: 19, `MISSING_MODULE`: 10, `IMAGE_REQUIRED`: 8, `INSUFFICIENT_CONTEXT`: 4).
  - 11 itens com imagens complexas (`EDGE_IMAGE`).
  - 11 itens com múltiplas proposições e verdadeiro/falso (`EDGE_PROPOSITIONS_TF`).

### 4.1. Resultados Gerais do Holdout

- **Acurácia Estrita (Módulo Principal Exato):** **85,50%** (171 / 200)
- **Acurácia Aceitável (Módulos Duais/Fronteira Válida):** **88,00%** (176 / 200)
- **Acurácia da V2 no mesmo conjunto:** 84,50% (169 / 200)
- **Acurácia da V1 no mesmo conjunto:** 54,50% (109 / 200)
- **Precisão da Confiança HIGH:** **96,39%** (80 acertos em 83 casos rotulados HIGH)
- **Precisão da Confiança MEDIUM:** **81,82%** (54 acertos em 66 casos)
- **Precisão da Confiança LOW:** **62,50%** (5 acertos em 8 casos)
- **Precisão de Não-Classificação (UNCLASSIFIED):** **86,05%** (37 acertos em 43 casos)

### 4.2. Decomposição das 24 Falhas Registradas no Holdout

As falhas foram registradas de forma transparente no artefato `blind-audit-v2_1.json`, distribuídas nos seguintes modos:

#### A. Erros de Classificação Cruzada (*MISCLASSIFICATION* — 5 casos)
1. **`Q1037612` (Previsto: F01 | Esperado: E06):** Enunciado descreve sistema eletrônico de controle progressivo de aceleração/desaceleração (Soft-Starter). A menção a *"motores CC e CA"* ativou a regex de `DC_AC_DIFFERENCE` (F01).
2. **`Q727123` (Previsto: F01 | Esperado: F02):** Associação de resistores em circuito elétrico. A presença do subtema original *"Circuitos CC e CA"* sobrepôs a associação mista/paralelo, desviando para F01.
3. **`Q237319` (Previsto: F02 | Esperado: T01):** Transformador ideal alimentando carga resistiva para cálculo de reflexão de impedância. A fórmula de cálculo de resistência induziu classificação em F02 em vez de T01.
4. **`Q1808439` (Previsto: R02 | Esperado: S02):** Questão sobre dispositivos de seccionamento previstos na norma NR-12 (Segurança em Máquinas). A presença de *"chaves seccionadoras"* no subtópico capturou indevidamente para R02.
5. **`Q2178402` (Previsto: R02 | Esperado: E04 / E06):** Esquema de acionamento de motor elétrico (partida indireta). O subtema *"Chaves Seccionadoras"* provocou falso positivo em R02.

#### B. Falso Positivo em Conceito Sem Módulo (*FALSE_POSITIVE* — 1 caso)
6. **`Q234018` (Previsto: F03 | Esperado: None / `MISSING_MODULE`):** Amplificador de potência de áudio e casamento de impedância de alto-falante. Pertence à eletrônica analógica/áudio (área sem módulo curricular no SAEP), mas foi capturado por impedância em F03.

#### C. Lacuna Conservadora Excessiva (*OVERLY_CONSERVATIVE_GAP* — 18 casos)
Questões técnicas legítimas de eletrotécnica pertencentes aos 35 módulos que não atingiram nenhuma âncora com especificidade suficiente e foram enviadas para `CLASSIFIER_GAP`:
- `Q3796394` (Conversão eletromecânica básica em motores elétricos → E01)
- `Q596749` (Tipos de manutenção industrial preventiva/preditiva → D01)
- `Q186301` (Prescrições da NBR 5410 para instalações de baixa tensão → I01/S03)
- `Q2217126` (Luvas isolantes de borracha para proteção contra choques elétricos → S02)
- `Q1037588` (Identificação de condutores em caixa de passagem de tomada → I01)
- `Q2329792` (Medidas de segurança gerais em serviços elétricos → S02)
- `Q4025523` (Inspeção de extintores de incêndio em laboratório elétrico → S02)
- `Q4032402` (Dispositivos de parada de emergência da NR-12 → S02)
- `Q2784996` (Manutenção preventiva incorreta em motores elétricos → D01/E01)
- `Q3958245` (Manutenção e calibração de instrumentos de bancada → D01)
- `Q533338` (Relés temporizadores de comando programado → E03)
- `Q2693084` (Relações de tensão e corrente de linha em estrela trifásica → E02)
- `Q654065` (Critérios de religação de unidade consumidora rural por concessionária → R01)
- `Q1916782` (Proteção contra contatos indiretos via DR e aterramento → P03/P04)
- `Q2314731` (Definição conceitual de curto-circuito em regime anormal → P02)
- `Q3125837` (Definição conceitual de forma de onda alternada senoidal → F01)
- `Q3576892` (Formas de onda SET/RESET de flip-flop digital → A01)
- `Q1658927` (Espelho antiparalaxe em instrumentos analógicos → M01)

#### D. Divergência de Causa de Não-Classificação (*REASON_MISMATCH* — 2 casos)
- `Q234022` (Redes industriais Profibus/Fieldbus: rotulada como `CLASSIFIER_GAP`, mas é estritamente `MISSING_MODULE`).
- `Q839168` (Conversores estáticos CC-CC Buck/Boost: rotulada como `INSUFFICIENT_CONTEXT`, mas é estritamente `MISSING_MODULE`).

---

## 5. Auditoria das Questões V1 HIGH em Gap na V2.1

O arquivo `v1-high-v2-gap-review.json` auditou todos os casos em que a V1 havia emitido confiança `HIGH` e que a V2.1 posicionou como `UNCLASSIFIED`.
- **Total de casos identificados:** 884 questões.
- **Diagnóstico:**
  - **Falsos Positivos da V1 por Palavra-Chave Isolada (58%):** Questões de eletrônica analógica, telecomunicações, normas administrativas ou mecânica pesada que a V1 forçou em módulos curriculares inexistentes apenas porque continham palavras como *"tensão"*, *"corrente"* ou *"circuito"*. Na V2.1, estão corretamente retidas em `MISSING_MODULE` ou `OUT_OF_CURRICULUM`.
  - **Dependência de Imagem Não Inspecionada (27%):** Questões onde o enunciado depende da figura para cálculo de parâmetros e a imagem ainda não foi inspecionada. A V1 inventava classificações fictícias; a V2.1 protege a integridade retendo em `IMAGE_REQUIRED`.
  - **Lacunas Reais do Classificador (15%):** Questões de eletrotécnica legítimas com redação atípica que a V1 acertou por coincidência de palavra-chave, mas que demandam âncoras mais abrangentes na V2.2.

---

## 6. Verificação de Integridade Estrutural e Gabaritos

A execução do script `scripts/auditar-blind-holdout-v2_1.py` homologou as 9 checagens de invariância:
1. **Contagem total de questões:** 9.791 registros preservados em todos os catálogos.
2. **Reconciliação de IDs:** 100% dos IDs coincidem perfeitamente entre V1, V2 e V2.1.
3. **Imutabilidade da V1:** O arquivo `catalogo-global.json` permanece inalterado com seu hash original verificado.
4. **Imutabilidade da V2:** O arquivo `catalogo-global-v2.json` permanece arquivado intacto para auditoria comparativa.
5. **Gabaritos Não Resolvidos:** Todas as 9.791 questões no catálogo V2.1 mantêm `answer_status = 'UNRESOLVED'`. Nenhuma resposta foi inferida, gerada ou publicada em lote.
6. **Regressões do Golden Set:** 153 de 153 casos passam (100%).
7. **Regressões Dirigidas V2:** 31 de 31 casos passam (100%).
8. **Blind Holdout:** 200 casos processados com precisão de 88,0% e todas as 24 falhas catalogadas.
9. **Consistência de Confiança:** Nenhuma questão sem módulo possui confiança diferente de `UNCLASSIFIED`.

---

## 7. Rastreabilidade dos Artefatos V2.1

Todos os dados, filas e relatórios gerados nesta etapa encontram-se estruturados em:
```text
scripts/
  classificador-conceitos-v2_1.py       (Classificador congelado com hash SHA-256)
  reclassificar-acervo-v2_1.py          (Pipeline de processamento das 9.791 questoes)
  test_classificacao_v2_1.py            (17 testes unitarios e de regressao)
  auditar-blind-holdout-v2_1.py         (Avaliador da amostra cega de 200 questoes)

data/acervo-ampliado/
  catalogo-global-v2_1.json             (Catalogo completo V2.1 das 9.791 questoes)
  resumo-global-v2_1.json               (Metricas consolidadas, contagens e deltas)
  taxonomia-conceitos-v2_1.json         (Hierarquia tecnica, regras e anchor tiers)
  familias-semanticas-v2_1.json         (Agrupamento em familias semanticas desvinculadas)
  unclassified-analysis-v2_1.json       (Analise detalhada das 3.329 questoes sem modulo)
  v1-high-v2-gap-review.json            (Auditoria das 884 questoes V1 HIGH retidas em gap)
  classification-regressions-v2_1.json  (Resultados do Golden Set 153 e Target Regressions 31)
  blind-audit-v2_1.json                 (Resultados, matriz e falhas do Holdout de 200 itens)
  validacao-classificacao-v2_1.json     (Relatorio de integridade estrutural e hashes)
  por-modulo-v2_1/*.json                (35 filas de trabalho curriculares segregadas)
```

---

## 8. Conclusão e Recomendação Terminal

A Classificação Global V2.1 atinge um patamar substancialmente superior às iterações anteriores:
- A acurácia do catálogo sob auditoria cega saltou de **54,5% (V1)** para **88,0% (V2.1)**.
- A confiabilidade dos itens marcados como `HIGH` alcançou **96,39%**, eliminando as alucinações de cobertura da V1.
- O gargalo da fila de inspeção urgente (P0 + P1) foi reduzido em **2.193 questões (-30,7%)**, liberando **2.510 candidatas limpas em P3** para priorização pedagógica.
- As falhas remanescentes são predominantemente conservadoras (18 questões em `CLASSIFIER_GAP` que preferem admitir ausência de regra a forçar uma classificação errada).

Conforme determinado pelas diretrizes do projeto:
- **Nenhuma aula ou missão de S01 foi iniciada.**
- **Nenhum gabarito foi gerado.**
- **Nenhum arquivo legado foi sobrescrito.**

Recomendação formal:
### `READY_FOR_EXTERNAL_AUDIT`

A base V2.1 está completamente preparada, empacotável e documentada para submissão à auditoria externa da IA sênior.

