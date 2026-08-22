# Build invocation — Step 2 only

Continue the approved Build and implement only **Step 2 — Extract shipping
policy** from `planning/corrected-plan.md`.

Current expected revision: `9ea62b0`.

Requirements:

- Add `ShippingCalculator` to `store/pricing.py` with exactly the current rule:
  shipping is `5.0` when subtotal is less than `100`, otherwise `0.0`.
- Add one minimal shipping behavior contract to `store/contracts.py` and make it
  a required `OrderService` constructor dependency with no default/fallback.
- Wire the concrete calculator in `store/main.py` and adapt only the necessary
  real-wiring test helper.
- Replace only the inline shipping rule. Do not extract notification-message
  formatting or receipt presentation.
- Add focused tests at `99.99`, `100.00`, and `100.01`, plus injection and
  unchanged end-to-end totals.
- Run focused tests, all discovered tests, compilation, and demo from
  `02-Applied-OOD-Principles/`. Inspect the complete scoped diff and report
  actual counts/measurements.
- Do not begin Step 3, add Cash Payment, edit protected sources, or commit.
