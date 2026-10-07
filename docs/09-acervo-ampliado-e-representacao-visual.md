# Acervo ampliado e proposta visual — 06/10/2026

## Material conferido

Raiz externa: `C:\dev\extrator de perguntas`. Leitura apenas de dossiês, questões, índices e documentação; nenhum arquivo do acervo externo foi alterado. Não foram lidas sessões, tokens ou arquivos de autenticação.

- 93 dossiês temáticos: 93 PDFs de fontes, 93 JSONs, 246 Markdown e 4.080 PNGs de figuras.
- 49 lotes contendo 9.791 ocorrências e 9.791 IDs distintos; todos os IDs coincidem com o índice.
- 87 arquivos de temas com 9.549 questões nos cabeçalhos internos; o README informa 242 sem tema, fechando 9.791. Organização auxiliar, não matriz oficial SAEP.
- 2.861 arquivos de imagens das questões, em diferentes formatos.
- Alternativas: 6.215 questões com cinco, 2.545 com quatro e 1.031 com duas. Não converter silenciosamente todas para quatro.

Verificação estrutural dos 49 lotes, não resolução individual dos itens. Identificadores únicos não garantem unicidade pedagógica; a assinatura de texto/alternativas/URLs não encontrou duplicatas exatas candidatas, mas não detecta variantes semânticas ou imagens idênticas em URLs distintas.

## Lacunas encontradas

- Os 9.791 campos `gabarito` estão nulos. Não há gabarito extraído nesses lotes; não usar como banco autocorrigível até resolver/verificar os itens selecionados.
- Quatro registros sem texto de enunciado. Questões podem depender de imagens; precisam de inspeção, não descarte automático.
- Sete referências de imagem sem arquivo local válido, em quatro IDs; onze registros têm mais imagens no HTML que nos objetos de imagem. São sinais distintos, não devem ser somados como falhas únicas. O log registra 21 erros históricos, alguns podem ter sido recuperados.
- 62 dossiês têm ao menos uma chave sem fonte selecionada. Isso não demonstra ausência do assunto nos livros: a busca é lexical e pode omitir sinônimos, trechos ou seções.
- Exemplo S01/4.4: `reenergizacao` não recebeu fonte e `bloqueio` trouxe “Válvulas de bloqueio” do livro de dispositivos automatizados. Trata-se de um falso positivo temático confirmado pelo título da seção. Também entram sinalização de poste/sinaleiro: pertinência depende do contexto, não apenas da palavra.
- Há páginas só com imagem candidatas a OCR. Limpeza de texto ou OCR não certifica fórmulas, símbolos, páginas e unidades.

## O que muda no planejamento

Criado `data/acervo-ampliado/cruzamento-35-temas.json`, com referências candidatas para cada módulo e lacunas explícitas. Não altera a ordem, pré-requisitos ou escore SAEP da coleta original. Frequência em concurso geral não deve ser misturada à frequência das provas SAEP.

F01 pode ganhar pequenos apoios de matemática/unidades dentro do tema existente (0.1–0.5), sem criar uma trilha nova automaticamente. Circuitos CC e medições ganham apoio mais detalhado. S01 possui um arquivo de 101 questões classificadas por assunto, mas sem gabarito extraído nos lotes e com cobertura do dossiê que precisa ser corrigida. O tema será preparado apenas após seleção/revisão, sem começar a aula nesta etapa.

H01/H02 não têm dossiês dedicados nesta organização; verificar livros de atuadores já disponíveis. V01, E05 e parte de E06 recebem apenas referências gerais: fotovoltaica, Dahlander e soft-starter requerem conferência específica. Mais fontes não significam cobertura completa de todos os temas.

## Como representar circuitos, fórmulas e curvas

| Uso | Ferramenta proposta | Execução |
|---|---|---|
| Esquema estático original com símbolos | Schemdraw → SVG | Python na preparação; servir arquivo leve no site |
| Gráficos de senoide, potência, curvas e resultados | Matplotlib → SVG/PNG | Python na preparação; dados e modelos revisados |
| Circuito manipulável, selecionar/arrastar, instrumentos e animação | SVG/Canvas + TypeScript/React | Navegador, com motor lógico separado da figura |
| Fórmulas escritas em sintaxe LaTeX | KaTeX; MathJax quando comandos necessários não forem suportados | JavaScript no navegador, com dependências locais para futura operação offline |
| Equipamento com aparência fotográfica/3D | Fotos/renders revisados ou modelos 3D | Assets distintos de diagramas esquemáticos |

Matplotlib é Python: não roda nativamente em JavaScript apenas por inserir um componente React. Pode gerar assets previamente ou por servidor Python; executá-lo no navegador exigiria uma camada adicional de Python/WebAssembly. Para esta aplicação estática e celular, a proposta é gerar gráficos/esquemas na preparação e deixar a interação leve no navegador. Um SVG exportado não conhece a topologia elétrica: terminais, nós, conexões e regras devem ser modelados separadamente.

KaTeX/MathJax interpretam sintaxe matemática; não são compiladores de documentos LaTeX completos. Usar textos/unidades acessíveis, preservar subscritos e não inserir HTML extraído diretamente como código confiável. Imagens recortadas servem como referência visual; esquemas redesenhados precisam conferir conexões, símbolos, polaridade e valores, sem apresentar o desenho como cópia certificada.

Fontes técnicas consultadas:
- [Schemdraw: geração e formatos](https://schemdraw.readthedocs.io/en/stable/usage/start.html).
- [Matplotlib: backends, SVG/PNG e WebAgg](https://matplotlib.org/stable/users/explain/figure/backends.html).
- [KaTeX: renderização no navegador](https://katex.org/docs/api).
- [MathJax: sintaxe matemática](https://docs.mathjax.org/en/latest/basic/mathematics.html).

Matplotlib e Schemdraw não estão instalados no Python atualmente usado; nenhuma instalação foi feita nesta etapa. Também não foram adicionados renderizadores de fórmulas ao app ainda. A recomendação é uma decisão de preparação, não uma funcionalidade entregue.

## Próxima seleção, antes de S01

Conferir manualmente o dossiê 4.4/4.2, preencher reenergização com trechos e norma verificados, retirar válvulas de bloqueio dessa seleção e selecionar poucos itens úteis com soluções revisadas. Registrar origem e estado de validação. Os enunciados de concurso são material externo de referência; produzir os itens originais do app como previsto no projeto, mantendo separados origem, adaptação e autoria.

Inventário reexecutável: `python scripts/inventariar-acervo-ampliado.py`. Saída: `data/acervo-ampliado/inventario.json`. O cruzamento dos 35 temas é editorial, não gerado automaticamente pelo inventário. Os fontes externos permanecem nas suas pastas; o projeto guarda apenas metadados e a análise, sem copiar o banco inteiro para o bundle.

## Diretrizes editoriais recebidas

Ver `docs/10-processo-editorial-e-diagnostico.md` na raiz: validação progressiva, estados editoriais, proveniência, diagnóstico por etapas e V/F com justificativa. Antes de produção, apresentar candidatas/rejeitadas, resoluções e conversões. Nenhum gabarito preenchido em massa.
