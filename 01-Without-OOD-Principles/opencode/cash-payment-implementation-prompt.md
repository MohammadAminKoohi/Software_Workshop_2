# OpenCode Cash Payment Implementation Prompt

## Invocation metadata

- Date: 2026-08-22
- Mode: Build
- Model: `opencode/big-pickle`
- Working directory: repository root
- Human approval: recorded in issue #29 and
  `analysis/cash-payment-analysis-review.md`

## Exact prompt

```text
Implement the approved Cash Payment experiment only inside
`01-Without-OOD-Principles/`.

The analysis and human approval are complete. Inspect the existing preserved
code before editing, then make only these approved changes:

1. In `01-Without-OOD-Principles/store/payment.py`, preserve the existing
   architecture and modify `PaymentProcessor.process` by adding an
   `elif method == "cash"` branch before the final `else`.
2. The branch must print exactly:
   `[payment] Receiving cash {amount:.2f}`
3. The branch must return exactly:
   `paid_by_cash:{amount:.2f}`
4. Add focused tests using only Python's built-in `unittest` under
   `01-Without-OOD-Principles/tests/`. Cover the cash receipt and console
   output, regression behavior for credit_card, paypal, and bitcoin, and the
   unknown-method ValueError.

Constraints:

- Preserve the current string selector, conditional dispatch, and direct
  dependencies even though the architecture has SOLID problems.
- Do not introduce a strategy, factory, interface, dependency injection, new
  production class, or new dependency.
- Do not change Customer, Order, OrderService, pricing, storage, notification,
  the root `store/`, or the demo in `store/main.py`.
- Do not refactor or opportunistically fix any existing behavior.
- Do not commit or tag.

After editing, run these checks from `01-Without-OOD-Principles/`:

- `python3 -m compileall -q store tests`
- `python3 -m unittest discover -s tests -v`
- `python3 -m store.main`

Summarize the exact files changed, behavior added, test results, and any
limitations. Then stop for human diff review.
```
