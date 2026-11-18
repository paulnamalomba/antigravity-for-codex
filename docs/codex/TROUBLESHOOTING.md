# Troubleshooting

> **Upstream Attribution Notice:** This troubleshooting guide was compiled from empirical testing and issue resolutions originally reported in [`antigravity-for-claude-code`](https://github.com/yuting0624/antigravity-for-claude-code) by [linyuting](https://github.com/yuting0624) and community contributors. Issue references (e.g., `upstream #6`, `upstream #37`) link to historical upstream investigations. New issues regarding the Codex port should be filed at [`paulnamalomba/antigravity-for-codex`](https://github.com/paulnamalomba/antigravity-for-codex/issues).

## Codex setup and diagnostics

From the repository root, register the local marketplace and install the plugin:

```sh
codex plugin marketplace add --json .
codex plugin add --json antigravity@antigravity-for-codex
```

The install JSON returns `installedPath`, the absolute cached plugin root. Start a new Codex session, review and trust the Antigravity hooks in `/hooks`, and select `antigravity:antigravity-setup`. To run diagnostics directly, set `PLUGIN_ROOT` to that returned path:

```sh
PLUGIN_ROOT='/absolute/path/from/installedPath'
"$PLUGIN_ROOT/bin/agy-doctor" --codex
```

The doctor checks Codex registration and enablement, packaged files, and agy health. A marketplace or plugin-list failure can also mean Codex did not return usable JSON. The doctor queries agy but does not authenticate for you. Check `agy models` and the configured authentication route if agy is missing, unauthenticated, or has no usable model. Python 3 is required for the Codex hooks. See the [port guide](CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md) for observed test limits.

- **Skill or wrapper missing:** install the plugin, start a new session, and use the `antigravity:` skill namespace. Use the absolute cached `installedPath` for direct wrapper calls. Codex does not put the plugin's `bin/` on the shell `PATH`. After editing the checkout, rerun `codex plugin add --json antigravity@antigravity-for-codex` to refresh the cache and review changed hook approvals.
- **Hook or delegate role unavailable:** review `/hooks` and trust the current hook code. The optional `antigravity-delegate` role is supplied in this trusted project's `.codex/agents/`; to use it elsewhere, place the role file in that project's `.codex/agents/` or the Codex home's `agents/`. Its hook supplies the exact cached wrapper path and guards matched calls for this named role: a fresh, literal, POSIX `agy-delegate --read-only` invocation, with supported options and workspace paths. It requires an agy version advertising `--settings`. The guard does not cover every main-session tool call. Use main-session skills for edits, jobs, and handoffs.
- **Permission denied or missing output:** inspect the wrapper's exit code and `AGY_SIGNAL`, agy's permission rules, and Codex sandbox and approval settings. For an authorized URL read, `--read-only --allow-url` is a scoped option, not a web-search grant. Do not automatically broaden a research task to `--yolo`, which approves all agy tools. On the tested account, agy 1.5.11 URL probes returned `URL_READ_FAILED` and timeout; successful URL access remains unverified.
- **A request hangs:** inspect agy MCP configuration and logs as described below. Exit 12 identifies a wrapper timeout. Narrow the request or adjust the timeout after investigating the cause.

### Jobs and authorized edits

Use `antigravity:antigravity-jobs` for background work. For direct calls, use `PLUGIN_ROOT` as set above and run `list` from the directory where the job was started. Set `JOB_ID` to the ID returned by `start`:

```sh
JOB_ID='replace-with-job-id'
"$PLUGIN_ROOT/bin/agy-job" list
"$PLUGIN_ROOT/bin/agy-job" status "$JOB_ID"
"$PLUGIN_ROOT/bin/agy-job" result "$JOB_ID"
```

Use the job ID returned at start. `result` exits 2 while the job is running and exits 0 once output is available, including for failed or cancelled jobs. Check `status` and the result's stderr for the actual outcome. Treat partial and cancelled results as unverified.

For an authorized edit, choose the narrowest appropriate target directory. On agy 1.5.7 or later, `--mode accept-edits --dir "$AGY_TARGET"` grants in-workspace edit approval without granting terminal commands. For example, from the main session or an appropriate skill:

```sh
AGY_TARGET='/absolute/path/to/authorized/target'
AGY_TASK='Describe the authorized, bounded edit task here'
"$PLUGIN_ROOT/bin/agy-delegate" --mode accept-edits --dir "$AGY_TARGET" "$AGY_TASK"
```

Set the variables to the real target and authorized task. This mode was not a headless write grant on agy 1.1.13–1.5.6. If permission is denied, inspect the reported rule and effective scope rather than silently escalating. Independently inspect `git status` and `git diff` in the repository and run tests appropriate to the edit. Verify any reported file changes and test results.

## Shared agy runtime diagnostics

- **MCP startup hangs:** agy loads MCP servers from `~/.gemini/config/mcp_config.json` and plugin `mcp_config.json` files under `~/.gemini/config/plugins/`. Inspect `~/.gemini/antigravity-cli/log/cli-*.log` for a server that never becomes ready. The doctor reports configured stdio server counts on timeout. An earlier stdout-pipe hang was addressed by sending wrapper output to a temporary file; a server that blocks agy startup can still cause a timeout. See [upstream #37](https://github.com/yuting0624/antigravity-for-claude-code/issues/37).
- **Windows and WSL:** historical native Windows headless agy builds could hang without a console. WSL avoids that reported mechanism; use a repository on the WSL Linux filesystem to avoid slow access through `/mnt/c/`. See [upstream #6](https://github.com/yuting0624/antigravity-for-claude-code/issues/6) and the [archived investigation](../claude/TROUBLESHOOTING.md#windows-delegation-hangs-or-exits-12-timeout-with-a-0-byte-log).
- **Authentication or models:** inspect `agy models` and the auth route reported by the doctor. Model entitlement varies by account, project, location, and route. Unremapped tiers may fall back to entitled models; explicit `--model` or tier remaps do not. The [implementation notes](CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md) describe the tested account's observed fallback. Do not assume a binary on `PATH` means authentication succeeded.
- **Working directory:** `agy-job list` shows jobs started from the current directory. Set `--dir` to the intended workspace for delegation and verify changes in that repository. A successful reply alone does not establish that requested edits occurred.
- **Denied action:** exit 15 covers headless permission denials, including the agy 1.1.13 hard error and the soft denial observed again from 1.1.20. Check stderr and `denied_actions` when present for the tool and target, then inspect effective agy permissions. `--allow-url` grants authorized URL reads. Search uses separate permissions. Keep any retry within the authorized scope.

### Wrapper exit codes

The wrapper prints `AGY_SIGNAL` on classifiable failures. Read stderr and consult the installed wrapper's `--help` for details.

| Exit | Meaning and next check |
| --- | --- |
| 0 | Success; independently verify output and changes. |
| 1 | Invalid usage; check flags. |
| 2 | Unclassified agy failure; inspect stderr. |
| 3 | Empty output; inspect stderr and model availability. |
| 10 | Quota or rate limit; inspect the account and provider response. |
| 11 | Authentication failure; check the configured agy auth route. |
| 12 | Timeout; inspect partial output and narrow or adjust the request. |
| 13 | agy missing from `PATH`. |
| 14 | Model unavailable or not entitled; inspect `agy models`. |
| 15 | Permission denied; inspect the denied action and scope. |
| 16–18 | Migration-specific missing Python, failed steps, or missing prerequisites; inspect the migration report. |

The [archived Claude troubleshooting guide](../claude/TROUBLESHOOTING.md) preserves the full upstream version-specific findings, exit-code details, and issue attribution. Report Codex-port problems in the [downstream issue tracker](https://github.com/paulnamalomba/antigravity-for-codex/issues). Include sanitized doctor output, OS, Codex and agy versions, install method, and relevant errors.
