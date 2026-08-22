---
name: solid-refactoring
description: Use when analyzing or refactoring application code for SRP, OCP, LSP, ISP, or DIP; requires exact code evidence, minimal proposals, explicit approval before edits, and verification after approved changes.
compatibility: opencode 1.18.3
metadata:
  assignment: SWE-Lab-2-step-4.3
  version: "1.0"
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

## Completion guard for analysis runs

Use static inspection first. For a small repository, run no more than two
read-only behavioral probes unless the user explicitly requests exhaustive
testing; a probe must resolve a material uncertainty, not merely repeat source
evidence. Once enough evidence exists to classify the requested candidates,
stop using tools and produce the required output.

Make probes side-effect safe. For Python, use `PYTHONDONTWRITEBYTECODE=1` or a
temporary `PYTHONPYCACHEPREFIX` outside the repository. For other ecosystems,
redirect caches/build artifacts outside the repository when supported. Do not
call a probe read-only if it can create tracked or untracked project files.

An analysis run is incomplete until it returns the candidate table, proposals,
uncertainties, approval request, and edit-status statement. Never end the run
immediately after a read, search, or probe. Before the final response, compare a
read-only working-tree status with the initial status and distinguish pre-existing
untracked Skill/test evidence from changes made during the run.

## Phase A: inspect and analyze without editing

1. Read the scoped source before naming a violation. Trace relevant callers,
   clients, subtypes, implementations, and tests instead of judging one method
   in isolation.
2. Cite repository-relative file paths plus class/method names and current line
   ranges. Describe the exact code behavior that supports each claim.
3. Classify each candidate as `confirmed`, `not demonstrated`, or `uncertain`.
   Never turn a generic smell into a SOLID violation without principle-specific
   evidence.
   When the request names principles explicitly, include at least one table row
   for every named principle, even when the conclusion is `not demonstrated`.
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
7. Map every proposal back to candidate IDs in the evidence table. Do not add a
   proposal for a principle omitted from the table. Do not delete apparently
   unused code solely because no caller was found; distinguish dead-code
   evidence from domain intent. Never state a predicted numeric behavior change
   unless it was calculated from inspected code and inputs; otherwise describe
   the direction of change and mark the value unknown.

## Proposal validity checks

For each proposal, state the candidate IDs, exact files, smallest change,
preserved or changed behavior, required tests, main risk, tradeoff, and why a
smaller change would not address the principle.

Check that the correction actually addresses the named principle:

- An OCP proposal must let the next demonstrated variant be added without
  editing stable dispatch/policy code. Moving conditionals into a list in the
  same stable file is reorganization, not OCP, unless the rule set is supplied
  through an extension boundary.
- Constructor parameters with concrete defaults created inside a high-level
  class improve testability but are only a transitional seam for DIP. Full DIP
  moves concrete wiring to a composition root and makes the high-level policy
  depend only on required behavior.
- If an LSP correction changes observable behavior and domain intent is
  uncertain, present the minimal alternatives and request the domain decision;
  do not silently select a behavior-changing option.

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
