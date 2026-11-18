# Codex A/B measurement

The recorded A/B experiment used Claude Code as the conductor and agy as the executor. In one upstream run per arm, the hybrid’s Claude-side cost proxy was about 27% below solo at high effort and 64% below solo at max effort. All three passed the same 3/3 evaluation gate. The proxy excludes Gemini costs. The archive contains the original tables and the small-task comparison. [Historical Claude results](../claude/AB-RESULTS.md)

## Collect Codex results

1. Install and verify the Codex plugin. Use the same conductor model, sandbox, starting commit, prompt, and independent quality gate in both arms. [Codex implementation and setup](CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md)
2. Run a solo arm with Codex and a hybrid arm that uses `antigravity:antigravity` for a bounded part of the same task. Confirm which executor calls occurred. Record noncompliance and failed trials alongside completed results. [Matched trials](POC-PLAYBOOK.md#3-run-matched-arms)
3. Keep the `codex exec --json` event stream and the executor’s `AGY_USAGE` log. Record the usage fields and actual model from each source. Treat missing telemetry as unknown. `scripts/measure-session.py` and the archived weighting formula are for Claude session records. [How to read and price the evidence](POC-PLAYBOOK.md#4-read-and-price-the-evidence)
4. Report the sample size, gate results, wall time, usage, pricing basis, and exclusions. Calculate cost per passing result when both sides can be priced. Include spend from failures. [Codex demo task](DEMO-KIT.md)

Codex benchmark results are pending. Preserve new runs with their own task, environment, and evidence.
