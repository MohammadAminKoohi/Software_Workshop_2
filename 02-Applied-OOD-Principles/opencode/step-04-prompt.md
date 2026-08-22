# Build invocation — Step 4 only

Continue the approved Build and implement only **Step 4 — Make payment methods
extensible** from the corrected Plan.

Current expected revision: `8b3f2ba`.

Requirements:

- Replace the conditional chain in `store/payment.py` with one small handler for
  each existing method: credit card, PayPal, and Bitcoin.
- `PaymentProcessor` must require an injected method-to-handler registry. It
  must have no internal default registry, `None` fallback, factory, or Cash
  handler.
- Assemble the three existing handlers in `store/main.py`.
- Preserve every existing payment stdout line, returned receipt token, amount
  formatting, customer field, and exact unknown-method `ValueError` text.
- Add focused tests for all existing methods, unknown methods, registry
  injection, and a synthetic test-only handler proving extension without an
  edit to `PaymentProcessor.process` or existing handlers.
- Adapt prior test wiring only where the approved constructor change requires
  it; do not weaken characterization assertions.
- Run focused tests, full discovery, compilation, and demo from the applied
  workspace; inspect/report complete scoped diff and metrics.
- Do not implement Cash Payment, discount rules, notifier/bundle changes, or
  begin Step 5. Do not edit protected sources or commit.
