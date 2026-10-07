# Requisitos e critérios de aceite

## Requisitos funcionais

| ID | Comportamento | Verificação prevista |
|---|---|---|
| RF01 | Catálogo dos 35 subtemas, complementos e pré-requisitos; filtros por área, dificuldade e erro | Todos os IDs do mapa ligados ao catálogo; lacunas de matriz visíveis |
| RF02 | Ciclo explicação curta → laboratório aplicável → perguntas por etapas → erros | Fluxo completo do módulo motores no MVP |
| RF03 | Cálculos paramétricos com valores e distratores calculados, quatro alternativas por etapa | Mesma semente reproduz dados; uma única resposta correta por etapa; resultado com unidade |
| RF04 | Feedback específico, nova tentativa e dica opcional | Um feedback por distrator; dica e tentativas registradas |
| RF05 | Laboratório: pares de bobinas, placa, tensão da rede e ligações de força/comando | Terminais conectáveis por toque, clique e teclado; estado rastreável |
| RF06 | Segurança precede mudanças de ligação; sequência completa validada com fonte | Ordem insegura reconhecida no cenário; procedimento não reduzido às três primeiras etapas |
| RF07 | Falhas de ligação geram efeitos coerentes: partida, rotação, corrente, calor e proteção | Casos de catálogo e regras verificadas; nenhuma consequência aleatória sem causa |
| RF08 | Modos estudo e prova | Estudo explica causas; prova adia explicação até entrega |
| RF09 | Som opcional com equivalentes visuais e legendas | Toda falha compreensível com som desligado |
| RF10 | Mini-simulado contextualizado com cronômetro e quatro ou cinco alternativas por perfil | Perfil informado antes de começar; correção e desempenho por tema |
| RF11 | Progresso por subtema, histórico de erros e fila de revisão | Reabertura offline mantém resultados; versões do conteúdo preservadas |
| RF12 | Backup/importação local do progresso | Round-trip, validação de versão e recuperação de arquivo inválido |
| RF13 | Baixar módulos e verificar disponibilidade offline | Módulo só indicado como disponível após assets e dados completos |
| RF14 | Fontes, revisão técnica e status [VERIFICAR] por conteúdo | Fonte rastreável; norma pendente não publicada como fato certificado |

## Requisitos não funcionais

Atualização de 04/10/2026: RF15 — representar motores, componentes e ferramentas usados em cada tema com assets detalhados, tecnicamente revisados e partes próprias para interação/animação; RNF10 — entregar primeiro um exemplo pequeno e executável do tema inicial, revisar com o usuário e só então ampliar em incrementos. Critérios e obtenção de assets em [07-assets-e-revisao-visual.md](07-assets-e-revisao-visual.md).

| ID | Critério | Limite/observação |
|---|---|---|
| RNF01 | Android e PC pelo navegador, sem instalação pesada | Adicionar à tela inicial é opcional; instalação PWA não é requisito para estudar |
| RNF02 | Offline após primeira carga e download do módulo | Primeiro acesso precisa obter os arquivos; nenhum servidor remoto durante estudo |
| RNF03 | Interface por teclado, toque e leitor de tela | Foco visível; conectores também operáveis por seleção de origem/destino |
| RNF04 | Legibilidade e feedback independente de cor/áudio | Texto, formas e rótulos; contraste e zoom verificados |
| RNF05 | Desempenho em aparelho modesto | Orçamentos propostos em 06; validar em dispositivo real, além de emulação |
| RNF06 | Conteúdo separado do código, versionado e validado | JSON Schema e verificações semânticas no build |
| RNF07 | Dados pessoais locais por padrão | Nenhuma conta, telemetria ou sincronização obrigatória no escopo proposto |
| RNF08 | Atualização sem apagar estudo ou interromper prova | Migração versionada, backup e atualização fora da sessão |
| RNF09 | Manutenção por uma pessoa | Dependências pequenas, domínio testável sem interface; README de autoria de conteúdo |

## Escopo dos motores

O MVP será uma fatia completa com partida direta e motor de seis pontas, ampliada gradualmente para monofásico, estrela/triângulo, estrela-triângulo, reversão e diagnóstico. Motores de 9/12 pontas e Dahlander permanecem no roadmap; exigem esquemas e regras próprias, sem reaproveitar fechamento de seis pontas por suposição. Identificação de polaridade será uma atividade distinta da continuidade, baseada em procedimento técnico validado.

O pedido de corrente, aquecimento e falhas coerentes será atendido conforme fidelidade escolhida. Onde faltarem parâmetros, usar indicadores qualitativos rotulados; nunca apresentar um número arbitrário como medição real. Casos quantitativos dependem de fonte e de testes.

## Critérios de encerramento do MVP

Fluxo explicação/laboratório/etapas/mini-simulado/progresso completo; fonte e testes para todas as regras liberadas; uso offline verificado; feedback sem áudio; interação por teclado; backup funcional; README para executar e adicionar conteúdo. A aprovação da Fase 3 não equivale a aprovação automática da Fase 4.
