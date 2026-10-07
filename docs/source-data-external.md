# Fonte de dados externa do projeto SAEP

O repositório GitHub mantém código, schemas, documentação e artefatos editoriais. O banco bruto de questões e imagens permanece fora do GitHub porque o repositório é público e esses dados são volumosos.

A fonte oficial bruta fica no Google Drive na pasta persistente:

`prova-saep - Dados Fonte (NAO APAGAR)`

Folder ID: `15eK70chiWDawD8cKBpIYAwLAFi6AKFYr`

Estrutura esperada:

- `questoes/` — 49 arquivos `lote_*.json` originais.
- `imagens/` — imagens disponíveis referenciadas pelo inventário editorial.
- `manifests/` — manifests e relatórios de fidelidade/integridade.
- `SOURCE_DATA_MANIFEST.json` — snapshot com contagens e SHA-256.
- `_SOURCE_READY.json` — marcador de que a sincronização e validação terminaram.

Invariantes oficiais do snapshot inicial:

- 49 arquivos fonte.
- 9.791 registros e 9.791 IDs únicos.
- alternativas: 1.031×2, 2.545×4, 6.215×5.
- 2.665 questões com contexto visual.
- 2.653 com imagem disponível.
- 12 `REFERENCE_MISSING`.
- 2.861 arquivos de imagem disponíveis/referenciados.

A pasta acima é persistente e **não deve ser apagada** durante a limpeza das entregas temporárias em `prova-saep - Atualizacoes ChatGPT`.
