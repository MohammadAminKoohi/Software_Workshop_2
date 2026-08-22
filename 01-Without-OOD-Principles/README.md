# Original Design Experiment

`01-Without-OOD-Principles/` preserves the starter implementation for the
Cash Payment experiment that must occur before any SOLID refactoring.

## Baseline

- Source checkpoint: `baseline-initial`
- Source commit: `ace844f31cb5e39c2e0fc48faecabe07d60f30f0`
- Preserved implementation: `store/`
- Cash Payment implementation: complete, pending pull-request review
- Approval status: approved on 2026-08-22 and recorded in issue #29

The seven files under this directory's `store/` were copied byte-for-byte from
the root `store/` at `baseline-initial`. OpenCode then added Cash Payment to the
preserved copy without refactoring its conditional-dispatch architecture. The
root starter `store/` remains unchanged.

## Evidence

- [Exact OpenCode prompt](opencode/cash-payment-analysis-prompt.md)
- [Verbatim OpenCode output](opencode/cash-payment-analysis-output.md)
- [Analysis review and approval gate](analysis/cash-payment-analysis-review.md)
- [Exact implementation prompt](opencode/cash-payment-implementation-prompt.md)
- [Verbatim implementation output](opencode/cash-payment-implementation-output.md)
- [Change report and measurements](analysis/cash-payment-change-report.md)

OpenCode 1.18.3 performed the analysis with the `opencode/big-pickle` model in
an analysis-only agent. Its initially configured Cloudflare model was
unavailable on the configured free plan, so that failed attempt produced no
analysis or repository changes and the prompt was rerun unchanged with the
available model.

## Integrity verification

From the repository root:

```bash
diff -ru store 01-Without-OOD-Principles/store
```

Before Cash Payment implementation, the command returned exit code 0 with no
output. After implementation, the only production difference is the approved
four-line Cash Payment branch in `store/payment.py`.

## Baseline checks

Run from `01-Without-OOD-Principles/`:

```bash
PYTHONPYCACHEPREFIX=/tmp/swe-lab2-without-pycache python3 -m compileall -q store
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v
PYTHONDONTWRITEBYTECODE=1 python3 -m store.main
```

At the preserved baseline, standard-library discovery found zero tests and
returned exit code 5. After the approved experiment, compilation passes, all
six focused tests pass, and the unchanged demo retains the baseline totals of
`$819.99` for the simple VIP order and `$5.00` for the bundle order.
