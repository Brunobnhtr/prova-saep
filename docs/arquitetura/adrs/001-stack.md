# ADR 001 - Stack da aplicação

Data: 02/10/2026. Status: **proposta; aguardando escolha do usuário**.

Contexto: muitos módulos com explicações, perguntas por etapas, instrumentos e progresso; Android modesto e PC; manutenção individual. Distribuição estática/offline proposta, sem backend obrigatório.

Alternativas: A React/TypeScript/Vite; B TypeScript/DOM nativo/Vite; C Svelte/TypeScript/Vite. Comparação detalhada em [opções](../02-opcoes-e-decisoes.md).

Recomendação: A. Componentes reutilizáveis para diferentes módulos e domínio independente da interface. Consequências: aprendizado de estado/efeitos, dependências de UI e necessidade de controlar renders. Não há benchmark local que certifique desempenho. B reduz dependência do framework, mas exige convenções de DOM; C oferece templates concisos e outra sintaxe reativa.

Decisão final: pendente. Não gerar aplicativo antes de registrar a escolha e a aprovação da fase.
