---
name: antigravity-handoff
description: Hand a whole test-covered implementation task to Antigravity and independently verify the outcome. Use when the user requests an Antigravity handoff.
---

# Whole-task handoff

The handoff wrapper invokes agy with `--yolo`, which broadly auto-approves tools, and may register the project with agy. It is not contained by `--sandbox`. Use it only when the user has authorized this level of execution and the task; do not infer broad approval from a request for read-only research. Isolate the run in a dedicated worktree or equivalent environment appropriate to that authority, with a clean committed Git baseline and no unrelated sensitive data or credentials accessible to the executor. A branch alone does not isolate tools or credentials.

Before running, establish that the relevant tests exist and are committed in the clean baseline. Run the verification command and record its results, including expected failures from tests defining the new behavior; distinguish those from unrelated baseline failures. Use a suitable verification command; supply `--verify` if auto-detection is unsuitable and name the protected tests with `--tests`. Do not use `--allow-dirty` or `--no-verify` for this workflow. Avoid this workflow for small or judgment-heavy tasks.

Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Use `"$PLUGIN_ROOT/bin/agy-handoff" --dir <isolated-worktree> --verify '<test command>' --tests <comma-separated-paths> '<observable requirement>'`. The wrapper may do one fix-up and rerun verification; see `--help` for flags and exit codes. Background execution is available via `--background`, with job status/result collected through `agy-job`.

Inspect the resulting changes and run appropriate independent checks before claiming completion; tests alone do not prove correctness or safety. Report what ran, the result, and remaining issues. Never commit or push unless authorized.
