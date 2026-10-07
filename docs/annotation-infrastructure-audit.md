# Annotation Infrastructure Audit

## 1. Curriculum Extraction Coverage
A exaustiva varredura dos documentos (plataforma-saep/src/data/modules.ts, docs/02-trilha-estudo.md, docs/02-matriz-cobertura.md, data/fase2/mapa-conteudo.json) confirmou que **não existem** definições explícitas de learning_objectives, subtopics, includes, xcludes ou overlaps_with. O extrator produziu apenas code, 	itle e prerequisites. Todos os 35 módulos receberam a tag 
eeds_editorial_definition: true e o status da matriz deve ser considerado **CURRICULUM_SOURCE_SKELETON**, necessitando autoria editorial subsequente. Os dados extraídos foram mapeados em curriculum-source-evidence.json.

## 2. Alternative Preservation & Source Fidelity Tests
O script gerar-pacote-anotacao.py foi refatorado para ler preferencialmente da raiz dos lotes originais (--source-root). Se um pacote original de lote (com 2, 4 ou 5 alternativas) estiver disponível, ele os importa diretamente, contornando a estrutura planificada e esvaziada de lternativas do catalogo-global-v2_2.json. Testes confirmam preservação fiel da estrutura de enunciados e opções se alimentados pela raiz original.

## 3. Image Manifest Coverage
A reconciliação foi executada. Há exatas 2.665 questões no acervo com a sinalização original has_image: true. Destas, 2.653 questões possuem referências (image_references), enquanto 12 possuem apenas o booleano has_image original (sendo catalogadas como REFERENCE_MISSING). O manifesto gerado possui o registro granular xists, loadable (validado com PIL.Image.verify), ormat e size_bytes de todas.

## 4. Schema & Validator Tests
A estrutura JSON Schema em schema-anotacao-v2.json recebeu invariantes com llOf/if-then. Foram aplicados testes negativos garantindo que:
- ANNOTATED exige módulo válido, recusa nulos.
- OUT_OF_CURRICULUM recusa módulo preenchido e exige nulo.
- AMBIGUOUS força mbiguity_reason string preenchida.
- Arrays como cceptable_modules recusam códigos de módulo inexistentes ou sobrepostos ao principal.
O utilitário alidar-anotacoes.py executa jsonschema + checagens hardcoded.

## 5. Cross-process Seed & Leakage Tests
O script 	est_annotation_infra.py confirmou que stable_seed() utilizando a conversão SHA-256 é imune à randomização de hashes nativos e retorna idêntico resultado em subprocessos separados. Adicionalmente, 	est_leakage() atesta que nenhum artefato gerado como CONTENT ou SUPPLEMENT revela predições como primary_module, semantic_family, classification_evidence ou dados de confiança da V2.2 aos anotadores.

