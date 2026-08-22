# RUN THIS IN OPENCODE PLAN MODE

## Invocation metadata

- Date: 2026-08-22
- OpenCode version: 1.18.3
- Agent: `plan`
- Model: `opencode/big-pickle`
- Skill: `solid-refactoring` version 1.0
- Branch: `refactor/opencode-plan`
- Clean source revision: `6e0c56534416b9a3c015c4aa3a9fb4922ed24c87`

## Exact prompt

```text
Use the project `solid-refactoring` Skill and produce an implementation plan
only. This is assignment step 4.4 and must remain in OpenCode Plan mode.

Plan the incremental SOLID refactoring of the clean original source copied to
`02-Applied-OOD-Principles/store/`. Inspect that copy, its callers, the unchanged
root `store/`, `docs/solid-analysis.md`, and relevant experiment evidence before
planning. Independently verify source evidence; use the accepted SOLID document
as the confirmed scope, not as a substitute for inspection.

Confirmed scope:

- SRP: `OrderService` mixes checkout orchestration with validation, shipping
  policy, notification-message construction, and receipt presentation.
- OCP: `PaymentProcessor.process` and `DiscountCalculator.calculate` require
  existing conditional code to change for new payment/discount variants.
- LSP: `BundleOrder` is not a valid substitute for `Order`, and
  `SmsOnlyNotifier` rejects inherited email/push operations.
- ISP: the notification API forces an SMS-only implementation to expose
  unsupported operations.
- DIP: `OrderService` directly constructs concrete payment, pricing,
  notification, and storage collaborators.

Constraints:

1. Plan only; do not edit, create, rename, format, or delete any file and do not
   implement any refactoring.
2. All future implementation changes must stay under
   `02-Applied-OOD-Principles/`; do not modify root `store/` or
   `01-Without-OOD-Principles/`.
3. Preserve current observable application behavior unless a separately stated
   domain decision is required. In particular preserve:
   - simple-order total `$819.99`;
   - current bundle total `$5.00` during the behavior-preserving refactoring;
   - payment console strings, receipt tokens, and unknown-method `ValueError`;
   - discount precedence VIP → quantity → coupon and rounding;
   - notification and receipt output.
4. Do not add Cash Payment to the refactored copy yet. That is a later
   experiment.
5. Avoid frameworks, broad plugin systems, unnecessary base classes, and new
   external dependencies. Python standard-library `unittest` is sufficient.
6. A proposed correction must actually address its named principle. Flag any
   confirmed violation that cannot be corrected while preserving behavior and
   present the smallest alternatives instead of silently choosing one.
7. Make the plan incremental. Each logical step must identify:
   - confirmed violation/candidate addressed;
   - exact affected files, classes, and methods;
   - dependencies on earlier steps;
   - precise behavior to preserve;
   - focused tests to add/run before and after;
   - risks and rollback/checkpoint criteria;
   - suggested small commit boundary.
8. Include a complete affected-file map, dependency/order map, consolidated risk
   register, and complete test plan. State any new files explicitly.
9. Separate required work from optional/deferred ideas. Reject unsupported or
   unnecessary abstractions.
10. End with a numbered approval request for the exact plan and state that no
    files were edited.

Required output order:

1. scope, revision, repository state, and files inspected;
2. confirmed-violation-to-plan mapping table;
3. characterization-test step;
4. numbered incremental refactoring steps;
5. affected-file map;
6. dependency and ordering map;
7. risk register;
8. complete test plan and expected baseline results;
9. rejected/deferred suggestions and unresolved domain decisions;
10. approval request with exact proposed scope and `No files have been edited.`
```
