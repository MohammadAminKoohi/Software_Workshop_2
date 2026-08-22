# Refined Skill Test Output — Version 0.2

## Run metadata

- OpenCode version: 1.18.3
- Agent: `plan`
- Model: `opencode/big-pickle`
- Exit code: 0
- Final response produced: yes
- Source edits: none
- Unwanted side effect: `store/__pycache__/` created by the smoke probe

The final response below is preserved verbatim.

---

Analysis complete per the skill's required output format.

---

# SOLID Analysis Run — root `store/` (analysis only)

## 1. Scope, revision, files inspected

- **Revision:** `4a7e0b6` ("Merge pull request #41"), working tree clean of tracked changes at start
- **Scope:** root `store/` only; `01-Without-OOD-Principles/` copy and `docs/solid-analysis.md` inspected for context only, every conclusion below re-verified independently against root source
- **Files inspected:** all 7 scoped files (`models.py`, `order_service.py`, `payment.py`, `pricing.py`, `notification.py`, `storage.py`, `main.py`)
- **Caller trace:** `store/main.py` is the sole entry point; no tests exist in root scope
- **Probes (1 of 2 allowed):** `python3 -m store.main` → exit 0

## 2. Candidate table

| # | Principle | Evidence (file:lines) | Classification | Confidence |
|---|---|---|---|---|
| C1 | SRP | `OrderService.process_order` does validation (order_service.py:17-20), shipping rule (:25), status mutation (:32), notification policy+message formatting (:36-39); `_print_receipt` is console presentation (:45-53). Distinct change reasons: shipping threshold edits :25; receipt format edits :45-53 | **Confirmed** | High |
| C2 | OCP | `PaymentProcessor.process` if/elif dispatch on method string with `ValueError` fallback (payment.py:8-23). Adding a variant requires editing stable dispatch code | **Confirmed** | High |
| C3 | OCP | `DiscountCalculator.calculate` first-match elif chain VIP→bulk→coupon (pricing.py:8-15). Plausible axis, but no repo evidence rules must grow or that first-match exclusivity isn't intended policy | **Uncertain** | Low |
| C4 | LSP | `BundleOrder.__init__` passes `items=[]` to base (models.py:49), so inherited `subtotal`/`item_count` (models.py:38-44) return 0 despite $1194.99 / 6 child items; forces `isinstance` escape hatch (order_service.py:17). Probe: bundle charged **$5.00** total on $0.00 subtotal | **Confirmed** | High |
| C5 | LSP + ISP | `SmsOnlyNotifier` overrides `send_email`/`send_push` to raise `NotImplementedError` (notification.py:13-17) — cannot substitute for base clients entitled to call them (notification.py:2-9). However: **zero callers** anywhere in scope | **Confirmed structurally**, latent (dead code) | High |

## 3. Smallest proposals for confirmed violations

**P1 — DIP: inject collaborators into `OrderService`** (order_service.py:9-13)
Constructor accepts optional `discount_calculator`, `payment_processor`, `notification`, `database`, defaulting to today's concrete classes. Behavior identical; enables test doubles where none are currently possible (zero tests exist because process_order hardwires printing/charging/emailing).
*Risks:* minimal (None-sentinel keeps call sites unchanged). *Tests:* fake storage/notifier/payment capturing calls; assert `total = subtotal − discount + shipping`, `status == "paid"`.

**P2 — LSP `BundleOrder`: needs a domain decision first**
- (a) *Smallest safe:* stop claiming substitutability (separate type, update main.py) — zero behavior change.
- (b) *Defect fix:* aggregate child items so subtotal/item_count/receipt reflect children — **changes observable charging from $5.00 to ~$1,055+** (VIP discount applies). Cannot choose without knowing intended bundle pricing/shipping semantics.

**P3 — SRP: extract receipt presentation** into an injected `ReceiptPrinter`; keep shipping inline until rules actually grow (size alone isn't evidence; validation extraction likewise deferred).

**P4 — OCP payment:** map method string → handler selected from an injected registry; preserve exact receipt strings and the `Unknown payment method` ValueError. *Tests:* parity per existing branch.

**P5 — ISP/LSP `SmsOnlyNotifier`:** smallest = delete (no callers). If it encodes a real future requirement, fold narrow channel contracts into P1's injection instead.

## 4. Rejected claims / false positives / missing info

- `Customer` holding `credit_card`/`bitcoin_address` — passive record; **not demonstrated** as SRP
- `MySqlDatabase` being an in-memory dict with a misleading name — smell, **not a SOLID violation**
- Missing explicit Python interfaces per se — **not** DIP/ISP evidence
- Three-method `NotificationService` alone — **not** ISP evidence without an unsupported-ops implementer (C5 supplies it)
- Discount conditionals alone (C3) — conditional ≠ violation without a demonstrated extension axis
- **Missing:** intended bundle pricing semantics (blocks P2 choice)

## 5. Approval request

1. Approve P1 (DIP injection)?
2. P2: choose (a) de-typing or (b) defect fix — (b) requires stating expected bundle totals?
3. Approve P3 (receipt extraction)?
4. Approve P4 (payment strategy registry)?
5. P5: delete `SmsOnlyNotifier`, or defer to channel protocols?

Please approve, revise, or reject any subset; partial approval authorizes only approved items.

**Edit-status disclosure:** `No files have been edited.` Working tree matches the initial snapshot except `store/__pycache__/`, an untracked bytecode-cache byproduct of the read-only probe (contains no source changes).
