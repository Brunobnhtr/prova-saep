# Conferência do acervo antes da Fase 2

Data: 02/10/2026. Escopo: quatro PDFs e um DOCX fornecidos pelo usuário; documentos operacionais, planos de curso, livros e os cinco PDFs autorais para Scribd não são contados como provas.

| Documento | Páginas | Ocorrências de questões | Alternativas | Gabarito |
|---|---:|---:|---|---|
| avaliações.pdf | 40 | 40 | A-D | 40 respostas extraídas |
| avaliações 2.pdf | 37 | 40 | A-D | 40 respostas extraídas |
| SIMULADO 2026.pdf | 32 | 41 | A-D | Não localizado |
| Simulado Eletrotécnica 2022.2 | 14 | 40 | A-E | Não localizado |
| Questões SAEP 2023 DOCX | 47 renderizadas | 80 | A-E, incluindo alternativas em imagem | Sem gabarito formal; há anotações e setas |

Total: **241 ocorrências**. As 47 páginas do DOCX foram confirmadas por exportação local do Word em modo somente leitura. O PDF de conferência fica em `tmp/pdfs/colecao-2023-conferencia.pdf`; não é uma nova prova do acervo.

## Correção da divergência do DOCX

A questão 11 tem o enunciado curto “A figura a seguir representa a planta baixa de uma cozinha residencial”. O limite de comprimento usado na primeira extração não a reconhecia como início de questão. O ajuste e a comparação com o documento renderizado recuperaram **80 questões em sequência**, sem lacuna entre 1 e 80.

As alternativas textuais foram novamente extraídas do PDF de conferência, reconhecendo os formatos `A)`, `(A)` e `A-`. **76 itens possuem alternativas textuais A-E; quatro (13, 15, 17 e 27) possuem alternativas gráficas**, com as imagens originais vinculadas. Foram preservadas também imagens do formato VML, antes ausentes de alguns vínculos de parágrafo. Todos os 62 arquivos de mídia do DOCX estão salvos. A inspeção visual percorreu as 47 páginas em folhas de contato, com ampliação das páginas que explicam a divergência e as alternativas gráficas. Não equivale à revisão técnica integral das soluções ou à transcrição acessível de cada desenho.

Há setas indicando alternativas e uma resolução anexada à opção A da questão 11. Elas são anotações de autoria não certificada. Nenhuma foi transformada em gabarito oficial. O JSON de conferência mantém fonte e páginas; o original não foi editado.

Para os quatro itens com alternativas gráficas, também foram salvas páginas completas compostas em `data/fase2/figuras-conferencia/`, vinculadas aos itens. Isso conserva desenhos agrupados e setas que não aparecem como uma imagem simples no parágrafo do DOCX.

## Deduplicação conservadora

- A1/A2: 33 identificadores SAEP compartilhados, sem divergência das letras de gabarito nesses dois documentos.
- S26: itens 10 e 23 repetidos, conforme conferência anterior.
- C23: itens 3 e 61 repetem a situação de termografia/manutenção preditiva, com pequenas diferenças de redação e alternativas reordenadas. Consolidar a frequência do conteúdo em um grupo, preservando ambas as ocorrências; nunca transferir letra de resposta entre alternativas reordenadas.
- C23 item 31 e S26 itens 10/23 apresentam situação semelhante de medição de alimentação do motor, mas têm comandos/alternativas diferentes; foram mantidos separados.
- S22: 40 IDs distintos e nenhum compartilhado com A1/A2. Não surgiu outro candidato na comparação textual das extrações.

Resultado: **206 grupos conservadores**, calculados como 241 - 33 - 1 - 1. Similaridade serve para localizar candidatos, não para excluir automaticamente questões. Não afirmar que inexistem outras variantes semânticas. Os grupos, páginas e ocorrências ficam em `data/fase2/indice-deduplicado.json`; candidatos e decisões estão registrados nesta conferência e em `candidatos-duplicatas.json`.

## Limites preservados

O acervo é de avaliações, simulados e coleção de terceiros; aplicação nacional e anos de todas as avaliações não estão certificados. Cruzamentos impressos em S22 foram preservados literalmente, sem converter para uma matriz atual desconhecida. Continuam válidos os alertas técnicos do diagnóstico inicial. A questão 69 do DOCX menciona “5410/2015” ao tratar de SPDA: [VERIFICAR] referência do autor antes de reutilizar conteúdo normativo.

Conferência de estrutura e contagem concluída; revisão técnica integral, descrições acessíveis e confirmação de respostas pertencem ao trabalho de conteúdo dos próximos módulos.
