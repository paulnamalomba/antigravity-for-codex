<div align="center">

# Antigravity for Codex CLI

Delegate bounded work to the Antigravity CLI (`agy`) while Codex plans and verifies the result.

[![Upstream Claude CI](https://github.com/yuting0624/antigravity-for-claude-code/actions/workflows/ci.yml/badge.svg)](https://github.com/yuting0624/antigravity-for-claude-code/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

This is a work-in-progress Codex port maintained by [Paul Namalomba](https://github.com/paulnamalomba), based on [antigravity-for-claude-code](https://github.com/yuting0624/antigravity-for-claude-code) by [linyuting](https://github.com/yuting0624) and contributors. The badge reports **upstream Claude project CI**, not this port's CI. See [provenance](docs/codex/PROVENANCE.md) and [license](LICENSE).

## Install locally

Install Codex CLI and the [Antigravity CLI](https://antigravity.google/docs/cli-using), authenticate `agy`, and check available models with `agy models`. From a trusted checkout of this repository, run:

```bash
codex plugin marketplace add --json .
codex plugin add --json antigravity@antigravity-for-codex
```

The repo marketplace is [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json), and the plugin manifest selects the dedicated [`codex/skills/`](codex/skills/) tree. In a Codex CLI 0.170.0 local test, registration returned `marketplaceName`, `installedRoot`, and `alreadyAdded`. The install returned these fields (the temporary home path is redacted):

```json
{
  "pluginId": "antigravity@antigravity-for-codex",
  "name": "antigravity",
  "marketplaceName": "antigravity-for-codex",
  "version": "0.31.2",
  "installedPath": "<temporary Codex home>/plugins/cache/antigravity-for-codex/antigravity/0.31.2",
  "authPolicy": "ON_INSTALL"
}
```

Start a new Codex session after installation. Review the Antigravity hooks in `/hooks` and trust them to enable their behavior. After editing the plugin, rerun `codex plugin add --json antigravity@antigravity-for-codex` to refresh the cache and review any changed hook approvals.

A local Git checkout can be copied into the Codex cache in its entirety, including `.git/config`. Install only from a trusted clean checkout. Build any shareable package from a clean tracked export without `.git`, and retain the [MIT license and copyright notices](LICENSE).

In the skill picker, select `antigravity:antigravity-setup` for diagnostics or `antigravity:antigravity` for bounded delegation. Other skills cover research, review, jobs, handoff, media, cloud debugging, and migration. See the [implementation notes](docs/codex/CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md) for hooks, wrapper flags, permissions, and verification.

The Codex hooks check agy at startup, add routing guidance at startup and compaction, and suggest delegation for bulk prompts. The tool guard applies to the optional `antigravity-delegate` role. In authenticated `agy 1.5.11` probes, one URL read returned `URL_READ_FAILED` and another timed out. URL access remains unverified on the tested account.

Use the [Codex PoC playbook](docs/codex/POC-PLAYBOOK.md) to measure delegation. The [upstream A/B results](docs/claude/AB-RESULTS.md) report one Claude run per arm and exclude Gemini costs.

## Community project

Not affiliated with or endorsed by Google, Anthropic, or OpenAI. You are responsible for your own credentials, data-sharing choices and usage costs. Historical Claude documentation and measurements remain available in [README.md.bak](README.md.bak) and [the Claude guides](docs/claude/). The [original proposal and audit](docs/research/) record the port’s research history. Contributions to this port and the separate upstream project are described in [CONTRIBUTING.md](CONTRIBUTING.md).
