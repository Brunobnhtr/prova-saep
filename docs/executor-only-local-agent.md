# Local Agent Protocol — Executor Only

The local agent is an execution worker, not an author or reviewer.

## Authority split

- **IA mestre (web):** designs the method, writes code, fixes code, writes tests, chooses annotation labels for Annotator A, audits results, and decides PASS/FAIL gates.
- **Local agent:** copies pre-generated files, runs the exact commands supplied, reports stdout/stderr and hashes, commits/pushes only after all required gates pass, and cleans the temporary delivery folder.

## Prohibited actions for the local agent

The local agent MUST NOT:

- edit Python/JSON/Markdown files delivered by the IA mestre;
- change tests to make them pass;
- change the validator because a test failed;
- invent a workaround;
- choose annotation modules by script, random selection, keyword routing, fixed maps, round-robin, or templates;
- commit when any mandatory test is failing;
- continue after a base-commit mismatch or dirty-worktree check fails.

If any command fails, the local agent must stop and return the exact failure output. It must not attempt a repair.

## Canonical application mechanism

When a delivery contains `APLICAR.ps1`, that script is the only authorized application path. The local agent executes it and does not manually reproduce its internal steps.

## Commit gate

A commit/push is authorized only when the application script has confirmed all of the following:

1. expected base commit matches;
2. worktree is clean before applying;
3. only allow-listed files changed;
4. all mandatory tests exit with code 0;
5. `git diff --check` passes;
6. commit succeeds;
7. push succeeds;
8. remote `master` resolves to the new local HEAD.

A failing test means **NO COMMIT**.
