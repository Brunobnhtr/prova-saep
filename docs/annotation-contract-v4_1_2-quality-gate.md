# Annotation Contract V4.1.2 — Semantic Quality Gate

## Motivo

O primeiro lote real revelou um falso positivo do validador V4.1.1: um arquivo podia ser estruturalmente válido mesmo usando justificativas e evidências placeholder.

O artefato `ANNOTATOR_B.json` do primeiro batch continha `reasoning_summary = "Auto generated reasoning."` e `module_evidence[].text = "evidence"`. O schema aceitava as strings porque elas atendiam somente tipo e comprimento mínimo.

## Novas regras

`validar-anotacoes.py` mantém todas as regras V4.1.1 e acrescenta:

1. `reasoning_summary` deve ter pelo menos 20 caracteres úteis e não pode ser placeholder conhecido.
2. `ANNOTATED` exige evidência semanticamente útil.
3. Evidência `STATEMENT`:
   - mínimo de 10 caracteres;
   - não pode ser placeholder;
   - quando o pack contém `statement`, deve corresponder a trecho real do enunciado.
4. Evidência `CURRICULUM_SUBTOPIC` exige módulo e subtópico não vazios.
5. Metadados de imagem precisam permanecer sincronizados com o `content.json`.
6. Uma mesma justificativa idêntica não pode ser reutilizada em mais de 3 itens do mesmo arquivo.
7. Saída positiva passa a emitir também `ANNOTATION_QUALITY_VALID = true`.

## Compatibilidade

Nenhum campo do schema V3 é removido ou renomeado. A alteração é um gate semântico adicional no validador.

## Primeiro lote real

- 25 itens.
- acordo primário/status estrito A×B: 22/25 = 88%.
- acordo de status: 24/25 = 96%.
- acordo considerando módulos aceitáveis: 23/25 = 92%.
- adjudicação final: 21 `ANNOTATED`, 4 `OUT_OF_CURRICULUM`.

Os rótulos por questão permanecem fora do GitHub público, na pasta persistente de anotação do Google Drive.
