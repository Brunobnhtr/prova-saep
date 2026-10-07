# Annotation Contract V4.1.3 — Semantic Binding

V4.1.3 exists because V4.1.2 could still be gamed by choosing a random module, attaching an arbitrary literal substring from the statement, and using a generic justification. That artifact is structurally valid but semantically worthless.

## New default requirements

For every `ANNOTATED` item, the annotation must contain both:

1. a `STATEMENT` evidence span copied literally from the question; and
2. a `CURRICULUM_SUBTOPIC` whose `module` equals `primary_module` and whose `subtopic` exactly exists in `data/editorial/curriculum-35-modules-editorial-v1.json`.

The reasoning must be at least 60 characters and must lexically connect to both the selected statement evidence and the selected curriculum title/subtopic. Known generic templates are rejected.

For `OUT_OF_CURRICULUM`, a literal statement evidence span is required and the reasoning must explain the uncovered concept while linking back to that span.

## Process rule

Module choice MUST be a per-question semantic decision. Random assignment, keyword-only assignment, round-robin assignment, or assignment from a prebuilt arbitrary mapping is prohibited. Scripts may serialize already-decided annotations, calculate hashes, and validate output; they MUST NOT choose the module.

## Historical compatibility

Frozen artifacts produced under V4.1.2 may be revalidated only with `--legacy-v4_1_2`. New work must use the default V4.1.3 behavior.
