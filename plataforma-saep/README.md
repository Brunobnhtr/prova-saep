# Plataforma SAEP — base revisada

Revisão de 06/10/2026. Este projeto é o catálogo e o planejamento da trilha, não uma plataforma com 35 aulas prontas. Trilha editorial baseada no acervo; a matriz oficial integral ainda não foi confirmada.

## Executar

```powershell
cd plataforma-saep
npm install
npm run dev
```

Acesse http://127.0.0.1:5174/. Porta fixa para não conflitar com o laboratório de motores da raiz (5173). Se já estiver em uso, verifique o servidor existente; não mudar silenciosamente de porta. Após atualizar dependências, pode ser necessário reiniciar com `npm run dev -- --force`.

## Funciona nesta versão

- Catálogo dos 35 temas, com ordem, pré-requisitos e 542 questões como metas de produção.
- Busca sem acentos, filtros por área, bases iniciais e temas salvos.
- Consulta dos planos, inclusive dos temas com pré-requisitos pendentes.
- Favoritos persistentes e recuperação defensiva de dados locais.
- Interface de teclado, português, desktop e tela de celular.
- Grafo e requisitos verificados contra os dados originais da coleta.

## Ainda não foi implementado

Aulas, questões, correção, avaliação de domínio, desbloqueio por avaliação, revisão espaçada, mini-simulados, backup por arquivo, sincronização entre abas, service worker/offline, APK e visualização 3D. Todos os módulos têm `contentStatus: planned`. Nenhum botão declara conclusão fictícia. S01 será o primeiro conteúdo incremental, sujeito à revisão antes de avançar.

O laboratório de motores existente está preservado na raiz como prévia técnica independente. Sua implementação autorizada não equivale a pular a trilha de aprendizagem, nem está integrada ao progresso do catálogo.

## Progresso e dados

`saep.study.v1` guarda temas salvos e registros históricos, com versão e validação. O antigo `saep_progress` é somente lido, sem apagá-lo. Antes de sobrescrever uma chave nova existente, a primeira cópia é preservada em `saep.study.v1.previous`. Arquivos/versões desconhecidos e registros inconsistentes são ignorados com aviso. Falha de quota ou permissão mantém as escolhas na sessão e informa que não houve persistência.

Conclusões antigas não têm avaliação verificável; são registros históricos em andamento, sem liberar pré-requisitos ou compor percentual de domínio. Timestamps são strings ISO, não instâncias `Date` após JSON. Storage é por origem: `localhost`, `127.0.0.1` e portas diferentes têm dados distintos. A migração automática só alcança chaves da mesma origem; não há ferramenta de importação nesta versão.

## Verificar

```powershell
npm test
npm run build
npm run lint
```

Na raiz do repositório: `node scripts/testar-plataforma.mjs` com a prévia em 5174. Utiliza Chrome instalado e Playwright da raiz. Verifica teclado, busca, filtros, favoritos/reload, estados pendentes, erros de storage e larguras 1400/390. Não é medição de desempenho em Android físico.

## Fontes e auditoria

- `../docs/02-trilha-estudo.md`: sequência e objetivos.
- `../data/fase2/mapa-conteudo.json`: metas, prioridades e pré-requisitos.
- `../docs/08-auditoria-plataforma-2026-10-06.md`: achados e correções.
- `docs/historico/entrega-inicial/`: documentação recebida, preservada como histórico.

A trilha de estudo e a sequência de prototipação do laboratório são planos distintos. Normas, capítulos dos livros e itens precisam de conferência antes de publicar cada conteúdo.

## Acervo ampliado antes de produzir conteúdo

Consultar `../docs/09-acervo-ampliado-e-representacao-visual.md` e `../data/acervo-ampliado/cruzamento-35-temas.json`. Foram encontrados 93 dossiês e 9.791 questões externas, mas nenhum gabarito nos lotes. Dossiês são seleções automáticas com lacunas e falsos positivos, não conteúdo validado. Para S01, revisar 4.4/4.2 e a seleção de reenergização antes da aula. Manter as prioridades SAEP da coleta original separadas das frequências de concursos.
