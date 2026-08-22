# Build invocation — Step 1 only

Continue the approved Build using `opencode/build-prompt.md` and implement only
**Step 1 — Invert existing checkout dependencies** from the corrected Plan.

Current expected revision: the coordinator's Step 0 commit `ff28085`.

Requirements:

- Add minimal structural contracts for only discount calculation, payment
  processing, email sending, SMS sending, and order saving. The repository
  contract must expose `save_order` only; do not add `load_order`.
- Make `OrderService.__init__` require those five collaborators. Do not retain
  concrete default construction or a `None` fallback.
- Wire the existing concrete implementations in `store/main.py`; one
  `NotificationService` instance may satisfy both channel contracts.
- Keep shipping and receipt logic inside `OrderService` in this step.
- Add focused injected-fake tests. Adapt characterization setup only where the
  approved constructor API change makes it necessary; do not weaken observable
  assertions.
- Run commands with `02-Applied-OOD-Principles/` as cwd. Run focused Step 1
  tests, the complete discovered suite, compilation, and demo smoke.
- Inspect and report the scoped diff and actual measurements.
- Do not edit root `store/`, add Cash Payment, begin Step 2, or commit.
