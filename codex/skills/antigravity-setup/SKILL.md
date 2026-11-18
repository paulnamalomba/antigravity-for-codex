---
name: antigravity-setup
description: Check Antigravity CLI installation, authentication, models, and plugin readiness when the user requests setup or diagnostics.
---

# Antigravity setup

Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Run `"$PLUGIN_ROOT/bin/agy-doctor" --codex` and summarize installation, model access, script readiness, Codex version and plugin registration, and configured project/region when available. Marketplace or plugin list failures may also mean Codex could not return valid JSON, rather than proving they are absent. The doctor may query agy and local configuration; it does not authenticate on the user's behalf. Give actionable steps for failures without claiming authentication succeeded merely because the binary exists. Wrapper options can be passed directly; do not invent Codex configuration tables or expect Claude plugin option injection.
