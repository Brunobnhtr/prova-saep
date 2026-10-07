# Modelo de dados

## Conteúdo separado do código

JSON contém catálogo, módulos, fontes, cenários e templates de questões. Texto de lição usa Markdown restrito, sem HTML executável. Código implementa geradores registrados por ID; os templates só indicam parâmetros, faixas e identificadores. Não executar funções serializadas, scripts embutidos ou fórmulas arbitrárias com eval.

Schemas propostos em `schemas/`: módulo, template de questão e backup de progresso. O exemplo em `exemplos/modulo-motores.json` é um contrato de metadados em rascunho, não conteúdo técnico liberado. [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation).

| Entidade | Campos centrais | Regra |
|---|---|---|
| Module | id, contentVersion, title, subthemeIds, prerequisites, sources, technicalStatus, lessons, labs, questionTemplates | Versão imutável ao salvar sessão; subtemas precisam existir no mapa |
| Source | id, title, locator, verificationStatus | Página/trecho/edição rastreável; pendência explícita |
| Lesson | id, markdownPath, sourceIds | Caminho local permitido; nenhum acesso remoto para estudar |
| Lab | id, scenarioId, family, sourceIds | Família precisa de regras/modelo registrado e revisão |
| QuestionTemplate | id, subthemeId, kind, generatorId, parameterBounds, optionCount, sourceIds | Etapas: 4 opções; simulado: perfil 4 ou 5; resposta gerada pelo domínio |
| QuestionInstance | templateId, templateVersion, generatorVersion, seed, parameters, steps, optionPermutation | Materializada ao iniciar; valores mantidos durante retomada |
| Attempt | id, instanceId, stepId, selectedOptionId, correct, hints, attemptIndex, occurredAt | Registrar erro específico e não só nota final |
| ReviewCard | subthemeId, dueAt, intervalDays, lapses, schedulerVersion | Agendamento por fonte de erro; clock/versão explícitos |
| ExamSession | id, profileId, startedAt, deadlineAt, status, instances, answers | Não recalcular parâmetros ou permutação ao reabrir |
| LabSession | scenarioVersion, modelVersion, mode, state, connections | Salvar marcos, não todos os frames |
| ProgressBackup | schemaVersion, exportedAt, moduleVersions, attempts, reviews, sessions | Migrações compatíveis e importação transacional |

## Integração com a Fase 2

Os IDs F01–V01 e demais IDs do mapa são as chaves de subtema; não IDs da matriz oficial. `matrixItemId` deve aceitar null e vir acompanhado de status “pendente” até confirmação. Cruzamentos antigos do acervo ficam em dados de pesquisa, sem convertê-los em código oficial do módulo por inferência.

## Armazenamento proposto

IndexedDB para sessões, tentativas, revisão e configurações; Cache API para aplicação/arquivos do conteúdo. LocalStorage apenas para preferência simples de tema/áudio, se necessário, sem histórico volumoso. Interface de repositório permite usar API nativa ou wrapper pequeno depois; essa biblioteca não é requisito arquitetural.

O backup distingue versão de schema, conteúdo, gerador, simulador e scheduler. Mudanças de conteúdo não reescrevem respostas antigas. Ao remover conteúdo, os resultados continuam com título/versão da sessão, sem quebrar a interface.

## Validações além do schema

IDs únicos; referências existentes; pré-requisitos sem ciclos; min <= max; quantidade de opções coerente; gerador/modelo registrados; unidade suportada; uma resposta correta; distratores distintos após arredondamento; fontes completas para conteúdo liberado; arquivo de lição/SVG existente; pacote sem provas reais. Schemas verificam estrutura, não certificam física ou norma.
