# Fase 1 - Coleta pública oficial

**Fase 2 autorizada e concluída:** conferência ampliada, cobertura e trilha disponíveis em [02-mapa-conteudo.md](02-mapa-conteudo.md). Os estados de pendência registrados abaixo são históricos da coleta.

**Simulado recebido do usuário:** `616470170-ELETROTECNICA-II-1-SIMULADO-2022-2-prova.pdf`, com 14 páginas e 40 itens. Consulte [01-simulado-2022.md](01-simulado-2022.md) para metadados e comparação com o acervo.

**Arquivo recebido do usuário:** a coleção `754180435-Questoes-SAEP-2023.docx` está disponível localmente e foi extraída. Veja a [conferência do documento](01-documento-saep-2023.md), incluindo imagens, numeração e limitações de contagem/gabarito.

**Atualização:** após a autorização para pesquisar em qualquer site e a indicação de livros locais, foi realizada a extensão descrita em [01-busca-ampliada.md](01-busca-ampliada.md). O resultado abaixo corresponde à primeira rodada, limitada a fontes oficiais. Os livros novos estão em [01-inventario-livros.md](01-inventario-livros.md).

Data: 02/10/2026. Fontes aceitas: SENAI nacional/regionais e servidores institucionais do Sistema Indústria que hospedam documentos identificados como SENAI. Sem login, pagamento ou acesso a formulários administrativos. Os três PDFs locais não foram contabilizados como novos downloads.

## Resultado

| Categoria | Local | Novos downloads oficiais | Situação |
|---|---:|---:|---|
| Avaliações com gabarito | 2 | 0 | Locais SisBia; edição nacional não comprovada |
| Simulados com itens | 1 | 0 | Local Forms; 41 itens, sem gabarito |
| Matriz de Referência SAEP de Eletrotécnica | 0 | 0 | Não localizada publicamente nesta busca |
| Planos de curso de Eletrotécnica | 0 | 2 | Ceará: 84 páginas; Roraima: 178 páginas |
| Páginas oficiais sobre SAEP | 0 | 4 | Explicação da ADE/instrumentos e duas notícias |
| Livro de metodologia de 2019 | 0 | 0 | Download respondeu HTTP 503 |

**Nenhuma nova prova ou simulado completo foi obtido.** Não há evidência suficiente para afirmar que não existam arquivos públicos; o resultado é “não localizado nesta pesquisa”. Não substituí provas por seleções de ingresso, notícias, apostilas ou documentos de outros cursos na contagem.

## Arquivos e manifesto

`data/provas/manifesto.json` registra URL original/final, data de download ou tentativa, ano e natureza do documento, curso quando aplicável, condições de uso, tamanho, SHA-256, resultado HTTP e falhas. Os originais locais continuam na raiz e estão inventariados no manifesto; os downloads estão em `data/provas/`. Não houve duplicata binária entre os arquivos obtidos. A deduplicação de itens locais está no índice da Fase 0, sem destruir a proveniência.

| Arquivo baixado | Fonte / finalidade | Ano / licença |
|---|---|---|
| [Plano CE](../data/provas/plano-eletrotecnica-ce-2016.pdf) | [SENAI-CE / FIEC](https://arquivos.sfiec.org.br/senai/files/files/planos_de_cursos/tecnico-eletrotecnica-barra-2016-1.pdf), referência curricular histórica | 2016 no endereço do arquivo; confirmar revisão interna. Licença não verificada |
| [Plano RR](../data/provas/plano-eletrotecnica-rr-semipresencial.pdf) | [SENAI-RR / Portal da Indústria](https://static.portaldaindustria.com.br/media/filer_public/04/1c/041c82d7-693a-4b1f-8e69-307d5cfd0680/001_plano_de_curso_tecnico_em_eletrotecnica_semipresencial_com_correcao_gramatical_1807.pdf), referência curricular | 2024 na capa/ficha; página 5 permite reprodução de partes com atribuição |
| saep-sobre-ade.html | [SENAI nacional: etapas da ADE](https://saep.senai.br/SobreADE/Parte1) | Página menciona ADE 2025; licença não verificada |
| saep-instrumentos.html | [SENAI nacional: instrumentos](https://saep.senai.br/SobreADE/Parte3) | Sem edição específica de caderno |
| saep-ap-simulado-2018.html | [SENAI-AP: notícia sobre SISAES](https://www.ap.senai.br/noticias/sistema-do-senai-avalia-preparacao-dos-alunos-para-o-mercado-de-trabalho.html) | 2018; noticia simulado, mas não disponibiliza seus itens |
| saep-rn-aplicacao-2026.html | [SENAI-RN: aplicação 2026.1](https://www.rn.senai.br/senai-natal-aplica-provas-saep-para-avaliar-cursos-da-instituicao/) | 2026; notícia, não caderno |

Texto integral dos dois PDFs em TXT e JSON por página, em `data/extraidos/`; todas as 262 páginas têm texto suficiente para extração nativa. As quatro páginas HTML foram preservadas e extraídas em TXT/JSON, sem executar scripts. O HTML bruto inclui navegação; é um registro de fonte, não conteúdo pronto para o app.

Os planos de curso **não são a Matriz de Referência do SAEP**. Não criamos códigos de capacidade, cruzamentos ou itens da matriz com base nesses documentos. O plano do Ceará é histórico e contém referências textuais a outras habilitações no trecho de organização curricular; o documento se identifica como Eletrotécnica, mas exige leitura crítica. O plano de Roraima é de outra regional: deve ser confrontado com o currículo efetivamente cursado pelo usuário.

## Pesquisa realizada e limites

Registro de consultas em `data/provas/registro-buscas.json`: buscas por SAEP + Eletrotécnica + prova/simulado + matriz de referência + PDF; buscas gerais e restritas a portais SENAI, com consultas adicionais a RS, PR, CE, RJ e MG. Foram examinados os portais nacionais SAEP, páginas oficiais de instrumentos, notícias regionais e resultados que anunciavam materiais. Resultados de Scribd, Slideshare, fóruns e outros repositórios não oficiais foram descartados. PDFs de resoluções de autorização, relatórios de gestão e provas de seleção de ingresso não foram contados nem baixados como provas SAEP.

A [página institucional da ADE](https://saep.senai.br/SobreADE/Parte1) informa que cada curso tem matriz específica baseada no currículo e utilizada para construir os itens. A [página de instrumentos](https://saep.senai.br/SobreADE/Parte3) descreve provas objetivas de múltipla escolha e práticas baseadas em situações-problema. Essas fontes fundamentam a distinção entre matriz avaliativa e currículo; não fornecem a matriz específica.

O [portal de resultados](https://saep.senai.br/) apresenta acesso a resultados com autenticação; não foi feita tentativa de login. O [Portal SAEP](https://portalsaep.senai.br/) não expôs um catálogo de cadernos na leitura pública realizada. Isso não comprova que todo material do SAEP seja restrito. A notícia do RN explica acesso individual às provas daquela edição, mas não disponibiliza um arquivo público. Não usamos a duração de uma notícia como regra fixa do aplicativo.

## Downloads manuais e materiais ainda necessários

| Material | Link / ação | Motivo |
|---|---|---|
| Metodologia SENAI de Educação Profissional 2019 | [PDF no SENAI-SP EAD](https://sp.senaiead.senai.br/files_scorm/27120_2/Layout/Aula/docs/Livro_Msep_2019.pdf) | HTTP 503 no download; tentar abrir no navegador e salvar localmente |
| Matriz de Referência de Eletrotécnica, versão/edição correspondente | Solicitar à coordenação/docente da unidade; [portal nacional](https://portalsaep.senai.br/) é ponto de consulta | Não foi encontrado link público direto; não há URL de download confirmada |
| Cadernos públicos adicionais e seus gabaritos | Solicitar links oficiais à unidade; usar apenas arquivos autorizados para estudo | Nenhum link direto público foi localizado |
| Gabarito do SIMULADO 2026 | Solicitar ao docente/autor | Não está no PDF; não inferido |
| Plano e apostilas do curso efetivamente cursado | Adicionar ao workspace quando disponíveis | Nenhum material adicional local encontrado; regional ainda desconhecida |

O livro bloqueado é complementar, não uma prova ou matriz. Não há lista fictícia de links de cadernos para baixar manualmente: somente URLs efetivamente verificadas.

## Uso futuro das fontes

Provas locais: referência de estilo/frequência, com procedência e autorização a confirmar. Questões, figuras e explicações da versão compartilhável deverão ser originais. JSONs e figuras extraídos não devem ser empacotados automaticamente no aplicativo. Gabarito extraído significa fidelidade ao documento, não validação da correção técnica. Público e oficial não significa licença aberta; a autorização de atribuição do plano RR não se estende aos outros arquivos.

## Decisão pendente para a Fase 2

| Opção | Vantagem | Limitação |
|---|---|---|
| **A - Mapa provisório com os 87 itens e planos oficiais (recomendado)** | Permite avançar no estudo e registrar lacunas | Códigos da Matriz de Referência ficam `null` / [VERIFICAR]; cobertura integral do SAEP não pode ser afirmada |
| B - Aguardar a matriz e o plano da unidade | Permite mapear diretamente capacidades e cruzamentos oficiais | Depende de obter materiais da unidade antes de iniciar a Fase 2 |

Não escolhemos a opção pelo usuário. Após sua aprovação das Fases 0/1 e escolha A/B, a Fase 2 seguirá o caminho autorizado. Stack, algoritmo e fidelidade serão decididos na Fase 3 com comparação e escolha do usuário.

## Resumo da Fase 1 (8 linhas)

1. Busca em fontes oficiais nacionais e regionais concluída e registrada.
2. Zero novas provas/simulados completos públicos obtidos.
3. Matriz avaliativa específica de Eletrotécnica não localizada.
4. Dois planos oficiais baixados: CE (84 páginas) e RR (178 páginas).
5. Quatro páginas oficiais preservadas; texto extraído dos seis downloads.
6. Manifesto e SHA-256 registrados; nenhuma duplicata binária nos downloads.
7. Livro de metodologia com HTTP 503; link manual registrado.
8. Fases 0/1 encerradas; aguardando aprovação, escolha A/B e informações da unidade.
