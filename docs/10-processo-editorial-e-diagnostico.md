# Processo editorial e diagnóstico — 06/10/2026

Requisitos recebidos nos dois anexos, preservados em `editorial/`. Este documento orienta o próximo incremento; não publica questões nem implementa avaliações. A etapa atual é preparação, sem alterar o banco externo ou o código de produção.

## Três processos independentes

1. Recuperação: enunciado, alternativas originais, imagens, tabelas, unidades, origem e falhas. Um gabarito nulo permanece UNRESOLVED; imagem indispensável ausente requer inspeção antes de invalidar. OCR é ferramenta de recuperação, não evidência de correção.
2. Validação: resolução independente de cada item selecionado, exame de todas as alternativas, premissas, ambiguidade, cálculo/referências e confiança justificada. Não preencher 9.791 respostas automaticamente. Registrar resposta inferida separada do gabarito recuperado.
3. Transformação: decidir normal/interativa, definir habilidades, passos, distratores plausíveis, feedback, dicas e resolução final. Adaptação cria outra identidade/versionamento; não muda silenciosamente a fonte.

## Estados editoriais e liberação

- UNRESOLVED: não analisado; sem correção automática.
- SOLVED_AI: solução independente documentada; ainda sem segunda verificação.
- VERIFIED: evidência registrada de verificação técnica, não simples autodeclaração.
- AMBIGUOUS: interpretação/informação insuficiente; não autocorrigível.
- INVALID: defeito impeditivo confirmado; não autocorrigível.

Imagem essencial ausente é motivo `IMAGE_MISSING` dentro de INVALID, evitando criar um estado paralelo incompatível com a lista. Não invalidar todo item sem enunciado textual: sua informação pode estar na imagem.

Política recebida permite SOLVED_AI de alta confiança no treino autocorrigível. Se usado, deve ter solução completa, premissas explícitas, nenhuma dependência essencial faltante e aviso de resposta inferida ainda não verificada. VERIFIED é preferível. Para avaliação de domínio, manter somente VERIFIED. Alta confiança não transforma SOLVED_AI em VERIFIED; não inventar probabilidades como 0,98 sem calibração. Usar faixa LOW/MEDIUM/HIGH com justificativa e evidências. Confiança editorial e certeza declarada pelo aluno são campos distintos.

Rever a validação se mudar enunciado, imagem, alternativas, norma ou parâmetros. Cada adaptação também precisa de solução/verificação própria. Encontrar um gabarito externo depois exige reconciliar divergências, não sobrescrever a resolução silenciosamente.

## Origem e formatos

`source_question`, `adapted_question`, `original_app_question` identificam autoria/proveniência; `normal`, `interactive` identificam experiência. São eixos diferentes. Preservar alternativas de 2/4/5 opções da fonte. Uma nova atividade pode ter outro formato, explicitamente registrado. Não converter uma sequência V/F com cinco alternativas finais em item binário sem registrar adaptação.

Questão normal: tentativa → correção → explicação; nenhuma solução antes da tentativa. Questão interativa: etapas adequadas ao raciocínio natural, não uma receita fixa de fórmula para todos os assuntos. Cálculo, procedimento, leitura de diagrama e comandos têm percursos diferentes. A quantidade de passos deve servir ao diagnóstico, sem fragmentação artificial.

## Erros e evidências

Taxonomia inicial em `../data/editorial/taxonomia-erros.json`, incluindo códigos dos anexos e FORMULA_SUBSTITUTION_ERROR. Distratores carregam tags e justificativa pedagógica. Registrar alternativa efetivamente escolhida, versão da questão e etapa, habilidade, dificuldade, tentativa, tempo, dica/solução vista e resposta correta vigente.

Uma escolha pode ter várias causas. Tags são hipóteses de diagnóstico, não prova de “exatamente” qual processo mental falhou. Não afirmar esquecimento de fórmula com base apenas em reconhecimento de alternativa: avaliar recordação em uma tarefa apropriada. CARELESS_ERROR não deve ser atribuído automaticamente. Certeza alta em um erro é indício de concepção incorreta, a confirmar com tarefas diversas; não rotular definitivamente o aluno a partir de um item.

Separar tags de erro, resultados positivos e sinais derivados. FALSE_STATEMENT_IDENTIFIED é resultado positivo, não erro. HIGH_CONFIDENCE_MISCONCEPTION é sinal derivado de resposta errada + certeza alta. UNJUSTIFIED_GUESS exige declaração/evidência, não inferência só por tempo de resposta.

## Feedback e dicas

Três níveis opcionais: orientação conceitual, orientação específica e procedimento quase explícito. No primeiro erro não revelar a resposta final; guardar cada tentativa imutável. A solução completa pode ser solicitada após tentativa no treino; isso registra tarefa assistida, não domínio independente. Em avaliação, explicações ficam para após envio/finalização. Regras de revelação pertencem à sessão, não apenas à ocultação visual de um botão.

## Verdadeiro/Falso

TF_L1: classificação simples quando pedagogicamente suficiente; acerto isolado não comprova domínio. TF_L2: classificação + justificativa. TF_L3: classificação + localização + correção. TF_L4: raciocínio por etapas. TF_L5: aplicação em cenário/diagrama/simulação.

Fluxo recomendado: afirmação → V/F e certeza (Tenho certeza/Acho que sei/Estou chutando, ou não informado) → compromisso bloqueado → justificativa neutra → localização/correção/aplicação → retorno consolidado. Não revelar acerto antes da justificativa. Ambos V e F têm segunda etapa; evitar pistas pelo fluxo. Se uma ramificação revelar que a afirmação é falsa, preservar a primeira resposta bloqueada e registrar a pista como ajuda para as etapas seguintes.

Localização pode aceitar múltiplos trechos. No exemplo do paralelo, tanto a corrente obrigatoriamente igual quanto a tensão dividida são problemáticos; a interface não deve exigir um único trecho. Verdades podem exigir condição/princípio ou aplicação equivalente, sem inventar uma parte errada para corrigir.

V/F/Depende é formato de item autoral/adaptado com condições explícitas, nunca alteração silenciosa de item-fonte. Palavras “sempre/nunca” devem ser avaliadas pelo conceito e contexto, não ensinadas como heurística de chute. Múltiplas proposições são classificadas individualmente; aprofundamento adaptativo preserva o resultado de cada uma.

## Pontuação e perfil

Manter classificação correta e raciocínio correto separados. O acerto com justificativa errada produz FALSE_REASONING_WITH_CORRECT_ANSWER e não domínio completo. Pesos 0,30C + 0,30J + 0,20L + 0,20A são proposta, não decisão universal ou critério oficial SAEP. Definir pesos por atividade e normalizar somente entre dimensões realmente avaliadas; jamais premiar uma dimensão inexistente. TF_L1 não recebe selo de domínio pleno só por pontuação interna de 100%.

Tentativa independente, repetição assistida e resposta após solução são evidências diferentes. Não contar tentativas repetidas como itens novos dominados. Separar famílias semanticamente equivalentes entre treino/revisão/avaliação. Perfil deve informar quantidade de evidências e recorrência em tarefas diversas, sem fabricar certeza estatística. Explicação de raciocínio em texto livre não pode ser certificada por simples clique de confirmação.

## Pacote de revisão antes da produção

Para cada módulo, apresentar fora do banco publicado:

A. Candidatas: ID, tema, motivo e objetivos cobertos.
B. Rejeitadas: motivo e estado; redundância não torna a fonte INVALID.
C. Resoluções: resposta proposta, solução auditável, premissas, evidências, status e confiança.
D. Transformação: normal/interativa, autoria e relação com a fonte.
E. Etapas: objetivo, prompt, opções/ações, resposta, tags, feedback/dicas e solução final.

Depois integrar apenas o pacote revisado e elegível. S01 continua próximo módulo, mas nenhum item foi selecionado/resolvido nesta consolidação. Fontes normativas devem ser verificadas na edição vigente ao preparar o conteúdo. Não preencher respostas ou fabricar candidatos para aparentar entrega.

## Contratos preparados

`data/editorial/contrato-editorial.schema.json` descreve recuperação/validação de itens selecionados. A tabela de candidatos será criada por módulo, não aplicada em massa ao acervo. O esquema valida estrutura e algumas condições; não valida verdade técnica nem habilita publicação sozinho. As regras de sessão, domínio e validação independente deverão ser implementadas com o primeiro exemplo, antes de qualquer integração.

Representação visual permanece separada do modelo lógico: SVG/Schemdraw/Matplotlib para figura, nós/estados/conexões para comportamento, KaTeX/MathJax para fórmulas. Não basta a imagem parecer certa.
