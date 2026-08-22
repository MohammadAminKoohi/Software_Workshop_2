# Test and Integrity Plan

## Planning-phase verification

All commands must run with `02-Applied-OOD-Principles/` as the working
directory.

```bash
PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-applied-plan-pycache python3 -m compileall -q store
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v
PYTHONDONTWRITEBYTECODE=1 python3 -m store.main
```

At this planning checkpoint, the source copy must remain byte-identical:

```bash
diff -ru ../store store
```

The absent-suite result before Step 0 is baseline evidence, not a passing test
suite. Record its actual exit status and discovery count. Once Step 0 creates a
test directory, use this exact command and record actual totals rather than
estimates:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Focused checks by future Build step

| Step | Focused regression check |
|---:|---|
| 0 | Exact payment, discount, validation, persistence, notification, receipt, simple demo, bundle demo, and known LSP behavior |
| 1 | Injected fakes receive the expected calls; `OrderService` does not construct concrete dependencies |
| 2 | Shipping below/at/above `$100`; simple and bundle totals unchanged |
| 3 | Exact receipt text and observable call/output order |
| 4 | All three existing payment methods and error text; synthetic registered handler without processor edits |
| 5 | Each discount rule, overlap priority, no match, rounding, and synthetic ordered rule |
| 6 | Independent channel substitutes; standalone SMS sender; unchanged demo notifications |
| 7 | No `Order` inheritance; preserved bundle fields, zero values, `$5.00` total, persistence, and receipt |
| 8 | Full compile, discovery, demo, scoped diff, clean generated-file check, and actual measurements |

No test should assert a new business rule that is not present in the baseline.
In particular, bundle child aggregation and Cash Payment are excluded.
