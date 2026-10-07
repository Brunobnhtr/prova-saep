# Registro de decisões arquiteturais

Cada ADR terá status proposta → aceita ou substituída. Data 02/10/2026. Ainda não há decisão aceita por escolha presumida.

| ADR | Questão | Recomendação proposta | Status |
|---|---|---|---|
| 001 | Stack e distribuição | React/TypeScript/Vite; aplicação estática preparada para offline | Aguarda escolha |
| 002 | Algoritmo de simulação | Grafo de ligações com regras e estados | Aguarda escolha |
| 003 | Fidelidade | Intermediária pedagógica com números apenas onde validados | Aguarda escolha |
| 004 | Dados e persistência | Conteúdo JSON versionado, IndexedDB e backup local | Proposta; consolidar na aprovação da arquitetura |
| 005 | Áudio e feedback | Síntese opcional e equivalente visual obrigatório | Proposta; gravações permanecem alternativa |
| 006 | Revisão e tentativas | Histórico detalhado e regra simples versionada inicialmente | Proposta; algoritmos alternativos podem ser escolhidos |

Contexto, alternativas, consequências e fontes das três primeiras decisões estão em [02-opcoes-e-decisoes.md](../02-opcoes-e-decisoes.md). Dados em [04-modelo-dados.md](../04-modelo-dados.md); áudio/revisão em [05-motores.md](../05-motores.md). Após a escolha, escrever um ADR por decisão com alternativa selecionada, razão e consequências finais. Não registrar recomendações como aceita antes da resposta.
