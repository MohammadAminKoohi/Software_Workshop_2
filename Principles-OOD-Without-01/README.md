# Original Design Experiment

`Principles-OOD-Without-01/` preserves the starter implementation for the
Cash Payment experiment that must occur before any SOLID refactoring.

## Baseline

- Source checkpoint: `baseline-initial`
- Source commit: `ace844f31cb5e39c2e0fc48faecabe07d60f30f0`
- Preserved implementation: `store/`
- Cash Payment implementation: not started
- Approval status: pending human review of the OpenCode analysis

The seven files under this directory's `store/` were copied byte-for-byte from
the root `store/` at `baseline-initial`. No architecture, behavior, package
metadata, dependency, or test was added to the preserved copy in this phase.

## Evidence

- [Exact OpenCode prompt](opencode/cash-payment-analysis-prompt.md)
- [Verbatim OpenCode output](opencode/cash-payment-analysis-output.md)
- [Analysis review and approval gate](analysis/cash-payment-analysis-review.md)

OpenCode 1.18.3 performed the analysis with the `opencode/big-pickle` model in
an analysis-only agent. Its initially configured Cloudflare model was
unavailable on the configured free plan, so that failed attempt produced no
analysis or repository changes and the prompt was rerun unchanged with the
available model.

## Integrity verification

From the repository root:

```bash
diff -ru store Principles-OOD-Without-01/store
```

Expected result before Cash Payment implementation: exit code 0 and no output.

## Baseline checks

Run from `Principles-OOD-Without-01/`:

```bash
PYTHONPYCACHEPREFIX=/tmp/swe-lab2-without-pycache python3 -m compileall -q store
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v
PYTHONDONTWRITEBYTECODE=1 python3 -m store.main
```

The preserved baseline compiles and its demo runs. Standard-library discovery
finds zero tests and returns exit code 5; this is recorded as an absent test
suite rather than a passing suite. The demo retains the baseline totals of
`$819.99` for the simple VIP order and `$5.00` for the bundle order.
