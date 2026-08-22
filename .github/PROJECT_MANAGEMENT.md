# SWE Lab 2 Project Management

This file defines the intended GitHub Project structure. It is a setup manifest,
not an implementation plan approval and not assignment evidence by itself.

## Project and board

- Project title: `SWE Lab 2`
- View name: `Kanban`
- Layout: Board
- Group by: `Status`
- Default repository: `MohammadAminKoohi/Software_Workshop_2`
- Initial status for every new item: `Backlog`

Keep the `Status` options in this order:

1. `Backlog`
2. `Ready`
3. `In Progress`
4. `Review`
5. `Testing`
6. `Done`

## Labels

Keep existing repository labels. Add only missing labels from this table.

| Label | Color | Description |
|---|---|---|
| `setup` | `0E8A16` | Repository, tooling, and environment setup |
| `feature` | `1D76DB` | User-visible behavior or requirement |
| `testing` | `BFDADC` | Tests, verification, and regression checks |
| `solid` | `5319E7` | SOLID analysis or design principles |
| `refactor` | `D4C5F9` | Behavior-preserving structural improvement |
| `opencode` | `0052CC` | OpenCode configuration, prompts, plans, or skills |
| `documentation` | `0075CA` | Improvements or additions to documentation |
| `experiment` | `FBCA04` | Baseline, comparison, evidence, or metrics |

The existing `documentation` label already matches this definition and should
not be recreated or overwritten.

## Work breakdown

Create every issue in `Backlog`. The suggested branch is created only when work
actually starts; do not create empty branches or test commits.

| # | Workstream | Issue title | Labels | Suggested branch |
|---:|---|---|---|---|
| 1 | Setup | Verify starter project and tests | `setup`, `testing` | `setup/verify-starter-project` |
| 2 | Setup | Configure OpenCode and AGENTS.md | `setup`, `opencode` | `setup/opencode-and-agents` |
| 3 | Baseline experiment | Preserve original project | `experiment`, `documentation` | `baseline/preserve-original` |
| 4 | Baseline experiment | Analyze Cash Payment requirement | `experiment`, `feature` | `baseline/analyze-cash-payment` |
| 5 | Baseline experiment | Implement Cash Payment without SOLID refactoring | `experiment`, `feature` | `baseline/cash-payment` |
| 6 | Baseline experiment | Test baseline Cash Payment | `experiment`, `testing` | `baseline/test-cash-payment` |
| 7 | Baseline experiment | Record baseline change metrics | `experiment`, `documentation` | `baseline/record-change-metrics` |
| 8 | SOLID analysis | Analyze SRP | `solid` | `analysis/srp` |
| 9 | SOLID analysis | Analyze OCP | `solid` | `analysis/ocp` |
| 10 | SOLID analysis | Analyze LSP | `solid` | `analysis/lsp` |
| 11 | SOLID analysis | Analyze ISP | `solid` | `analysis/isp` |
| 12 | SOLID analysis | Analyze DIP | `solid` | `analysis/dip` |
| 13 | SOLID analysis | Document confirmed SOLID violations | `solid`, `documentation` | `analysis/confirmed-solid-violations` |
| 14 | OpenCode Skill | Design SOLID review Skill | `opencode`, `solid` | `opencode/solid-review-skill` |
| 15 | OpenCode Skill | Test and refine SOLID review Skill | `opencode`, `testing` | `opencode/test-solid-review-skill` |
| 16 | Refactoring | Generate OpenCode refactoring Plan | `opencode`, `refactor` | `refactor/generate-plan` |
| 17 | Refactoring | Review and correct refactoring Plan | `opencode`, `refactor` | `refactor/review-plan` |
| 18 | Refactoring | Apply approved SOLID refactoring | `solid`, `refactor` | `refactor/apply-solid` |
| 19 | Refactoring | Run regression tests | `refactor`, `testing` | `refactor/regression-tests` |
| 20 | Second experiment | Add Cash Payment to SOLID version | `feature`, `experiment` | `feature/cash-payment-solid` |
| 21 | Second experiment | Test Cash Payment in SOLID version | `testing`, `experiment` | `feature/test-cash-payment-solid` |
| 22 | Second experiment | Compare baseline versus SOLID change effort | `experiment`, `documentation` | `experiment/compare-change-effort` |
| 23 | Report | Document important OpenCode prompts | `opencode`, `documentation` | `docs/opencode-prompts` |
| 24 | Report | Evaluate OpenCode results and corrections | `opencode`, `documentation` | `docs/opencode-evaluation` |
| 25 | Report | Complete final README/report | `documentation` | `docs/final-report` |
| 26 | Report | Final repository/submission verification | `testing`, `documentation` | `docs/submission-verification` |

## Issue content

Create each item with the reusable `Task` issue form and retain these sections:

- Goal
- Acceptance criteria
- Expected files/components
- Testing
- Evidence/report notes

Do not close an issue until its acceptance criteria and evidence are recorded.

## Branch conventions

Use one focused branch per active issue:

- `setup/...`
- `baseline/...`
- `analysis/...`
- `opencode/...`
- `refactor/...`
- `feature/...`
- `docs/...`
- `experiment/...` for comparison-only work

Branch names use lowercase kebab-case after the prefix. Link each pull request to
its issue with `Closes #<issue-number>` and do not create empty branches or test
commits solely to manufacture activity.

## Status policy

- `Backlog`: captured but not selected for immediate work.
- `Ready`: acceptance criteria are clear and dependencies are satisfied.
- `In Progress`: a developer is actively working on the issue.
- `Review`: a pull request is open and ready for teammate review.
- `Testing`: review is complete and final validation is underway.
- `Done`: the issue is completed and closed, normally after its pull request is merged.

At most one issue per developer should normally be `In Progress`.

## Project automation

Configure these built-in GitHub Project workflows:

1. `Auto-add to project`: repository `MohammadAminKoohi/Software_Workshop_2`,
   filter `is:issue,pr`.
2. `Item added to project`: for issues and pull requests, set `Status` to
   `Backlog`.
3. `Item reopened`: set `Status` to `Ready` if that built-in workflow is
   available in the account's Project UI; otherwise move reopened items manually.
4. `Item closed`: set `Status` to `Done`.
5. `Pull request merged`: set `Status` to `Done`.

The transitions to `Ready`, `In Progress`, `Review`, and `Testing` require human
judgment and should remain manual. In particular, opening a pull request does
not prove that it is ready for review, and no reliable built-in event means
"active development started" or "testing started." Custom GitHub Actions can
implement event-based transitions through the Projects GraphQL API, but they
require a GitHub App or project-scoped personal access token and are deliberately
out of scope for this minimal setup.
