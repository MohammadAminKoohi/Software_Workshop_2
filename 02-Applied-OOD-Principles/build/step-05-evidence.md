# Step 5 Evidence — Composable Discount Rules

## Attribution and traceability

This step was implemented and reviewed by the coordinator after the user's
explicit instruction to stop using OpenCode. No OpenCode execution is claimed.

| Plan requirement | Accepted implementation |
|---|---|
| Preserve three rules | `VipDiscountRule`, `QuantityDiscountRule`, and `WelcomeCouponDiscountRule` |
| Preserve precedence | Composition root supplies rules in VIP → quantity → coupon order; calculator stops at first match |
| Preserve rounding | Selected result is rounded to two decimals exactly once |
| No hidden defaults | `DiscountCalculator(rules)` requires and copies the supplied sequence |
| Demonstrate extension | Synthetic test-only rule returns `12.345`, observed as `12.35`, without algorithm edits |

## Measurements before this evidence document

- Existing production files modified: 2
- Production changes: 47 insertions, 14 deletions
- Existing test files modified: 2
- Focused test file added: `test_discount_rules.py`, 73 lines, 8 tests
- Full suite: 63 tests

## Verification

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_discount_rules.py -v` | 0 | 8/8 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 63/63 passed |
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-step5-review-pycache python3 -m compileall -q store tests` | 0 | No output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | Exact `$819.99` and `$5.00` baseline output preserved |
| `git diff --quiet HEAD -- store 01-Without-OOD-Principles` | 0 | Protected sources untouched |

No Cash Payment or unrelated pricing abstraction was added.
