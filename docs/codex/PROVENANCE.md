# Provenance and attribution

This repository is a downstream Codex port maintained by [Paul Namalomba](https://github.com/paulnamalomba), based on [antigravity-for-claude-code](https://github.com/yuting0624/antigravity-for-claude-code) by [linyuting](https://github.com/yuting0624) and its contributors. The inherited history also credits Vitor Amaral de Melo for migration documentation and fixes (commits `4ebe239`, `0db8c5a`, and `8c40ad8`). The historical upstream base branch is `master`; this port's default branch is `main`. Branch names do not imply that a downstream change has been contributed upstream.

The root [LICENSE](../../LICENSE) preserves both copyright notices and the full MIT permission notice. Include the applicable copyright and permission notices in **all copies or substantial portions** of the software; attribution in a manifest or README alone does not replace that condition. The Codex manifest description credits the original project and port maintainer; legacy loader behavior should not be assumed to preserve arbitrary author or upstream metadata fields.

Inherited results and reports describe the original Claude Code project, its environments, and its contributors. See [AB-RESULTS.md](AB-RESULTS.md) for the limits of its Claude-side benchmark. No Codex performance or total-cost result is established by that experiment.

Historical references are to upstream issues: [#6](https://github.com/yuting0624/antigravity-for-claude-code/issues/6), [#10](https://github.com/yuting0624/antigravity-for-claude-code/issues/10), [#11](https://github.com/yuting0624/antigravity-for-claude-code/issues/11), [#15](https://github.com/yuting0624/antigravity-for-claude-code/issues/15), [#37](https://github.com/yuting0624/antigravity-for-claude-code/issues/37), [#115](https://github.com/yuting0624/antigravity-for-claude-code/issues/115), and [#117](https://github.com/yuting0624/antigravity-for-claude-code/issues/117). Report new port-specific problems in the [downstream issue tracker](https://github.com/paulnamalomba/antigravity-for-codex/issues).

Upstream contribution work belongs on a separate future branch. Preserve the original author metadata and record the full source commit ID when carrying forward upstream changes. The upstream guide covers development setup, tests, changelog and version conventions, and pull requests. [Upstream contribution guide](https://github.com/yuting0624/antigravity-for-claude-code/blob/master/CONTRIBUTING.md)

## Codex port scope

The current workflow installs `antigravity@antigravity-for-codex` from the repository's local marketplace, selects skills under the `antigravity:` namespace, and reviews hooks in Codex `/hooks`. The [installation instructions](../../README.md#install-locally) show registration, installation, and cache refresh; the [implementation notes](CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md) identify tested versions, hooks, role scope, and limitations. Use the absolute cached `installedPath` from the install response to run `bin/agy-doctor --codex` directly. The shared `agy-migrate` tool imports Claude Code configuration only; the [migration guide](MIGRATION.md) distinguishes that inherited reference from manual Codex-to-agy interoperability.

Upstream sync is deferred and is not a step in installing or operating the Codex port. The historical upstream guide linked above remains attribution and reference material.

The [archived Claude provenance document](../claude/PROVENANCE.md) preserves the original source and historical upstream-sync guidance.
