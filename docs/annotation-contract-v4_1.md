# Contrato de Anotação V4.1

Este documento descreve as regras de validação adicionadas e reforçadas no pipeline de infraestrutura editorial V4.1, visando assegurar a paridade rígida entre o pacote exportado e as anotações, bem como aplicar regras semânticas de campos e rastreabilidade visual.

## 1. Paridade de IDs e Envelope (`validar-anotacoes.py`)
- **Envelope do Lote**: O arquivo gerado pelo anotador agora deve conter um envelope JSON identificando o lote (`batch_id`), o anotador (`annotator_id`) e a lista de anotações em (`annotations`).
- **Paridade Estrita 1:1**: A validação agora compara todos os IDs (`source_id`) do `content.json` (`--pack`) contra os IDs presentes nas `annotations`.
  - Nenhuma anotação pode faltar.
  - Nenhum ID pode ser desconhecido.
  - Nenhum ID pode estar duplicado.

## 2. Validação Cruzada (Cross-Field Logic)
- **Primary vs Acceptable**: O módulo definido em `primary_module` não pode constar dentro da lista `acceptable_modules`.
- **Match de Versão**: Os campos `curriculum_version` e `source_question_version` de cada anotação devem bater exatamente com as respectivas versões reportadas no `content.json`.
- **Regras `OUT_OF_CURRICULUM`**: Quando `annotation_status` for `OUT_OF_CURRICULUM`, o script agora garante via lógica dupla (schema + validação imperativa) que:
  - `in_curriculum = false`
  - `primary_module = null`
  - `acceptable_modules = []`

## 3. Preservação de Contexto de Imagens (`gerar-pacote-anotacao.py`)
- O sinalizador de presença de imagem (`has_image`) e o respectivo `image_inventory_status` agora são carregados **diretamente do inventário de imagens global** (`data/editorial/image-manifest.json`).
- Questões que dependiam de imagens mas as tiveram perdidas durante a carga não reportam mais falsamente `has_image: false`. Elas repassam a informação real para os anotadores, assinalando que há uma imagem esperada e alertando que ela consta como `REFERENCE_MISSING` (ou `UNLOADABLE`, `FILE_MISSING`), evitando que o avaliador anote a questão sem o devido contexto.
- Em caso de execuções sem lote real (`--source-mode MOCK`), `source_manifest_sha256` é anulado e evita de contaminar hash de produção.

