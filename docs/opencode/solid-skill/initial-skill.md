# Initial OpenCode SOLID Skill — Version 0.1

This file preserves the exact initial Skill body before evaluation and
refinement. The runnable copy initially had the same contents at
`.opencode/skills/solid-refactoring/SKILL.md`.

---
name: solid-refactoring
description: Use when analyzing or refactoring application code for SRP, OCP, LSP, ISP, or DIP; requires exact code evidence, minimal proposals, explicit approval before edits, and verification after approved changes.
compatibility: opencode 1.18.3
metadata:
  assignment: SWE-Lab-2-step-4.3
  version: "0.1"
---

# Evidence-Gated SOLID Refactoring

## Purpose

Help a user evaluate possible SOLID violations and, only after explicit
approval, apply the smallest useful refactoring while preserving behavior.

## Required context

Before making claims, determine from the request and repository:

- the source scope and exclusions;
- the current revision and working-tree state;
- relevant classes, clients, callers, implementations, and tests;
- existing behavior and commands used to verify it;
- whether the user requested analysis only or implementation;
- whether the user has explicitly approved a specific proposal.

If a missing input would materially change the conclusion or edit scope, ask
for it. Otherwise inspect the repository and state reasonable assumptions.

## Phase A: inspect and analyze without editing

1. Read the scoped source before naming a violation. Trace relevant callers,
   clients, subtypes, implementations, and tests instead of judging one method
   in isolation.
2. Cite repository-relative file paths plus class/method names and current line
   ranges. Describe the exact code behavior that supports each claim.
3. Classify each candidate as `confirmed`, `not demonstrated`, or `uncertain`.
   Never turn a generic smell into a SOLID violation without principle-specific
   evidence.
4. Use these evidence tests:
   - **SRP:** identify distinct reasons the same unit must change. Size alone is
     not evidence.
   - **OCP:** identify a real extension axis where adding another variant
     requires editing stable conditional or dispatch code. A conditional alone
     is not evidence.
   - **LSP:** show an observable base contract, invariant, precondition, or
     postcondition that a subtype breaks. Inheritance alone is not evidence.
   - **ISP:** show a client or implementation forced to depend on operations it
     does not use or cannot support. A multi-method API alone is not evidence.
   - **DIP:** show high-level policy directly tied to replaceable concrete
     details. Missing explicit interfaces in a dynamic language is not evidence.
5. For every confirmed violation, propose the smallest useful correction,
   affected files, preserved behavior, tests, risks, and tradeoffs. Reject a
   framework or broad redesign unless repository evidence requires it.
6. List false positives, rejected suggestions, and unresolved domain questions
   explicitly.

## Approval gate

End analysis with a numbered proposal and ask the user to approve, revise, or
reject it. State: `No files have been edited.`

Analysis requests, general agreement with SOLID, or approval of a different
proposal are not implementation approval. Before explicit approval of the exact
files and changes:

- do not edit, create, rename, delete, format, or generate project files;
- do not run a formatter or code generator that writes files;
- do not commit, tag, push, or open a pull request.

Partial approval authorizes only the approved items. If new evidence expands
the file list or design, stop and request approval for the expanded scope.

## Phase B: implement only an approved proposal

1. Re-read the approved files and check repository state before editing.
2. Apply one logical refactoring at a time. Preserve public behavior unless the
   approved proposal explicitly changes a demonstrated defect.
3. Avoid unrelated cleanup, renaming, new dependencies, or speculative
   abstractions.
4. Inspect the diff after each logical change and run the narrowest relevant
   tests. Then run the complete discovered suite and build/smoke checks.
5. If a test fails, distinguish a regression from documented baseline behavior.
   Correct only in-scope regressions; request approval for scope expansion.
6. Do not commit, tag, push, or create reviews unless separately requested.

## Required output

For analysis-only work, return:

1. scope, revision, and files inspected;
2. candidate table: principle, exact evidence, classification, and confidence;
3. smallest proposal per confirmed violation with tradeoffs and tests;
4. rejected/uncertain findings and missing information;
5. numbered approval request ending with `No files have been edited.`

After approved implementation, return:

1. approved scope and any deviations;
2. files/classes/methods changed;
3. behavior preserved or intentionally changed;
4. commands, exit codes, and meaningful test output;
5. diff measurements and remaining risks;
6. any manual corrections to generated work.
