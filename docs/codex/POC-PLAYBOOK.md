# PoC playbook — Codex with Antigravity delegation

> **Codex adaptation:** The [historical Claude document](../claude/POC-PLAYBOOK.md) is retained separately.

This playbook adapts [linyuting’s upstream Claude Code methodology](https://github.com/yuting0624/antigravity-for-claude-code) to Codex. The [archived A/B results](AB-RESULTS.md) are Claude measurements, not evidence of Codex savings. Historical issues such as [#10](https://github.com/yuting0624/antigravity-for-claude-code/issues/10) and [#37](https://github.com/yuting0624/antigravity-for-claude-code/issues/37) belong to that upstream project.

## 1. Define the question and quality gate

Choose a representative task and a machine-checkable gate before running either arm: for example, tests, lint and type checks in a clean environment. Codex owns the result and independently inspects the diff and runs the same gate for both arms; an agy self-report is not a pass. The upstream experiment caught an executor modifying its environment to force a green check.

Use isolated copies of the same starting commit, identical `AGENTS.md`, dependencies, data, permissions, conductor model and configuration. Randomize arm order, use at least three independent trials per arm, retain failures, and report individual results and ranges. Match wall-clock and spending caps. Record cache conditions and run order; do not assume a universal five-minute cache TTL for Codex. A coding task may require the conductor to reread the work to own correctness. A digest-only research or log-analysis deliverable may have different economics; measure each regime rather than generalizing.

## 2. Install and prepare Codex

From a trusted checkout of this repository, with Codex and agy already installed and authenticated:

```bash
codex plugin marketplace add --json .
codex plugin add --json antigravity@antigravity-for-codex
```

Start a new Codex session; use `/hooks` to review and trust the plugin hooks when prompted. Select `antigravity:antigravity-setup` for diagnostics and `antigravity:antigravity` for delegation. The manifest exposes skills and hooks, not Claude slash commands. The skills resolve the installed plugin root from their own absolute `SKILL.md` path; do not assume a bare `agy-delegate` is on `PATH`. Reinstall after plugin edits. See [README](../../README.md) and the [Codex delegation skill](../../codex/skills/antigravity/SKILL.md).

Run the setup skill before measuring, record `codex --version`, `agy --version`, plugin version, selected models and available permissions, and check that agy is usable. Share only task data authorized for the external executor. For read-only work check that `agy --help` advertises `--settings`; the wrapper cannot enforce its read-only settings without it.

The hooks add advisory guidance at startup/compaction and prompt submission. The guard applies to the optional `antigravity-delegate` role, not all Codex commands. Hook trust and Codex sandbox policy are separate from agy permissions; installation alone does not ensure delegation or grant writes.

## 3. Run matched arms

Use the same installed plugin and trusted hook state in both arms. Pin the same Codex model and configuration, same prompt, task, starting state and gate. Add only the arm instruction:

- **Solo:** “Complete this task yourself. Do not invoke agy or delegate.”
- **Hybrid:** “Use the `antigravity:antigravity` skill to delegate the bounded bulk portion to agy. Keep architecture, review and the quality gate in Codex. Verify the executor's result.”

The skill invocation and explicit direction are the experimental treatment; keep both prompts and all configuration in the trial record. If the hybrid performs no delegation, label it noncompliant rather than treating it as a hybrid result. If the solo delegates, label it noncompliant too. Do not change model, effort, permissions, tools or caps between arms. Select the same authorized sandbox for both (the example below uses `workspace-write`); do not bypass approvals or hook trust merely to make an arm pass.

For each fresh trial prepare `TASK_FILE` with the common task and chosen arm instruction, `TRIAL_REPO` as its isolated Git checkout, `RUN_DIR` as a unique precreated absolute log directory outside the trial checkout, and `CODEX_MODEL` as the same available model for both arms. Using Codex CLI 0.170.0:

```bash
mkdir -p "$RUN_DIR/executor"
AGY_USAGE_LOG="$RUN_DIR/executor/agy-usage.log" codex exec --json \
  --model "$CODEX_MODEL" --sandbox workspace-write --cd "$TRIAL_REPO" --add-dir "$RUN_DIR/executor" \
  - < "$TASK_FILE" > "$RUN_DIR/codex-events.jsonl" 2> "$RUN_DIR/codex-stderr.log"
```

`--add-dir` grants the sandbox access only to the executor telemetry subdirectory for both arms. The invoking shell captures Codex events and stderr in its parent, outside that additional writable directory. Keep the logs out of the Git checkout so they do not alter the diff. Confirm your platform applies the requested sandbox and that the directory is writable. Record start/end time and exit status separately, and preserve the task, diff, gate output and logs. Do not put credentials or sensitive material in shared trial artifacts. Ensure the environment passes `AGY_USAGE_LOG` to the wrapper; check the log actually contains an `AGY_USAGE` line for each completed delegation. The wrapper appends, so use a fresh log per trial. It emits `AGY_USAGE` and `AGY_SIGNAL` on stderr too; plain-text fallback, failures, or unfinished steps can leave usage missing or incomplete. Missing is **unknown**, not zero.

For a bounded read-only delegation, the installed skill uses `--read-only --dir <repo> --digest` after checking `--settings`. For authorized edits on agy 1.5.7+, `--mode accept-edits` permits in-workspace file writes, not shell commands. An appropriately scoped `permissions.allow` rule is another option. `--yolo` broadly approves tools and is only appropriate with explicit authorization and suitable isolation; `--sandbox` is not a reliable containment boundary under it. Never silently escalate after a denial. Exit 15 is a denial; exit 12 is a timeout and can include partial output. Inspect the diff and gate independently. See [troubleshooting](TROUBLESHOOTING.md).

For headless trials keep the delegation attached and wait for completion before Codex exits, or explicitly start, inspect and collect an `antigravity:antigravity-jobs` job while the session remains alive. A background start alone is not a completed delegation. Do not assume a Claude-specific shell timeout applies to Codex.

## 4. Read and price the evidence

`codex exec --json` writes JSONL events, including `thread.started`, `turn.completed`, `turn.failed` and possibly `error`; inspect the full stream and process exit status. The following prints the thread ID and completed usage, without substituting zeros for missing fields:

```bash
python3 - "$RUN_DIR/codex-events.jsonl" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as stream:
    for line in stream:
        event = json.loads(line)
        if event.get("type") == "thread.started":
            print("thread_id:", event.get("thread_id"))
        elif event.get("type") in ("turn.completed", "turn.failed", "error"):
            print(json.dumps(event, ensure_ascii=False))
PY
```

Inspect `turn.completed.usage` for the fields actually returned, normally `input_tokens`, `cached_input_tokens` and `output_tokens`; 0.170.0 also defines cache-write and reasoning-output fields. Record raw fields and their semantics, and reconcile with provider billing; do not add a reasoning subset to output again. The 0.170.0 [event processor](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/exec/src/event_processor_with_jsonl_output.rs) defaults usage to zero when it has no usage data, so a zero-filled event alone does not establish zero cost. Cached input is part of input, not an extra input charge. For a resumed thread, verify whether reported totals are cumulative before summing; never add cumulative snapshots together. A completed turn is not itself proof that the quality gate passed. The [Codex event definitions](https://github.com/openai/codex/blob/rust-v0.170.0/codex-rs/exec/src/exec_events.rs) document the 0.170.0 format; preserve the raw events because versions may differ.

Price Codex usage using the actual model, provider, billing arrangement and current rates, if a meaningful marginal cost is available. Do not apply the archived Claude weighted proxy or `scripts/measure-session.py` to Codex: that script reads Claude transcripts. On the agy side, inspect every `AGY_USAGE` record for model, tier and `usage` counters and apply the actual executor rates separately. The wrapper's existing accounting treats `thinking` as included in output and agy's `cache_read` as separate from `input + output`; verify this against the actual provider and version before pricing. If reported counts are incomplete or inconsistent, report uncertainty rather than a precise total. Do not mistake an estimate for a bill.

Report per trial: task/arm and starting commit; conductor and executor model, versions and configuration; delegation count; raw Codex and agy usage; gate result; elapsed time; rates and date; exclusions; and failures. Where total spend is measurable, use **cost per correct result** = all trial spend ÷ number of passes, with failures included in spend. If there are no passes, report it as undefined. Include a range and an observed break-even curve only where the sample supports one.

## 5. Interpret and roll out

Upstream saw a small weather task at approximately 1.0M solo vs 1.4M hybrid Claude-side weighted units, and a larger task with a lower hybrid Claude-side proxy; Gemini cost was excluded and the larger experiment had one run per arm. Upstream also reported a 62k-token corpus reduced to a 4.4k-token digest, with estimated carry costs of $0.002 vs $0.031 per subsequent turn and $0.53 vs $2.05 over 50 turns; those estimates depend on its rates and assumptions. It observed 1.3–1.9× latency for a single delegation, and a corpus-specific inversion around 5.7 calls. These are historical observations, not Codex predictions or universal thresholds. See [AB-RESULTS.md](AB-RESULTS.md) for the original figures and limitations.

If the matched Codex trials show parity, report parity. Other questions worth testing include whether a digest fits a context limit, whether independent scans improve recall, and whether parallel work changes wall-clock time. Keep Codex responsible for verification. An `AGENTS.md` instruction and plugin hooks are advisory; enforce organization-wide spend limits through the actual provider or gateway controls available to you. On Windows, consult the [upstream headless issue](https://github.com/google-antigravity/antigravity-cli/issues/508) and test your environment; WSL2 may be needed.

A report can say: “On {task}, {passes}/{trials} hybrid and {passes}/{trials} solo passed {gate}. Total measured cost per pass was {amounts}, including {cost components}; {missing components} were unavailable. Codex {version/model}, agy {version/model}, plugin {version}; rates dated {date}; range and elapsed times {values}.” Do not claim savings if either side cannot be priced.
