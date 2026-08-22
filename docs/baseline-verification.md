# Baseline Verification

This document records the unchanged starter project's structure and executable
behavior before the Cash Payment experiments or any SOLID refactoring. The
verification was performed on branch `setup/baseline-verification` from commit
`ace844f31cb5e39c2e0fc48faecabe07d60f30f0`.

## Checkpoint

- Annotated tag: `baseline-initial`
- Tag target: `ace844f31cb5e39c2e0fc48faecabe07d60f30f0`
- Parent starter commit: `c34b3aa95f7ca84e3b01b36c6ff48bd08096002b`
- Source changes between the parent starter commit and the checkpoint: none
- Checkpoint-only additions: the three GitHub project-management templates
- Working tree before verification documentation: clean

The checkpoint includes the GitHub management templates while leaving every
file under `store/` unchanged from the starter commit. This makes later Git
comparisons exclude repository-setup documentation from Cash Payment metrics.

## Tool versions

```text
Python 3.13.2
git version 2.39.5 (Apple Git-154)
```

No dependency manifest, packaging configuration, dedicated build script, or
test configuration is present in the starter repository.

## Architecture overview

The project is a small Python checkout example. `OrderService` constructs its
dependencies directly and coordinates validation, pricing, payment, storage,
notification, and receipt output in a single synchronous workflow.

| File | Important classes/functions | Responsibility |
|---|---|---|
| `store/main.py` | `build_demo_orders`, `main` | Constructs example data and runs two checkout scenarios. |
| `store/models.py` | `Customer`, `OrderItem`, `Order`, `BundleOrder` | Stores customer and order state and calculates item, subtotal, and item-count values. |
| `store/order_service.py` | `OrderService` | Validates an order, calculates its total, requests payment, saves it, sends notifications, and prints a receipt. |
| `store/payment.py` | `PaymentProcessor` | Selects credit-card, PayPal, or Bitcoin behavior from `Order.payment_method`. |
| `store/pricing.py` | `DiscountCalculator` | Applies VIP, quantity, or coupon discount rules. |
| `store/storage.py` | `MySqlDatabase` | Exposes save/load operations backed by an in-memory dictionary. |
| `store/notification.py` | `NotificationService`, `SmsOnlyNotifier` | Prints email, SMS, and push notifications; the subclass rejects unsupported channels. |

### Payment-related code

- `Order.payment_method` holds the payment selector as a string.
- `Customer.credit_card` supplies credit-card data.
- `Customer.email` is used for PayPal processing.
- `Customer.bitcoin_address` supplies Bitcoin data.
- `PaymentProcessor.process` contains branches for `credit_card`, `paypal`, and
  `bitcoin`; other values raise `ValueError`.
- `OrderService.process_order` calculates the amount and invokes
  `PaymentProcessor.process` before changing the order status to `paid`.

No Cash Payment branch or cash-specific customer field exists at this
checkpoint.

## Source measurements

The following physical line counts were recorded with `wc -l store/*.py`:

| File | Lines |
|---|---:|
| `store/main.py` | 43 |
| `store/models.py` | 50 |
| `store/notification.py` | 17 |
| `store/order_service.py` | 53 |
| `store/payment.py` | 24 |
| `store/pricing.py` | 17 |
| `store/storage.py` | 10 |
| **Total** | **214** |

The starter source contains 10 explicitly declared classes and 19 explicitly
declared functions or methods. Dataclass-generated methods are not included in
that count.

## Build status

Python bytecode compilation is used as the available build/syntax check. The
cache is redirected outside the repository so verification does not dirty the
working tree.

```bash
PYTHONPYCACHEPREFIX=/tmp/swe-lab2-baseline-pycache python3 -m compileall -q store
```

Result: passed with exit code 0 and no output.

## Test discovery status

Standard-library test discovery was run exactly as follows:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v
```

Result:

```text
----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
```

The command returned exit code 5 because no tests were discovered. This is a
missing starter test suite, not a passing automated-test result.

Pytest availability was also checked:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
```

Result:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3: No module named pytest
```

The command returned exit code 1. No dependency was installed during baseline
verification because the repository does not declare pytest as a dependency.

## Smoke-test status

The documented executable demonstration was run without writing bytecode:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m store.main
```

Result: passed with exit code 0. The significant observed totals were:

- Simple VIP order: `$819.99`
- Bundle order: `$5.00`

The bundle contains nested orders but inherits `Order.subtotal`, which reads the
bundle's empty `items` list. Its recorded subtotal is therefore `$0.00`, and the
existing shipping rule produces the `$5.00` total. This behavior is preserved
as baseline evidence and is not corrected in this phase.

## Clean-diff confirmation

Before this document was added, these commands produced no changed-file output:

```bash
git status --short --untracked-files=all
git diff --check
git diff --stat
```

The only intended change in this task branch is this verification document.
No application source, build behavior, test behavior, or architecture was
modified. OpenCode was not used for this phase, because the task requires direct
baseline inspection rather than an OpenCode Plan, Build, or Skill activity.
