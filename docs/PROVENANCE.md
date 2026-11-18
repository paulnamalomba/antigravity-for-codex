# Project Provenance, Lineage & Attribution Guide

> **Repository:** `https://github.com/paulnamalomba/antigravity-for-codex`  
> **Downstream Port Maintainer:** Paul Namalomba ([@paulnamalomba](https://github.com/paulnamalomba))  
> **Upstream Project:** [`antigravity-for-claude-code`](https://github.com/yuting0624/antigravity-for-claude-code)  
> **Upstream Author & Architect:** linyuting ([@yuting0624](https://github.com/yuting0624))  
> **License:** MIT License  

---

## 1. Executive Summary & Project Lineage

`antigravity-for-codex` is a downstream port of the open-source [`antigravity-for-claude-code`](https://github.com/yuting0624/antigravity-for-claude-code) plugin created and designed by **linyuting**. 

The upstream project pioneered the **dual-core agentic architecture**: pairing an intelligent frontier conductor model (responsible for requirements, architecture, deep reasoning, and strict verification) with a high-throughput, low-cost executor model (Google Antigravity CLI / Gemini) for boilerplate generation, migrations, test scaffolding, and grounded web research. This architecture was empirically demonstrated by linyuting to reduce frontier model token expenditure by **27% to 64%** on scaled tasks while preserving machine-checked quality.

The goal of `antigravity-for-codex` is to bring this exact dual-core architectural philosophy and its battle-tested runtime wrappers to **Codex CLI (`0.170.0+`)**, while maintaining complete backwards-compatibility and dual-runtime capability with Claude Code.

---

## 2. License Compliance & Copyright Retention

Both the upstream project and this port are licensed under the **MIT License**.

### 2.1 The MIT License Terms
The MIT license grants broad permissions to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, provided that:

> *"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."*

### 2.2 Dual-Copyright Retention
In accordance with section 1 of the MIT license:
- The original copyright notice belonging to **linyuting** is preserved unmodified in the root [`LICENSE`](../LICENSE) file and throughout the project documentation:
  ```text
  Copyright (c) 2026 linyuting
  ```
- Downstream additions, Codex CLI adaptations, skills conversions, and documentation authored by **Paul Namalomba** carry co-existing copyright notice:
  ```text
  Copyright (c) 2026 Paul Namalomba
  ```

### 2.3 Upstream Attribution in Plugin Manifests
The plugin manifest specification for Codex CLI (`.codex-plugin/plugin.json`) explicitly acknowledges the upstream creator:
- **`author`**: Paul Namalomba (`https://github.com/paulnamalomba/antigravity-for-codex`)
- **`developerName`**: Paul Namalomba
- **`upstream`**: linyuting (`https://github.com/yuting0624/antigravity-for-claude-code`)
- **`longDescription`**: Highlights that the extension is a port maintained by Paul Namalomba, based on the original work by linyuting.

---

## 3. Git Remote & Upstream Syncing Conventions

To maintain synchronization with upstream improvements, bug fixes, and compatibility updates, every local clone of this repository should configure both `origin` (downstream port) and `upstream` (original repository) remotes.

### 3.1 Remote Configuration

Inspect your current remotes:
```bash
git remote -v
```

Add the upstream tracking remote if not already present:
```bash
# Set origin to the active port repository
git remote set-url origin https://github.com/paulnamalomba/antigravity-for-codex.git

# Add upstream pointing to linyuting's repository
git remote add upstream https://github.com/yuting0624/antigravity-for-claude-code.git
```

Verify your configuration:
```text
origin    https://github.com/paulnamalomba/antigravity-for-codex.git (fetch)
origin    https://github.com/paulnamalomba/antigravity-for-codex.git (push)
upstream  https://github.com/yuting0624/antigravity-for-claude-code.git (fetch)
upstream  https://github.com/yuting0624/antigravity-for-claude-code.git (push)
```

### 3.2 Fetching and Integrating Upstream Updates

Upstream frequently ships improvements to:
- Process tree lifecycle management (e.g. `agy-job cancel` process tree termination)
- Safe handling of Google CLI timeouts and exit codes
- Gemini model tier mappings and fallback heuristics
- Pricing matrix updates in `prices.json`

To safely pull upstream changes into your work:

```bash
# 1. Fetch latest upstream commits and tags
git fetch upstream --tags

# 2. Check incoming upstream commits
git log --oneline HEAD..upstream/main

# 3. Cherry-pick specific upstream bug fixes or features
git cherry-pick <upstream-commit-sha>

# Or rebase a feature branch against upstream/main:
# git rebase upstream/main
```

### 3.3 Commit Message Conventions for Upstream Work

When porting or backporting changes from upstream, include git trailers linking to the upstream commit:

```text
fix(job): sync upstream process tree termination fix

Backport of upstream commit 1615e6f to enhance agy-job cancel cleanup.

Upstream-Commit: 1615e6f
Upstream-PR: https://github.com/yuting0624/antigravity-for-claude-code/pull/121
Author: linyuting <yuting0624>
```

---

## 4. Issue Tracking & Reference Disambiguation

Because this codebase retains empirical notes, troubleshooting solutions, and benchmarks developed during Claude Code testing, historical issue and pull request numbers appear throughout the documentation.

### 4.1 Historical Upstream References
To prevent ambiguity with GitHub issue tracking on `paulnamalomba/antigravity-for-codex`:
- All historical issue numbers referencing Claude Code findings are explicitly labeled as **`[upstream #N]`**.
- Examples:
  - `[upstream #6](https://github.com/yuting0624/antigravity-for-claude-code/issues/6)`: Windows headless console hang.
  - `[upstream #10](https://github.com/yuting0624/antigravity-for-claude-code/issues/10)`: Headless agy write permission semantics.
  - `[upstream #11](https://github.com/yuting0624/antigravity-for-claude-code/issues/11)` / `[upstream #15](https://github.com/yuting0624/antigravity-for-claude-code/issues/15)`: Marketplace PATH resolution.
  - `[upstream #37](https://github.com/yuting0624/antigravity-for-claude-code/issues/37)`: Stdio MCP inheritance and stdout buffering.
  - `[upstream #115](https://github.com/yuting0624/antigravity-for-claude-code/issues/115)`: `--print-timeout` exit 3 vs exit 12 handling.
  - `[upstream #117](https://github.com/yuting0624/antigravity-for-claude-code/issues/117)`: Windows Git Bash `taskkill` process tree termination.

### 4.2 Where to File New Issues

| Issue Category | Target Repository | Link |
| --- | --- | --- |
| **Codex CLI Plugin Issues** (Skills, Manifests, Codex hooks, dual-runtime) | `paulnamalomba/antigravity-for-codex` | [New Issue](https://github.com/paulnamalomba/antigravity-for-codex/issues/new/choose) |
| **Original Claude Code Plugin** (Claude commands, Claude marketplace) | `yuting0624/antigravity-for-claude-code` | [Upstream Issues](https://github.com/yuting0624/antigravity-for-claude-code/issues) |
| **Google Antigravity CLI** (`agy` core binary, auth, server protocols) | `google-antigravity/antigravity-cli` | [Google CLI Issues](https://github.com/google-antigravity/antigravity-cli/issues) |

---

## 5. Architectural Adaptation Matrix

| Domain | Upstream (`antigravity-for-claude-code`) | Downstream Port (`antigravity-for-codex`) |
| --- | --- | --- |
| **Runtime Conductor** | Claude Code CLI (`claude`) | Codex CLI (`codex`) & Claude Code CLI |
| **Manifest Format** | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` + `.claude-plugin/plugin.json` (dual) |
| **Marketplace Registry** | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` + Claude registry |
| **User Workflows** | Slash commands (`commands/*.md`) | Codex Skills (`skills/<name>/SKILL.md`) + Commands |
| **Hook Execution** | Claude Code hooks (`hooks/hooks.json`) | Codex `codex_hooks` JSON IPC engine (`hooks/hooks.json`) |
| **Environment Options** | `CLAUDE_PLUGIN_OPTION_*` & `~/.claude/settings.json` | `CODEX_PLUGIN_OPTION_*` + `CLAUDE_PLUGIN_OPTION_*` dual loader |
| **Process Supervision** | `bin/agy-*` bash wrappers | Preserved, hardened with Codex login shell (`-lc`) compliance |
| **Cost Verification** | `prices.json` (Claude 4 + Gemini) | `prices.json` (Expanded for GPT-6.1/5.6-sol + Gemini) |

---

## 6. Open Source Ethics & Maintenance Pledge

This repository operates under transparent open-source ethics:
1. **Respect for Upstream Authorship:** linyuting's foundational role as original architect and author is permanently recorded across documentation, manifests, and commit history.
2. **Community Reciprocity:** Any bug fixes, performance improvements, or portability hardening discovered in the development of `antigravity-for-codex` will be offered back to upstream where applicable.
3. **Accuracy in Claims:** Empirical claims regarding token reduction and benchmark results cite the original experimental setups and methodologies established upstream.
