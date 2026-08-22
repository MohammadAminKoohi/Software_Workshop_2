# Build-Mode Manual Corrections

| Step | OpenCode output or behavior | Coordinator correction | Reason |
|---:|---|---|---|
| 0 | The first non-interactive run failed because OpenCode could not open its user log; the retry with attached files parsed the final message as another filename; a later run stalled at permissions. | Restarted the same scoped Step 0 prompt in a permission-capable TTY with project-scoped automatic approval. Successful session: `ses_fd4dceb8bffeRJxcTrv1Y9YGMG`; failed session: `ses_fd4e10930ffeGehIn5uk3UDxPu`. | Preserve actual OpenCode use while making the CLI capable of editing the isolated worktree; no assistant-authored substitute was used. |
| 0 | Initial exploratory demo/probe commands imported root `store/` because their working directory was the repository root. | Required and independently reran compilation, tests, and smoke from `02-Applied-OOD-Principles/`; accepted evidence only from the applied workspace. | Identical source made the initial values informative, but the attribution was incorrect and future steps may diverge. |
| 0 | First generated expectations used `999.99` for the demo laptop subtotal, `90.00` for books, and one extra receipt-padding space. | OpenCode corrected them to observed values `1024.99`, `170.00`, child total `1194.99`, and the exact output spacing; coordinator reran all 26 tests. | Characterization must describe existing behavior rather than force incorrect expectations. |
| 1 | OpenCode used Bash's `PIPESTATUS` under zsh, producing an empty reported full-suite status, and initially scoped `git diff` with paths relative to the wrong directory. | It reran the suite without a pipeline and obtained exit 0, then reran the diff with `git -C` and repository-relative paths. The coordinator independently repeated both checks. | Exit codes and measurements must be observed, not inferred from a successful-looking tail or an accidentally empty diff. |

No generated Step 1 production correction was necessary after review. Later
corrections will be appended after their focused diff and test review.
