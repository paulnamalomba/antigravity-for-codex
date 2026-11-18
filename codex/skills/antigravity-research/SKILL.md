---
name: antigravity-research
description: Conduct sourced research with Antigravity as a worker, checking citations and claims independently. Use when the user requests Antigravity research.
---

# Research with Antigravity

Codex plans, verifies, and synthesizes; agy is an external research worker. Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Execute `"$PLUGIN_ROOT/bin/agy-delegate"`, not a bare command or a path relative to the working directory.

Before delegation, verify that `agy --help` advertises `--settings`; without it, the wrapper cannot apply its read-only settings. If unavailable, use another authorized tool or report the limitation. Break the question into focused subquestions. The wrapper settings `--tier` and `--timeout` belong before the prompt; default to `--tier flash --timeout 15m` for searches, and `--tier pro --timeout 10m` for verification unless the user selects otherwise. Example:

```sh
"$PLUGIN_ROOT/bin/agy-delegate" --read-only --allow-url --tier flash --timeout 15m --digest 'Research <subquestion>. Return findings with exact source URLs and publication dates.'
```

`--read-only --allow-url` configures permissions for reading known URLs; it does not guarantee that search tools are available or approved. If web search is unavailable or denied, report that limitation and use another authorized search tool if available. Never fall back to `--yolo` merely to make search or URL access work. On timeout (exit 12), assess any partial output, narrow the query or retry with a longer timeout; on permission denial (exit 15), report the denied action.

Open sources independently where possible. Ask agy to check a specific URL for a claim when useful, but verify load-bearing claims against the actual sources, preferably independent primary sources. Check dates and whether the cited page supports the claim; domain-only citations and model recollections are not evidence. Clearly label unverified claims and synthesize with direct links. Respect user constraints on browsing and source use.
