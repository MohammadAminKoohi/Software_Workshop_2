# Critical Review of the OpenCode Plan

## Review basis

The original Plan was compared with the confirmed SOLID evidence in
`docs/solid-analysis.md`, the seven original `store/` files, and the required
observable demo behavior. The reviewer is the AI coding coordinator; human
approval is not claimed.

## Manual corrections

| # | Original Plan item | Correction | Reason |
|---:|---|---|---|
| 1 | The violation-to-step table omitted DIP, although Step 1 discussed it. | Add the confirmed `OrderService` DIP violation and map it to corrected Step 1. | Every planned change must trace to a confirmed violation. The direct concrete imports and construction in `OrderService.__init__` are confirmed evidence. |
| 2 | The run narrative said the smoke check was executed from the applied copy, but OpenCode's tool call ran from the repository root. | Treat that run only as original-baseline evidence; require all future commands to run with `02-Applied-OOD-Principles/` as the working directory. | The sources were byte-identical, so the values remain useful, but the command attribution must be exact. |
| 3 | Test totals were estimated as approximately 14 and 22–26. | Remove predicted counts and record actual discovered, passed, failed, and skipped counts after each run. | Evidence must report observed results, not invented future measurements. |
| 4 | Step 0 proposed `tests/__init__.py`. | Add it only if an import problem actually requires it; discovery will use `-s tests`. | An empty package marker is unnecessary for the planned discovery command. |
| 5 | `contracts.py` included both `save_order` and unused `load_order`. | Define only client-required operations; the repository port initially exposes `save_order`. | Adding an unused operation creates a broader interface and conflicts with ISP. |
| 6 | The SRP step extracted a one-line `build_checkout_message` function. | Keep the message construction in the checkout orchestrator; extract only shipping policy and receipt presentation. | No independent message-format change is demonstrated. The extra function adds indirection without solving a confirmed problem. |
| 7 | Payment and discount classes could construct default registries/rules internally through `None` defaults and factories. | Require registries/rules through constructors and assemble defaults in `main.py`. | Hidden defaults retain concrete policy selection inside the service. The composition root is the correct place to choose implementations. |
| 8 | Notification splitting was mixed into the broad dependency step. | Step 1 injects the exact email and SMS collaborators; Step 6 removes false inheritance and leaves `SmsOnlyNotifier` with only SMS behavior. | This keeps DIP work incremental and makes the later LSP/ISP correction explicit. |
| 9 | Bundle alternative A deferred a confirmed LSP violation; alternative B added an unspecified special checkout path. | Use composition while preserving the exact current fields, zero subtotal/item count, `$5.00` checkout, and receipt behavior. Keep the existing explicit bundle validation exception, now as a domain-type branch rather than a subtype workaround. | The assignment requires a plan for confirmed violations. Composition removes the false subtype without silently inventing child aggregation or repricing semantics. |
| 10 | Rollback guidance included broad file restoration. | Use focused commits and revert only the failing step's commit if necessary. | This preserves unrelated user work and creates an auditable incremental history. |
| 11 | Cash Payment was mentioned as a future extension test. | Keep Cash Payment completely outside implementation scope; use a synthetic test-only handler to prove extensibility. | Step 4.4 plans only confirmed SOLID corrections. The repeated Cash experiment is a later assignment step. |

## Accepted parts of the OpenCode Plan

- It correctly started from the clean original architecture, not the Cash
  experiment.
- It identified the affected production classes and preserved the simple-order
  `$819.99` and bundle `$5.00` outputs.
- It proposed characterization tests before refactoring and incremental commit
  boundaries.
- It rejected DI containers, plugin frameworks, pytest, and unsupported claims
  about `Customer` or `MySqlDatabase`.
- It correctly retained discount precedence and exact payment errors as
  regression-sensitive behavior.

## Rejected or deferred work

- Cash Payment implementation: belongs to the later comparison experiment.
- Validation-policy extraction: the two current checks do not justify another
  abstraction yet.
- Bundle child aggregation/repricing: requires a product decision and would
  change baseline behavior.
- Renaming `MySqlDatabase`: a naming concern, not a confirmed SOLID correction.
- General-purpose containers, plugins, abstract base hierarchies, and new
  external test dependencies: unnecessary for this project.
