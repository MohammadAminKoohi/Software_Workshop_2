# Risk Register

| Risk | Likelihood / impact | Mitigation and regression check |
|---|---|---|
| Tests accidentally import root `store/` instead of the applied copy | Medium / High | Run every command with the applied directory as cwd; print/import-path assertion in characterization setup if needed. |
| Output spacing, order, or monetary formatting drifts | Medium / High | Capture exact stdout for the demo, payments, notifications, and receipts before refactoring. |
| Required constructor injection breaks callers | Medium / Medium | Search all `OrderService(` call sites; update only composition root and tests in the same small commit. |
| Payment registry changes errors or method-specific data | Medium / High | Assert exact stdout, return strings, lookup behavior, and unknown-method message. |
| Discount rule ordering or rounding changes totals | Medium / High | Test overlapping rules and decimal edge cases; keep first-match semantics and final rounding. |
| Notification correction changes production behavior | Low / Medium | Keep demo wired to implementations supporting both channels; explicitly approve and test only the unsupported `SmsOnlyNotifier` API change. |
| Bundle composition breaks consumers relying on `isinstance(Order)` | Medium / High | Search all call sites, update annotations, retain required fields/properties, and run exact bundle smoke checks. |
| Bundle repricing is introduced accidentally | Low / High | Assert zero subtotal/count and `$5.00` total; defer child aggregation as a separate domain decision. |
| New contracts become broad or unused | Medium / Medium | Define only methods called by each client; reject unused `load_order`, push, container, and plugin abstractions. |
| Root or original experiment is edited | Low / High | Inspect `git status` after every step and scope commits to `02-Applied-OOD-Principles/`. |
| Characterization tests are rewritten to hide regressions | Low / High | Permit one reviewed update only for the intentional `SmsOnlyNotifier` contract correction. |
| Cash Payment leaks into the refactoring task | Low / Medium | Use only a synthetic test handler; reserve Cash for the later experiment. |

If a step fails, correct it within that focused step or revert that exact commit.
Do not broadly restore the working tree because it may discard unrelated work.
