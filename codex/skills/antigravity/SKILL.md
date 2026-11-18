---
name: antigravity
description: Delegate a bounded development or analysis task to the Antigravity CLI and independently verify its result. Use when the user asks for Antigravity or agy delegation.
---

# Antigravity delegation

Codex owns the task, authorization, and verification. Delegate only work within the user's requested scope. Tell the user what will be sent to the external CLI; do not send secrets or unrelated data. Do not treat the executor's output as proof of success.

## Locate the wrapper

Use the absolute path of this installed `SKILL.md` provided in the skill catalog. The plugin root is three directories above its directory. For example, replacing the placeholder with that actual path:

```sh
PLUGIN_ROOT="$(cd "$(dirname '/absolute/path/to/antigravity/SKILL.md')/../../.." && pwd -P)"
"$PLUGIN_ROOT/bin/agy-delegate" --help
```

Use this root for every wrapper in this plugin. Do not assume the current directory is the plugin or that its `bin` directory is on `PATH`.

## Delegate

For repository analysis, first verify that `agy --help` advertises `--settings`; the wrapper cannot enforce its read-only settings on older versions without that option. Then use `"$PLUGIN_ROOT/bin/agy-delegate" --tier flash --read-only --dir <repo> --digest "<bounded task>"`. If `--settings` is unavailable, stop or use another authorized tool rather than claiming the call is read-only. Use `--allow-url` only when URL access is needed. Select `--tier pro` or `--model <exact-name>` when appropriate; `--effort` and `--timeout` are wrapper options. See `--help` for other options and exit codes. A read-only task should not gain write or shell privileges on failure.

For authorized file edits on agy 1.5.7 or later, `--mode accept-edits` grants in-workspace edit approval; full agentic execution can use appropriately scoped explicit permissions; `--yolo` broadly auto-approves tools. Use that only when the user has authorized the actions and their scope, in an isolated environment appropriate to the work. `--sandbox` is not a reliable containment boundary under `--yolo`. Never silently escalate permissions after a denial. Treat exit 15 as a denial and report it; exit 12 indicates timeout and may include partial output. Avoid delegating tiny tasks when the overhead exceeds the benefit.

Inspect and test the result against the user's requirements. For research, use the antigravity-research skill; for jobs or whole-task handoff use their respective skills.
