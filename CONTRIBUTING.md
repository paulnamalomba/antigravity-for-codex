# Contributing to the Codex port

This repository is a downstream port of [antigravity-for-claude-code](https://github.com/yuting0624/antigravity-for-claude-code). Please report port-specific problems in the [downstream issue tracker](https://github.com/paulnamalomba/antigravity-for-codex/issues), with the relevant client and `agy` versions, platform, reproduction, and sanitized diagnostics.

For local Codex development, follow the [README](README.md) and [implementation notes](docs/codex/CODEX-PLUGIN-MIGRATION-IMPLEMENTATION.md). The repo marketplace and dedicated Codex skills are separate from the inherited Claude commands and hooks. Live delegation requires an installed and authenticated `agy`; the offline suite uses stubs:

```bash
bash tests/run-tests.sh
shellcheck --severity=error scripts/*.sh tests/*.sh hooks/*.sh
```

Target macOS system Bash 3.2 and BSD userland as well as Linux; avoid Bash 4-only constructs and GNU-only flags. Exercise new scripts and behavioral changes with meaningful tests, including failure paths, and include new scripts in the relevant test and lint commands. The CI workflow runs the suite on Ubuntu and macOS with system Bash 3.2. Validate changed JSON manifests and report which checks actually ran.

Keep behavior and documentation aligned. The Codex compatibility manifest has its own version and installation context; do not present inherited Claude release entries as Codex releases. For Claude-specific release conventions, consult the upstream guide linked below; coordinate any downstream version changes with their own validation. Pricing examples must use verifiable inputs and distinguish estimates from measured usage. Preserve the notices in [LICENSE](LICENSE) in copies or substantial portions of the software.

Contributing to the original Claude project is a separate activity. Its [contribution guide](https://github.com/yuting0624/antigravity-for-claude-code/blob/master/CONTRIBUTING.md) sets out upstream setup, test, changelog/version and pull-request expectations; it uses upstream `master`, while the downstream port uses `main`. Prepare any future upstream contribution on its own branch and preserve attribution and source evidence. This guide does not prescribe upstream synchronization or remote changes.
