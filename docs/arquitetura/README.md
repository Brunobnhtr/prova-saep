# Fase 3 - Proposta de arquitetura

Atualização de 04/10/2026: o usuário acolheu o conjunto recomendado e pediu início restrito à primeira prévia, com preparo seguro e assets provisórios identificados. React/TypeScript/Vite, grafo com regras/estados e fidelidade intermediária registrados; exemplo em [04-previa-01.md](../04-previa-01.md). A proposta histórica abaixo permanece como referência; ampliação aguarda revisão.

Data: 02/10/2026. Fase autorizada pelo usuário. **Status: proposta pronta para escolha de tecnologia, algoritmo e fidelidade; não é arquitetura aprovada nem aplicativo implementado.**

Recomendo uma aplicação web estática, preparada para uso offline, sem conta ou backend obrigatório. Conteúdo original em arquivos versionados, progresso no navegador e exportação de backup. As recomendações de stack e simulação abaixo ainda dependem de escolha explícita.

## Documentos

- [Assets de alta fidelidade e revisão por exemplos](07-assets-e-revisao-visual.md): requisito acrescentado em 04/10/2026; começar com uma prévia pequena de motores e revisar antes de ampliar.

- [Requisitos e critérios de aceite](01-requisitos.md).
- [Opções e decisões pendentes](02-opcoes-e-decisoes.md).
- [Componentes e fluxos](03-componentes.md).
- [Modelo de dados](04-modelo-dados.md), com schemas e exemplo em `schemas/` e `exemplos/`.
- [Simulação, perguntas, áudio e revisão](05-motores.md).
- [Offline, testes, desempenho e roadmap](06-entrega-e-qualidade.md).
- [ADRs propostos](adrs/README.md).

## Escolhas necessárias

| Decisão | Recomendação | Alternativas |
|---|---|---|
| Stack | React + TypeScript + Vite | TypeScript com DOM nativo + Vite; Svelte + TypeScript + Vite |
| Algoritmo da simulação | Grafo de ligações com regras e estados | Apenas cenários por regras; análise elétrica fasorial e circuito equivalente |
| Fidelidade | Pedagógica intermediária | Básica qualitativa; quantitativa avançada |

São escolhas separadas: o algoritmo identifica conectividade e condições; a fidelidade define quanto dos resultados é qualitativo ou quantitativo. Recomendo o conjunto da primeira coluna porque permite ligação livre de terminais, manutenção por módulos e respostas coerentes, sem exigir parâmetros elétricos ainda não disponíveis.

As comparações são avaliações de engenharia para este projeto, não benchmarks medidos. Os orçamentos de desempenho serão verificados na Fase 4. O suporte real do Android dependerá da versão do navegador; não foi prometida compatibilidade com todo Android antigo.

## Limites do planejamento

A Matriz de Referência integral e o currículo local ainda precisam de confirmação. Conteúdo com regra técnica pendente pode aparecer marcado no estudo, mas não entrar como resposta normativa certificada. Os 206 grupos do acervo servem como evidência de cobertura/estilo; a aplicação compartilhável receberá questões e diagramas originais.

Nenhuma dependência de aplicação foi instalada e nenhum esqueleto de app foi criado. A próxima ação é registrar as escolhas, consolidar os ADRs e encerrar a Fase 3 para aprovação antes do MVP.

## Resumo da proposta

1. Requisitos e critérios de aceite definidos com rastreabilidade ao pedido.
2. Três stacks comparadas; React/TypeScript/Vite recomendado, ainda pendente.
3. Grafo com regras e fidelidade intermediária recomendados, ainda pendentes.
4. Componentes, modelo de dados, schemas e exemplo documentados.
5. Questões por etapas, áudio equivalente visual, progresso e revisão previstos.
6. Estratégia offline, testes, riscos e roadmap documentados.
7. Nenhum aplicativo implementado ou tecnologia aprovada por inferência.
8. Aguardando escolhas para consolidar e concluir a Fase 3.
