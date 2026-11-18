"""Exercise the Codex hook wire format and scoped guard offline."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


root = Path(__file__).resolve().parents[1]
hook = root / "hooks" / "codex-hooks.py"

with tempfile.TemporaryDirectory() as directory:
    scratch = Path(directory)
    agy = scratch / "agy"
    agy.write_text('#!/bin/sh\ncase "$1" in --help) echo --settings ;; --version) echo 1.5.11 ;; esac\n')
    agy.chmod(0o755)
    env = dict(os.environ, PATH=f"{scratch}{os.pathsep}/usr/bin{os.pathsep}/bin")
    env.pop("AGY_CODEX_CODING_POLICY", None)
    env.pop("AGY_CODEX_DELEGATION_NUDGE", None)

    def run(event, overrides=None, **fields):
        result = subprocess.run(
            [sys.executable, str(hook)],
            input=json.dumps(dict(hook_event_name=event, **fields)),
            text=True, capture_output=True, check=True, cwd=scratch,
            env=dict(env, **(overrides or {})), timeout=8,
        )
        assert not result.stderr, result.stderr
        return json.loads(result.stdout or "{}")

    for source in ("startup", "compact"):
        assert "Codex plans" in run("SessionStart", source=source)["hookSpecificOutput"]["additionalContext"]
    assert not run("SessionStart", {"AGY_CODEX_CODING_POLICY": "off"}, source="compact")
    assert "missing from PATH" in run("SessionStart", {"PATH": ""}, source="startup")["systemMessage"]
    for prompt in ("Generate tests across the codebase. Secret test marker.", "リポジトリ全体のテスト"):
        reply = run("UserPromptSubmit", prompt=prompt)["hookSpecificOutput"]
        assert reply["hookEventName"] == "UserPromptSubmit"
        assert prompt not in reply["additionalContext"]
    assert not run("UserPromptSubmit", prompt="Fix a typo", cwd="/whole repo")
    assert not run("UserPromptSubmit", prompt="Use Antigravity to generate tests")
    assert not run("UserPromptSubmit", {"AGY_CODEX_DELEGATION_NUDGE": "0"}, prompt="Generate tests")
    assert not run("UserPromptSubmit", prompt=["generate tests"])
    assert not run(["invalid"])

    role = "antigravity-delegate"
    delegate = shlex.quote(str(root / "bin" / "agy-delegate"))
    command = f"{delegate} --read-only --dir . --digest 'Review module changes'"
    assert delegate in run("SubagentStart", agent_type=role)["hookSpecificOutput"]["additionalContext"]
    fields = {"cwd": str(scratch), "tool_name": "Bash"}
    assert not run("PreToolUse", **fields, tool_input={"command": "git status"})
    assert not run("PreToolUse", **fields, agent_type="reviewer", tool_input={"command": "git status"})
    assert not run("PreToolUse", **fields, agent_type=role, tool_input={"command": command})

    for blocked in (
        "git status", f"agy-delegate --read-only 'Review module changes'",
        command + " && pwd", command.replace("--read-only", "--yolo"),
        command.replace("--dir .", "--dir .."), command.replace("--dir .", "--settings '{}'"),
        command.replace("--dir .", "--mode auto"), command.replace("--dir .", "--conversation old"),
    ):
        reply = run("PreToolUse", **fields, agent_type=role, tool_input={"command": blocked})
        assert reply["hookSpecificOutput"]["permissionDecision"] == "deny", blocked
    assert run("PreToolUse", cwd=str(scratch), tool_name="apply_patch", agent_type=role,
               tool_input={})["hookSpecificOutput"]["permissionDecision"] == "deny"

    agy.write_text("#!/bin/sh\necho usage\n")
    assert run("PreToolUse", **fields, agent_type=role,
               tool_input={"command": command})["hookSpecificOutput"]["permissionDecision"] == "deny"
