# Applied OOD Principles — Refactored Workspace

This directory contains the behavior-preserving SOLID refactoring for
assignment step 4.5. It began as a clean copy of the original design at
`6e0c56534416b9a3c015c4aa3a9fb4922ed24c87`; the corrected Plan was approved
when repository owner `MohammadAminKoohi` merged PR #43 at
`db4e8450763aeadc20ab987cc423c48c8470f43c`.

Cash Payment is intentionally excluded. The protected root `store/` and
`01-Without-OOD-Principles/` were not changed by this branch.

## Refactoring result

| Confirmed problem | Applied correction | Commit |
|---|---|---|
| Missing regression safety | Characterized existing checkout behavior with 26 tests | `ff28085` |
| DIP: `OrderService` constructed concrete collaborators | Required narrow injected dependencies and moved wiring to `main.py` | `9ea62b0` |
| SRP: checkout owned shipping policy | Extracted and injected `ShippingCalculator` | `1f0fc23` |
| SRP: checkout owned receipt formatting | Extracted and injected `ReceiptPrinter` | `8b3f2ba` |
| OCP: payment extension required changing a conditional | Replaced the chain with injected method-to-handler dispatch | `7ff1ff2` |
| OCP: discount extension required changing a conditional | Replaced the chain with ordered, injected discount rules | `49a7cbf` |
| ISP/LSP: SMS-only notifier inherited unsupported operations | Made `SmsOnlyNotifier` a standalone narrow implementation | `efb353d` |
| LSP: bundle falsely inherited scalar order behavior | Replaced inheritance with composition while preserving baseline values | `040d774` |

`store/contracts.py` defines only the ports consumed by the checkout
orchestrator. `store/main.py` is the composition root. `OrderService` now
coordinates injected policies and adapters; pricing, payment dispatch, receipt
presentation, notifications, storage, and bundle modeling have focused roles.

## Verification

Run from this directory:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-final-pycache python3 -m compileall -q store tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 -m store.main
```

On Python 3.13.2, compilation exited 0, all 74 discovered tests passed, and the
demo exited 0 with the preserved simple-order total `$819.99` and bundle total
`$5.00`. `git diff --check origin/main...HEAD` passed. A repository-root scope
guard confirmed no branch diff in `store/`, `01-Without-OOD-Principles/`,
`.github/`, or `.opencode/`.

The production refactoring changes eight files in this workspace: six existing
files and two new files, with 242 inserted and 66 removed lines. Eight focused
test modules contain 74 regression tests. Full command results and measurements
are retained in `build/final-verification.md`.

## Plan and evidence

- `planning/corrected-plan.md`: approved incremental Plan.
- `planning/review-notes.md`: critical Plan review and corrections.
- `planning/approval.md`: approval gate and PR #43 evidence.
- `build/plan-traceability.md`: Plan-to-commit/test mapping.
- `build/step-00-evidence.md` through `build/step-07-evidence.md`: per-step
  diffs, tests, decisions, and attribution.
- `build/manual-corrections.md`: OpenCode and coordinator corrections.
- `build/final-verification.md`: final regression, scope, and measurement record.
- `opencode/build-prompt.md` and `opencode/step-*-prompt.md`: exact Build
  prompts that were run.
- `opencode/step-*-output.md`: retained OpenCode outputs.

## Human/AI attribution

OpenCode 1.18.3 in Build mode (`opencode/big-pickle`) completed Steps 0–3 in
session `ses_fd4dceb8bffeRJxcTrv1Y9YGMG`. A new Step 4 run inspected scope and
left an incomplete `main.py` import edit. The user then explicitly instructed
the coordinator to stop using OpenCode. The coordinator completed Step 4 and
implemented Steps 5–7 manually, reviewing each diff and running focused and
full tests before every commit. The retained record therefore does **not**
claim that OpenCode executed the complete approved Plan.

No teammate review is claimed on this branch yet. A genuine review remains a
required PR checkpoint before merge.
