# Annotation Methodology V2 — Freeze A Before B

## Why this exists

A validator can verify structure, grounded excerpts, exact curriculum subtopics, and some anti-template rules. It cannot prove that a module choice was made by genuine per-question semantic reasoning.

REAL-BATCH-0002 demonstrated this limit: an annotator could hard-code a module map, select the first subtopic automatically, generate templated reasoning, and still aim to satisfy lexical gates. In addition, the B labels were exposed before Annotator A was frozen, invalidating blind agreement measurement for that batch.

## Mandatory order for all new real batches

1. Generate immutable batch and validate manifest.
2. Annotator A reviews the batch independently.
3. Save and validate `ANNOTATOR_A.json`.
4. Record SHA-256 of A and create `_A_FROZEN.json`.
5. Only after `_A_FROZEN.json` exists may the B task be released.
6. Annotator B performs independent per-question semantic decisions.
7. B saves `ANNOTATOR_B.json` plus a private `ANNOTATOR_B_AUDIT.md` with one section per question.
8. Run structural/quality validator.
9. Compare A × B only after both hashes are frozen.
10. Adjudicate disagreements and record final artifact.

## B process requirements

For each question, B must privately document:
- source_id;
- relevant literal statement span;
- selected primary module or OUT_OF_CURRICULUM;
- exact curriculum subtopic when in curriculum;
- nearest competing module(s), when applicable;
- why the selected module wins under the editorial boundary rules;
- image use when the question is visual.

Scripts may serialize already-decided objects, calculate hashes, and run validators. Scripts must not choose modules, assign modules randomly, use round-robin/keyword-only routing, select a fixed first subtopic for every item, or synthesize reasoning from a generic template.

## Validator scope

`validar-anotacoes.py` is a necessary gate, not semantic ground truth. A green validator means the artifact satisfies the contract; it does not by itself prove that annotation decisions were made correctly. Process logs and private audit artifacts are part of acceptance.

## Contamination rule

If B labels are exposed to A before A is frozen, that batch is permanently ineligible for blind agreement/accuracy metrics. It may remain useful for process auditing, curriculum-gap review, or adjudication practice, but it must not be counted as an independent dual-annotation batch.
