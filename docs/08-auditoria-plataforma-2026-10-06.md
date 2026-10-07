# Auditoria da base SAEP — 06/10/2026

## Resultado

A entrega recebida era uma estrutura de catálogo, não uma plataforma de ensino completa. Havia 35 registros coerentes com a trilha, mas nenhum conteúdo pedagógico implementado nos módulos: estudar/praticar exibiam placeholders. Não existia fluxo de avaliação ou conclusão. Build e navegação básica funcionavam; isso não demonstrava aprendizagem, desbloqueio por avaliação, revisão ou offline.

Escopo desta revisão: código de `plataforma-saep`, comparação da trilha com o mapa da coleta, design do catálogo/detalhes, dados locais e documentação. O laboratório da raiz foi preservado; esta revisão não constitui nova auditoria física/elétrica integral daquele protótipo.

## O que estava correto

- 35 IDs, ordem, pré-requisitos, prioridades e metas correspondem a `data/fase2/mapa-conteudo.json` e `docs/02-trilha-estudo.md`.
- Soma das metas: 542 questões originais planejadas, não entregues.
- S01 e F01 não têm pré-requisitos. O grafo existente não tem ciclos ou referências ausentes.
- Stack React/TypeScript/Vite, build e componentes de navegação existiam.

## Achados e tratamento

| Prioridade | Problema encontrado | Correção ou limite atual |
|---|---|---|
| Alta | “Completo/100% funcional” com estudo e prática vazios, sem avaliação/conclusão | Conteúdos marcados `planned`, sem iniciar/concluir ficticiamente; planos consultáveis; documentação corrigida |
| Alta | Um status `completed` de localStorage podia liberar temas sem evidência | Dados legados preservados como registros anteriores, sem domínio; nenhuma conclusão disponível nesta fase |
| Alta | `JSON.parse` e escrita de storage sem proteção; dados malformados podiam quebrar a aplicação | Validação de formato/versão/ID/contadores/score, tratamento de permissão/quota e aviso de recuperação |
| Alta | Bloqueio apenas no catálogo, sem distinguir publicação de requisitos | `contentStatus` separado da elegibilidade; `canStartModule` central; aulas continuam inacessíveis enquanto não publicadas |
| Média | Progresso e lista de concluídos duplicados, com risco de divergência | Estado persistido único; estatísticas desta fase representam planos/favoritos e zero avaliações verificadas |
| Média | Datas declaradas `Date` após serialização JSON | Tipos persistidos em strings ISO; normalização defensiva |
| Média | Gráfico baseado em acertos/meta podia ultrapassar 100%; estado em andamento era confundido com disponibilidade | Gráfico não usa tentativas como domínio; clamping da apresentação e explicitação de avaliações pendentes |
| Média | “Trilha oficial” sem matriz integral confirmada | Identificação como trilha editorial pessoal; preservada incerteza dos documentos da coleta |
| Média | Guia contraditório sobre sequência e confusão entre MVP e trilha | Referência única da trilha; ordem de prototipação distinta da aprendizagem; motores preservados |
| Média | Duas aplicações disputando 5173; servidor antigo deixou página em branco por cache de dependências | Catálogo 5174, `strictPort`, laboratório 5173; servidor da plataforma reiniciado com reotimização |
| Média | CSS com estilos duplicados, cards pouco acessíveis, filtros inexistentes e idioma HTML `en` | Novo design, cards em botões nativos, foco/skip-link, busca sem acentos, filtros, português e layout responsivo |
| Baixa | `any` nos componentes e TS sem `strict` | `unknown` e modo estrito; build/lint verificados |

A alegação de que começar pelo laboratório de motores era erro de sequência não corresponde ao histórico: o usuário autorizou expressamente a prévia técnica, e o último parágrafo da trilha distingue ordem de estudo e implementação do MVP. Os fontes da raiz já eram React/TypeScript, não apenas HTML standalone. Isso não torna o catálogo novo desnecessário; são trabalhos diferentes que ainda precisam ser integrados.

## Estado real após revisão

Novo catálogo editorial, detalhes de planejamento e favoritos persistidos. Todos os 35 temas permanecem em preparação; não existem aulas, itens avaliáveis ou conclusão de módulo no catálogo. É possível abrir o plano de um tema com requisitos pendentes: inspeção do planejamento não concede acesso a conteúdo avaliável.

S01 é o próximo incremento. A implementação deverá reunir explicação, cenário seguro com sequência verificável, questões originais, fontes/versões e evidência de avaliação. Não publicar todos os módulos de uma vez; revisar o primeiro exemplo antes de ampliar. A meta provisória de 8/10 sem dica não é critério oficial e não substitui o procedimento completo em segurança.

Ainda pendentes: conteúdo, avaliações, revisão espaçada, mini-simulados, modo offline, backup/importação por arquivo, sincronização entre abas, integração do laboratório, APK, 3D e medição no Android do usuário. Service worker futuro não equivale a offline funcionando.

## Persistência

- `saep.study.v1`: envelope versionado com favoritos e registros históricos.
- `saep_progress`: somente leitura na migração; não apagado.
- `saep.study.v1.previous`: primeira cópia do registro existente antes de sobrescrevê-lo. Se o backup ou a gravação falham, há aviso e as escolhas ficam na sessão.
- IDs desconhecidos, versões futuras e contadores incoerentes não são aceitos.
- Conclusão não é inferida de abertura, favorito ou `completed` legado.
- Storage é por origem; trocar localhost/127.0.0.1/porta não transfere dados automaticamente. Ainda não há importação para isso.

## Verificação executada

- `npm test` em plataforma-saep: 7 testes passando, incluindo comparação completa com o mapa de conteúdo, grafo e persistência adversarial.
- `npm run build`: passando, JS 76,48 KB gzip e CSS 3,14 KB gzip na revisão. São artefatos, não custo completo de rede/cache.
- `npm run lint`: sem avisos.
- `node scripts/testar-plataforma.mjs`: Chrome headless instalado, larguras 1400/390, 35 planos, busca sem acento, filtros, teclado, favorito após reload, pré-requisitos pendentes, JSON corrompido, conclusão legada, storage bloqueado e quota. Sem erro de página ou overflow horizontal nesses fluxos.
- Inspeção visual: `output/previa/plataforma-inicio-1400.png`, `plataforma-inicio-390.png` e planos S01.

Não foi testado no aparelho Android físico, instalado APK ou servido como PWA offline. A ilustração do catálogo é SVG esquemático, sem alegação de asset fotográfico final.

## Abrir e revisar

Catálogo: http://127.0.0.1:5174/ (`cd plataforma-saep; npm run dev`). Laboratório: http://127.0.0.1:5173/ (servidor independente na raiz). A documentação anterior está preservada em `plataforma-saep/docs/historico/entrega-inicial/` e marcada como histórico.
