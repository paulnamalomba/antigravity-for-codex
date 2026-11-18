---
name: antigravity-review
description: Request an independent Antigravity review of a specified diff and reconcile the findings against the code.
---

# Antigravity review

Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Determine the requested scope; if no scope is given, inspect the working tree and last commit, clearly stating what was reviewed. Do not send secrets or unrelated files to the external CLI.

Verify that `agy --help` advertises `--settings` before relying on `--read-only`; if absent, use another authorized tool. Provide both the diff and a review instruction to `"$PLUGIN_ROOT/bin/agy-delegate" --read-only --tier pro -` on stdin. Ask for correctness, security, and performance issues with file and line references; include design tradeoffs if adversarial review was requested. Check every finding against the actual source and report confirmed findings ordered by severity, with residual uncertainty and verification performed. Do not treat the executor's review as authoritative.
