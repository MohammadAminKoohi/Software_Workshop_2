# Cash Payment Analysis Review

## Status

- OpenCode analysis: complete
- Cash Payment implementation: not started
- Human approval: pending
- Baseline architecture preserved: yes

## Confirmed affected code

The smallest architecture-preserving production change proposed by OpenCode is:

| Requirement | Exact target | Change |
|---|---|---|
| Accept Cash Payment | `Principles-OOD-Without-01/store/payment.py`, `PaymentProcessor.process` | Add one `elif method == "cash"` branch before the existing unknown-method error. |

Potential evidence-only additions remain optional until approval:

| Purpose | Exact target | Decision |
|---|---|---|
| Automated verification | A new standard-library `unittest` file inside `Principles-OOD-Without-01/` | Pending |
| Demonstrate cash in the executable sample | `Principles-OOD-Without-01/store/main.py`, `build_demo_orders` and `main` | Pending |

No change is proposed for `Customer`, `Order`, `OrderService`,
`DiscountCalculator`, `MySqlDatabase`, or notification classes. No payment
interface, strategy, factory, or dependency injection is permitted in this
experiment.

## Manual review of OpenCode output

The OpenCode analysis correctly:

- traced the current string-based payment flow;
- identified `PaymentProcessor.process` as the only required production change;
- preserved the conditional dispatch and direct construction architecture;
- avoided inventing a cash-specific customer field;
- separated required production work from optional demo/test work;
- stopped before implementation and requested approval.

The following clarifications correct or tighten the output without replacing its
analysis:

1. References such as `store/payment.py` in the OpenCode response mean
   `Principles-OOD-Without-01/store/payment.py`, not the root baseline copy.
2. The future metrics must record **one existing method changed**
   (`PaymentProcessor.process`), even though zero methods are added.
3. The repository has no pytest dependency. If automated tests are approved,
   prefer Python's built-in `unittest` unless the team separately approves and
   documents a new dependency.
4. The existing `BundleOrder` smoke behavior remains the recorded `$5.00`
   baseline. Cash Payment work must not opportunistically correct it.

## Approval decision required

Before any implementation, the team must explicitly approve or revise all four
choices:

- selector: `payment_method == "cash"`;
- receipt: `paid_by_cash:<amount with two decimals>`;
- console text: `[payment] Receiving cash <amount with two decimals>`;
- evidence scope: whether to add a built-in `unittest` test file, a demo cash
  order, or both.

Recommended minimal approval: accept the selector, receipt, and console text;
add focused built-in `unittest` coverage for cash and existing payment paths;
do not change the demo unless the assignment specifically requires visible demo
output.

Approval must be recorded in issue #29 or its pull request before task #30 begins.
Merging the preservation/analysis PR confirms that the evidence is accepted; it
does not itself authorize implementation unless the four choices above are
explicitly approved.
