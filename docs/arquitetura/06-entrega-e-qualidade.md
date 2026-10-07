# Offline, qualidade, riscos e roadmap

## Funcionamento offline

Aplicação e módulo inicial em cache; demais módulos baixados sob demanda. Manifesto de pacote declara versão, arquivos, tamanho e hashes. Baixar para cache temporário, validar o pacote inteiro, então promover a versão ativa. Falha ou falta de espaço conserva a versão anterior. Não remover o pacote usado por sessão em andamento.

O primeiro acesso precisa carregar os arquivos pela rede ou servidor local apropriado. Service workers exigem HTTPS, com exceção de desenvolvimento em localhost; abrir index.html por file:// não oferece a mesma estratégia. [Uso de service workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers).

Cache de interface/conteúdo e IndexedDB de progresso têm ciclos diferentes. Atualização de assets não apaga tentativas. Antes de migrar dados, produzir backup local e transação com rollback. Notificar atualização disponível e aplicá-la fora do laboratório/prova; não ativar nova versão no meio de uma sessão.

Dados do navegador podem ser removidos por quota, política de armazenamento ou limpeza do usuário. Solicitar persistência quando disponível, mostrar uso/espaço estimado e disponibilizar exportação manual; sem prometer armazenamento permanente. [Quotas e remoção de dados](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria).

## Desempenho e acessibilidade

Orçamentos propostos, a medir na Fase 4: JavaScript inicial comprimido até 250 KB; pacote inicial de motores até 5 MB sem livros/provas; resposta comum ao toque até 100 ms na maioria das interações do aparelho-alvo; renderização adaptável entre 20 e 30 fps durante laboratório. Essas metas podem ser revistas com medições, sem transformar médias em garantia absoluta.

Carregar uma lição/laboratório por vez. Usar SVG para diagramas e terminais; Canvas apenas se uma animação justificar. Não atualizar toda a interface a cada frame; estado do domínio em passos controlados, renderização via requestAnimationFrame, áudio por eventos. Pausar renderização invisível. Worker só se perfil de desempenho revelar cálculo que bloqueia a UI.

Verificar teclado, leitor de tela, zoom a 200%, redução de movimento, alvos de toque, contraste, legendas e modos com som desligado. Arrastar fios sempre terá alternativa “selecionar terminal de origem → destino”. Informação de cor terá texto/símbolo. O dispositivo Android e navegador-alvo ainda não foram informados.

## Estratégia de testes

| Camada | Casos relevantes | Evidência de aceite |
|---|---|---|
| Conteúdo | Schema, IDs, referências, fontes, ciclos e arquivos | Build rejeita pacote incoerente |
| Cálculos | Exemplos resolvidos independentes, unidades, arredondamento, limites de parâmetros | Resultado esperado e uma única opção correta |
| Simulação | Fase ausente, tensão incompatível, fechamentos, sequência, intertravamento, segurança | Causa e efeito corretos com casos técnicos conhecidos |
| Propriedades | Ordem dos fios/nome dos nós não muda conectividade; sem progressão de calor desenergizado no modelo aplicável | Testes reproduzíveis por semente |
| Progresso | Atualização, exportação/importação, quota e migração | Dados anteriores recuperáveis; erro explícito |
| E2E | Fluxo completo, reload offline, prazo de prova, modos e teclado | Passa no build de produção em contexto seguro |
| Dispositivo real | Toque, legibilidade, áudio, memória e bateria | Registro do aparelho/navegador; emulação não basta |

Ferramentas propostas para a stack web: testes unitários com Vitest e E2E com Playwright; escolher versões compatíveis ao iniciar o app. Playwright oferece emulação de dispositivos e rede, mas não reproduz hardware modesto. [Vitest](https://vitest.dev/guide/), [Playwright: emulação](https://playwright.dev/docs/emulation).

Não usar o mesmo gerador como único oráculo de seus próprios testes. Fixtures técnicas precisam de resultado verificado e fonte. Testes não substituem revisão de normas, parâmetros ou direitos de publicação.

## Roadmap

Atualização de 04/10/2026: dividir a Fase 4 em incrementos com prévia e revisão do usuário. O primeiro exemplo proposto é motor trifásico de seis pontas e multímetro virtual para continuidade, com assets detalhados. Validar essa experiência antes de implementar os demais laboratórios e o restante da fatia. Ver [assets e revisão visual](07-assets-e-revisao-visual.md).

| Marco | Entrega | Porta de aprovação |
|---|---|---|
| F3a, esta proposta | Requisitos, opções, componentes, contratos e roadmap | Escolher stack, algoritmo e fidelidade |
| F3b | ADRs consolidados e compatibilidade revisada | Aprovar encerramento da Fase 3 |
| F4a | Revisão técnica das regras e questões do módulo motores | Conteúdo para a fatia validado |
| F4b | Aplicação, offline, laboratório e perguntas por etapas | Testes e fluxo completos |
| F4c | Mini-simulado, progresso, backup, README e verificação Android | Aprovar MVP antes de ampliar |
| F5 | Demais módulos por prioridade e pré-requisitos | Aprovar cada módulo |
| F6 | Revisão técnica final, desempenho, acessibilidade e documentação | Aceite dos critérios originais |

Sem prazo fechado: fontes pendentes, fidelidade e disponibilidade do usuário afetam esforço. O módulo motores continua primeiro na implementação; os pré-requisitos necessários entram como revisão curta na fatia vertical.

## Riscos e tratamento

| Risco | Tratamento |
|---|---|
| Matriz integral desconhecida | Manter código oficial null; rastrear cobertura editorial; atualizar após fonte confirmada |
| Regra incorreta derivada de questão antiga | Fonte primária, revisão e fixture técnica antes de liberar |
| Modelo de falha exageradamente universal | Delimitar família, carga, estado de partida e proteção; qualitativo quando necessário |
| Perda de armazenamento do navegador | Backup exportável, persistência quando disponível e migração segura |
| Primeiro acesso sem rede | Informar necessidade de obter pacote; confirmar “pronto offline” antes do uso |
| Dispositivo/browser antigo | Identificar aparelho e testar suporte; adaptar build e efeitos após medição |
| Reprodução de terceiros em versão compartilhada | Pacotes autorais; excluir data/provas, data/livros e extrações do build |
| Conteúdo malicioso importado | Validar JSON/tamanho/caminhos; Markdown restrito; sem eval nem HTML não confiável |
| Falta de parâmetros para modelo avançado | Não prometer medições quantitativas; escolha de fidelidade explícita |

## Referências consultadas

Documentação oficial dos projetos e MDN consultadas em 02/10/2026. Links estão junto às afirmações. As comparações de manutenção e recomendações são inferências de engenharia para os requisitos deste projeto.
