# OpenCode Plan Completion Prompt

The initial Plan-mode session inspected the repository and exited without a
final response. This exact follow-up was sent to the same session.

```text
Your repository inspection is complete, but the previous turn ended without
the required Plan output. Do not call any more tools and do not edit any file.
Using only the evidence already collected, now return the complete plan in the
10-section order required by the original prompt. Include every confirmed
violation, incremental steps, affected files/classes/methods, dependencies,
risks, focused tests, rejected/deferred work, unresolved domain decisions, and
the exact approval request. End with `No files have been edited.`
```
