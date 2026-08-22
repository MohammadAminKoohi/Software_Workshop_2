# Step 2 Evidence — Shipping Policy Extraction

## Plan traceability

| Requirement | Accepted change |
|---|---|
| Preserve `< 100` rule exactly | `ShippingCalculator.calculate` returns `5.0` below threshold, else `0.0` |
| Invert shipping dependency | One-method `ShippingCalculatorPort`; required constructor argument |
| Composition-root wiring | `build_demo_service()` supplies `ShippingCalculator()` |
| Keep other concerns in place | Receipt and message formatting remain in `OrderService` |
| Focused regressions | Boundary, injection, simple-total, and bundle-total tests |

## Measurements before evidence documents

- Production files modified: 4
- Production changes: 16 insertions, 2 deletions
- Existing test files modified: 2
- Focused test file added: `test_shipping.py`, 94 lines, 6 tests
- Full discovered suite after correction: 44 tests

## Coordinator verification

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_shipping.py -v` | 0 | 6/6 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 44/44 passed |
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-step2-review-pycache python3 -m compileall -q store tests` | 0 | No output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | `$819.99` and `$5.00`; stdout preserved |
| `git diff --quiet HEAD -- store 01-Without-OOD-Principles` | 0 | Protected sources untouched |

The initial full suite failed because OpenCode omitted the new import from the
composition root. That and a generated test syntax error were corrected and are
retained in `manual-corrections.md`.
