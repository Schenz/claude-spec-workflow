---
name: address-comments
description: Address PR comments on the current branch one at a time — fix, test, commit, repeat. Use when the user pastes a reviewer comment or asks to work through PR feedback.
---

# Address PR Comments

Your job is to address **a single comment** on a pull request, then move to the next. One
comment, one fix, one commit.

**Read `.claude/workflow-config.md`** for the test and lint commands and the test layout.

## When To Address, And When To Push Back

Reviewers are usually right, but not always.

- If a comment does not make sense, **ask for clarification** rather than guessing at intent.
- If you do not agree the change improves the code, **push back and explain why.** Do not
  silently apply something you believe is wrong — a change made without conviction is a
  change nobody will defend later.

Invoke `superpowers:receiving-code-review` to triage the comment before implementing. It
exists to prevent both failure modes: performative agreement, and dismissing a valid point
because it was phrased bluntly.

If the comment points at a bug or unexpected behavior, invoke
`superpowers:systematic-debugging` — reproduce, isolate the root cause, then fix. Do not
patch at the symptom the reviewer happened to notice.

## Addressing The Comment

- **Address only the comment provided.** No unrelated changes, no opportunistic refactors.
- **Keep the change as small as possible.** Less is more.
- **If the same issue exists in several places within the changed code, fix all of them** —
  not only the instance called out. A reviewer who finds one instance is reporting a class.
- **Add or update test coverage** whenever the change affects runtime behavior and tests do
  not already cover it. Tests go in the location the config names.
- **No spec references in source.** Never add a comment, docstring, test name or identifier
  citing a PR comment, task id, item number, plan, guide or design-doc section. That
  provenance belongs in the commit message. Explaining *why* the code behaves as it does is
  welcome — write the reason itself, without the citation. If the file already carries such
  references, drop the citation from lines you touch; do not sweep beyond the comment's
  scope.

## After Fixing

### Run the relevant checks

Use the config's commands, invoked through the repo's documented entrypoint:

- Targeted unit tests for the changed module
- The lint/format check
- Schema or spec validation when a definition changed

If you do not know which tests cover the change, **ask the user** rather than running the
full suite and calling it proof.

### Provide proof

Record how the fix was verified — the test that now covers it, the trimmed command output,
or a brief description of manual verification where no automated check applies. Update the
item's review document if one exists.

### Commit

One commit per comment, with a message naming the area addressed:

```
Address review: tighten terminal status retry semantics
```

One comment per commit keeps the audit trail clean and makes any single fix revertable on
its own.

### Move on

Move to the next comment, or ask the user for it.

## Always-on Rules

- **One comment at a time.** Working through several at once produces a commit nobody can
  review and a revert nobody can scope.
- **Never mark a comment addressed without verification.**
- **A pushback is a valid outcome.** Record the reasoning where the reviewer will see it.
