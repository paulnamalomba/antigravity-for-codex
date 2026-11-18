---
name: antigravity-migrate
description: Inspect or migrate an existing Claude Code setup to Antigravity CLI with a dry run and explicit authorization for changes.
---

# Migrate Claude Code settings to Antigravity

This migrates Claude Code settings to Antigravity; it does not migrate Codex settings. Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. First run `"$PLUGIN_ROOT/bin/agy-migrate"` with requested scope flags but without `--apply` or `--apply-permissions`; include `--uninstall` only when the user is considering reversal. Explain linked skills versus generated files, warnings, omissions, and any flags needed for optional units. Refer to `"$PLUGIN_ROOT/docs/codex/MIGRATION.md"` for the current workflow and historical compatibility reference.

Only apply after the user has reviewed the dry-run and authorized the changes. Permission translation may widen grants, so apply permissions only with specific authorization. Report backups and the printed reversal command; session history is not migrated. Uninstall also changes local settings: inspect its dry run and obtain authorization before applying it. Do not imply this migration is needed to install the Codex plugin.
