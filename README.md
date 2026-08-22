# SWE Lab 2 — OpenCode and SOLID Refactoring Report

## 1. Objective and team

This repository records a controlled comparison between extending the original
checkout design and correcting its confirmed SOLID violations. The assignment
was completed incrementally: establish a clean baseline, add Cash Payment
without improving the design, analyze SOLID problems, design and validate an
OpenCode Skill, produce and review an OpenCode Plan, apply the approved
refactoring, and evaluate the result honestly.

| Role | Contributor | Recorded responsibility |
|---|---|---|
| Repository owner/coordinator | [MohammadAminKoohi](https://github.com/MohammadAminKoohi) | Task scope, approvals, manual corrections, final verification, and report assembly |
| Teammate | [arshiaizd](https://github.com/arshiaizd) | Authored or merged several focused PRs, including the Task 5 merge |
| OpenCode | OpenCode 1.18.3 using `opencode/big-pickle` | Cash analysis/implementation, Skill validation runs, Plan generation, and approved Build Steps 0–3 plus the beginning of Step 4 |
| AI coding coordinator | Codex | Evidence review, Skill/Plan refinement, manual completion after OpenCode was stopped, testing, and documentation |

GitHub records genuine teammate authorship and merge activity, but it records
**no submitted pull-request reviews** on PRs #38–#44. Those merges are not
misrepresented here as formal approval reviews. The final-report PR must request
a genuine review and remain unmerged until another person reviews it.

## 2. Project/OpenCode setup and baseline

The unchanged Python starter contains seven files under `store/`, 10 explicitly
declared classes, 19 explicitly declared functions/methods, and 214 physical
source lines. `OrderService` directly constructs pricing, payment,
notification, and storage collaborators and coordinates the entire checkout.
The repository has no dependency manifest, packaging configuration, build
script, or root test suite.

The clean baseline is documented in
[`docs/baseline-verification.md`](docs/baseline-verification.md).

| Baseline item | Evidence |
|---|---|
| Starter commit | [`c34b3aa`](https://github.com/MohammadAminKoohi/Software_Workshop_2/commit/c34b3aa95f7ca84e3b01b36c6ff48bd08096002b) |
| Baseline checkpoint commit | [`ace844f`](https://github.com/MohammadAminKoohi/Software_Workshop_2/commit/ace844f31cb5e39c2e0fc48faecabe07d60f30f0) |
| Annotated tag object | `baseline-initial` → `57ad6260c3990934e6ccd67d6183882cc289654e` |
| Tag target | `ace844f31cb5e39c2e0fc48faecabe07d60f30f0` |
| Python / Git | Python 3.13.2 / Git 2.39.5 (Apple Git-154) |
| Compilation | Exit 0 |
| Root unittest discovery | Exit 5; 0 tests; `NO TESTS RAN` |
| Demo | Exit 0; simple order `$819.99`; bundle `$5.00` |

The zero-test result is a missing baseline suite, not a passing result. The
bundle contains child orders totaling `$1194.99`, but inherited order properties
read an empty `items` collection, so the baseline bundle subtotal is `$0.00`
and checkout charges only `$5.00` shipping.

Repository setup used `.github/` issue/PR templates and the project-local
OpenCode Skill under `.opencode/skills/solid-refactoring/`. No secret, generated
dependency, or external test framework was added.

## 3. Original-design Cash Payment experiment

The first experiment is preserved under the exact required directory
[`01-Without-OOD-Principles/`](01-Without-OOD-Principles/). It intentionally
adds Cash Payment to the existing conditional design before any SOLID
correction.

OpenCode first ran an analysis-only prompt, identified
`PaymentProcessor.process` as the only required production target, separated
optional tests/demo work, and stopped at an approval gate. The human-approved
contract was:

- selector: `payment_method == "cash"`;
- console output: `[payment] Receiving cash {amount:.2f}`;
- receipt token: `paid_by_cash:{amount:.2f}`;
- built-in `unittest` coverage; and
- no strategy, factory, interface, DI, demo change, or unrelated refactoring.

OpenCode Build then implemented the approved branch and tests. It corrected one
of its own tests that leaked uncaptured console output; subsequent human review
required no production-source correction. The root `store/` remained unchanged.

Evidence:

- [analysis prompt](01-Without-OOD-Principles/opencode/cash-payment-analysis-prompt.md)
  and [verbatim output](01-Without-OOD-Principles/opencode/cash-payment-analysis-output.md);
- [human analysis review and approval](01-Without-OOD-Principles/analysis/cash-payment-analysis-review.md);
- [implementation prompt](01-Without-OOD-Principles/opencode/cash-payment-implementation-prompt.md)
  and [verbatim output](01-Without-OOD-Principles/opencode/cash-payment-implementation-output.md);
- [measurements and independent checks](01-Without-OOD-Principles/analysis/cash-payment-change-report.md);
- [Task 1 issue #29](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/29)
  and merged PRs [#39](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/39)
  and [#40](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/40).

## 4. Required file/class change table and necessity explanations

The implementation measurement compares the preserved original-design tree
immediately before Build (`469cbbb`) with the completed experiment.

| File/class | Change | Why it was necessary |
|---|---|---|
| `01-Without-OOD-Principles/store/payment.py` / `PaymentProcessor.process` | Modified one existing method; added one `elif` condition and four production lines | The experiment required Cash Payment while explicitly preserving the original string selector and conditional dispatcher. |
| `01-Without-OOD-Principles/tests/test_payment.py` / `CashPaymentTest` | Added a test class | Pins the exact cash console message and receipt token. |
| `01-Without-OOD-Principles/tests/test_payment.py` / `ExistingPaymentRegressionTest` | Added a test class | Protects credit-card, PayPal, and Bitcoin behavior from accidental changes. |
| `01-Without-OOD-Principles/tests/test_payment.py` / `UnknownPaymentMethodTest` | Added a test class | Confirms unsupported selectors still raise `ValueError`. |

| Required metric | Result |
|---|---:|
| Files changed | 2 |
| Production files modified | 1 |
| Existing classes modified | 1 |
| Existing methods changed | 1 |
| Conditions added | 1 |
| New production classes | 0 |
| New test classes | 3 |
| Production dependencies changed | 0 |
| Lines added / removed | 90 / 0 |
| Production lines added / removed | 4 / 0 |

This small change is empirical OCP evidence: the new payment variant could only
be added by modifying stable dispatch code.

## 5. SOLID table for the original design

The detailed source analysis is retained in
[`docs/solid-analysis.md`](docs/solid-analysis.md) and tracked by
[Task 2 issue #31](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/31)
and [PR #41](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/41).

| Principle | Followed? | Exact evidence | Conclusion |
|---|---|---|---|
| SRP | No | `store/order_service.py`, `OrderService.process_order` and `_print_receipt` | Checkout orchestration also owns validation, shipping policy, notification-message construction, and receipt presentation—independent reasons to change. |
| OCP | No | `store/payment.py`, `PaymentProcessor.process`; `store/pricing.py`, `DiscountCalculator.calculate` | New payment or discount variants require edits to closed conditional chains. The Cash experiment demonstrates the payment cost directly. |
| LSP | No | `store/models.py`, `BundleOrder`; `store/notification.py`, `SmsOnlyNotifier` | Bundle inherited values ignore contained orders and require a subtype exception; SMS-only substitution removes supported base operations by raising `NotImplementedError`. |
| ISP | No | `NotificationService` / `SmsOnlyNotifier` | The SMS-only implementation is forced to expose unsupported email and push operations. |
| DIP | No | `store/order_service.py`, imports and `OrderService.__init__` | The high-level workflow imports and constructs replaceable concrete collaborators instead of consuming narrow injected behavior. |

Claims deliberately rejected include treating `Customer` fields as automatic
SRP evidence, treating the `MySqlDatabase` name/dictionary mismatch as a SOLID
violation, or requiring explicit interfaces everywhere merely because the code
is Python.

## 6. Cause, correction, and rationale for each confirmed violation

| Principle | Cause | Applied correction | Rationale |
|---|---|---|---|
| SRP | Shipping policy and receipt formatting lived inside the checkout orchestrator. | Injected `ShippingCalculator` and `ReceiptPrinter`; retained small orchestration and current validation. | Separates demonstrated change reasons without splitting every line or inventing a validation framework. |
| OCP | Payment and discount variants were hard-coded in conditional ladders. | Injected a payment-handler registry and an ordered list of discount rules. | New synthetic handlers/rules can be supplied without changing stable algorithms; exact output, priority, and rounding remain pinned. |
| LSP — bundle | `BundleOrder(Order)` contained orders but inherited scalar-order behavior based on an empty item list. | Replaced inheritance with composition while retaining the baseline-compatible fields and `$5.00` behavior. | States the relationship honestly without silently choosing new bundle aggregation/pricing semantics. |
| LSP/ISP — notifier | `SmsOnlyNotifier` inherited and rejected email/push operations. | Made it a standalone SMS implementation and injected separate narrow email/SMS contracts. | Clients see only supported operations; substitutes no longer remove promised behavior. |
| DIP | `OrderService` selected and constructed concrete dependencies. | Required narrow structural contracts through its constructor; `store/main.py` became the composition root. | High-level checkout policy now depends on required behavior while the entry point owns concrete selection. |

Cash Payment, bundle repricing, validation-policy extraction, a DI container,
plugin framework, broad base-class hierarchy, and renaming `MySqlDatabase` were
excluded because they were outside the confirmed correction scope.

## 7. SOLID Skill purpose, supplied information, structure rationale, and test

The project Skill is
[`solid-refactoring`](.opencode/skills/solid-refactoring/SKILL.md). Its complete
design and four-run refinement history are recorded in
[`docs/opencode/solid-skill/README.md`](docs/opencode/solid-skill/README.md),
[Task 3 issue #32](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/32),
and [PR #42](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/42).

### Purpose

The Skill prevents generic smells from being labeled as SOLID violations,
prevents broad redesign before behavior is understood, and enforces an explicit
approval gate before edits.

### Information supplied to the Agent

The Skill supplies required context (scope, exclusions, revision, state,
callers, implementations, tests, behavior, mode, and approval status),
principle-specific evidence rules, honest classifications, proposal validity
checks, side-effect-safe probe rules, approval semantics, incremental Build
instructions, and required output schemas. Repository-specific prompts supplied
the root `store/` scope and required all conclusions to be reverified rather
than copied from the existing analysis.

### Why the Skill has this structure

- Evidence tests prevent size, a conditional, inheritance, a broad API, or a
  missing explicit Python interface from becoming proof by itself.
- A completion guard requires the evidence table, proposals, uncertainties,
  approval request, and edit-status disclosure before the Agent stops.
- Proposal checks reject fake OCP/DIP fixes such as merely moving a conditional
  or retaining hidden concrete defaults in the high-level service.
- The approval gate separates diagnosis from authorization and limits partial
  approval to exact numbered items.
- Incremental Build guidance requires diff inspection and focused plus complete
  verification after approval.

### Validation

`opencode debug skill` discovered the Skill successfully. Four Plan-mode runs
used `opencode/big-pickle` without authorized source edits:

| Version | Concrete finding | Refinement |
|---|---|---|
| 0.1 | Inspected correctly but ended without the required final response. | Added completion guard and probe budget. |
| 0.2 | Omitted DIP and created `__pycache__`; suggested unsafe deletion/speculative numbers. | Added safe-probe, full-principle, dead-code, and numeric-claim rules. |
| 0.3 | Complete and side-effect safe, but proposed a non-extensible discount tuple list and only partial DIP. | Added proposal-validity and tradeoff checks. |
| 1.0 | Produced the complete evidence table, safe probes, false-positive section, scoped proposals, approval gate, and identical before/after state. | Accepted with one recorded wording correction for an unsupported approximate bundle charge. |

Exact acceptance evidence: [prompt](docs/opencode/solid-skill/acceptance-test-prompt.md)
and [output](docs/opencode/solid-skill/acceptance-test-output.md).

## 8. Original OpenCode Plan, review, corrections, reasons, and approved Plan

OpenCode 1.18.3 ran in Plan mode in session
`ses_fd4fd85bfffepTQyqsyt0U4c3F` using the exact
[Plan prompt](02-Applied-OOD-Principles/opencode/plan-prompt.md). Its
[original output](02-Applied-OOD-Principles/opencode/original-plan-output.md)
was preserved before the AI coding coordinator reviewed it against source and
behavioral evidence.

Important retained corrections include:

| Original Plan issue | Correction | Reason |
|---|---|---|
| DIP was omitted from the violation-to-step table. | Added DIP and mapped it to dependency injection/composition-root wiring. | Every step must trace to confirmed evidence. |
| A smoke command was described as running in the applied copy but ran at root. | Kept it only as baseline evidence and required future commands to run inside the applied workspace. | Command attribution must be exact. |
| Future test counts were estimated. | Removed estimates and required observed counts. | Measurements cannot be invented. |
| Contract included unused `load_order`. | Retained only client-required `save_order`. | Avoid a new ISP problem. |
| One-line message construction was extracted. | Kept it in the orchestrator; extracted only shipping and receipts. | No independent change reason was demonstrated. |
| Registries/rules could be hidden behind defaults. | Required constructor-supplied collections and composition-root wiring. | Hidden concrete selection would leave DIP/OCP incomplete. |
| Bundle alternatives either deferred LSP or changed pricing. | Chose composition while preserving zero values and the `$5.00` total. | Correct the type relationship without an unapproved business change. |
| Cash was suggested as a future extension test. | Used synthetic test-only variants and excluded Cash. | Cash belongs only to the original-design comparison experiment. |

The full [critical review](02-Applied-OOD-Principles/planning/review-notes.md),
[corrected Plan](02-Applied-OOD-Principles/planning/corrected-plan.md),
[affected-file map](02-Applied-OOD-Principles/planning/affected-files.md),
[risk register](02-Applied-OOD-Principles/planning/risk-register.md), and
[test plan](02-Applied-OOD-Principles/planning/test-plan.md) are retained.
Repository owner `MohammadAminKoohi` approved the corrected Steps 0–8 by merging
[PR #43](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/43)
as `db4e8450763aeadc20ab987cc423c48c8470f43c`. GitHub records no submitted
review on that PR; the owner merge is the attributable approval decision.

## 9. Build-mode refactoring, commits, tests, and corrections

The exact [Build prompt](02-Applied-OOD-Principles/opencode/build-prompt.md)
authorized only the corrected Plan inside
[`02-Applied-OOD-Principles/`](02-Applied-OOD-Principles/). Cash Payment and
protected root sources/configuration were excluded.

| Step | Result | Commit | Authoring attribution |
|---:|---|---|---|
| 0 | Added 26 characterization tests. | `ff28085` | OpenCode; coordinator reviewed/corrected expectations. |
| 1 | Injected narrow checkout dependencies. | `9ea62b0` | OpenCode; coordinator reviewed. |
| 2 | Extracted shipping calculation. | `1f0fc23` | OpenCode; corrected invalid DI-test syntax and missing composition-root import. |
| 3 | Extracted receipt presentation. | `8b3f2ba` | OpenCode; corrected duplicate discovery, presenter contract, spacing, and caller adaptation. |
| 4 | Replaced payment conditionals with handler dispatch. | `7ff1ff2` | OpenCode began an incomplete import edit; coordinator stopped it and completed the step. |
| 5 | Composed ordered injected discount rules. | `49a7cbf` | Coordinator after the user explicitly stopped OpenCode. |
| 6 | Separated notification channel contracts. | `efb353d` | Coordinator after OpenCode was stopped. |
| 7 | Replaced false bundle inheritance with composition. | `040d774` | Coordinator after OpenCode was stopped. |
| Final evidence | Recorded full verification and checkpoint. | `88a17f0` | Coordinator. |

OpenCode 1.18.3 completed Steps 0–3 in Build session
`ses_fd4dceb8bffeRJxcTrv1Y9YGMG`. It began Step 4 but left an incomplete edit.
The user explicitly instructed the coordinator to stop using OpenCode, so it
was not restarted. The coordinator completed Step 4 and manually implemented
Steps 5–7. **Complete OpenCode execution of the approved Plan is not claimed.**

Per-step prompts, outputs, diffs, tests, and attribution are indexed by the
[Plan traceability table](02-Applied-OOD-Principles/build/plan-traceability.md)
and [manual-correction record](02-Applied-OOD-Principles/build/manual-corrections.md).
Final refactoring measurements are 8 changed production files (6 modified, 2
new), 242 additions, 66 removals, 8 focused test modules, and 74 tests.

The annotated `solid-refactored` tag object is
`76be03a3a3cbb4f2917fe39e8770b1958ae6e84a` and resolves to
`88a17f0e2389dd74fb21bbf1b21054386ce1dce9`.
[Task 5 issue #34](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/34)
was closed by merged [PR #44](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/44).
`arshiaizd` genuinely merged the PR, but GitHub records no formal submitted
review; merge activity is not labeled as review evidence.

## 10. OpenCode evaluation

### 10.1 What OpenCode analyzed correctly

- The Cash analysis traced the string payment flow, selected the one necessary
  production method, avoided a cash-specific customer field, preserved the poor
  architecture deliberately, and stopped for approval.
- Skill validation found concrete SRP, payment OCP, bundle/notifier LSP,
  notifier ISP, and concrete-construction DIP evidence while rejecting generic
  false positives.
- The Plan began with characterization tests, preserved `$819.99`/`$5.00`,
  proposed focused commits, kept discount priority and exact payment errors,
  and rejected DI/plugin frameworks and external test dependencies.
- Build Steps 0–3 created a useful regression foundation and correct dependency,
  shipping, and receipt boundaries after review.

### 10.2 Where Agent responses required correction

- Skill v0.1 ended without its required output; v0.2 omitted DIP and polluted
  the tree with bytecode; v0.3 proposed incomplete OCP/DIP fixes.
- The accepted Skill response still used one unsupported approximate future
  bundle amount; the report records direction only unless the domain rule is
  selected and calculated.
- The original Plan omitted DIP mapping, misattributed one command's working
  directory, predicted test counts, broadened a repository interface, added an
  unjustified helper, and allowed hidden concrete defaults.
- Build characterization initially used incorrect demo expectations and receipt
  spacing. Later steps exposed an invalid signature, missing import, duplicate
  test discovery, an invalid presenter fake, and missed caller adaptation.
- Step 4 was incomplete when OpenCode was stopped; leaving it unchanged would
  have imported classes that did not exist.

### 10.3 Most important prompts

1. The [Cash analysis prompt](01-Without-OOD-Principles/opencode/cash-payment-analysis-prompt.md)
   forced inspection, affected-file listing, architecture preservation, and an
   exact approval-gate ending.
2. The [Cash Build prompt](01-Without-OOD-Principles/opencode/cash-payment-implementation-prompt.md)
   encoded the approved strings, file boundary, tests, and prohibited redesign.
3. The [Skill acceptance prompt](docs/opencode/solid-skill/acceptance-test-prompt.md)
   required independent evidence for all five principles and no edits.
4. The [Plan prompt](02-Applied-OOD-Principles/opencode/plan-prompt.md)
   required incremental scope, invariants, dependencies, risks, tests, and an
   approval request.
5. The [Build prompt](02-Applied-OOD-Principles/opencode/build-prompt.md)
   restricted each invocation to one approved step and required exact evidence.

### 10.4 How the Skill affected response quality

The Skill made later analysis more reviewable by requiring exact evidence,
confidence/classification, false positives, smallest proposals, tradeoffs,
side-effect-safe probes, and explicit edit status. Its refinement history also
shows that instructions alone are insufficient: completion and proposal-validity
guards had to be added after observing failures. The strongest improvement was
separating a plausible refactoring pattern from a correction that actually
creates an extension or dependency boundary.

### 10.5 What the team would change next time

- Use a permission-capable OpenCode session from the start and pin the working
  directory in every command.
- Add characterization tests before asking any Agent to propose production
  refactoring, eliminating speculative expected values.
- Require machine-readable per-step command/exit summaries and compare test
  counts as well as pass/fail state.
- Test Skill completion, filesystem side effects, and proposal validity before
  using it for an assignment run.
- Define ambiguous domain behavior—especially bundle pricing—before planning.
- Arrange formal GitHub review before merge and verify the submitted review
  record, rather than treating merge authority as review evidence.
- Stop immediately when a user revokes tool authorization, preserve the partial
  diff, and attribute later manual work separately, as done here.

## 11. Conclusion and final verification

The assignment now contains the exact required directories, the original-design
Cash comparison, source-backed SOLID analysis, the reusable Skill, the original
and corrected Plan, incremental Build evidence, honest manual corrections, and
this final evaluation. The refactoring improves SRP, OCP, LSP, ISP, and DIP
without adding Cash Payment or changing the observed demo totals.

### Final command results

These checks were rerun on 2026-08-23 at `02:01 +0330` from a clean local copy
of the Task 5 tree plus this report:

| Scope | Command | Exit | Result |
|---|---|---:|---|
| Root baseline | `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-task6-root-pycache python3 -m compileall -q store` | 0 | No output |
| Root baseline | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` | 5 | 0 tests; known missing-suite baseline |
| Root baseline | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | `$819.99` and `$5.00` |
| Cash experiment | `python3 -m compileall -q store tests` with external cache | 0 | No output |
| Cash experiment | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 6 tests passed |
| Cash experiment | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | `$819.99` and `$5.00` |
| Applied design | `python3 -m compileall -q store tests` with external cache | 0 | No output |
| Applied design | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 74 tests passed |
| Applied design | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | `$819.99` and `$5.00` |
| Repository | `git diff --check db4e845..88a17f0` | 0 | No whitespace errors |
| Scope guard | Diff Task 5 against `store/`, `01-Without-OOD-Principles/`, `.github/`, `.opencode/` | 0 | Protected paths unchanged |
| Hygiene | `find . -name __pycache__ -o -name '*.pyc'` | 0 | No generated bytecode found |

### GitHub and repository verification

| Item | Verified state |
|---|---|
| Current main before Task 6 | `051562c7d3bcba95301798b8d59b0322b1a56eec` (merge of PR #44) |
| Required directories | `01-Without-OOD-Principles/` and `02-Applied-OOD-Principles/` both present exactly |
| Root report | `README.md` present |
| Baseline tag | Annotated and resolves to `ace844f31cb5e39c2e0fc48faecabe07d60f30f0` |
| SOLID tag | Annotated and resolves to `88a17f0e2389dd74fb21bbf1b21054386ce1dce9` |
| Focused Task issues | #28, #29, #31, #32, #33, and #34 closed; [Task 6 #36](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/36) remains open pending final PR review/merge |
| Prior PRs | #38–#44 merged; no formal reviews recorded |
| GitHub CI/checks | No workflow exists under `.github/workflows/`; PR #44 reported 0 check runs and 0 commit statuses |
| Task 6 branch | `docs/final-report` |
| Kanban intent | Task 6 moves from Backlog/In Progress to Review when the final PR is opened, then Done only after genuine review and merge |

### Final repository tree

```text
.
├── .github/
├── .opencode/skills/solid-refactoring/
├── 01-Without-OOD-Principles/
│   ├── analysis/
│   ├── opencode/
│   ├── store/
│   └── tests/
├── 02-Applied-OOD-Principles/
│   ├── build/
│   ├── opencode/
│   ├── planning/
│   ├── store/
│   └── tests/
├── docs/
│   ├── baseline-verification.md
│   ├── opencode/solid-skill/
│   └── solid-analysis.md
├── store/
└── README.md
```

### Final submission checklist

- [x] README sections follow the required assignment order.
- [x] Both required directories use their exact names.
- [x] Prompts, outputs, approvals, AI review, corrections, tests, measurements,
  commits, and tags are linked and traceable.
- [x] The OpenCode evaluation answers all five required questions with concrete
  examples.
- [x] OpenCode Steps 0–3, partial Step 4, and coordinator Steps 4–7 are
  distinguished accurately.
- [x] Baseline, Cash, and applied compile/test/smoke checks were rerun.
- [x] Protected root/configuration paths and repository hygiene were verified.
- [x] Genuine teammate merge activity is distinguished from absent formal
  review submissions.
- [ ] Final Task 6 PR receives a genuine submitted review and is merged by a
  teammate; this cannot be self-generated or self-approved.

The final report branch head SHA, PR URL, Task 6 check status, and submission
timestamp are recorded in the Task 6 pull request and handoff after the branch
is published. The owner must not self-review or self-merge that PR.
