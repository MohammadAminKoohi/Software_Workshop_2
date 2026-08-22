# Refined Skill Test Prompt

## Invocation metadata

- Date: 2026-08-22
- OpenCode mode: Plan
- Model: `opencode/big-pickle`
- Skill under test: `solid-refactoring` version 0.2
- Source scope: unchanged root `store/`

## Exact prompt

```text
Use the `solid-refactoring` Skill for an analysis-only validation run.

Inspect the unchanged root `store/` implementation before making claims. The
Cash Payment copy under `01-Without-OOD-Principles/` and the existing
`docs/solid-analysis.md` may be inspected for context but must not be treated as
proof; independently verify every conclusion against root source code and its
callers.

Evaluate representative possible SRP, OCP, LSP, ISP, and DIP violations. Cite
repository-relative files, classes/methods, and current line ranges. For each
candidate say whether it is confirmed, not demonstrated, or uncertain, explain
why, and propose only the smallest useful correction with behavior risks,
tradeoffs, and required tests. Explicitly identify false positives or claims
that the code does not support.

This is analysis only. Do not edit, create, rename, format, or delete any file;
do not implement a refactoring; do not commit. End by requesting approval for a
numbered proposal and explicitly state whether any files were edited.
```
