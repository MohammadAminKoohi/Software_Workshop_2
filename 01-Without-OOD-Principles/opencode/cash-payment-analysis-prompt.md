# OpenCode Cash Payment Analysis Prompt

The following prompt is the exact instruction supplied to OpenCode for the
original-design Cash Payment experiment.

The prompt was run before the assignment directory name was corrected. Its
historical `Principles-OOD-Without-01/` reference means the directory now named
`01-Without-OOD-Principles/`; the prompt below remains verbatim.

```text
You are analyzing the SWE Lab 2 starter project for the first Cash Payment
experiment. Inspect the repository, with the implementation target specifically
being Principles-OOD-Without-01/store/.

Your task is analysis only. Do not edit, create, delete, move, or format any
repository file. Do not implement Cash Payment. Do not create a branch, commit,
test, abstraction, interface, strategy, factory, dependency-injection mechanism,
or SOLID refactoring.

The experiment intentionally requires adding Cash Payment BEFORE correcting the
existing design. Preserve the current architecture even where it is poor:
- keep Order.payment_method as the string selector;
- keep PaymentProcessor.process and its conditional dispatch style;
- keep OrderService constructing and calling PaymentProcessor as it does now;
- do not reorganize responsibilities or generalize the payment design.

First inspect the actual code. Then return a concise analysis with exactly these
sections:

1. Current payment flow
2. Cash Payment behavior assumptions
3. Affected files and classes (list these before proposing implementation)
4. Smallest architecture-preserving changes
5. Tests/checks required
6. Measurement expectations (files/classes/methods/conditions/dependencies)
7. Risks and ambiguities
8. Approval gate

For every proposed change, cite the exact existing file, class, and method or
field. Distinguish required changes from optional demo/test changes. Do not
invent requirements: if the precise cash receipt wording or demo behavior is not
specified, state a minimal assumption and flag it for approval.

End your response with this exact line:

AWAITING APPROVAL — DO NOT IMPLEMENT
```
