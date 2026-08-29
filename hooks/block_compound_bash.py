#!/usr/bin/env python3
"""PreToolUse hook: hard-block compound Bash commands and inline heredocs.

Enforces two standing rules that advisory memory / CLAUDE.md could not, because
a session can read guidance and still ignore it. A PreToolUse hook is enforced
by the harness regardless of what any session decides:

  - one command per Bash call: no unquoted '&&', ';', or newline separators
    (rule: feedback_chain_bash_commands)
  - no inline script heredocs / heredoc commit bodies: no unquoted '<<'
    (rule: feedback_no_inline_script_heredocs)
  - no newline-then-'#' inside a quoted argument: a multiline `python -c "..."`
    blob with a '#' comment line can hide arguments from path validation, so the
    harness never auto-approves it -- it prompts every time
    (rule: feedback_no_inline_script_heredocs)

The rationale: single, simple commands auto-approve; compound commands, heredoc
bodies, and commented multiline blobs do not. Blocking them here forces the
split/Write-a-file pattern so each run auto-approves.

The scan is quote- and escape-aware so operators inside '...'/"..." or after a
backslash are ignored -- this avoids false positives on URLs, echo strings,
line continuations, and `find ... -exec ... \\;`. The newline-then-'#' check is
the exception: it fires ONLY inside quotes, because that is the shape the
harness's path-validation heuristic refuses to auto-approve.
"""
import json
import sys


def _newline_then_hash(cmd, i, n):
    """True if cmd[i] is a newline followed (past blanks) by '#'.

    This is the shape the harness's path-validation heuristic refuses to
    auto-approve: a comment line inside a quoted multiline argument.
    """
    if cmd[i] not in ("\n", "\r"):
        return False
    j = i + 1
    while j < n and cmd[j] in (" ", "\t", "\n", "\r"):
        j += 1
    return j < n and cmd[j] == "#"


def scan(cmd):
    """Return a violation code for the first unquoted operator found, else None.

    Codes: 'heredoc', 'compound_and', 'compound_semicolon', 'compound_newline',
    'quoted_comment' (newline-then-'#' inside a quoted argument).
    """
    in_single = False
    in_double = False
    escaped = False
    i = 0
    n = len(cmd)
    while i < n:
        c = cmd[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if in_single:
            # single quotes are fully literal in bash -- no escaping
            if _newline_then_hash(cmd, i, n):
                return "quoted_comment"
            if c == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            if _newline_then_hash(cmd, i, n):
                return "quoted_comment"
            if c == "\\":
                escaped = True
            elif c == '"':
                in_double = False
            i += 1
            continue
        # unquoted context
        if c == "\\":
            escaped = True  # handles line continuation (backslash-newline) too
            i += 1
            continue
        if c == "'":
            in_single = True
            i += 1
            continue
        if c == '"':
            in_double = True
            i += 1
            continue
        if c == "<" and i + 1 < n and cmd[i + 1] == "<":
            return "heredoc"
        if c == "&" and i + 1 < n and cmd[i + 1] == "&":
            return "compound_and"
        if c == ";":
            return "compound_semicolon"
        if c in ("\n", "\r"):
            return "compound_newline"
        i += 1
    return None


def reason_for(code):
    if code == "heredoc":
        return (
            "Blocked: heredoc (<<) in a Bash command. Do not run inline script "
            "heredocs or heredoc commit bodies -- they cannot auto-approve. "
            "Write a /tmp/*.py (or /tmp/*.txt) file with the Write tool and run "
            "that file instead. (rule: feedback_no_inline_script_heredocs)"
        )
    if code == "quoted_comment":
        return (
            "Blocked: newline followed by '#' inside a quoted argument (a "
            "multiline `-c \"...\"` blob with a comment line). This shape hides "
            "arguments from path validation, so it never auto-approves and "
            "prompts every time. Write a /tmp/*.py file with the Write tool and "
            "run that file instead. (rule: feedback_no_inline_script_heredocs)"
        )
    op = {
        "compound_and": "&&",
        "compound_semicolon": ";",
        "compound_newline": "a newline separator",
    }[code]
    return (
        f"Blocked: compound Bash command (found {op}). Run ONE command per Bash "
        "call so each auto-approves -- split this into separate tool calls. "
        "(rule: feedback_chain_bash_commands)"
    )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return  # unparseable input -> do not block
    if data.get("tool_name") != "Bash":
        return
    cmd = (data.get("tool_input") or {}).get("command")
    if not isinstance(cmd, str) or not cmd.strip():
        return
    code = scan(cmd)
    if not code:
        return
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason_for(code),
                }
            }
        )
    )


if __name__ == "__main__":
    main()
