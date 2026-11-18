# Codex plugin migration: implementation and evidence

Codex CLI runs the session, decides whether to delegate within the user’s authorization, and verifies the result. Antigravity CLI (`agy`) executes a bounded task through the packaged wrappers. The inherited Claude Code files document the upstream integration. The port is based on linyuting’s project. [Provenance](PROVENANCE.md) · [MIT license](../../LICENSE)

## Install and run in Codex

From the trusted checkout, register the local marketplace and install the package. Save the cached plugin path if you plan to call a wrapper directly.

```bash
codex plugin marketplace add --json .
plugin_root="$(
  codex plugin add --json antigravity@antigravity-for-codex |
    python3 -c 'import json, sys; print(json.load(sys.stdin)["installedPath"])'
)"
"$plugin_root/bin/agy-doctor" --codex
```

Open Codex in the project you want to work on. Review the installed hooks with `/hooks`. For interactive work, choose the relevant skill from the picker. A headless session can request the same workflow through a prompt.

```bash
codex exec --json 'Use the antigravity:antigravity-jobs skill to list jobs for this project.'
```

| Task | Installed Codex skill |
| --- | --- |
| Check the installation and agy access | `antigravity:antigravity-setup` |
| Delegate bounded analysis or authorized workspace edits | `antigravity:antigravity` |
| Retrieve and independently verify sources | `antigravity:antigravity-research` |
| Review a specified diff | `antigravity:antigravity-review` |
| Start, inspect, collect, or cancel jobs | `antigravity:antigravity-jobs` |
| Hand off a test-gated implementation task | `antigravity:antigravity-handoff` |
| Analyze media with scoped permissions | `antigravity:antigravity-media` |
| Diagnose Cloud Run logs | `antigravity:antigravity-cloud-debug` |
| Inspect a legacy Claude-to-agy settings import from Codex | `antigravity:antigravity-migrate` |

For setup issues and benchmark workflows, see [troubleshooting](TROUBLESHOOTING.md) and the [Codex PoC playbook](POC-PLAYBOOK.md).

## Packaging

- The Codex package declares its own skills and hooks. `commands: []` disables the compatibility import of the inherited slash commands. [Codex manifest](../../.codex-plugin/plugin.json) · [Skills](../../codex/skills) · [Codex hook configuration](../../hooks/codex-hooks.json)
- [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json) is the repo marketplace and its `./` source resolves to this repository root. OpenAI's [packaging guide](https://developers.openai.com/plugins/build/plugins) explains repo marketplaces, local sources, and plugin enablement. Installing a local plugin uses a cached copy, so refresh it after edits.
- Attribution appears in the Codex manifest description and in the repository license. Set Codex workflow options with documented wrapper flags and environment variables such as `AGY_USAGE_LOG`. The shared wrappers can also load legacy Claude settings when present.
- The explicit Codex hook path separates the two runtimes. Omitting it causes Codex 0.170.0 to discover the inherited `hooks/hooks.json`. [Codex hook loader](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/loader.rs)

## Codex hooks

Review and trust the plugin hooks through `/hooks`. Codex requests renewed trust when the cached hook code changes. Python 3 is required to run these handlers. [Codex hook configuration and trust](https://learn.chatgpt.com/docs/hooks)

| Hook purpose | Codex behavior |
| --- | --- |
| Startup agy check | `SessionStart` checks `agy --version` with a two-second timeout and surfaces a warning if needed. |
| Routing policy at startup and compaction | `SessionStart` supplies Codex-specific guidance at both points. Set `AGY_CODEX_CODING_POLICY=off` in the hook environment to disable the guidance. |
| Bulk-prompt nudge | `UserPromptSubmit` scans the prompt for bulk-work cues and returns fixed advisory text. Set `AGY_CODEX_DELEGATION_NUDGE=off` to disable it. |
| Subagent Bash gate | `PreToolUse` checks shell calls and rejects direct patch calls for the `antigravity-delegate` role. `SubagentStart` supplies the role with the exact cached wrapper path. |

The role uses a fresh read-only call to the packaged `agy-delegate` wrapper on POSIX. Use the main-session skills for file edits, job management, and handoffs. A supported agy must advertise `--settings`. Codex loads the [role file](../../.codex/agents/antigravity-delegate.toml) in this trusted project. To use the role in another project, place the file in that project’s `.codex/agents/` or your Codex home’s `agents/` and trust the installed plugin hooks. Codex’s sandbox, approvals, and the agy permission configuration govern execution. The hook covers the named role’s matched calls. [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Codex hook tool coverage](https://learn.chatgpt.com/docs/hooks#tool-coverage)

## Runtime guidance

Use the cached wrapper paths provided by the Codex skills. For read-only work, check that `agy --help` advertises `--settings`, then use `agy-delegate --read-only`. Add `--allow-url` for known-URL reads. Web search, commands, and writes depend on the available tools and effective permissions. If retrieval is denied, use an authorized source tool and report the gaps. Consult `agy-delegate --help` and `agy-doctor --codex` for the installed versions.

`agy-job list` lists jobs for the current directory; `status`, `result`, and `cancel` take an ID. `agy-handoff` uses broad `--yolo` permissions internally. For a test-gated handoff, start from a clean, committed baseline, pass `--verify '<test command>'` and `--tests '<existing test paths>'`, and review the resulting diff and test output. The test protection compares against Git; pre-existing test edits can trigger a failure and uncommitted changes obscure attribution. `--dir` is not machine-wide containment. See `agy-handoff --help` for details.

For a Codex comparison, record the conductor’s `codex exec --json` usage and the wrapper’s `AGY_USAGE` records separately, including retries and verification. Use actual rates or plan data when calculating cost. The inherited Claude benchmark reports a separate Claude-side weighted proxy. [Benchmark results and Codex measurement guidance](AB-RESULTS.md)

## Audit resolution and evidence

These source links are pinned to Codex `rust-v0.170.0` (commit `29eb79e9866b3262a777fdf8195c1b9e63684c91`); current documentation and later versions may differ.

| Area | Evidence and resolution |
| --- | --- |
| Manifest and skills | The [legacy manifest parser](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/manifest.rs) and [loader](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/loader.rs) inform the explicit `skills` path and description attribution in [the compatibility manifest](../../.codex-plugin/plugin.json). The dedicated [Codex skills](../../codex/skills) invoke the shared wrappers without assuming Claude slash commands or plugin PATH setup. |
| Marketplace | The pinned [marketplace parser](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/marketplace.rs) and [local source handling](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/marketplace_add/source.rs) inform [the repo marketplace](../../.agents/plugins/marketplace.json), whose `./` source points to the plugin root. |
| Hook discovery | The pinned [loader](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/loader.rs) and [hook discovery](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/engine/discovery.rs) inform the explicit [Codex hook file](../../hooks/codex-hooks.json), preventing default discovery of the Claude hook configuration. |
| Hook protocol | The [Codex handler](../../hooks/codex-hooks.py) uses the tagged [wire schema](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/schema.rs). It checks the tool and agent scope before reusing the inherited wrapper-argument validator. |
| Permissions | The [research skill](../../codex/skills/antigravity-research/SKILL.md) distinguishes search from known-URL reads. The [media wrapper](../../scripts/agy-media.sh) provides `--require-scoped` to refuse broad approval when scoped permissions are unavailable. [Regression tests](../../tests/run-tests.sh) |
| Diagnostics | `agy-doctor --codex` checks the CLI, JSON files, marketplace registration, plugin enablement, and packaged files before reporting agy health. The default command retains the Claude checks. [Doctor implementation](../../scripts/doctor.sh) |
| Provenance and benchmarks | The inherited MIT notices, issue lineage, contributor credit, and separate upstream contribution branch are documented in [provenance](PROVENANCE.md). The [A/B results](AB-RESULTS.md) distinguish the Claude-side proxy from end-to-end cost. |

## Verification and remaining work

- Codex CLI 0.170.0 registered and installed the plugin. The app server discovered nine Codex skills and the four Codex hook declarations. Rerunning the local install refreshed the same-version cache. See the [installation instructions](../../README.md#install-locally).
- In an isolated Codex home, the four hooks started untrusted and could be approved. An authenticated session ran a normal main-thread shell command. The delegate role’s unrelated shell command was blocked and its installed read-only wrapper dry run succeeded. Reinstalling after a change to the hook script marked all four approvals as modified.
- An authenticated `codex exec` session read the installed `$antigravity-jobs` skill and ran the cached `bin/agy-job list` from a separate Git repository. It returned `(no jobs)` with exit 0. A temporary Codex home and job registry isolated the check.
- A stubbed delegation verified `request-review` with a `read_url` grant and no broad approval flag. The Codex doctor reported the real registration and enablement in an isolated install and returned exit 1 in a fresh Codex home.
- The Bash 3.2 regression suite passed 605 checks with zero failures, including startup, compaction, prompt nudge, and scoped guard payloads. The changelog placement check was skipped because no pull request base was present. ShellCheck and all eight CI JSON parses passed.
- Authenticated `agy 1.5.11` fell back to Gemini 3.8 Flash High on the tested account. One public URL probe returned `URL_READ_FAILED`. The second probe reached the wrapper’s timeout path and returned exit 12. Live URL access remains unverified.

Plugin Eval provides optional static checks through `plugin-eval analyze . --format markdown`. It flagged the absent privacy and terms URLs for the local manifest. Those fields need real project policies before submission. Local installation and skill invocation were verified separately.

Public-directory submission requires a separate packaging review. The current submission guide requires removing lifecycle hooks for public-directory submissions. [OpenAI public submission guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin)

Prepare upstream contributions on a separate branch. [Upstream contribution guide](https://github.com/yuting0624/antigravity-for-claude-code/blob/master/CONTRIBUTING.md)
