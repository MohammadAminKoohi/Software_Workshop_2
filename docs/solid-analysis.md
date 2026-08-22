# SOLID Analysis of the Original Design

## Scope

This analysis evaluates the unchanged root `store/` at merge revision
`7f48aedaf29656dc072c48da51e4889944ed2e08`. The Cash Payment implementation
under `01-Without-OOD-Principles/` is experimental evidence only and is not the
source being analyzed. No application code was changed for this task.

## README-ready SOLID table

| Principle | Followed? | Exact location | Evidence-based explanation |
|---|---|---|---|
| SRP | No | `store/order_service.py`, `OrderService.process_order` (lines 15–43) and `_print_receipt` (lines 45–53) | The service owns workflow orchestration but also contains validation, the shipping-price rule, state mutation, notification-message construction, and receipt presentation. Those concerns change for different reasons. |
| OCP | No | `store/payment.py`, `PaymentProcessor.process` (lines 5–24); `store/pricing.py`, `DiscountCalculator.calculate` (lines 5–17) | Both extension points are closed conditional chains. A new payment method or discount rule requires editing the existing method. The first Cash Payment experiment empirically required adding an `elif` to `PaymentProcessor.process`. |
| LSP | No | `store/models.py`, `BundleOrder` (lines 47–50) relative to `Order` (lines 29–44); `store/notification.py`, `SmsOnlyNotifier` (lines 12–17) relative to `NotificationService` (lines 1–9) | `BundleOrder` initializes the inherited `items` collection as empty even though it contains child orders, so inherited `subtotal` and `item_count` report zero; `OrderService` needs an explicit subtype exception. `SmsOnlyNotifier` rejects inherited email and push operations with `NotImplementedError`, so it cannot safely replace its base class. |
| ISP | No | `store/notification.py`, `NotificationService` (lines 1–9) and `SmsOnlyNotifier` (lines 12–17) | The inherited notification contract combines email, SMS, and push. The SMS-only client/implementation is forced to expose two unsupported methods and fail at runtime. |
| DIP | No | `store/order_service.py`, imports (lines 2–5) and `OrderService.__init__` (lines 9–13) | The high-level checkout workflow imports and constructs concrete payment, discount, notification, and MySQL-named storage classes. Replacing any collaborator requires changing `OrderService`; no constructor-supplied contract or dependency boundary exists. |

## Confirmed violations and corrections

### SRP — `OrderService`

**Cause.** `process_order` coordinates the checkout use case, which is a valid
single responsibility, but it also owns rules and presentation details that are
not orchestration: order validation (lines 17–20), shipping calculation (line
25), notification message formatting (line 37), and receipt printing (lines
45–53). A validation-policy change, shipping-policy change, or receipt-format
change therefore modifies the same class.

**Proposed correction.** Keep `OrderService` as the small checkout orchestrator,
but move the shipping calculation and receipt output behind focused
collaborators. Extract validation only if its rules are expected to grow; the
existing payment, discount, persistence, and notification delegation can remain.

**Why this correction.** It removes the clearly independent reasons for change
without splitting every line into a class or replacing the recognizable
checkout workflow with unnecessary abstractions.

### OCP — payment and discount conditionals

**Cause.** `PaymentProcessor.process` switches on the payment-method string, and
`DiscountCalculator.calculate` switches on rule conditions in priority order.
Both methods must be edited when another alternative is introduced. In the
original-design experiment, Cash Payment changed one existing production method
and added one condition, directly demonstrating the payment extension cost.

**Proposed correction.** Give each payment method a small handler implementing a
common payment contract, selected by an injected registry or factory. Represent
discount policies as an ordered set of rules only if discount rules are an
intended extension point; preserve the current VIP → quantity → coupon priority.

**Why this correction.** A new payment handler can then be added without editing
existing payment implementations. An ordered discount-rule boundary permits
extension while retaining observable precedence. A general plugin framework is
not justified by this small project.

### LSP — `BundleOrder`

**Cause.** `BundleOrder` claims to be an `Order` but passes `items=[]` to the
base constructor. Consequently, inherited `Order.subtotal` and
`Order.item_count` ignore its child orders. `OrderService` exposes the mismatch
with `isinstance(order, BundleOrder)` at line 17. The demo confirms a bundle with
child subtotal `$1194.99` and six child items reports subtotal `$0.00` and zero
items, then checks out for `$5.00` shipping.

**Proposed correction.** Prefer composition: model a bundle as an aggregate of
orders instead of inheriting from `Order`, and give bundle checkout an explicit
contract/path. If the domain requires a bundle to be accepted everywhere an
order is accepted, it must instead implement equivalent subtotal, item-count,
validation, and receipt semantics before the subtype exception is removed.

**Why this correction.** The current object contains orders rather than order
items, so composition states the existing relationship honestly and removes a
false substitutability promise. The alternative is valid only after the team
defines the intended bundle pricing behavior; the analysis does not silently
change that baseline behavior.

### LSP and ISP — `SmsOnlyNotifier`

**Cause.** `SmsOnlyNotifier` inherits `send_email`, `send_sms`, and `send_push`
but overrides email and push solely to raise `NotImplementedError`. A caller
typed against or expecting `NotificationService` can use all three operations;
substitution with `SmsOnlyNotifier` therefore introduces failures. It also
demonstrates that the three-method contract is too broad for an SMS-only
implementation.

**Proposed correction.** Define narrow channel contracts such as an SMS sender
and email sender, and let concrete notifiers implement only supported channels.
Inject the exact channel collaborators required by the checkout workflow rather
than subclassing the broad concrete service.

**Why this correction.** No implementation must advertise unsupported methods,
and substituting one implementation of a narrow channel contract does not remove
operations that its clients are entitled to call.

### DIP — concrete construction in `OrderService`

**Cause.** `OrderService` imports and constructs `DiscountCalculator`,
`PaymentProcessor`, `NotificationService`, and `MySqlDatabase`. The high-level
workflow controls both policy and concrete infrastructure choices, making
replacement and focused testing require mutation of service attributes or
changes to its constructor body.

**Proposed correction.** Accept the required collaborators through constructor
parameters described by small behavioral contracts. Keep convenient default
wiring in the application composition root (`store/main.py`) rather than in the
high-level service.

**Why this correction.** Dependency direction then points from the checkout
workflow to stable behavior contracts, while the executable entry point chooses
concrete implementations. Python structural protocols or documented callable
contracts are sufficient; a large interface hierarchy is unnecessary.

## Behavioral evidence

Commands were run from the repository root with Python 3.13.2:

| Command | Result |
|---|---|
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-solid-pycache python3 -m compileall -q store` | Exit 0; no output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` | Exit 5; zero tests discovered (`NO TESTS RAN`) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | Exit 0; simple order `$819.99`; bundle `$5.00` |
| `git diff --quiet baseline-initial..HEAD -- store` | Exit 0; the analyzed root sources still match the clean baseline |
| Bundle property probe using `build_demo_orders()` | Exit 0; bundle subtotal `$0.00` versus child subtotal `$1194.99`, bundle item count `0` versus child item count `6` |
| Substitute `SmsOnlyNotifier` for `NotificationService` and call `send_email` | Exit 1; `NotImplementedError: An SMS notifier cannot send email` |

The zero-test result is an absent root test suite, not a passing test suite. The
focused tests under `01-Without-OOD-Principles/` belong to the separate Cash
experiment and were deliberately excluded from original-source analysis.

## Claims deliberately not made

- The data fields on `Customer` alone do not prove an SRP violation; it is a
  passive domain record in this project.
- `NotificationService` having three methods would not alone prove ISP failure.
  The concrete evidence is `SmsOnlyNotifier` being forced to reject two of them.
- `MySqlDatabase` storing data in a dictionary and its misleading name may be a
  design smell, but that naming/implementation mismatch is not itself a SOLID
  violation.
- The lack of explicit interfaces on every Python class is not automatically a
  DIP or ISP violation. The confirmed DIP problem is the high-level service's
  direct construction of replaceable concrete collaborators.
- No claim is made that `OrderItem`, `Order.subtotal`, or every individual model
  violates SOLID. The bundle problem is the subtype's inconsistent inherited
  behavior, not the base calculations themselves.

## Review status

This document is ready for genuine teammate review. No refactoring has been
performed, and no teammate approval is claimed yet.
