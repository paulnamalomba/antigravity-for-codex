---
name: antigravity-jobs
description: Start, inspect, collect, or cancel background Antigravity delegation jobs when the user requests a job or an asynchronous task.
---

# Antigravity jobs

Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Run `"$PLUGIN_ROOT/bin/agy-job"`; do not assume the plugin is on `PATH`. See `--help` for syntax and permission options. Pass only authorized task content and permissions, following the antigravity skill.

- Start: `"$PLUGIN_ROOT/bin/agy-job" start --read-only --dir <repo> --digest "<task>"`. Save and report the job ID. Use the permission mode appropriate to the authorized task; do not silently escalate.
- List jobs for the current directory: `"$PLUGIN_ROOT/bin/agy-job" list`.
- Inspect: `"$PLUGIN_ROOT/bin/agy-job" status <id>`.
- Collect: `"$PLUGIN_ROOT/bin/agy-job" result <id>`. If still running, report that. Treat cancelled or partial results as unverified. Inspect stderr for failure and fallback details; independently verify completed output.
- Cancel when requested: `"$PLUGIN_ROOT/bin/agy-job" cancel <id>`. Report whether it was cancelled or had already finished.
