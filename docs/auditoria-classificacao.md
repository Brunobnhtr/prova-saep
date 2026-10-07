# Auditoria da classificação V2

**V2 produzida, com 9.791 IDs preservados.** A V1 continua intacta. A classificação permanece preliminar; não foram resolvidos gabaritos, publicados itens ou alterado o acervo externo. S01 não foi iniciado.

## Golden set e regressões

O conjunto tem **153 questões reais**, expectativas editoriais anotadas após leitura de enunciados e alternativas, com exemplos dos 35 módulos e casos sem módulo. Quatro imagens foram abertas e inspecionadas: Q4148970, Q4148977, Q4150424 e Q4027618. Outros itens visuais têm revisão temática baseada no texto e dependências explícitas, sem alegar interpretação de figuras não vistas.

Resultados: **153 casos passaram / 0 falharam**; V1 acertou o módulo principal em 99/153 casos e V2 em 153/153. As checagens cobrem módulo principal, secundários, conceito, família, tipo principal, tipos requeridos e causa de ausência de módulo.

**Limite decisivo:** o golden set foi usado no desenvolvimento das regras. Resultado perfeito nesse conjunto, se obtido, é concordância de regressão, não prova de 100% de precisão do catálogo. Não é holdout. A seleção privilegia enunciados curtos, poucos visuais e estratos da V1; foi completada com três casos dirigidos de H01/H02. Sem revisão humana independente.

## Comparação V1 → V2

| Indicador | Total |
|---|---:|
| TOTAL_QUESTIONS | 9791 |
| CLASSIFIED | 6246 |
| UNCLASSIFIED | 3545 |
| SEMANTIC_FAMILY_ASSIGNED | 6984 |
| MODULE_ASSIGNMENTS | 6293 |
| HIGH_INTERACTION_POTENTIAL | 716 |
| V1_UNCHANGED | True |
| ANSWERS_UNRESOLVED | True |
| PRIMARY_MODULE_CHANGED | 5181 |
| LEFT_UNCLASSIFIED | 118 |
| OUT_OF_CURRICULUM | 14 |
| NEW_SEMANTIC_FAMILY | 6007 |
| CHANGED_SEMANTIC_FAMILY | 747 |
| HIGH_DOWNGRADED | 1939 |
| LOW_MEDIUM_PROMOTED | 1301 |
| THEMATIC_TIES_RESOLVED | 1752 |

A redução do número de módulos atribuídos é intencional: tópico anterior sozinho não escolhe um módulo, e assuntos de eletrônica sem módulo dedicado ficam MISSING_MODULE. Isso é mais conservador que manter falsos encaixes só para aumentar cobertura. Os conceitos reconhecidos continuam visíveis. Menções incidentais a motor/transformador deixam de gerar filas secundárias.

## Casos obrigatórios

| ID | V1 | V2 | Justificativa |
|---|---|---|---|
| Q4148970 | E02 / THREE_PHASE_POWER | E03 / MOTOR_REVERSING | Imagem inspecionada: K1/K2 invertem fases, com contatos de selo e intertravamento; avaliar funcionamento/reversão, não calcular potência trifásica. |
| Q4148977 | A03 / SERIES_EQUIVALENT_RESISTANCE | F02 / WHEATSTONE_BRIDGE | Imagem inspecionada: ponte de quatro braços, voltímetro entre pontos médios, extensômetro e condição de equilíbrio. F02 para cálculo de ponte; M01 como reutilização em medição. |
| Q4150424 | None / None | None / TRANSISTOR_IDENTIFICATION | Imagem inspecionada e opções lidas: identificar família do transistor. Não existe módulo de eletrônica de componentes na trilha de 35; reconhecer conceito, manter MISSING_MODULE. |
| Q4151541 | F01 / None | E01 / INDUCTION_MOTOR | Pergunta a máquina assíncrona; alternativas discriminam classes de máquinas. E01 cobre operação/velocidade de motor; corrente alternada é apenas contexto. |

Transistor identificado com confiança conceitual não cria um módulo curricular inexistente. Q4150424 recebe TRANSISTOR_IDENTIFICATION + MISSING_MODULE. E01 acolhe operação/velocidade de motores, incluindo reconhecimento de máquina assíncrona. Wheatstone entra em F02 como análise de circuito e M01 como reutilização na técnica de medição.

## As 878 questões originalmente sem módulo

| Resultado/causa preliminar | Total |
|---|---:|
| CLASSIFIER_GAP | 214 |
| IMAGE_REQUIRED | 148 |
| INSUFFICIENT_CONTEXT | 42 |
| MISSING_MODULE | 350 |
| OUT_OF_CURRICULUM | 6 |
| RECLASSIFIED | 118 |

Cada ID tem causa e evidência em unclassified-analysis.json. CLASSIFIER_GAP não significa fora do currículo. IMAGE_REQUIRED é uma dependência, não INVALID. OUT_OF_CURRICULUM exige enquadramento explícito em assunto externo; não foi atribuído só porque uma regra falhou. MISSING_MODULE indica conceito técnico reconhecido sem espaço curricular natural nos 35 módulos atuais.

## Auditoria por módulo

Acertos abaixo são apenas nos exemplos revisados. Foram auditados HIGH, MEDIUM e LOW da V1 quando existiam candidatos elegíveis; a divisão V2 permite ver estratos vazios, sem fabricar precisão. False negatives são itens cujo módulo esperado era diferente da previsão, dentro da amostra. Nenhum desses números estima exaustivamente as falhas do banco.

| Módulo | Esperados no golden | V1 HIGH corretos/amostrados | V2 HIGH corretos/amostrados | Falsos negativos V1/V2 |
|---|---:|---|---|---|
| S01 | 4 | 2/2 | 4/4 | 1/0 |
| S02 | 6 | 2/2 | 6/6 | 2/0 |
| F01 | 2 | 1/2 | 2/2 | 1/0 |
| M01 | 6 | 2/2 | 4/4 | 3/0 |
| F02 | 5 | 2/2 | 5/5 | 3/0 |
| F03 | 3 | 0/2 | 3/3 | 3/0 |
| F04 | 5 | 2/2 | 4/4 | 2/0 |
| I03 | 5 | 1/2 | 3/3 | 2/0 |
| R01 | 2 | 0/2 | 2/2 | 2/0 |
| H01 | 2 | 0/0 | 2/2 | 0/0 |
| A01 | 5 | 2/2 | 4/4 | 1/0 |
| E01 | 8 | 2/2 | 7/7 | 4/0 |
| T01 | 3 | 2/2 | 3/3 | 1/0 |
| T02 | 2 | 2/2 | 2/2 | 0/0 |
| R02 | 2 | 1/2 | 2/2 | 1/0 |
| I01 | 5 | 1/2 | 5/5 | 3/0 |
| P01 | 6 | 1/2 | 6/6 | 3/0 |
| P02 | 6 | 1/2 | 4/4 | 4/0 |
| I02 | 3 | 2/2 | 3/3 | 0/0 |
| P03 | 5 | 2/2 | 5/5 | 1/0 |
| M02 | 2 | 1/2 | 2/2 | 0/0 |
| S03 | 2 | 0/0 | 2/2 | 1/0 |
| V01 | 4 | 2/2 | 4/4 | 0/0 |
| D01 | 2 | 1/2 | 2/2 | 0/0 |
| D02 | 2 | 0/0 | 2/2 | 1/0 |
| E02 | 2 | 1/2 | 2/2 | 1/0 |
| E03 | 4 | 2/2 | 3/3 | 1/0 |
| H02 | 1 | 0/0 | 1/1 | 1/0 |
| A02 | 5 | 1/2 | 4/4 | 2/0 |
| E06 | 4 | 2/2 | 4/4 | 0/0 |
| E04 | 3 | 2/2 | 3/3 | 0/0 |
| A03 | 3 | 2/2 | 3/3 | 0/0 |
| E05 | 1 | 1/1 | 1/1 | 0/0 |
| P04 | 3 | 2/2 | 2/2 | 0/0 |
| P05 | 3 | 2/2 | 3/3 | 0/0 |

MEDIUM/LOW, secundários revistos e IDs de falsos positivos constam em auditoria-classificacao-v2.json. Zero amostras é ausência de estimativa, não zero erro. Um exemplo Dahlander e um eletropneumático são insuficientes para inferir a qualidade dos respectivos módulos.

## O que mudou no mecanismo

Taxonomia com pais conceituais e mapeamento curricular separado da família; padrões de relações técnicas específicas e precedência contextual. Conceito explícito ou observação visual revisada domina assunto original; tópico anterior e alternativas só apoiam. Distratores não criam um conceito principal por votação. Intertravamento não é bloqueio hidráulico; circuito de potência não é cálculo de potência; testes de isolamento aplicados a motores/transformadores permanecem medições.

HIGH exige quadro técnico explícito, especificidade e ausência de empate/visual essencial não inspecionado. Não equivale ao antigo score≥5. Confiança conceitual é separada da atribuição de módulo: um conceito pode ser reconhecido e continuar sem módulo. As regras são determinísticas auditáveis; não são compreensão semântica exaustiva por embeddings/LLM.

Interação V2 usa critérios explícitos de decomposição, extração, unidades, múltiplas etapas, leitura de imagem, proposições, sequência e diagnóstico. HIGH requer riqueza de raciocínio, não presença de número. Reconhecimento simples pode permanecer questão normal. Os critérios são hipóteses de planejamento, não etapas prontas. TF_L2–TF_L5 são sugestões de profundidade, sem conversão ou inferência de gabarito.

Inspeção: P0 para falhas estruturais/sinais de imagem faltante e normas críticas; P1 para empates, visuais não inspecionados, lacunas aparentes ou interação rica; P2 para classificação incerta; P3 para candidatos textuais fortes. Motivos da V1 permanecem em v1_inspection_reasons; classification_inspection_reasons é a leitura vigente.

Variantes semânticas são grupos candidatos por conceito + estrutura da pergunta; isso encontra contas equivalentes com números/enunciados diferentes, mas não garante duplicidade. Não excluímos nenhuma questão. Questões da mesma família de habilidade não contam automaticamente como evidências independentes de domínio.

## Arquivos e reprodução

```powershell
python scripts/reclassificar-acervo-v2.py
python scripts/auditar-classificacao-v2.py
python -m unittest discover -s scripts -p "test_classificacao_v2.py" -v
```

Não regenerar o golden set automaticamente após alterações no classificador; expectativas só mudam por revisão editorial documentada. anotar-golden-classificacao.py registra as anotações desta sessão sem chamar a inferência. As listas V1 não são sobrescritas.

- catalogo-global-v2.json, resumo-global-v2.json e por-modulo-v2/: previsões e filas.
- taxonomia-conceitos-v2.json, familias-semanticas-v2.json e variantes-semanticas-v2.json: conceitos e agrupamentos.
- unclassified-analysis.json: causas, incluindo todos os 878 IDs anteriores.
- classification-golden-set.json e classification-regressions.json: expectativas e resultados por campo.
- auditoria-classificacao-v2.json, validacao-classificacao-v2.json e observacoes-visuais-classificacao-v2.json: revisão e integridade.

## Antes de liberar produção de S01

Os casos óbvios foram corrigidos e a regressão editorial foi executada. A V2 pode orientar seleção assistida por revisão; não deve publicar ou escolher conteúdo sozinha. Próxima verificação de qualidade: amostra cega, fora do golden set, com mais enunciados longos, imagens reais e normas; decidir como tratar os conceitos de eletrônica/instrumentação sem módulo. Reunir candidatos S01 de todas as forças, sem excluir itens CLASSIFIER_GAP ligados à segurança, e revisar um subconjunto antes de resolver. Não iniciar S01 completo automaticamente.
