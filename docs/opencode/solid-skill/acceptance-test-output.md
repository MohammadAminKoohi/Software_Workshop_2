# Release Skill Acceptance Test Output — Version 1.0

## Run metadata

- OpenCode version: 1.18.3
- Session: `ses_fd50ea122ffecFs9W2YUF6JN0B`
- Agent: `plan`
- Model: `opencode/big-pickle`
- Exit code: 0
- Final response produced: yes
- Working-tree status before/after: identical
- Project files created or edited by OpenCode: none

The final response below is preserved verbatim.

---

Analysis complete — all tools stopped, producing required output. Working-tree status matches the initial state exactly (only pre-existing untracked `.opencode/` and `docs/opencode/`).

# SOLID Analysis — root `store/` (analysis only)

## 1. Scope, revision, files inspected

- **Scope:** unchanged root `store/` (7 files). **Revision:** `4a7e0b6` on `opencode/solid-skill`, identical to `origin/main` (`git diff origin/main..HEAD -- store` empty; no extra commits). Untracked `.opencode/`, `docs/opencode/` pre-date this run.
- **Independence check:** the Cash copy under `01-Without-OOD-Principles/store/` differs from root in exactly one file — `payment.py` gained an `elif method == "cash"` branch inside the existing `PaymentProcessor.process`. Used as context only; every conclusion below rests on root source plus my own probes.
- **Callers traced:** `store/main.py` (only external entry, builds orders, calls `OrderService.process_order`); `OrderService` wires all collaborators internally. `SmsOnlyNotifier` and `MySqlDatabase.save/load` have **no production callers**. No test suite exists at root (tests live only under the non-importable `01-Without-OOD-Principles/tests/`).
- **Probes (2, side-effect-safe, `PYTHONDONTWRITEBYTECODE=1`):**
  - P1: `BundleOrder(103)` reports `subtotal=0`, `item_count=0`, `items=[]` while its children sum to `$1194.99` / 6 items; it then checks out at `$5.00` (shipping only).
  - P2: `svc.notification = SmsOnlyNotifier()` passes `isinstance(sub, NotificationService)` but `process_order(...)` fails with `NotImplementedError: An SMS notifier cannot send email`.

## 2. Candidate table

| ID | Principle | Location | Evidence | Classification | Confidence |
|---|---|---|---|---|---|
| S1 | SRP | `store/order_service.py`, `OrderService.process_order` (15–43), `_print_receipt` (45–53) | One unit owns four independently-motivated concerns: validation policy (17–20), shipping rule `5.0 if subtotal < 100 else 0.0` (25), notification-message construction (37), receipt formatting (42, 45–53). A receipt-format change, shipping-policy change, or validation-rule change each edits this same class. | **Confirmed** | High |
| C1 | OCP | `store/payment.py`, `PaymentProcessor.process` (8–24) | Closed `if/elif` dispatch on `payment_method` string across a real, growing variant axis (3 methods today). Adding a variant forces editing stable dispatch code — empirically what the Cash experiment had to do (context). Unknown-method `ValueError` (23–24) is part of the observable contract. | **Confirmed** | High |
| C2 | OCP | `store/pricing.py`, `DiscountCalculator.calculate` (8–15) | Same closed-chain structure (VIP → qty ≥ 10 → coupon). Structurally identical friction, but no repository evidence that discount rules are an intended extension axis (one hardcoded coupon ever). | **Uncertain** | Medium |
| L1 | LSP | `store/models.py`, `BundleOrder` (47–50) vs `Order` (29–44) | Subclass passes `items=[]` to base, so inherited `subtotal` (38–40) and `item_count` (42–44) observably return 0 for a non-empty aggregate (probe P1: $0.00 vs $1194.99). Caller compensates with `isinstance(order, BundleOrder)` exception (`order_service.py`:17) — a documented base-contract escape hatch. | **Confirmed** | High |
| L2 | LSP | `store/notification.py`, `SmsOnlyNotifier` (12–17) vs base (1–9) | Substitution breaks the base contract: passes `isinstance`, then `send_email` raises `NotImplementedError` (probe P2). Overrides exist solely to reject inherited operations. Currently unused in production, so blast radius is nil today. | **Confirmed** | High |
| I1 | ISP | `store/notification.py`, `NotificationService` (1–9) + `SmsOnlyNotifier` (12–17) | Implementation forced to depend on operations it cannot support (email, push) — the runtime-rejection overrides are direct proof. Additional signal: the only production client (`order_service.py`:38–39) uses just email + SMS; `send_push` is never called. | **Confirmed** | High |
| D1 | DIP | `store/order_service.py`, imports (2–5) + `__init__` (9–13) | High-level checkout workflow directly constructs `DiscountCalculator`, `PaymentProcessor`, `NotificationService`, `MySqlDatabase`. Replacing any collaborator requires editing the service body or mutating attributes post-construction (exactly the workaround my probe P2 used). Storage is concretely bound to a MySQL-named dict implementation. | **Confirmed** | High |

## 3. Smallest proposals per confirmed violation

**P‑1 (S1, SRP):** Extract receipt rendering into `store/receipt.py` (`print_receipt(order, ...)`) and move the shipping rule into a named helper/collaborator next to pricing. `OrderService` keeps pure orchestration. Files: `store/order_service.py`, new `store/receipt.py`. Behavior preserved byte-for-byte. Tests: stdout-golden test for `process_order`; boundary tests for shipping (<100 → $5.00; ≥100 → $0). Risk: low (pure move). Tradeoff: one more import/indirection. A smaller change (deleting nothing, reordering) wouldn't separate the change reasons.

**P‑2 (C1, OCP):** Give each payment method a handler object conforming to a tiny common contract; `PaymentProcessor` looks up handlers from an injected mapping and keeps the `ValueError` fallback for misses. Next variant = new handler, zero edits to dispatch or existing handlers. Files: `store/payment.py` (+ wiring in P‑5). Tests: port the regression-test style already proven in `01-Without-OOD-Principles/tests/test_payment.py` (exact print strings + receipt tokens + unknown-method error). Risk: must reproduce exact console strings. Tradeoff: 3 small classes replace one method.

**P‑3 (L1, LSP — domain decision required):** Two minimal alternatives, **I will not choose for you** because either changes observable totals:
- (a) Composition: `BundleOrder` stops inheriting `Order`; bundle checkout gets an explicit path/pricing rule. Removes the false substitutability promise and the `isinstance` special case; bundle total becomes an explicit domain rule.
- (b) Repair substitutability: override `subtotal`/`item_count` to aggregate `orders` — bundle then charges ≈ $1194.99 instead of $5.00 (direction certain, exact figure depends on discount/shipping interaction — value intentionally not asserted).
Question: is the current $5.00 bundle checkout a defect or accepted demo behavior?

**P‑4 (L2+I1, LSP/ISP):** Split the broad service into narrow channel contracts (e.g., `EmailSender`, `SmsSender` structural protocols). `NotificationService` implements both; `SmsOnlyNotifier` implements only SMS and drops the `NotImplementedError` overrides entirely; `OrderService` depends only on the two channels it uses. Files: `store/notification.py`, `store/order_service.py` typing/wiring. Tests: SMS-only object satisfies every SMS-typed site; no method anywhere raises `NotImplementedError` by design. Risk: low; unused-by-production status limits fallout. Tradeoff: slightly more types.

**P‑5 (D1, DIP):** Add the four collaborators as `__init__` parameters **and move concrete construction to the composition root** `store/main.py` (constructor-injected concrete defaults alone would be only a transitional seam, not DIP). Only caller is `store/main.py`, so no compatibility break inside the repo. Sequencing note: do P‑5 before/with P‑2/P‑4 so injected seams land once. Tests: build `OrderService` with stub collaborators; assert orchestration order and messages without touching real implementations. Risk: low. Tradeoff: `main.py` gains explicit wiring.

## 4. False positives, rejected claims, open questions

- **`MySqlDatabase` name-vs-dict mismatch** (`storage.py:1–10`): misleading smell, **not** a SOLID violation by itself.
- **`Customer` field breadth** (`models.py:6–14`): passive record; no SRP claim supported.
- **Three-method API alone ≠ ISP violation**: without `SmsOnlyNotifier`'s forced rejections, `NotificationService`'s shape would be unremarkable.
- **No explicit Python interfaces ≠ automatic DIP/ISP violation**; D1 stands on concrete construction in high-level policy, not on missing ABCs.
- **Inheritance alone ≠ LSP**: `BundleOrder` is flagged for observed zero-subtotal behavior + caller-side `isinstance` compensation, not for subclassing.
- **Dead code caution:** `SmsOnlyNotifier` (and `send_push`) have no production callers. Deletion is a separate dead-code/domain-intent decision, not part of these proposals.
- **Open questions:** (1) bundle pricing intent (gates P‑3); (2) whether discount rules are a live extension axis (gates whether C2 warrants work); (3) whether `SmsOnlyNotifier` is deliberate demo scaffolding.

## 5. Approval request

Please approve, revise, or reject individually:

1. **P‑1** — SRP: extract receipt printer + shipping rule (`store/order_service.py`, new `store/receipt.py`).
2. **P‑2** — OCP: payment-handler registry replacing the `elif` chain (`store/payment.py`).
3. **P‑3** — LSP: `BundleOrder` — choose option (a) composition or (b) repaired aggregation after you decide intended bundle pricing.
4. **P‑4** — LSP/ISP: narrow sender contracts; retire the `NotImplementedError` overrides (`store/notification.py`).
5. **P‑5** — DIP: constructor injection with composition-root wiring (`store/order_service.py`, `store/main.py`).

No files have been edited.
