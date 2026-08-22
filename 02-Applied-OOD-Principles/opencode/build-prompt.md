# RUN THIS IN OPENCODE BUILD MODE

OpenCode version: 1.18.3
Required agent: `build`
Model: `opencode/big-pickle`
Branch: `refactor/apply-solid`
Starting revision: `db4e8450763aeadc20ab987cc423c48c8470f43c`

Use the repository Skill `solid-refactoring` and execute only the approved
corrected Plan at:

`02-Applied-OOD-Principles/planning/corrected-plan.md`

Approval is recorded in:

`02-Applied-OOD-Principles/planning/approval.md`

The scope is strictly `02-Applied-OOD-Principles/**`. Never edit root `store/`,
`01-Without-OOD-Principles/`, unrelated documentation, GitHub configuration, or
the Skill. Do not add Cash Payment. Do not commit, tag, push, or open a PR;
those actions are performed by the human coordinator after diff review and
tests.

Work incrementally. For each invocation, implement only the Plan step named in
the invocation prompt, inspect your changes, run only that step's focused
checks, and return:

1. approved Plan step and exact scope;
2. files/classes/methods changed;
3. behavior preserved or intentionally changed;
4. commands, exit codes, and meaningful results;
5. diff measurements;
6. deviations, risks, rejected work, and required manual corrections;
7. confirmation that no later step was started.

Preserve the exact documented simple-order and bundle behavior. Stop if a
required change exceeds the approved Plan.
