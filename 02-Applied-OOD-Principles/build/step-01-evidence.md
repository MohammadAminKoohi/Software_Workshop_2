# Step 1 Evidence — Dependency Inversion

## Plan traceability and diff review

| Plan requirement | Accepted implementation |
|---|---|
| Depend on five required behaviors | Five one-method structural protocols in `store/contracts.py` |
| No unused repository operation | `OrderRepository` contains `save_order` only |
| No concrete construction in `OrderService` | Five required constructor arguments with no defaults/fallbacks |
| Exact notification channels | Separate `EmailSender` and `SmsSender`; calls routed independently |
| Concrete choices at composition root | `build_demo_service()` in `store/main.py` |
| Shipping and receipt unchanged | Rule and `_print_receipt` remain in `OrderService` |

Coordinator review found no unrelated production change and no need to alter the
generated implementation. The characterization helper was updated only because
the approved constructor contract changed; its assertions remain unchanged.

## Measurements before evidence documents

- Existing production files modified: 2
- Existing test files modified: 1
- Production file added: 1 (`contracts.py`, 28 lines)
- Focused test file added: 1 (`test_dependency_injection.py`, 218 lines)
- Tracked modifications: 53 insertions, 16 deletions
- Cash Payment changes: 0

## Coordinator verification

All commands ran from `02-Applied-OOD-Principles/` with Python 3.13.2.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_dependency_injection.py -v` | 0 | 12/12 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 38/38 passed |
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-step1-review-pycache python3 -m compileall -q store tests` | 0 | No output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | Baseline `$819.99` and `$5.00` output preserved |
| `git diff --quiet HEAD -- store 01-Without-OOD-Principles` | 0 | Protected sources untouched |
