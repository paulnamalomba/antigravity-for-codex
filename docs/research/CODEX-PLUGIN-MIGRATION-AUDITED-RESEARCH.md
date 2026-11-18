# Research & Migration Blueprint: Porting Antigravity to Codex CLI

> **Historical audit.** This is the audit from `research/codex-agy-plugin` at `b888c2f`. For the shipped Codex hooks, skills, and validation results, use the [current implementation guide](../codex/CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md). Findings below describe the earlier checkout.

> **Target Workspace:** `/Users/kabwe/Development/antigravity-for-codex`  
> **Target Repository:** `https://github.com/paulnamalomba/antigravity-for-codex` (Port Maintainer: Paul Namalomba)  
> **Upstream Repository:** `https://github.com/yuting0624/antigravity-for-claude-code` (Original Author: linyuting / @yuting0624)  
> **Audit baseline:** Codex CLI `0.170.0` and Antigravity CLI `1.5.11`
> **Status:** Audited migration proposal. See [audit findings and verification](#10-audit-findings-and-verification).
> **Document Version:** v0.0.4 (18 Nov, 13:39 UTC).

---

## 1. Executive Summary & Dual-Core Agentic Philosophy

The `antigravity-for-claude-code` plugin was built on a core insight: **intelligent model routing across the software development lifecycle (SDLC)**. Rather than relying on a single frontier model for every operation, it pairs a conductor model with an external executor (`agy` / Gemini).

The proposal assigns these roles:

- **Codex CLI as the Conductor/Synthesizer:** Codex excels at local tool execution, terminal orchestration, project-level repository understanding, and complex software specification.
- **Antigravity (`agy` / Gemini) as the Research & Execution Engine:** Antigravity supplies an external worker for retrieval and implementation. Available models and tools depend on the installed CLI, account, and permission settings. See [Google's Antigravity documentation](https://antigravity.google/docs/cli/overview/).

### 1.1 Open Source Provenance, Ethics & Attribution

This project (`antigravity-for-codex`) is an open-source port of the foundational [`antigravity-for-claude-code`](https://github.com/yuting0624/antigravity-for-claude-code) project created and architected by **linyuting** ([@yuting0624](https://github.com/yuting0624)).

- **MIT license.** Retain linyuting’s original copyright notice and the MIT permission notice in all copies or substantial portions of the upstream software. The [downstream LICENSE](../LICENSE) retains the full text and adds Paul Namalomba’s notice for downstream contributions. Carry the license into distributed plugin bundles. See the [upstream license at the shared baseline](https://github.com/yuting0624/antigravity-for-claude-code/blob/6f9b383f6a41b7bd0b97b9702ddd2902f3538fac/LICENSE) and the [MIT license text](https://opensource.org/license/mit).
- **Authorship and support.** Credit linyuting and upstream contributors for the original architecture and wrappers. Direct reports about the Codex port to the [downstream issue tracker](https://github.com/paulnamalomba/antigravity-for-codex/issues). Link inherited reports to their original upstream issue or pull request.
- **Maintenance.** This checkout has both remotes configured. Upstream synchronization is deferred until a separate upstream contribution branch exists. Section 10 records the contribution boundary and the stale sync instructions in the [provenance guide](PROVENANCE.md).
- **Benchmark scope.** In one upstream scaled task, the hybrid arm’s Claude-side cost-weighted proxy was about 27% below solo high effort and 64% below solo max effort. All three arms passed the same 3/3 evaluation gate. The proxy excludes Gemini costs and the experiment used Claude as the conductor. See [local benchmark record](AB-RESULTS.md) and the [pinned upstream results](https://github.com/yuting0624/antigravity-for-claude-code/blob/6f9b383f6a41b7bd0b97b9702ddd2902f3538fac/docs/AB-RESULTS.md).

### 1.2 Core Architecture Shift

In Claude Code, extensions interact through slash commands (`commands/*.md`), lifecycle hooks (`hooks/hooks.json`), and Claude-specific environment variables (`CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_OPTION_*`).

In **Codex CLI**:

1. **Discovery.** Use a Codex manifest and an explicit repo marketplace entry. This proposal uses the `.codex-plugin/plugin.json` compatibility format for the pinned CLI. OpenAI also documents a portable root `plugin.json` format for new packages. [Plugin packaging](https://developers.openai.com/plugins/build/plugins)
2. **Workflows.** Author Codex workflows as skills. Codex 0.170.0 also includes migration of compatible legacy Markdown commands to skills. Keep runtime-specific behavior explicit in authored skills and test for duplicate discovery. [Tagged command migration](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/command_migration/plugin.rs)
3. **Runtime.** Share the agy wrappers where their behavior is portable. Give each client its own hook configuration and test both clients before claiming compatibility.

## 2. Component Mapping Matrix

| Claude Code | Codex proposal | Migration check |
| --- | --- | --- |
| `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` | Verify the entry name, enabled plugin ID, and packaged files. |
| `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` | Confirm that registration selects the Codex marketplace. |
| `commands/*.md` | `skills/<name>/SKILL.md` | Invoke each authored skill and check for overlaps with legacy migration. |
| `agents/antigravity-delegate.md` | Skill calling a packaged wrapper | Use a documented Codex TOML agent definition if a Codex subagent role is needed. |
| `hooks/hooks.json` | Dedicated Codex hook file when needed | Verify trust, event input, output, and tool matching against the pinned CLI. |
| `CLAUDE_PLUGIN_OPTION_*` and `.pluginConfigs` | Existing wrapper flags and explicit port-owned configuration | Resolve per option and test legacy behavior. |
| `claude -p` | `codex exec` | Test headless and interactive behavior separately. |
| `bin/agy-*` | The same packaged wrappers | Resolve an executable path and verify behavior from an unrelated project directory. |

[Codex skills](https://learn.chatgpt.com/docs/build-skills) · [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Codex 0.170.0](https://github.com/openai/codex/releases/tag/rust-v0.170.0)

## 3. Manifest & Marketplace Specifications

### 3.1 Codex Plugin Manifest: `.codex-plugin/plugin.json`

This example targets the legacy manifest reader in Codex 0.170.0. Use `./`-prefixed component paths. The loader accepts an optional `interface` block and up to three default prompts of at most 512 characters each. Plugin Eval and publication checks impose their own quality and submission criteria. The legacy reader does not consume `author`, `maintainers`, or `upstream` as runtime metadata. Use the visible description, repository provenance, and license to carry credit. If structured author metadata is needed, evaluate the documented portable manifest format and its OpenAI extension. [Tagged manifest reader](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/manifest.rs) · [OpenAI package formats](https://developers.openai.com/plugins/build/plugins#add-openai-specific-metadata)

Create `.codex-plugin/plugin.json`:

```json
{
  "name": "antigravity",
  "version": "0.31.1",
  "description": "Run the Antigravity CLI (Gemini) as a collaborating AI inside Codex CLI, with intelligent model routing across the SDLC. Codex conducts — requirements, architecture, deep reasoning, verification — and routes high-volume work (grounded web research, scaffolding, tests, first-pass review, migrations) to Antigravity.",
  "interface": {
    "displayName": "Antigravity",
    "shortDescription": "Grounded deep research, reasoning, and multi-model SDLC delegation.",
    "longDescription": "Intelligent model routing for Codex CLI. Ported and maintained by Paul Namalomba, based on the original antigravity-for-claude-code by linyuting (@yuting0624). Keep judgement-heavy architecture and verification on Codex, while routing high-volume scaffolding, test generation, and multi-source web/grounded research to Antigravity (Gemini). Includes cost tracking, automated claim verification, and background jobs.",
    "developerName": "Paul Namalomba",
    "category": "Developer Tools",
    "capabilities": [
      "Interactive",
      "Write",
      "Read"
    ],
    "websiteURL": "https://github.com/paulnamalomba/antigravity-for-codex",
    "defaultPrompt": [
      "Deep research a topic using Antigravity web search",
      "Delegate boilerplate or test generation to Gemini",
      "Run doctor to verify Antigravity CLI connection"
    ],
    "brandColor": "#4285F4"
  },
  "skills": "./skills/",
  "hooks": "./hooks/codex-hooks.json",
  "keywords": [
    "antigravity",
    "gemini",
    "multi-agent",
    "deep-research",
    "grounded-search",
    "model-routing",
    "sdlc"
  ]
}
```

Create `hooks/codex-hooks.json` with no handlers. The explicit path prevents the tagged loader from falling back to the inherited Claude `hooks/hooks.json` when the `hooks` field is omitted. [Tagged hook loading](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/loader.rs#L1186-L1235)

```json
{
  "hooks": {}
}
```

Review existing shared skills for Claude-specific instructions before publishing. The tracked PNGs are display graphics. Store submission requires square icons and real policy URLs where applicable. [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission#icons)

### 3.2 Codex Marketplace Manifest: `.agents/plugins/marketplace.json`

For this repository, register the Codex marketplace through `.agents/plugins/marketplace.json`. The marketplace policy does not establish agy authentication. [OpenAI marketplace packaging](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)

Create `.agents/plugins/marketplace.json`:

```json
{
  "name": "antigravity-for-codex",
  "interface": {
    "displayName": "Antigravity for Codex"
  },
  "plugins": [
    {
      "name": "antigravity",
      "source": {
        "source": "local",
        "path": "./"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Developer Tools"
    }
  ]
}
```

### 3.3 Installation Commands in Codex CLI

From the repository root, after both manifests exist, check that registration reports `antigravity-for-codex` before installing from it. With the audited checkout, registration selected the inherited `antigravity-for-claude-code` marketplace and the proposed Codex plugin ID could not be installed.

```bash
# Register local directory as a marketplace
codex plugin marketplace add --json .

# Install the antigravity plugin from that marketplace
codex plugin add --json antigravity@antigravity-for-codex
```

Use `installedPath` from the install response to find the cached plugin root. A local install records the marketplace and plugin in `~/.codex/config.toml`:

```toml
[marketplaces.antigravity-for-codex]
source_type = "local"
source = "/absolute/path/to/antigravity-for-codex"

[plugins."antigravity@antigravity-for-codex"]
enabled = true
```

---

## 4. Lifecycle Hooks and Trust

Keep the existing Claude hook manifest and validator. Start the Codex port with explicit skills, packaged wrappers, and the empty Codex hook file in Section 3. An opt-in Codex hook can later supply session guidance. The earlier proposal used an unconditional success stub as a command gate. That design would authorize every invocation reaching the stub and must be excluded from the implementation.

- **Protocol.** In Codex 0.170.0, `SessionStart` input uses top-level `session_id`, `cwd`, `hook_event_name`, and `source`. Shell calls through `exec_command` match `Bash` in `PreToolUse`. Test permitted and denied calls against the pinned runtime. With a synchronous `PreToolUse` handler, exit `2` and nonempty stderr produce a block. Other events have their own output and exit handling. `SessionStart` accepts plain stdout or structured `hookSpecificOutput.additionalContext`. The existing `hooks/policy-context.json` already contains a structured envelope, so extract its text or emit an appropriate existing envelope.
- **Environment.** The tagged runtime supplies `PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT` for plugin hooks. Its default command runner uses `-lc` on Unix and `/C` on Windows. Validate quoting, actual invocation, and executable discovery on each supported platform. Hook variables are scoped to the hook environment.
- **Trust and scope.** Review bundled hooks through `/hooks` and verify execution after trust approval and after updates. A session hook matching `Bash` applies to matching session tools and needs explicit scoping if intended for a specific delegation role. A hook supplements runtime permissions. Verify the agy child’s own settings, workspace access, and command restrictions separately.

[OpenAI hooks documentation](https://learn.chatgpt.com/docs/hooks) · [Tagged SessionStart implementation](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/events/session_start.rs) · [Tagged PreToolUse implementation](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/events/pre_tool_use.rs) · [Tagged hook environment](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/engine/discovery.rs) · [Tagged command runner](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/hooks/src/engine/command_runner.rs)

## 5. Commands-to-Skills Conversion Blueprint

Author a first-class skill for each workflow the port supports. Review the existing shared skills for Claude-only tool names and invocation instructions before including them in the Codex manifest. The shell examples below assume `agy-*` resolves to this plugin’s packaged `bin/` wrappers. Resolve and verify that path before invoking a wrapper from the user’s project.

### 5.1 Skill Frontmatter

Provide YAML `name` and `description`. Describe when the skill applies. Short instructions and a roughly 500-line ceiling are authoring guidance. Move detailed references into `references/` when that helps readers. [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills)

### 5.2 Complete Skills Directory Structure

```
skills/
├── antigravity/                  # Existing general overview skill
│   └── SKILL.md
├── antigravity-delegate/         # Replaces commands/delegate.md
│   └── SKILL.md
├── antigravity-research/         # Replaces commands/research.md (DEEP RESEARCH)
│   ├── SKILL.md
│   └── references/
│       └── research-recipes.md
├── antigravity-handoff/          # Replaces commands/handoff.md
│   └── SKILL.md
├── antigravity-review/           # Replaces commands/review.md
│   └── SKILL.md
├── antigravity-media/            # Replaces commands/media.md
│   └── SKILL.md
├── antigravity-jobs/             # Replaces commands/status.md, result.md, cancel.md
│   └── SKILL.md
├── antigravity-cloud-debug/      # Replaces commands/cloud-run-debug.md
│   └── SKILL.md
├── antigravity-setup/            # Replaces commands/setup.md
│   └── SKILL.md
└── migrate-to-antigravity/       # Reuse for commands/migrate.md after compatibility review
    └── SKILL.md
```

---

### 5.3 Detailed Specification for Key Skills

#### A. Deep Research Skill: `skills/antigravity-research/SKILL.md`

This skill directs Codex to plan the research, use Antigravity for retrieval, verify claims against the sources, and synthesize the report.

````markdown
---
name: antigravity-research
description: Conduct multi-source deep research using Antigravity (Gemini) for grounded web search and fetch, while Codex CLI plans, adversarially verifies citations, and synthesizes the final report. Use when the user asks for deep research, literature review, multi-perspective analysis, market scans, technical documentation lookups, or fact-finding across multiple web sources.
---

# Antigravity Grounded Deep Research

Conduct multi-source grounded research. Antigravity (`agy` / Gemini) acts as a retrieval worker. The wrapper resolves `flash` and `pro` against its mappings and the models available to the account. **Codex CLI owns the plan, the verification, and the synthesis.**

Never accept raw citations unchecked: agy's print-mode citations can be domain-level, and models can present parametric knowledge as sourced fact.

## Execution Workflow

### 1. Plan (Codex)
- Decompose the user's research topic into 3–6 concrete sub-questions.
- Identify the load-bearing claims that must be verified.
- Define what constitutes sufficient evidence (e.g., official docs, benchmarks, primary papers).

### 2. Fan-Out Fetch (Antigravity via `agy-delegate`)
For searches, first verify that the session permits the search tool. Pass known URLs to the retrieval wrapper:
```bash
agy-delegate --read-only --allow-url --tier flash --timeout 15m "Read <URL> for <sub-question>. Return findings with the exact source URL and publication date."
```

> [!TIP]
> `--read-only --allow-url` sets agy application permissions for URL reads and requests review for file writes and shell commands. Web search availability needs a separate check. If search is denied, use an authorized Codex retrieval tool.
> If a query hits timeout (exit `12`), salvage whatever partial URLs were emitted, then narrow the query.

### 3. Deepen on Load-Bearing Claims (Antigravity `pro`)

For critical claims, instruct Antigravity to inspect the specific URL and extract direct quotes:

```bash
agy-delegate --read-only --allow-url --tier pro --timeout 10m "Open <URL> and quote the exact sentence(s) supporting: '<claim>'. If the page does not support it, reply NOT SUPPORTED."
```

### 4. Adversarial Verification (Codex)

- Open each load-bearing source independently. Check exact URLs, quotations, and dates.
- Prefer the source that owns the API, result, or policy. Seek independent corroboration when the claim requires it.
- Check publication dates for currency and detect stale documentation.
- Detect hallucinations or parametric assertions disguised as page content.

### 5. Synthesis & Report Delivery (Codex)

- Synthesize findings into a structured report.
- Format all citations as Markdown links with source titles and publication dates.
- Explicitly flag any unresolved or uncorroborated points under an **Unverified / Open Questions** section.

## Background Execution for Long Researches

If a research pass involves many queries, run it asynchronously:

```bash
agy-job start --read-only --allow-url "Read <URL> and summarize the evidence."
agy-job status <job-id>
agy-job result <job-id>
```

````

---

#### B. Delegation Skill: `skills/antigravity-delegate/SKILL.md`
Replaces `commands/delegate.md`:

````markdown
---
name: antigravity-delegate
description: Delegate well-scoped, deterministic, or high-volume tasks (scaffolding, boilerplate, unit tests, migrations) to Antigravity CLI (Gemini) while Codex CLI conducts and verifies. Use when the user asks to delegate work to agy, run tasks on Gemini, scaffold repetitive code, generate unit tests, or run bulk refactoring.
---

# Antigravity Task Delegation

Delegate deterministic, high-volume implementation work to Antigravity (`agy`), keeping Codex CLI's context lean and preserving token budget.

## When to Delegate
- Scaffolding new modules, entities, or DTOs following an established pattern.
- Generating unit and integration test suites against existing interfaces.
- Repetitive migrations (e.g. updating deprecated API calls across 30 files).
- Multi-file boilerplate generation.

## Command Syntax
Run write tasks only in the intended workspace with authorization. On agy 1.5.11, `--mode accept-edits` provides an in-workspace write grant. Handle permission failures explicitly.
```bash
# Fast bulk work
agy-delegate --mode accept-edits --dir . --tier flash "Implement unit tests for src/auth/token.ts covering expired tokens and invalid signatures."

# Reasoning about a complex component
agy-delegate --read-only --tier pro "Analyze src/query-engine.ts for race conditions under concurrent writes."

# Background job for long tasks
agy-job start --mode accept-edits --dir . "Generate exhaustive test coverage for all modules in src/services/"
```

## Verification Rule

**Never trust delegated output blindly.** Inspect tracked and untracked changes and run the relevant tests before accepting Antigravity’s edits.

````

---

#### C. Handoff Skill: `skills/antigravity-handoff/SKILL.md`
Replaces `commands/handoff.md`:

````markdown
---
name: antigravity-handoff
description: Hand off a whole test-covered implementation task to Antigravity CLI, using unit tests as the verification gate. Codex CLI writes the failing tests and specification, Antigravity implements until tests pass, and Codex inspects the diff. Use when the user wants to hand off a feature or bugfix to agy with test-driven gates.
---

# Test-Gated Antigravity Handoff

Hand off an entire self-contained task to Antigravity CLI using Test-Driven Development (TDD).

## Procedure
1. **Define the contract.** Establish failing tests in a clean, authorized worktree with the tests already committed as part of the baseline. The wrapper rejects dirty worktrees by default and checks protected paths against `HEAD`.
2. **Execute handoff where authorized.** The current wrapper enables agy’s broad auto-approval mode, subject to applicable policy. Run the existing handoff only in a suitably isolated workspace where that access is authorized.
   ```bash
   agy-handoff --verify "npm test" --tests tests/auth.spec.ts "Make all tests in tests/auth.spec.ts pass without modifying the test file."
   ```
3. **Verify.** Run the test suite independently and inspect the complete change set.

````

---

#### D. Jobs Skill: `skills/antigravity-jobs/SKILL.md`
Unifies `commands/status.md`, `commands/result.md`, and `commands/cancel.md`:

````markdown
---
name: antigravity-jobs
description: Manage asynchronous background Antigravity tasks. Check status, inspect results, or cancel running jobs. Use when the user asks about background jobs, checks agy job status, retrieves job results, or cancels an active delegation.
---

# Antigravity Background Jobs Management

Manage long-running tasks dispatched via `agy-job`.

## Commands
```bash
# List all active and recent jobs
agy-job list

# Check a specific job ID
agy-job status <job-id>

# Retrieve the completed result of a job
agy-job result <job-id>

# Cancel a running background job
agy-job cancel <job-id>
```

````

---

## 6. Runtime and Script Adaptation

### 6.1 Options and executable discovery

Use the existing wrapper flags for initial Codex calls. Preserve `scripts/lib/plugin-options.sh` for Claude. Codex 0.170.0’s plugin config schema excludes `[plugins."name@marketplace".options]`, and the audit found no native `CODEX_PLUGIN_OPTION_*` contract. If persistent Codex-side settings are needed, define port-owned settings and resolve each recognized option once. Explicit wrapper flags and environment values should win over configured defaults. Test mixed, partial, malformed, and legacy inputs before sharing the resolver. [Tagged Codex config schema](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core/config.schema.json) · [OpenAI Claude plugin migration](https://developers.openai.com/plugins/guides/submit-claude-plugin)

Use the installed plugin’s executable path or a verified `PATH` entry for the packaged `bin/` wrappers. Test from a project directory outside the plugin checkout. Keep the delegated task’s working directory independent of the wrapper’s own location.

### 6.2 Diagnostics

Extend `scripts/doctor.sh` with an optional Codex check. Verify versions, manifest parsing, registration under the right marketplace, installed wrapper access, and skill discovery. Exercise agy authentication separately with an authorized minimal probe. Distinguish checks based on file presence from successful runtime validation. Keep the Claude-only workflow usable when Codex is absent.

### 6.3 Pricing and measurement

Retain the flat `prices.json` schema consumed by `scripts/agy-cost-compare.sh` and `scripts/measure-session.py`. Add a price only with a dated provider source, the exact billing model, the units, and the applicable usage tier. Keep API estimates distinct from subscription usage and record unknown rates as unknown. Measure both conductor and executor usage, verification retries, wall time, and the common quality gate before making a Codex savings claim. [OpenAI API pricing](https://platform.openai.com/docs/pricing) · [Gemini API pricing](https://aistudio.google.com/docs/pricing) · [Antigravity plans](https://antigravity.google/pricing)

## 7. Deep Research Workflow

1. Codex defines the questions and identifies claims that need primary sources.
2. The retrieval tool returns candidate evidence with precise URLs. When agy reads known URLs, the wrapper translates its read-only and URL options into agy session settings. Treat partial timeout output as candidate evidence.
3. Codex opens the cited sources and verifies what each source supports. Use a second source or model where the claim merits independent corroboration.
4. Codex writes the report and identifies open questions. Establish any performance or cost advantage by comparing complete runs on the same workload.

## 8. Implementation Roadmap

1. **Package.** Create the two manifests and the empty Codex hook file from Section 3. Test local registration and installation with a temporary `CODEX_HOME` outside the source tree. Confirm the selected marketplace name, plugin ID, and installed `LICENSE`, wrappers, and skill files.
2. **Port workflows.** Inventory the existing commands. Port the planned skills and exercise explicit invocations in a fresh Codex session. Test installed wrappers from a separate project and retain the existing Claude entry points.
3. **Add runtime features.** Validate direct wrapper execution first. Add Codex-specific hooks only after testing trust, update review, event dispatch, and permitted and denied operations. Run the existing shell suite on macOS and Linux. Test the supported agy versions and exercise live opt-in read-only retrieval plus job status, timeout, and cancellation.
4. **Evaluate.** Run `plugin-eval analyze . --format markdown` from the plugin root if Plugin Eval is available. Its bundled script also accepts `node /path/to/plugin-eval/scripts/plugin-eval.js analyze . --format markdown`. Review findings and confirm the target was detected as a plugin. Then test actual installation and behavior in Codex. [Plugin Eval source and usage](https://github.com/openai/plugins/tree/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/plugin-eval)
5. **Verify release artifacts.** Check policy URLs, presentation assets, attribution, and the license in the actual bundle. Confirm the distribution channel supports any bundled hooks. [OpenAI packaging and distribution](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks)

## 9. Release Readiness

The first deliverable is a local, installable Codex plugin with discoverable skills and verified wrapper execution. Live agy permission behavior, optional hooks, Claude regression coverage, and cost claims each need their own evidence.

## 10. Audit Findings and Verification

**Audit baseline.** 2026-11-18, commit `0b5ea90` on `feature/codex-marketplace`. The audit compared the blueprint and claimed completed work with the checkout, public primary sources, tagged Codex implementation, and isolated Codex CLI probes. It corrected the blueprint in this file. Follow-up changes to the other repository files below remain open.

### Findings by priority

| Priority | Finding | Resolution or remaining work |
| --- | --- | --- |
| Blocker | The checkout has no `.codex-plugin/plugin.json` or `.agents/plugins/marketplace.json`. The untracked `.codex-plugin/marketplace.json` has plugin-style fields and lacks the marketplace `plugins` list. Codex does not discover a marketplace at that path. | Section 3 supplies the proposed two-file layout. This audit did not implement it. [Tagged marketplace discovery](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core-plugins/src/marketplace.rs) |
| Blocker | The previous hook design put an always-successful validator behind an `exec_command` matcher. It also used the wrong stdin schema and described exit `2` as universal. | Sections 3 and 4 select a separate, initially empty hook file and remove the stub. Omitting the hook path would load the inherited default. Actual hook approval and behavior still need a live test. [OpenAI hook tool coverage](https://learn.chatgpt.com/docs/hooks#tool-coverage) |
| High | The draft assumed native Codex per-plugin options and supplied a loader whose two prefixes could let a configured value override an explicit environment value read by existing scripts. | Section 6 uses existing flags as the initial interface. Preserve per-key precedence if adding settings. [Current Claude loader](../scripts/lib/plugin-options.sh) · [Tagged Codex schema](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/core/config.schema.json) |
| High | Research examples confused known-URL reads with web search and background jobs omitted permission flags. Handoff used `--test` and job listing used `status` without an ID. | The blueprint carries read-only flags into background retrieval, requires verification of search permissions, and uses the wrapper’s actual options. [Delegate](../scripts/agy-delegate.sh) · [Handoff](../scripts/agy-handoff.sh) · [Jobs](../scripts/agy-job.sh) |
| High | The proposed rate table used a different schema from the existing consumers and lacked primary evidence for the quoted prices. The savings claims exceeded the historical benchmark. | Sections 1 and 6 scope the evidence and remove the unverified table. [Rates](../prices.json) · [Consumer](../scripts/agy-cost-compare.sh) · [Historical results](AB-RESULTS.md) |

### Audit of completed provenance work

| Claim | Verified result |
| --- | --- |
| MIT notice and dual copyright | The local `LICENSE` matches the shared upstream baseline with one added downstream copyright line. MIT requires the copyright **and permission notice** in copies or substantial portions. The original summary omitted the latter. Retain the full license in the installed archive and release bundle. [Local license](../LICENSE) · [Upstream license](https://github.com/yuting0624/antigravity-for-claude-code/blob/6f9b383f6a41b7bd0b97b9702ddd2902f3538fac/LICENSE) · [MIT terms](https://opensource.org/license/mit) |
| Repository pointers and author credit | The blueprint names the downstream repository and credits linyuting. Its former `author` and `upstream` entries were proposed fields and the installed-version legacy parser ignores them. The revised proposal retains attribution in `interface.longDescription` and `developerName` identifies the port maintainer. The draft policy links pointed at absent files. |
| Provenance guide and trailers | The guide records lineage, license, two remotes, and an upstream commit trailer. Its references to MIT “section 1” and `upstream/main` need correction. The sample `1615e6f` is already an ancestor of this branch and is a historical example. Git records Yuting Lin as the author. Preserve Git’s original author metadata and record a full upstream SHA. [Provenance guide](PROVENANCE.md) · [Original fix](https://github.com/yuting0624/antigravity-for-claude-code/commit/1615e6fb64776b2bd436e26fb74c101ee64417a5) |
| Troubleshooting and POC playbook | Both have attribution notices and historical upstream links. Troubleshooting points Codex users to the downstream tracker, but the troubleshooting commands are still largely Claude-specific. Label runtime scope when adding tested Codex instructions. [Troubleshooting](TROUBLESHOOTING.md) · [POC playbook](POC-PLAYBOOK.md) |
| Demo kit | Attribution exists and launch and measurement paths use `ANTIGRAVITY_PLUGIN_DIR`. Set it to an absolute path before the recipe changes directory. The shared build spec uses an outer three-backtick fence around a Python code fence, which breaks rendering after the embedded block. Give the outer fence four backticks. The experiment still launches Claude. [Demo kit](DEMO-KIT.md) |
| Migration guide | The upstream credit exists. Git history also shows substantive contributions by Vitor Amaral de Melo (`4ebe239`, `8c40ad8`, `0db8c5a`). Credit upstream contributors as well as linyuting. [Migration guide](MIGRATION.md) · [Example upstream contribution](https://github.com/yuting0624/antigravity-for-claude-code/pull/81) |
| A/B results | Attribution exists. Report the Claude-side proxy and shared gate with `n=1` per arm. The text claiming that adding Gemini cost increases the total-cost advantage has the sign reversed. Adding a positive cost to the hybrid arm reduces its measured savings relative to a fixed solo baseline. The total effect remains unmeasured. [Benchmark data](AB-RESULTS.md) |
| Historical issues | The provenance guide links all seven cited reports. The selected support guides resolve their cited issues. Bare references still appear in `CHANGELOG.md`, `commands/research.md`, and `skills/antigravity/SKILL.md`. Label and link inherited references where they are carried into Codex-facing material. Issues 11 and 15 concern `CLAUDE_PLUGIN_ROOT` in marketplace installs and injected model context, respectively. [Upstream #6](https://github.com/yuting0624/antigravity-for-claude-code/issues/6) · [#10](https://github.com/yuting0624/antigravity-for-claude-code/issues/10) · [#11](https://github.com/yuting0624/antigravity-for-claude-code/issues/11) · [#15](https://github.com/yuting0624/antigravity-for-claude-code/issues/15) · [#37](https://github.com/yuting0624/antigravity-for-claude-code/issues/37) · [#115](https://github.com/yuting0624/antigravity-for-claude-code/issues/115) · [#117](https://github.com/yuting0624/antigravity-for-claude-code/issues/117) |
| Git remotes | `origin` and `upstream` have the stated fetch and push URLs. The live upstream default is `master`. The checkout had no fetched `upstream/*` refs. Configuration alone does not establish a sync history. The downstream remote `main` still pointed at the shared baseline. The provenance commit was present on `origin/research/codex-agy-plugin`. |

### Upstream contribution boundary

Upstream synchronization is out of the current Codex workflow. Any future sync for upstream contributions belongs on the separate contribution branch once it exists. The existing `PROVENANCE.md` examples use `upstream/main`, but the original repository’s default branch is `master`.

For future contributions, follow the upstream maintainer’s guidelines. They ask for focused pull requests linked to the relevant issue, the stubbed test suite, ShellCheck, Bash 3.2 compatibility, and JSON checks when manifests change. Update the skill when behavior changes and follow the upstream changelog and version rules for the contribution. [Upstream contribution guidelines](https://github.com/yuting0624/antigravity-for-claude-code/blob/master/CONTRIBUTING.md)

### Validation record

- `codex --version` reported `0.170.0`. `agy --version` reported `1.5.11`. CLI help confirmed the marketplace and installation command syntax. The packaged wrappers exist. `agy-delegate` and `agy-doctor` did not resolve by bare name in the audit shell.
- A temporary Codex home registered the current checkout as `antigravity-for-claude-code`. Installing `antigravity@antigravity-for-codex` returned a plugin-not-found error. A separate fixture containing only `.codex-plugin/marketplace.json` failed discovery. With `.agents/plugins/marketplace.json` and a minimal Codex plugin manifest, registration and installation succeeded using `source.path: "./"`. The fixture cache contained the license, executable, and skill files.
- The exact Section 3 examples installed from a temporary archive of `HEAD` under `antigravity@antigravity-for-codex`. The cache contained the complete license, executable wrapper, and existing skill. The cached `bin/agy-delegate --help` worked from another directory. The app server’s `hooks/list` returned zero hooks with the explicit empty file. Omitting the manifest’s `hooks` field exposed the inherited `hooks/hooks.json` in the inventory.
- Plugin Eval ran against the checkout. It produced a generic repository analysis because the Codex plugin manifest was absent. The result does not validate a packaged plugin.
- `bash tests/run-tests.sh` reported 601 passed, zero failed, and one skipped. The skipped changelog check requires a pull request base. The suite uses a stub agy. `shellcheck --severity=error scripts/*.sh tests/*.sh hooks/*.sh` passed.
- Hook inventory was tested without executing hook commands or making authenticated model calls. Hook trust and execution, skill invocation, live retrieval, end-to-end compatibility, and release packaging remain unverified.

### Council review

The first round scored implementation readiness of the original blueprint. The second scored documentation quality after revision. The scores use different criteria.

| Delegate | Scope | Round 1 | Round 2 |
| --- | --- | --- | --- |
| GPT-6.2 Sol | Manifests, CLI installation, evaluator, and options | 4/10 | 8/10 |
| GPT-6.1 Terra | Hooks, wrappers, workflow, and pricing | 3/10 | 8/10 |
| GPT-6.1 Terra | License, attribution, benchmarks, and contribution workflow | 5/10 | 9/10 |

Round 2 identified the implicit hook fallback and the handoff prerequisites. The blueprint now specifies an explicit empty Codex hook file, a clean handoff baseline, and the write permissions for its delegation examples. The manifest delegate confirmed the hook fix on a focused third pass and scored its documentation 9/10. Upstream contribution guidance reflects the maintainer’s follow-up. The council skill describes four delegates and three providers. This harness ran the three enumerated delegates using OpenAI models.
