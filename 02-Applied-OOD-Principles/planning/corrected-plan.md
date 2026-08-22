# Corrected and Recommended SOLID Refactoring Plan

## Scope and invariants

All future implementation is confined to `02-Applied-OOD-Principles/`. The
root `store/` and `01-Without-OOD-Principles/` remain untouched. Cash Payment is
excluded. Preserve these observable behaviors unless a step explicitly records
an approved contract correction:

- simple demo total `$819.99` and receipt `paid_by_credit_card:819.99`;
- bundle demo subtotal `$0.00`, shipping `$5.00`, total `$5.00`, and receipt
  `paid_by_credit_card:5.00`;
- discount priority VIP, then quantity, then `WELCOME10`, with current rounding;
- supported payment stdout, return strings, and exact unknown-method error;
- email, SMS, receipt ordering, formatting, order status, and persistence.

The one intentional API correction is that `SmsOnlyNotifier` will no longer
advertise unsupported email or push methods. This requires explicit human
approval before implementation.

## Confirmed violations and planned steps

| Confirmed violation | Exact evidence | Corrected step |
|---|---|---:|
| SRP | `OrderService.process_order` owns shipping policy; `_print_receipt` owns presentation | 2–3 |
| OCP | `PaymentProcessor.process` and `DiscountCalculator.calculate` are extension condition chains | 4–5 |
| LSP | `BundleOrder(Order)` reports inherited zero values despite containing orders; `SmsOnlyNotifier` rejects inherited operations | 6–7 |
| ISP | `SmsOnlyNotifier` is forced to expose email and push | 6 |
| DIP | `OrderService` imports and constructs concrete collaborators | 1–3 |

## Incremental implementation sequence

### Step 0 — Pin baseline behavior

Add `tests/test_characterization.py` under the applied workspace. Cover exact
payment outputs and unknown-method errors; discount precedence and rounding;
empty-order/payment validation; simple and bundle demo totals/stdout; order
status and persistence; email/SMS/receipt output; `SmsOnlyNotifier`'s current
`NotImplementedError`; and bundle zero-value versus child-value evidence.

Run compilation, the focused file, all discovered tests, and the demo from the
applied workspace. Record actual counts and output. Commit boundary:
`test: characterize original checkout behavior`.

### Step 1 — Invert existing checkout dependencies

Add minimal structural contracts in `store/contracts.py` for discount
calculation, payment processing, email sending, SMS sending, and order saving.
Each contract contains only methods called by `OrderService`; the repository
port has `save_order` only.

Change `OrderService.__init__` to require these five collaborators. Do not
construct defaults inside the service. Update `store/main.py` as the composition
root; it may pass one `NotificationService` instance as both narrow channels.
Keep shipping and receipt code unchanged in this step. Add focused injected-fake
tests proving orchestration without concrete construction. Commit boundary:
`refactor: inject checkout dependencies`.

### Step 2 — Extract shipping policy

Add `ShippingCalculator` to `store/pricing.py` with the exact current rule:
`5.0` below `$100`, otherwise `0.0`. Add the minimal shipping contract and
inject it through `OrderService`; wire it in `main.py`. Do not extract the
one-line notification message. Test values immediately below, at, and above the
threshold plus unchanged end-to-end totals. Commit boundary:
`refactor: extract shipping calculation`.

### Step 3 — Extract receipt presentation

Add `store/receipt.py` with `ReceiptPrinter.print_receipt` preserving every
line and spacing. Add the minimal presenter contract, inject it, and remove
`OrderService._print_receipt`. Test exact simple and bundle receipt output and
unchanged call ordering visible in the demo. Commit boundary:
`refactor: extract receipt presentation`.

### Step 4 — Make payment methods extensible

Replace the conditional chain in `store/payment.py` with one handler per
existing method and a `PaymentProcessor` that requires an injected
method-to-handler registry. The composition root constructs the registry for
credit card, PayPal, and Bitcoin. Preserve stdout, result strings, and the exact
unknown-method `ValueError`.

Prove extension with a test-only synthetic handler registered under a new key;
do not implement Cash Payment. Adding that handler must not require changing
`PaymentProcessor.process` or existing handlers. Commit boundary:
`refactor: dispatch payments through handlers`.

### Step 5 — Make discount rules extensible

Represent VIP, quantity, and coupon behavior as ordered rules in
`store/pricing.py`. `DiscountCalculator` requires its ordered rules through the
constructor; `main.py` selects the default order. Stop at the first applicable
rule and preserve final two-decimal rounding.

Test all rules, overlap precedence, no-match behavior, rounding, and a synthetic
test-only rule that requires no edit to the calculator algorithm. Commit
boundary: `refactor: compose ordered discount rules`.

### Step 6 — Correct notifier ISP/LSP

Keep the already injected email and SMS contracts separate. Make
`SmsOnlyNotifier` a standalone SMS implementation rather than a subclass of the
broad `NotificationService`; it exposes only `send_sms`. Production demo output
must not change because `main.py` continues to provide supported email and SMS
senders.

Update only the characterization assertion tied to the intentionally corrected
unsupported API: verify SMS works and email/push are not part of the object.
Test substitute email and SMS fakes independently. Commit boundary:
`refactor: separate notification channel contracts`.

### Step 7 — Replace false bundle inheritance with composition

Change `BundleOrder` into a standalone dataclass/domain object containing
`id`, `customer`, and `orders`, plus baseline-compatible `items`, `status`,
`payment_method`, `coupons`, `subtotal`, and `item_count` behavior. Preserve
zero subtotal and count, the explicit empty-item exemption in the workflow, the
`$5.00` bundle total, status mutation, persistence, and receipt output. Update
type annotations that accept both checkout types; do not aggregate child prices
or add a new special checkout workflow.

Tests must show that `BundleOrder` is no longer an `Order`, yet every baseline
observable remains unchanged. Commit boundary:
`refactor: model bundles with composition`.

### Step 8 — Final verification for the later Build task

From `02-Applied-OOD-Principles/`, run compilation, the complete unittest
suite, and the demo. Inspect the full diff against the clean copied baseline,
confirm no root or original-experiment source changed, and record exact counts
and outputs. No `solid-refactored` tag is part of this planning task; that tag
belongs after approved Build-mode implementation succeeds.

## Dependencies and approval gate

Step 0 precedes every production change. Step 1 establishes the composition
root. Steps 2 and 3 extend that injection boundary. Steps 4 and 5 then change
policy internals independently. Step 6 relies on the narrow channel injection
from Step 1. Step 7 is otherwise independent but runs last because its runtime
type change has the widest compatibility risk.

No Build-mode action or production edit is authorized until a human approves
this corrected plan and the intentional `SmsOnlyNotifier` API correction.
