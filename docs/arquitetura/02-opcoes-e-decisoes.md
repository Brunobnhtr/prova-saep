# Opções de tecnologia e simulação

Status: aguardando escolha. Todos os resultados de desempenho abaixo são expectativas de projeto, não medições.

## Stack

As três alternativas produzem uma aplicação web estática. Offline, SVG/Canvas, Web Audio e armazenamento local são capacidades do navegador integradas pelo projeto, não garantias automáticas de um framework. Vite documenta build e publicação estática. [Build do Vite](https://vite.dev/guide/build), [publicação estática](https://vite.dev/guide/static-deploy.html).

| Critério | A: React + TypeScript + Vite | B: TypeScript + DOM nativo + Vite | C: Svelte + TypeScript + Vite |
|---|---|---|---|
| Android/PC sem instalação | Navegador; compatibilidade a validar | Navegador; compatibilidade a validar | Navegador; compatibilidade a validar |
| Offline | Service worker e armazenamento adicionados | Mesma estratégia | Mesma estratégia |
| Áudio e animações | APIs do navegador; estado visual em componentes | APIs diretas; gerenciamento manual do DOM | APIs do navegador; componentes compilados |
| Aparelho modesto | Carregar por módulo; simulação fora de renders frequentes | Potencial menor custo de UI; medir | Potencial menor custo de UI; medir |
| Manter sozinho | Componentes facilitam telas/formulários; aprender hooks e estado | Menos ferramentas conceituais; mais disciplina para estados e atualizações | Templates concisos; aprender reatividade própria |
| Evolução dos 35 subtemas | Reuso explícito de explicação/etapas/laboratório | Reuso possível, exige convenções próprias | Bom reuso em componentes |
| Custo principal | Runtime e disciplina de efeitos/renders | Risco de DOM e estado se divergirem em telas complexas | Dependência de sintaxe e ecossistema específico |

**Recomendação A:** componentes para perguntas, instrumentos, progresso e acessibilidade reduzem repetição conforme o catálogo cresce. O domínio não dependerá de React. B é razoável se você preferir trabalhar diretamente com HTML/DOM; C é razoável se priorizar templates concisos e aceitar aprender Svelte. Documentação primária: [React](https://react.dev/learn), [TypeScript](https://www.typescriptlang.org/docs/handbook/intro.html), [Svelte](https://svelte.dev/docs/svelte/overview).

## Algoritmo da simulação

| Opção | Como funciona | Vantagem | Limitação |
|---|---|---|---|
| A: grafo de ligações + regras + estados | Nós representam terminais; arestas representam fios/chaves fechadas; regras reconhecem bobinas, tensões, topologia e sequência | Permite ligação livre e causas explicáveis; ligações equivalentes não dependem de desenho exato | Precisa de regras técnicas verificadas por família de motor; não resolve automaticamente toda rede elétrica |
| B: cenários apenas por regras | Lista de configurações e eventos previstos; resposta por cenário | Implementação inicial menor | Ligações livres combinatórias podem gerar casos sem cobertura; não comparar apenas uma lista de fios exata |
| C: análise fasorial + equivalente por fase | Resolve valores elétricos de redes suportadas e modelo do motor | Quantificação mais ampla em regime definido | Exige parâmetros, solver, convergência e domínio de validade; circuito equivalente em regime não representa sozinho toda dinâmica de partida/falha |

**Recomendação A:** cobre terminais livres e permite evolução. Regras validam conectividade elétrica e sequência, usando estados para segurança, operação e falhas. C pode ser um calculador restrito futuro, sem substituição silenciosa do modelo.

## Fidelidade

| Opção | Saídas | Custo e validade |
|---|---|---|
| A: intermediária pedagógica | Cálculos exatos apenas em modelos suportados; corrente/calor qualitativos em falhas; rotor, proteção e legendas coerentes | Exige fontes de cada regra; permite atingir o objetivo de diagnóstico sem inventar medidas |
| B: básica qualitativa | Mensagens, estado ligado/desligado, sentido e indicação de risco | Mais rápida; deixa limitada a exploração de corrente por fase e aquecimento |
| C: avançada quantitativa | Curvas temporais e valores por fase em cenários modelados | Mais parâmetros e validação; não é uma extensão gratuita das animações |

**Recomendação A:** amostras nominais podem usar placa; falhas sem parâmetros mostrarão “elevada”, “desequilibrada” e índice didático claramente identificado. Não prometer temperatura física ou tempo real para queima. Se você escolher C, revisaremos cronograma e fontes necessárias antes do MVP.

## Propostas de áudio e revisão

Áudio: síntese com Web Audio é a proposta inicial (assets menores e resposta contínua); gravações dão timbre mais realista, mas exigem licença/arquivos e podem aumentar downloads. As duas opções mantêm equivalente visual. A síntese é sinal didático, não reprodução acústica fiel. Iniciar após ação do usuário respeita a política de reprodução do navegador. [Boas práticas Web Audio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices).

Revisão: proposta inicial de intervalos configuráveis por regras simples e histórico de tentativas. Alternativas: algoritmo com fator de facilidade ou agendamento probabilístico com parâmetros/dados de treinamento. A regra simples é suficiente para iniciar e deve ser apresentada como heurística, sem prometer otimização científica. Esses detalhes podem ser ajustados na consolidação.
