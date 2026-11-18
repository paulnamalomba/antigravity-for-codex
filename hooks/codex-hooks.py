"""Command hooks for the Codex plugin."""

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys


HOOKS = Path(__file__).resolve().parent
DELEGATE = HOOKS.parent / "bin" / "agy-delegate"
ROLE = "antigravity-delegate"
DISABLED = {"off", "false", "0", "no", "disabled"}
BULK_WORK = re.compile(
    r"\b(?:all files|every file|across the codebase|entire codebase|whole repo|"
    r"migrat(?:e|ion)|generate tests|test coverage|exhaustive tests?|scaffold(?:ing)?|"
    r"boilerplate|deep research|web search)\b|一括|全ファイル|すべてのファイル|網羅|移行|大量|横断|リポジトリ全体",
    re.IGNORECASE,
)
EXPLICIT_DELEGATION = re.compile(r"\b(?:antigravity|agy(?:-delegate|-job)?)\b", re.IGNORECASE)


def enabled(variable):
    return os.environ.get(variable, "").strip().lower() not in DISABLED


def context(event, message):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}}


def probe(executable, option):
    return subprocess.run(
        [executable, option], stdin=subprocess.DEVNULL, capture_output=True, timeout=2
    )


def startup_warning():
    agy = shutil.which("agy")
    if agy is None:
        return "[Antigravity] agy is missing from PATH. Run the Antigravity setup skill for help."
    try:
        if probe(agy, "--version").returncode == 0:
            return None
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "[Antigravity] agy --version failed or timed out. Run the Antigravity setup skill."


def session_start(payload):
    reply = {}
    if payload.get("source") == "startup":
        warning = startup_warning()
        if warning:
            reply["systemMessage"] = warning
    if enabled("AGY_CODEX_CODING_POLICY"):
        reply.update(context("SessionStart", (
            "[Antigravity] Codex plans, follows the user's authorization, and verifies results. Consider the "
            "installed Antigravity skills for bounded bulk work when their benefit justifies "
            "the handoff. Keep small tasks local. Limit what is sent to agy to the authorized "
            "scope and verify its claims, changes, and test results independently."
        )))
    return reply


def prompt_nudge(payload):
    prompt = payload.get("prompt")
    if (enabled("AGY_CODEX_DELEGATION_NUDGE") and isinstance(prompt, str)
            and BULK_WORK.search(prompt) and not EXPLICIT_DELEGATION.search(prompt)
            and shutil.which("agy")):
        return context("UserPromptSubmit", (
            "[Antigravity] This prompt may contain bulk work. Consider the installed "
            "Antigravity skills for a bounded, authorized portion if useful. Verify the result."
        ))
    return {}


def deny(reason):
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}


def delegate_guard(payload):
    if payload.get("agent_type") != ROLE:
        return {}
    if payload.get("tool_name") != "Bash":
        return deny("The Antigravity delegate role can only run the installed read-only wrapper.")
    tool_input = payload.get("tool_input")
    cwd = payload.get("cwd")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not isinstance(cwd, str) or not os.path.isdir(cwd):
        return deny("The Antigravity delegate role requires a local shell command and working directory.")
    try:
        args = shlex.split(command)
    except ValueError:
        args = []
    if (os.name != "posix" or args[:2] != [str(DELEGATE), "--read-only"]
            or command.strip() != " ".join(map(shlex.quote, args))):
        return deny("Use the installed agy-delegate path followed by --read-only and literal arguments.")
    if any(arg in {"--settings", "--yolo", "--mode", "--allow-slash-commands", "-", "-c",
                   "--continue", "--conversation"} for arg in args[2:]):
        return deny("The Antigravity delegate role requires a fresh read-only invocation.")

    # The shared parser checks the wrapper's flag grammar and confines directory
    # and schema-file arguments to the actual tool working directory.
    wrapper_input = {"cwd": cwd, "tool_input": {
        "command": " ".join(map(shlex.quote, ["agy-delegate", *args[1:]])),
    }}
    try:
        validation = subprocess.run(
            ["bash", str(HOOKS / "validate-delegate-bash.sh")],
            input=json.dumps(wrapper_input), text=True, capture_output=True, timeout=2,
        )
        agy = shutil.which("agy")
        if validation.returncode == 0 and agy:
            help_result = probe(agy, "--help")
            if help_result.returncode == 0 and b"--settings" in help_result.stdout + help_result.stderr:
                return {}
    except (OSError, subprocess.TimeoutExpired):
        pass
    return deny("Use supported read-only options and workspace paths. agy must support --settings.")


def subagent_start(payload):
    if payload.get("agent_type") != ROLE:
        return {}
    return context("SubagentStart", (
        "Use the exact installed wrapper for a bounded read-only task. Pass a literal prompt "
        "and literal options using POSIX shell quoting. Example: "
        f"{shlex.quote(str(DELEGATE))} --read-only --digest 'Analyze the requested scope'"
    ))


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(payload, dict) or not isinstance(payload.get("hook_event_name"), str):
        return
    handler = {
        "SessionStart": session_start,
        "UserPromptSubmit": prompt_nudge,
        "SubagentStart": subagent_start,
        "PreToolUse": delegate_guard,
    }.get(payload.get("hook_event_name"))
    if handler:
        reply = handler(payload)
        if reply:
            print(json.dumps(reply))


if __name__ == "__main__":
    main()
