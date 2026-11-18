# Demo kit — Codex and Antigravity on the SDLC agent build

> **Codex adaptation:** The [historical Claude document](../claude/DEMO-KIT.md) is retained separately.

This adapts the upstream Experiment B by [linyuting](https://github.com/yuting0624/antigravity-for-claude-code) to Codex. The [published results](AB-RESULTS.md) are one Claude run per arm, exclude Gemini cost, and do not measure Codex. No Codex results have been established here.

The original goal was an ADK SDLC Expert Agent that produces 要件定義 → 基本設計 → 詳細設計 with grounded specialists, evaluated and deployed to Agent Engine. The original specification is preserved in the [Claude demo kit](../claude/DEMO-KIT.md#1-the-shared-build-spec-identical-text-in-all-3-arms--fairness). The demo protocol here uses a **local, offline application gate** so the built application does not silently create cloud resources, authenticate, or call live search. The Codex conductor and agy executor still need their configured model-provider traffic. Treat a live ADK eval and deployment as a separately authorized experiment with its own cost and quality records.

## Prepare the comparison

1. Install Codex and agy, authenticate through your normal setup, then from a trusted checkout install the plugin:

   ```bash
   codex plugin marketplace add --json .
   codex plugin add --json antigravity@antigravity-for-codex
   ```

2. Start a new Codex session, review/trust its hooks with `/hooks` and run `antigravity:antigravity-setup`. Record versions, conductor and executor models, environment, hook trust and permissions. The plugin provides `codex/skills/` and hooks; it does not install Claude slash commands. Its skills find the installed wrapper from their own paths.
3. Prepare identical isolated Git workspaces at one commit. Put the same pinned dependencies, fixtures, `AGENTS.md`, and a **prewritten independent test suite and executable gate** in each. Freeze the gate outside the agent's editable scope or verify it has not changed. The suite should test the original requirements: three ordered stages and state handoffs; nonempty artifacts; underspecified input handled by questions or explicit assumptions; and a mocked search interaction with each specialist. A mocked Stripe fixture tests use of the fixture, not current API accuracy. Fix fixtures and environment for every arm.
4. Fix the same Codex model, configuration, sandbox, budget and wall-clock cap. Use the same plugin and hook state in both arms. Do not expose credentials or production data to the built application. Its tests must not make live search, cloud deployment or authentication calls. Allow the configured Codex and agy model-provider traffic required to run the trial; if sandbox or network policy blocks it, record the failure rather than changing only one arm. Grant the executor only the work needed and tell Codex what can be sent to it.

## Common task and matched arms

Save this task, with one of the arm instructions below, in each trial's `TASK_FILE`. The artifact and independently supplied gate are identical in both arms:

```text
Build a local Python ADK SDLC Expert Agent in this workspace. The root validates a feature
brief, runs a SequentialAgent and assembles the result. In order, requirements writes
output_key='requirements', basic_design reads requirements and writes 'basic_design',
and detailed_design reads both prior stages and writes 'detailed_design'. Each specialist
is designed to use google_search as its sole tool; isolate live calls behind an injectable
fixture for this offline trial. Handle an underspecified brief with a question or explicit
assumptions. Provide reproducible setup and a local entry point.

Run the supplied independent gate in a clean environment; inspect the result and report
its actual output and any limitations. Do not modify the gate or fixtures. The application and its tests must not make live search, cloud, authentication, or
deployment calls. Codex and agy may use their configured model-provider connections. Do not claim that the mock
proves freshness or a successful deployment.
```

- **Solo:** prepend “Complete this task yourself. Do not invoke agy or delegate.”
- **Hybrid:** prepend “Use the `antigravity:antigravity` skill to delegate the bounded bulk implementation to agy. Keep architecture, independent review and the quality gate in Codex. Verify the executor's result.”

This arm instruction is the treatment. Verify actual calls: a hybrid run with zero delegations, or a solo run that delegates, is noncompliant. The optional upstream comparison of high vs max effort is a separate experiment, not evidence for a delegation effect. Avoid changing the conductor model or configuration for the matched comparison.

For each trial set `TASK_FILE`, `TRIAL_REPO`, `RUN_DIR` and the same `CODEX_MODEL` to real paths/model. `RUN_DIR` must be a unique, precreated absolute directory outside the checkout and writable by the trial; `--add-dir` grants both arms write access only to its `executor` telemetry subdirectory. The invoking shell captures Codex events and stderr in the parent directory, and the logs remain outside the Git diff. Confirm your platform applies the requested sandbox. With Codex CLI 0.170.0:

```bash
mkdir -p "$RUN_DIR/executor"
AGY_USAGE_LOG="$RUN_DIR/executor/agy-usage.log" codex exec --json \
  --model "$CODEX_MODEL" --sandbox workspace-write --cd "$TRIAL_REPO" --add-dir "$RUN_DIR/executor" \
  - < "$TASK_FILE" > "$RUN_DIR/codex-events.jsonl" 2> "$RUN_DIR/codex-stderr.log"
```

Save start/end time, exit status, prompt, diff and gate output. Check that `AGY_USAGE_LOG` reaches the wrapper and contains every expected usage record; absent or partial records are unknown, not zero. Keep synchronous delegation attached until finished, or start and collect an `antigravity:antigravity-jobs` job while the session remains alive. A started background job alone is not evidence of completion. For writes, agy 1.5.7+ supports `--mode accept-edits` for in-workspace edits; it does not grant shell commands. Keep retries within the authorized scope. For denials and partial timeout results, see [wrapper diagnostics](TROUBLESHOOTING.md#wrapper-exit-codes). Review the diff and run the gate independently.

## Measure and report

Run at least three independent trials per arm in randomized order. Inspect `thread.started`, `turn.completed.usage`, failures and errors in each JSONL stream using the parser in the [PoC playbook](POC-PLAYBOOK.md#4-read-and-price-the-evidence). Record raw Codex input, cached input and output fields as returned and do not add cached input twice. Price Codex with the actual billing arrangement and rate, and separately price each `AGY_USAGE` record by its actual model and rates. Reconcile missing or incomplete data and state uncertainty. The Claude-only `scripts/measure-session.py` and the archived Claude weighted proxy do not measure Codex.

Report each trial's pass/fail, delegation count, wall time, Codex and executor usage, actual or estimated costs, rate date and exclusions. Report total cost per passing result only when both sides can be priced, counting spend on failures; report undefined if no trial passes. A shared gate establishes only that the measured checks passed, not equal quality on every dimension. Do not fill the historical results table with new runs; publish Codex trials separately with their environment and gate.
