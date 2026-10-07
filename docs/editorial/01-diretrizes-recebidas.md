Seu prompt precisa deixar bem separado o que é **recuperação do acervo**, o que é **validação do gabarito** e o que é **transformação pedagógica em questão interativa**. Também vale impedir a IA de “inventar confiança”: se ela não conseguir validar uma resposta com segurança, a questão não deve entrar como autocorrigível ainda.

Use o arquivo de inventário e análise do acervo como fonte de contexto e siga rigorosamente as regras abaixo.

# OBJETIVO

O banco possui aproximadamente 9.791 questões, porém os campos de gabarito estão vazios porque os gabaritos originais não puderam ser extraídos.

NÃO tente preencher automaticamente o gabarito das 9.791 questões de uma só vez.

A validação deverá acontecer progressivamente, conforme os módulos do curso forem sendo construídos e as questões forem selecionadas para cada tópico específico.

O objetivo é transformar apenas questões realmente úteis e verificáveis em atividades pedagógicas autocorrigíveis e, quando apropriado, em QUESTÕES INTERATIVAS PASSO A PASSO capazes de diagnosticar exatamente em qual parte do raciocínio o aluno está errando.

---

# 1. TRATAMENTO DOS GABARITOS AUSENTES

Todos os campos `gabarito` atualmente nulos devem ser considerados:

`UNRESOLVED`

Isso NÃO significa que a questão é inválida.

Significa apenas que a resposta original não foi recuperada.

Quando uma questão for selecionada para um módulo, faça sua resolução independente.

Para cada questão selecionada:

1. interpretar cuidadosamente o enunciado;
2. inspecionar todas as alternativas existentes;
3. considerar imagens, esquemas, tabelas, fórmulas e unidades;
4. resolver a questão de forma independente;
5. determinar qual alternativa corresponde à resposta correta;
6. justificar tecnicamente a escolha;
7. verificar se existe ambiguidade;
8. registrar o nível de confiança.

Nunca selecionar uma alternativa apenas porque ela “parece mais provável”.

---

# 2. ESTADOS DE VALIDAÇÃO

Cada questão deve receber um estado editorial.

Usar:

`UNRESOLVED`
Questão ainda não analisada.

`SOLVED_AI`
Questão resolvida logicamente, mas ainda sem segunda validação.

`VERIFIED`
Resposta conferida por cálculo, referência técnica, norma, literatura ou outra verificação suficientemente forte.

`AMBIGUOUS`
Há mais de uma interpretação plausível ou falta informação.

`INVALID`
Há problema estrutural, enunciado incompleto, imagem indispensável ausente ou nenhuma alternativa corresponde ao resultado.

Somente questões `SOLVED_AI` com alta confiança ou, preferencialmente, `VERIFIED` podem entrar no sistema como autocorrigíveis.

Questões `AMBIGUOUS` e `INVALID` NÃO devem ser usadas como exercícios autocorrigíveis até serem corrigidas.

---

# 3. NÃO ALTERAR AS ALTERNATIVAS SEM NECESSIDADE

O acervo possui questões com:

- 2 alternativas;
- 4 alternativas;
- 5 alternativas.

Não converter silenciosamente todas para quatro alternativas.

Preservar inicialmente a estrutura original.

Caso seja criada uma NOVA questão pedagógica baseada no conceito da original, ela poderá ter outra estrutura, mas deverá ser registrada como:

`adapted`
ou
`original_app_question`

e nunca apresentada como se fosse reprodução literal da questão-fonte.

---

# 4. QUESTÕES NORMAIS X QUESTÕES INTERATIVAS

Existirão dois formatos distintos.

## A. QUESTÃO NORMAL

Formato tradicional:

enunciado
→ alternativas
→ resposta do aluno
→ correção
→ explicação.

Nessa modalidade a resposta correta só deve ser mostrada DEPOIS da tentativa do aluno.

## B. QUESTÃO INTERATIVA

A questão interativa NÃO deve simplesmente mostrar o enunciado e pedir a alternativa final.

Ela deve decompor o raciocínio necessário para chegar à resposta.

O aluno deverá resolver a questão em ETAPAS.

O sistema deverá descobrir:

- se ele não sabe qual conceito usar;
- se não lembra a fórmula;
- se escolhe a fórmula errada;
- se substitui valores incorretamente;
- se erra unidades;
- se erra conversões;
- se erra álgebra;
- se erra aritmética;
- se interpreta errado o enunciado;
- se interpreta errado gráfico/esquema;
- ou se consegue fazer todas as etapas e erra apenas a resposta final.

---

# 5. EXEMPLO — CÁLCULO DE RESISTÊNCIA

Suponha uma questão que exija:

R = V / I

Não começar perguntando diretamente:

“Qual é a resistência?”

Transformar a resolução em etapas.

### ETAPA 1 — Identificar o método

Pergunta:

“Qual relação deve ser utilizada para determinar a resistência?”

Alternativas possíveis:

A. R = V / I
B. P = V × I
C. I = P / V
D. E = P × t
E. R = ρL / A

A alternativa correta depende da questão.

Se o aluno errar aqui, classificar o erro como algo semelhante a:

`FORMULA_SELECTION_ERROR`

ou:

`CONCEPT_SELECTION_ERROR`

---

### ETAPA 2 — Identificar os dados

Exemplo:

“Quais valores devem ser usados na fórmula?”

A. V = 24 V e I = 2 A
B. V = 2 V e I = 24 A
C. V = 24 V e I = 12 A
D. ...

Isso permite detectar:

`DATA_EXTRACTION_ERROR`

---

### ETAPA 3 — Substituir corretamente

Exemplo:

R = 24 / 2

Alternativas erradas podem representar erros plausíveis:

24 × 2
2 / 24
24 + 2
24 - 2

Isso permite detectar:

`FORMULA_SUBSTITUTION_ERROR`

---

### ETAPA 4 — Executar o cálculo

R = 12

Aqui avaliar:

`ARITHMETIC_ERROR`

---

### ETAPA 5 — Unidade

Perguntar:

“Qual unidade deve acompanhar o resultado?”

V
A
Ω
W

Isso permite detectar:

`UNIT_ERROR`

---

### ETAPA 6 — Resposta final

Somente agora apresentar as alternativas finais da questão original ou uma resposta final equivalente.

Assim, se o aluno errar, saberemos exatamente ONDE o processo falhou.

---

# 6. NÃO USAR SEMPRE A MESMA ESTRUTURA

Nem toda questão precisa começar escolhendo uma fórmula.

A decomposição deve seguir o raciocínio natural da questão.

Exemplos:

## Questão conceitual

Pode seguir:

identificar fenômeno
→ distinguir conceitos semelhantes
→ aplicar conceito ao cenário
→ responder.

## Circuito elétrico

Pode seguir:

identificar topologia
→ localizar elementos relevantes
→ escolher lei/princípio
→ determinar grandezas intermediárias
→ calcular
→ verificar unidade
→ resposta.

## Comandos elétricos

Pode seguir:

identificar componente
→ determinar estado dos contatos
→ seguir lógica do circuito
→ determinar bobina energizada
→ identificar consequência
→ resposta.

## Segurança / NR

Pode seguir:

identificar situação de risco
→ identificar princípio normativo aplicável
→ eliminar alternativas incompatíveis
→ selecionar procedimento correto.

## Gráfico

Pode seguir:

identificar eixos
→ identificar escala
→ localizar ponto/região
→ interpretar relação
→ chegar à conclusão.

## Diagrama ou imagem

Pode seguir:

identificar componentes
→ identificar conexões
→ interpretar função
→ determinar comportamento.

A IA deve escolher o MELHOR caminho pedagógico para cada questão.

---

# 7. ALTERNATIVAS ERRADAS DEVEM SER INTELIGENTES

Não criar distratores absurdos apenas para preencher opções.

As alternativas erradas devem representar erros que alunos realmente poderiam cometer.

Exemplos:

- fórmula semelhante, mas inadequada;
- inversão de numerador e denominador;
- unidade errada;
- valor retirado do lugar errado;
- erro de conversão;
- associação em série confundida com paralelo;
- contato NA confundido com NF;
- potência confundida com energia;
- tensão de linha confundida com tensão de fase;
- interpretação incorreta de uma curva;
- regra de segurança parecida, porém inaplicável ao contexto.

Cada alternativa errada poderá carregar internamente um `error_tag`.

Exemplo:

```json
{
  "text": "R = I / V",
  "correct": false,
  "error_tag": "FORMULA_INVERSION"
}
```

---

# 8. TAXONOMIA DE ERROS DO ALUNO

Criar uma taxonomia consistente.

Começar pelo menos com:

`CONCEPT_SELECTION_ERROR`

`FORMULA_RECALL_ERROR`

`FORMULA_SELECTION_ERROR`

`FORMULA_INVERSION`

`DATA_EXTRACTION_ERROR`

`WRONG_VALUE_SELECTION`

`UNIT_ERROR`

`UNIT_CONVERSION_ERROR`

`ALGEBRA_ERROR`

`ARITHMETIC_ERROR`

`SIGN_ERROR`

`DIAGRAM_INTERPRETATION_ERROR`

`GRAPH_INTERPRETATION_ERROR`

`SERIES_PARALLEL_CONFUSION`

`COMPONENT_IDENTIFICATION_ERROR`

`SEQUENCE_LOGIC_ERROR`

`SAFETY_RULE_ERROR`

`FINAL_ANSWER_ERROR`

`CARELESS_ERROR`

Não limitar o sistema a essa lista. Criar novos códigos quando pedagogicamente necessário, mas evitar duplicar códigos equivalentes.

---

# 9. PERFIL DE APRENDIZAGEM

O objetivo futuro não é apenas dizer:

“Você acertou 70%.”

Queremos conseguir concluir coisas como:

- domina conceitos, mas erra cálculos;
- entende cálculo, mas esquece fórmulas;
- dificuldade recorrente com conversão de unidades;
- confunde circuitos série/paralelo;
- tem dificuldade de interpretar diagramas;
- consegue resolver matematicamente, mas extrai valores errados do enunciado;
- erra principalmente questões normativas;
- tem dificuldade em leitura de gráficos.

Por isso cada etapa precisa registrar:

- habilidade avaliada;
- resposta dada;
- resposta correta;
- tipo de erro;
- dificuldade;
- tempo;
- quantidade de tentativas;
- uso de dica.

---

# 10. FEEDBACK NÃO DEVE ENTREGAR A RESPOSTA IMEDIATAMENTE

Se o aluno errar uma etapa, preferir feedback progressivo.

Exemplo:

Primeiro erro:

“Observe quais grandezas foram fornecidas e qual grandeza está sendo procurada.”

Segundo erro:

“Você precisa relacionar tensão, corrente e resistência.”

Somente depois, se necessário:

“A relação adequada é R = V/I.”

O sistema deve ensinar sem transformar cada erro em revelação instantânea da solução completa.

---

# 11. HINT LEVELS

Preparar cada etapa, quando fizer sentido, para suportar:

`hint_1`
orientação conceitual leve.

`hint_2`
orientação mais específica.

`hint_3`
indicação quase explícita do procedimento.

`solution`
resolução detalhada, apresentada apenas após as regras pedagógicas permitirem.

---

# 12. EXPLICAÇÃO FINAL

Depois que a questão terminar, gerar uma resolução consolidada.

Ela deve explicar:

- por que a resposta correta está correta;
- quais conceitos foram utilizados;
- cálculos;
- fórmulas;
- unidades;
- interpretação física/técnica;
- por que os distratores principais estão errados.

Não mostrar essa solução completa antes da tentativa quando a atividade estiver em modo avaliativo/interativo.

---

# 13. VALIDAÇÃO TÉCNICA

Para questões selecionadas, consultar quando necessário:

- dossiês temáticos;
- livros;
- normas;
- documentação técnica;
- fórmulas consolidadas;
- fontes confiáveis disponíveis no projeto.

Uma questão não se torna correta simplesmente porque a IA conseguiu elaborar uma explicação plausível.

Quando existir dúvida, marcar a dúvida.

Não fabricar certeza.

---

# 14. QUESTÕES DEPENDENTES DE IMAGEM

Questões sem texto ou com informação essencial em imagem não devem ser descartadas automaticamente.

Primeiro verificar:

- imagem associada;
- esquema;
- gráfico;
- tabela;
- diagrama;
- símbolo.

Se a imagem estiver indisponível e for indispensável:

`validation_status = INVALID_IMAGE_MISSING`

ou equivalente.

Se for possível reconstruir corretamente a informação usando o material disponível, registrar que houve adaptação.

---

# 15. USO DE OCR

OCR pode ajudar a recuperar texto, mas NÃO é autoridade técnica.

Resultados de OCR contendo:

- fórmulas;
- expoentes;
- subscritos;
- sinais;
- unidades;
- símbolos elétricos;
- números decimais

devem ser conferidos.

Nunca transformar automaticamente OCR em resposta validada.

---

# 16. CIRCUITOS E GRÁFICOS

Para conteúdo original do aplicativo:

- Schemdraw pode gerar esquemas estáticos;
- Matplotlib pode gerar gráficos e curvas;
- SVG/Canvas pode ser usado para circuitos manipuláveis;
- KaTeX/MathJax para matemática.

Mas o desenho visual NÃO deve representar sozinho a lógica.

Separar:

`visual representation`

de:

`electrical/logical model`.

Em atividades interativas, terminais, nós, estados, contatos e conexões devem possuir representação lógica própria.

---

# 17. QUESTÕES INTERATIVAS DE CIRCUITOS

Quando adequado, não limitar a interação a alternativas de texto.

Podemos posteriormente criar atividades como:

- selecionar o componente correto;
- clicar no ponto de medição;
- selecionar quais contatos estão fechados;
- indicar o sentido da corrente;
- montar sequência lógica;
- arrastar instrumento para ponto correto;
- selecionar terminais;
- completar ligação;
- escolher escala do multímetro;
- interpretar estado de relé/contator;
- identificar falha em circuito.

O motor pedagógico deve permitir esse tipo de expansão.

---

# 18. ORIGINAL, ADAPTADA E AUTORAL

Manter separado:

`source_question`
questão de referência externa.

`adapted_question`
questão adaptada pedagogicamente.

`original_app_question`
questão criada especificamente para o aplicativo.

Registrar origem.

Não apresentar material adaptado como reprodução certificada da fonte.

---

# 19. ESTRUTURA DE DADOS SUGERIDA

Para cada questão convertida, gerar algo conceitualmente semelhante a:

```json
{
  "id": "S01-4.4-Q001",
  "source_id": "ID_ORIGINAL",
  "module": "S01",
  "topic": "4.4",
  "type": "interactive",
  "validation_status": "VERIFIED",
  "confidence": 0.98,
  "source_kind": "adapted_question",

  "statement": "...",

  "skills": [
    "ohms_law",
    "data_extraction",
    "arithmetic",
    "units"
  ],

  "steps": [
    {
      "id": "step_1",
      "objective": "select_formula",
      "prompt": "...",
      "options": [],
      "correct_option": "...",
      "error_tags": {},
      "hints": []
    }
  ],

  "final_answer": "...",

  "solution": {
    "summary": "...",
    "steps": []
  },

  "references": [],

  "editorial_notes": []
}
```

A estrutura exata poderá ser ajustada ao código existente.

---

# 20. GERAÇÃO PROGRESSIVA POR MÓDULO

NÃO criar milhares de questões agora.

Quando iniciarmos um módulo:

1. identificar exatamente os objetivos daquele módulo;
2. localizar questões candidatas;
3. descartar falsos positivos temáticos;
4. selecionar apenas questões pedagogicamente úteis;
5. resolver as selecionadas;
6. validar seus gabaritos;
7. classificar dificuldade e habilidade;
8. decidir se cada uma será normal ou interativa;
9. transformar as interativas em etapas;
10. criar feedback e diagnóstico;
11. revisar;
12. integrar ao módulo.

Assim construímos o banco validado progressivamente.

---

# 21. COBERTURA PEDAGÓGICA

Não selecionar questões apenas porque existem muitas sobre aquele assunto.

A seleção deve buscar cobertura equilibrada de:

- conceitos fundamentais;
- aplicação;
- interpretação;
- cálculo;
- diagnóstico;
- segurança;
- leitura de diagramas;
- problemas práticos.

Evitar dezenas de questões quase iguais.

IDs diferentes não garantem diversidade pedagógica.

---

# 22. DUPLICIDADE SEMÂNTICA

Além de duplicatas exatas, procurar questões que testam essencialmente a mesma habilidade com pequenas mudanças numéricas ou textuais.

Quando houver muitas equivalentes:

- selecionar as melhores;
- usar algumas como treino;
- algumas como revisão;
- algumas como avaliação;
- não inundar o módulo com repetições.

---

# 23. FALSOS POSITIVOS TEMÁTICOS

Não confiar exclusivamente em busca lexical.

Exemplo já identificado:

`bloqueio`

pode significar bloqueio elétrico de segurança ou “válvula de bloqueio”.

Verificar contexto antes de associar a questão ao módulo.

A classificação temática deve ser conceitual.

---

# 24. DIFICULDADE

Classificar cada questão considerando o raciocínio realmente exigido.

Sugestão:

`FOUNDATIONAL`
reconhecimento ou aplicação direta.

`BASIC`
uma ou duas etapas simples.

`INTERMEDIATE`
combinação de conceitos ou cálculos.

`ADVANCED`
várias etapas, interpretação ou integração de conceitos.

`CHALLENGE`
problema complexo ou diagnóstico.

Não usar apenas tamanho do enunciado como medida de dificuldade.

---

# 25. PRÉ-REQUISITOS

Para cada questão interativa, identificar quando possível:

- conhecimentos necessários;
- fórmulas;
- conceitos;
- habilidades matemáticas;
- leitura de diagramas;
- normas relacionadas.

Isso permitirá futuramente evitar apresentar atividades para as quais o aluno ainda não possui base.

---

# 26. RESULTADO ESPERADO AO TRABALHAR CADA MÓDULO

Antes de modificar arquivos de produção, apresente:

### A. Questões candidatas

ID
tema
subtema
motivo da seleção.

### B. Questões rejeitadas

ID
motivo.

Exemplos:

falso positivo;
imagem ausente;
ambígua;
redundante;
fora do nível;
gabarito não validável.

### C. Gabaritos resolvidos

Para cada selecionada:

resposta;
resolução;
nível de confiança;
status de validação.

### D. Conversão pedagógica

Definir:

normal
ou
interativa.

### E. Para cada interativa

Mostrar:

objetivo de cada etapa;
pergunta;
alternativas;
resposta correta;
erro diagnosticado em cada alternativa;
feedback;
hints;
resolução final.

Somente depois integrar ao banco do aplicativo.

---

# REGRA DE OURO

Não quero simplesmente transformar uma prova tradicional em uma prova digital.

Quero transformar as questões em um SISTEMA DE APRENDIZAGEM E DIAGNÓSTICO.

Uma questão interativa deve permitir descobrir:

“O aluno não sabe a resposta.”

E principalmente:

“POR QUE ele não sabe a resposta?”

O sistema deve conseguir diferenciar:

não conhece o conceito;
não lembra a fórmula;
escolheu fórmula errada;
não soube extrair os dados;
errou substituição;
errou unidade;
errou conta;
interpretou diagrama incorretamente;
ou apenas cometeu um erro final.

Esse diagnóstico será usado posteriormente para gerar feedback individual, revisão direcionada e exercícios específicos para as dificuldades reais do aluno.

Não sacrificar precisão técnica para gerar conteúdo em grande quantidade.

QUALIDADE E VALIDAÇÃO TÊM PRIORIDADE SOBRE VOLUME.

Eu acrescentaria uma decisão de arquitetura desde já: **guardar a alternativa errada escolhida com um `error_tag`, e não apenas `correct: false`**. Isso é o que permitirá, depois de 20 ou 50 exercícios, o sistema dizer algo realmente útil como “você acerta a escolha da fórmula, mas está errando frequentemente conversão de mA para A”, em vez de simplesmente mostrar uma porcentagem de acertos.