---
name: antigravity-cloud-debug
description: Diagnose Cloud Run errors using the Antigravity log digest, with changes only when explicitly requested.
---

# Cloud Run diagnosis

Require a service name. Resolve project and region explicitly: if project is omitted, show the configured project from `gcloud config get-value project` and confirm the scope before reading logs. Use existing gcloud credentials; never request tokens. The log digest sends relevant logs to the external CLI, so respect the user's authorization and data scope.

Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Run `"$PLUGIN_ROOT/bin/cloud-debug" --service <name> [--project <id>] [--region <region>] [--since 1h] [--limit 200]`. Before running, verify `agy --help` advertises `--settings`, which the wrapper needs to apply read-only permissions. The engine reads logs and delegates the digest; `--severity` and `--tier` are also available. Exit 3 indicates logging permission denied, and exit 4 means gcloud is unavailable. Explain the digest, evidence, likely cause, proposed fix and verification; do not re-fetch raw logs unnecessarily.

Only implement a fix if the user requested `--apply` or otherwise explicitly authorized changes. Use a dedicated branch or worktree with a clean baseline; show the diff. Do not deploy or merge without authorization.
