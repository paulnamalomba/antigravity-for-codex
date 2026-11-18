# Migration and interoperability

## Using this port with Codex

Installing the Codex plugin does not require a configuration migration. From the repository root, register the local marketplace and install the plugin:

```sh
codex plugin marketplace add --json .
codex plugin add --json antigravity@antigravity-for-codex
```

The install response's `installedPath` is the absolute cached plugin root. Start a new Codex session and review and trust the plugin hooks in `/hooks`. After changing this checkout, repeat the `codex plugin add` command to refresh the cached copy and review changed hook approvals. Select `antigravity:antigravity-setup` for diagnostics and `antigravity:antigravity-migrate` for the existing Claude migration workflow. See [installation](../../README.md#install-locally) and the [Codex implementation notes](CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md).

Set `PLUGIN_ROOT` to the absolute `installedPath` returned by installation, then run `"$PLUGIN_ROOT/bin/agy-doctor" --codex` when invoking diagnostics directly. The packaged Codex skills resolve their own installed root. Do not assume the plugin's `bin/` is on `PATH`.

**`agy-migrate` imports Claude Code configuration into Antigravity.** No automated Codex-to-agy migration is provided. Inspect and translate each desired asset manually, then verify it in an appropriately scoped agy session. The following Codex assets remain client-scoped unless explicitly adapted for agy:

| Codex asset | Manual interoperability step |
| --- | --- |
| Marketplace and installed plugin | Install or configure the desired capability for agy separately. Codex marketplace registration and its cached plugin are for Codex. |
| `AGENTS.md` and other instructions | Review the intended instructions and agy's workspace and rule discovery. Adapt them to a supported agy location and test that they load in the intended project. |
| Skills | Inspect each skill's instructions, dependencies, and permissions. Adapt it to agy's skill format and discovery paths, then invoke it and verify the behavior. |
| Hooks | Review events, matchers, commands, and runtime variables. Translate only supported agy hooks and test them in a controlled project. |
| Agent TOML | Review the role's instructions and tool scope. Create an equivalent supported agy agent only where its format and permissions allow, then test its behavior. |
| MCP servers and permissions | Configure only the needed server and narrowly scoped permissions using agy's formats. Check connectivity and effective grants without copying credentials. |

Verify outputs and permissions independently. Do not assume sessions or client-specific settings are portable. The archived matrix describes the different Claude-to-agy path.

For a Claude Code import, select `antigravity:antigravity-migrate` or run `"$PLUGIN_ROOT/bin/agy-migrate"` without `--apply` to inspect the plan. Review warnings, omissions, and scope before authorizing changes. `--apply-permissions` can widen grants and requires separate review. The tool reports its backup and reversal command. Consult the [historical Claude-to-agy compatibility matrix](../claude/MIGRATION.md#6-compatibility-matrix) for what it does and does not import, and verify its version-specific observations against the installed runtime.

The [archived migration reference](../claude/MIGRATION.md) retains upstream measurements, storage layouts, and attribution.
