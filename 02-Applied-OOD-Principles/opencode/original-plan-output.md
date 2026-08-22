# Original OpenCode Plan Output

## Run metadata

- OpenCode version: 1.18.3
- Session: `ses_fd4fd85bfffepTQyqsyt0U4c3F`
- Agent: `plan`
- Model: `opencode/big-pickle`
- Result: successful after same-session completion prompt
- Project files edited by OpenCode: none

The initial turn inspected the repository and exited without a final response.
The recorded completion prompt was sent to the same Plan-mode session. The
complete response below is preserved verbatim from that continuation.

---

# SOLID Refactoring Implementation Plan — `02-Applied-OOD-Principles/store/`

## 1. Scope, revision, repository state, and files inspected

**Scope.** All future changes confined to `02-Applied-OOD-Principles/**` (production under `store/`, tests under a new `tests/`). Root `store/`, `01-Without-OOD-Principles/`, `docs/`, `.github/`, `.opencode/` are excluded and protected.

**Revision/state.** Branch `refactor/opencode-plan` (tracks `origin/main`), HEAD `6e0c56534416b9a3c015c4aa3a9fb4922ed24c87` — matches the invocation metadata. Working tree: clean tracked files; sole untracked path `?? 02-Applied-OOD-Principles/` (the pre-existing assignment copy). `diff -r store 02-Applied-OOD-Principles/store` → exit 0: the copy is byte-identical to the analyzed root source. Python 3.13.2; no pytest installed; no CI workflows.

**Files inspected (repository-relative).**
- Scoped copy (all read in full): `02-Applied-OOD-Principles/store/{models,pricing,notification,payment,storage,order_service,main}.py`
- Root counterpart: verified identical via recursive diff (not re-analyzed separately)
- Evidence: `docs/solid-analysis.md` (accepted scope), `docs/baseline-verification.md`, `01-Without-OOD-Principles/analysis/cash-payment-analysis-review.md`, `01-Without-OOD-Principles/tests/test_payment.py`
- Assignment: `02-Applied-OOD-Principles/opencode/plan-prompt.md`

**Read-only probe (1, side-effect-safe).** From the copy: `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` → exit 0; exact baseline stdout captured (simple order subtotal `$1024.99`, VIP discount `$205.00`, **total `$819.99`**; bundle subtotal `$0.00`, **total `$5.00`**; receipts `paid_by_credit_card:819.99` / `:5.00`; email/sms lines). This transcript is the characterization oracle. No other callers exist: `main.py:32` is the only `OrderService(...)` construction site; `SmsOnlyNotifier` has no caller in the scoped copy.

## 2. Confirmed-violation-to-plan mapping table

All rows independently re-verified against the copy's source; classification matches the accepted document.

| # | Principle | Evidence (copy paths, lines) | Classification | Plan step |
|---|---|---|---|---|
| V1 | SRP | `order_service.py` — `process_order` mixes validation (17–20), shipping rule (25), notification-message construction (36–39), receipt delegation (42); `_print_receipt` presentation (45–53); distinct change reasons | Confirmed | S2, S3 (validation extraction deferred, §9) |
| V2 | OCP | `payment.py:5–24` closed if/elif on `credit_card/paypal/bitcoin`; Cash experiment empirically required editing this method | Confirmed | S4 |
| V3 | OCP | `pricing.py:5–17` fixed precedence chain VIP → qty≥10 → `WELCOME10` | Confirmed | S5 |
| V4 | LSP | `models.py:47–50` `BundleOrder(items=[])` → inherited `subtotal`/`item_count` return 0/0 vs child `$1194.99`/6; `isinstance` escape at `order_service.py:17` | Confirmed; **not correctable under strict behavior preservation without a domain decision** | S7 (flagged alternatives) |
| V5 | LSP+ISP | `notification.py:1–9,12–17` `SmsOnlyNotifier` inherits 3-channel contract, overrides email/push to raise `NotImplementedError` | Confirmed | S6 |

## 3. Characterization-test step

**Step 0 — Pin baseline behavior (checkpoint).**
- Candidate: prerequisite for all steps; no violation.
- New files (stated explicitly): `02-Applied-OOD-Principles/tests/__init__.py` (empty), `02-Applied-OOD-Principles/tests/test_characterization.py`.
- Content (~14 tests, exact count recorded on first run): payment console-string + receipt-token assertions for credit_card/paypal/bitcoin and `ValueError` containing `'barter'` for unknown methods (patterns mirror `01-.../tests/test_payment.py`); discount precedence (VIP beats quantity beats coupon; both non-VIP rules yield 10%) and rounding; `ShippingCalculator`-era boundaries pinned at service level (subtotal 99.99 → ship 5.00; 100.00 → 0.00); end-to-end `redirect_stdout` snapshots of `main.py` scenarios asserting the **verbatim probe transcript**, totals `$819.99`/`$5.00`; `NotificationService` email/sms/push formats; `SmsOnlyNotifier.send_email`/`send_push` raise `NotImplementedError`; `BundleOrder.subtotal == 0.0`, `item_count == 0` vs child sums `1194.99`/`6` (baseline-defect evidence, deliberately pinned).
- Gate: suite must pass on the untouched copy before Step 1. Suggested commit: `test: characterize baseline checkout behavior`.

## 4. Numbered incremental refactoring steps

Each step: run full suite before and after; commit only on green.

**Step 1 — DIP: constructor-inject `OrderService` collaborators.**
- Violation: DIP (`__init__` lines 9–13 directly constructs `DiscountCalculator`, `PaymentProcessor`, `NotificationService`, `MySqlDatabase`).
- Files/classes/methods: `store/order_service.py` (`OrderService.__init__`, imports); **new file** `store/contracts.py` (small `typing.Protocol`s: discount calculation, payment processing, email/sms sending, order save/load — client-owned contracts, so dependency direction points to behavior, not concretes); `store/main.py` (`main` becomes composition root, passing all four).
- Dependencies: Step 0.
- Preserved behavior: byte-identical stdout; no defaults constructed inside the service (full DIP, not the transitional concrete-default seam).
- Tests: characterization green unchanged; add one test injecting an in-memory repository double to prove substitution.
- Risks/rollback: missed wiring (single construction site verified); revert commit. Checkpoint: suite + smoke run green.
- Commit: `refactor(dip): inject order-service collaborators via contracts`.

**Step 2 — SRP (a): extract shipping policy and notification-message construction.**
- Violation: SRP V1 (shipping rule line 25; message f-string line 37 are non-orchestration change reasons).
- Files: `store/pricing.py` gains `ShippingCalculator.cost_for(subtotal)` (5.00 if subtotal < 100 else 0.00); `store/notification.py` gains module function `build_checkout_message(order_id, total, receipt)` returning exactly `"Order {id} total ${total:.2f} ({receipt})"`; `order_service.py` delegates; `main.py` wires the calculator (new constructor param).
- Dependencies: Step 1.
- Preserved: shipping thresholds, message text, totals.
- Tests: characterization green; add direct boundary tests (99.99→5.00, 100.00→0.00) and message-format test.
- Risks: none beyond float formatting — format specifiers copied verbatim. Commit: `refactor(srp): extract shipping policy and checkout message`.

**Step 3 — SRP (b): extract receipt presentation.**
- Violation: SRP V1 (`_print_receipt` lines 45–53).
- Files: **new file** `store/receipt.py` with `ReceiptPrinter.print_receipt(order, subtotal, discount, shipping, total, receipt)` reproducing every line/format width verbatim; `order_service.py` deletes `_print_receipt`, delegates; `main.py` wires it.
- Dependencies: Steps 1–2.
- Preserved: exact receipt layout (already snapshotted).
- Tests: characterization snapshot green; direct `ReceiptPrinter` unit test.
- Risks: whitespace drift — snapshot catches it. Commit: `refactor(srp): extract receipt printer`.

**Step 4 — OCP: registry-dispatched payment handlers.**
- Violation: OCP V2.
- Files: `store/payment.py` — `CreditCardPayment`, `PaypalPayment`, `BitcoinPayment` handlers (each owns its exact console string + token), `PaymentHandler` protocol (in `contracts.py`), `default_payment_handlers()` factory, `PaymentProcessor(handlers=None)` resolving `None` → factory, raising the **unchanged** `ValueError(f"Unknown payment method: {method!r}")` on miss; `main.py` passes the factory result. (A default inside `PaymentProcessor` is acceptable: it is the payment detail module, not high-level policy; DIP at the service level is untouched.)
- Dependencies: Step 1 (injection seam).
- Preserved: all three console strings, tokens, error message/type — pinned by Step 0.
- Tests: characterization green; **new** `tests/test_payment_dispatch.py` proving a synthetic `"loyalty_points"` handler processes without editing `payment.py` dispatch (OCP acceptance proof; Cash remains excluded per constraint 4).
- Risks: dispatch-order/error-path drift — exact-message test guards. Commit: `refactor(ocp): registry-dispatched payment handlers`.

**Step 5 — OCP: ordered discount rules.**
- Violation: OCP V3.
- Files: `store/pricing.py` — `VipDiscount`, `QuantityDiscount`, `CouponDiscount` ("WELCOME10") rules, `default_discount_rules()` factory, `DiscountCalculator(rules=None)` applying **first matching rule in order, then `round(..., 2)` once** (exact current semantics); `main.py` wires factory.
- Dependencies: Step 1.
- Preserved: precedence, rates, rounding position.
- Tests: characterization precedence/rounding green; **new** `tests/test_discount_rules.py` incl. first-match proof and a synthetic appended rule extending behavior without editing `pricing.py`.
- Risks: rounding-site relocation — covered. Commit: `refactor(ocp): ordered discount rules`.

**Step 6 — ISP/LSP: narrow notification channels.**
- Violations: ISP + LSP-SmsOnly (V5).
- Files: `store/notification.py` — `NotificationService` keeps its name, implements all three channels (valid substitute for each); `SmsOnlyNotifier` rewritten to implement **only** SMS (no inheritance, no email/push methods); `contracts.py` gains `EmailSender`/`SmsSender`/`PushSender` protocols; `order_service.py` depends on `EmailSender`+`SmsSender`; `main.py` passes `NotificationService()` (satisfies both).
- Dependencies: Step 1.
- Preserved: all notification/receipt output byte-for-byte.
- **Intentional, contained deviation:** `SmsOnlyNotifier` unsupported-channel failures change from `NotImplementedError` to absent attributes (`AttributeError`); no production caller exists. In the same commit, the corresponding Step 0 assertions are updated to assert absence of `send_email`/`send_push` — the only sanctioned test edit in the plan.
- Tests: **new** `tests/test_notification_channels.py` (sms-only prints correct format; lacks other channels; `NotificationService` satisfies both protocols); all other characterization green.
- Risks: hidden external callers — none found in scope; grep re-check at implementation time. Commit: `refactor(isp,lsp): narrow notification channels`.

**Step 7 — LSP `BundleOrder`: flagged decision step (execute only the approved alternative).**
- Violation V4 cannot be corrected while preserving `$5.00` and stdout, because every correction either changes totals or formalizes current semantics. Alternatives, smallest first:
  - **Alt A (default, recommended): defer.** No code change; keep `isinstance` exception; record the open domain decision. Zero risk; principle stays flagged-open.
  - **Alt B: composition, behavior-preserving.** After Steps 1–6: `models.py` `BundleOrder` stops inheriting `Order` (exposes honest `child_subtotal`/`child_item_count`); `order_service.py` gains an explicit bundle checkout path reproducing today's arithmetic exactly (subtotal 0 → discount 0 → shipping 5.00 → total `$5.00`, empty-item receipt) so stdout is byte-identical; `main.py` adjusted. Addresses LSP by removing the false subtype promise; touches 3 production files + tests.
  - **Alt C: aggregate pricing (behavior-changing, deferred).** Requires the domain decision below; forbidden now by constraint 3.

## 5. Affected-file map

| File | Steps | Nature |
|---|---|---|
| `store/order_service.py` | 1,2,3,6,(7B) | injection, delegation, channel deps |
| `store/main.py` | 1,2,3,4,5,6,(7B) | composition-root wiring only |
| `store/pricing.py` | 2,5 | ShippingCalculator; discount rules |
| `store/payment.py` | 4 | handlers, registry, factory |
| `store/notification.py` | 2,6 | message fn; channels; SmsOnlyNotifier rewrite |
| `store/models.py` | 7B only | BundleOrder de-subtyping |
| `store/storage.py` | — | untouched (structurally satisfies repository protocol) |
| **New:** `store/contracts.py` (S1), `store/receipt.py` (S3), `tests/__init__.py` + `tests/test_characterization.py` (S0), `tests/test_payment_dispatch.py` (S4), `tests/test_discount_rules.py` (S5), `tests/test_notification_channels.py` (S6) | | stated explicitly |
| Root `store/`, `01-Without-OOD-Principles/`, `docs/` | — | never modified |

## 6. Dependency and ordering map

```text
S0 ──> S1 ──> S2 ──> S3 ──> S4 ──> S5 ──> S6 ──> S7(decision)
        └─────────────> S4,S5,S6 all require S1's seam; S4⊥S5⊥S6 mutually independent
S7-Alt B additionally builds on S1–S6; Alt A/C: no code.
```
Linear execution order above is safe; each step is one revertible commit.

## 7. Consolidated risk register

| ID | Risk | Mitigation / trigger |
|---|---|---|
| R1 | Float/rounding drift (esp. S5 rounding site) | Round-once semantics copied; precedence+rounding tests; totals 819.99/5.00 asserted |
| R2 | Stdout byte-drift | Verbatim-transcript snapshots; fail = stop, compare diffs |
| R3 | `ValueError` message/type drift (S4) | Exact-message assertion |
| R4 | Discount precedence regression | Ordered first-match design + precedence tests |
| R5 | Wiring miss after injection | Single construction site verified; smoke run per step |
| R6 | `SmsOnlyNotifier` contract change unnoticed | Sanctioned, documented test edit in S6 only |
| R7 | S7-Alt-B entrenches legacy math or creeps toward repricing | Gated behind explicit approval; Alt A default |
| R8 | Import/discovery issues (`store.*` absolute imports) | Run all commands from `02-Applied-OOD-Principles/`; `PYTHONDONTWRITEBYTECODE=1` |
| R9 | Accidental edits outside scope | Per-step `git status` + `diff -r store 02-Applied-OOD-Principles/store` expectation changes only inside the copy |

Rollback per step: `git restore`/revert of that step's commit; characterization suite rerun.

## 8. Complete test plan and expected baseline results

Commands (from `02-Applied-OOD-Principles/`, every step):
1. `PYTHONPYCACHEPREFIX=/tmp/swe-lab2-pycache python3 -m compileall -q store` → exit 0.
2. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` → all green, exit 0 (replaces repo baseline of "0 tests / exit 5"; ~14 tests at S0, ~22–26 by S6 — exact counts recorded at each run).
3. `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` → exit 0; expected verified values: simple order subtotal `1024.99`, discount `-205.00`, **TOTAL `$819.99`**, receipt `paid_by_credit_card:819.99`; bundle subtotal `$0.00`, shipping `$5.00`, **TOTAL `$5.00`**, receipt `paid_by_credit_card:5.00`; email/sms lines exactly as captured; receipt block formatting identical.

## 9. Rejected/deferred suggestions and unresolved domain decisions

**Rejected:** ABC hierarchies and DI containers (Protocols suffice; constraint 5); pytest (undeclared dependency); renaming `MySqlDatabase` (naming smell, not a confirmed SOLID violation per accepted doc); plugin frameworks; per-consumer port modules (single `contracts.py` chosen for size); Protocols for shipping/receipt/message helpers (no demonstrated substitution axis); Cash Payment (constraint 4 — later experiment); any change to root `store/` or `01-/`.
**Deferred:** `OrderValidator` extraction (accepted doc: extract only if validation rules grow — currently two checks); S7-Alt-C repricing; demo-scenario changes beyond wiring.
**Unresolved domain decisions:** **D1** — intended bundle pricing semantics (child-aggregated totals vs current zero-subtotal shipping-only charge); gates Alt B's long-term shape and enables Alt C. **D2** — whether validation policy extraction is wanted now. Neither blocks Steps 0–6.

## 10. Approval request

Please approve, revise, or reject the following exact scope:
1. Execute Steps 0–6 in order, each with its named commit boundary, new files, tests, and preserved behaviors exactly as specified in §§3–8.
2. Step 7 executes **Alt A (defer, no code change)** unless you select Alt B or defer pending D1.
3. Accept the single documented test adjustment in Step 6 (`SmsOnlyNotifier` unsupported-channel assertions) as the only characterization edit.
4. Confirm all changes remain under `02-Applied-OOD-Principles/` with no commits pushed beyond local step boundaries unless separately requested.

During this planning session only read-only inspection and one side-effect-safe probe were performed; the working tree is unchanged from its initial state (`?? 02-Applied-OOD-Principles/` pre-existing). No files have been edited.
