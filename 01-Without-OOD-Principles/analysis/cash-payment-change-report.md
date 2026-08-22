# Original-Design Cash Payment Change Report

## Scope and attribution

- Baseline revision: `baseline-initial` at
  `ace844f31cb5e39c2e0fc48faecabe07d60f30f0`
- Pre-implementation branch revision: `469cbbb`
- Implementer: OpenCode 1.18.3, Build agent, `opencode/big-pickle`
- Human approval: granted on 2026-08-22 and recorded in issue #29
- Human source corrections after generation: none
- Architecture rule: preserve the original conditional payment design

OpenCode noticed that one initial test printed uncaptured production output and
corrected that test during its own Build run. Human review confirmed that the
final source diff stays within the approved scope.

## Change table

| File/Class | Change type | Explanation |
|---|---|---|
| `store/payment.py` / `PaymentProcessor.process` | Existing method modified; condition added | Added the approved `elif method == "cash"` branch so the original string-based dispatcher recognizes Cash Payment, prints the approved message, and returns the approved receipt. |
| `tests/test_payment.py` / `CashPaymentTest` | New test class | Verifies Cash Payment's formatted receipt and exact console output. |
| `tests/test_payment.py` / `ExistingPaymentRegressionTest` | New test class | Protects the existing credit-card, PayPal, and Bitcoin receipt/output behavior. |
| `tests/test_payment.py` / `UnknownPaymentMethodTest` | New test class | Confirms that unsupported payment selectors still raise `ValueError`. |

No existing method or dependency was removed. No Customer field, production
class, abstraction, factory, strategy, or dependency-injection mechanism was
introduced.

## Git-based implementation measurements

The implementation measurement compares the preserved tree immediately before
Build (`469cbbb`) with the final implementation files. Evidence-only Markdown
changes are excluded so the numbers remain reusable for the later SOLID-design
comparison.

| Metric | Result |
|---|---:|
| Files changed | 2 |
| Production files modified | 1 |
| Existing classes modified | 1 |
| New production classes | 0 |
| New test classes | 3 |
| Existing methods changed | 1 |
| Conditions/switch cases added | 1 |
| Production dependencies changed | 0 |
| Lines added | 90 |
| Lines removed | 0 |

Line accounting is `4` additions in `store/payment.py` plus `86` additions in
the new test file. For production code alone, the result is `4` additions and
`0` removals.

## Independent verification

Environment:

- Python 3.13.2
- OpenCode 1.18.3

Run from `01-Without-OOD-Principles/`:

| Command | Exact result |
|---|---|
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-without-cash-pycache python3 -m compileall -q store tests` | Exit 0; no output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | Exit 0; 6 tests run; all passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | Exit 0; unchanged smoke output, including `$819.99` simple order and `$5.00` bundle |
| `git diff --check` | Exit 0; no whitespace errors |

The root starter `store/` and the preserved demo remain unchanged. The known
bundle `$5.00` behavior is deliberately retained because this experiment must
not refactor or repair the original design.
