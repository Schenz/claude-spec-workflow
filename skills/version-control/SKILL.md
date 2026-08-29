---
name: version-control
description: Proactively advise when to pull from the base branch or commit during a task, stage the right files, write concise commit messages, and push. Use this skill frequently.
---

# Version Control

Proactively advise on pulling from the base branch, and on commit timing throughout a task.
Handle the full commit-and-push workflow when the user agrees.

**Read `.claude/workflow-config.md`** for the base branch and the test command.

## Advising When To Pull

When the user is working on a branch, check whether the base branch has new commits. If so,
advise pulling and rebasing before continuing.

```
git fetch origin <base>
git log HEAD..origin/<base> --oneline
```

If the user agrees, ask whether to rebase or merge, then run the appropriate command:

```
git pull --rebase origin <base>
```
```
git merge origin/<base>
```

If the user declines, continue — but remind them to pull before merging the branch.

**One case where pulling is not optional:** if the work involves a knowledge-base trap sweep,
the base branch must be merged first. A sweep on a branch that is behind reports full coverage
of an incomplete base, with no other signal.

## Advising When To Commit

As work progresses, suggest a commit whenever a **logical unit** is complete. A logical unit is
one of:

- A single bug fix — the minimal set of changes that resolves it.
- A comment or TODO added or removed that stands alone, e.g. a one-line note explaining an
  edge case.
- A new feature or endpoint wired up.
- A self-contained refactor.
- A batch of related test additions or updates.
- A configuration or dependency change.

**More frequent commits is better.** A large commit is a large revert.

When suggesting one, briefly state **what** would go in and **why this is a good boundary**:

> Good point to commit: the new router and its service function are wired up and tests pass.
> Want me to commit and push this now?

## Performing The Commit And Push

### 1. Review the working tree

```
git status
git diff --stat
```

Identify which files belong to the current logical unit.

Run the config's unit-test command. If tests fail, suggest fixing them before committing —
but proceed if the user insists. Say clearly in your response that the commit went in with
failing tests.

### 2. Stage explicitly

Use `git add <file> ...` with explicit paths. **Only stage files belonging to this commit's
logical unit.** If unrelated changes are present, mention them and leave them unstaged.

Never `git add -A` on a tree you have not just reviewed.

### 3. Write the message

Imperative mood, 72 characters maximum on the subject line.

Good:
- `Add profile ownership check to prompt update endpoint`
- `Fix 404 when fetching archived modules`
- `Rename service func to match router semantics`

When the work is task-driven, use the traceability format the task chain expects:

```
Task <ID>: <Short Description> (Plan <ItemId> → Guide → Task <ID>)
```

### 4. Commit

Pass the message with `-m`. Do not use a heredoc for the body — many harness configurations
refuse to auto-approve heredoc commands, and a multi-line body is rarely what makes a commit
reviewable anyway.

```
git commit -m "message here"
```

### 5. Push

```
git push
```

If the branch has no upstream, ask before setting one:

```
git push --set-upstream origin <branch-name>
```

### 6. Confirm

Report the commit hash.

## Rules

- **Warn before committing anything that may contain secrets** — `.env`, credential files,
  tokens, connection strings. Some may be deliberate dummies; check with the user rather than
  assuming either way.
- **Never commit generated or vendored output** the repo ignores, and never commit anything
  from the spec folder or the scratch directory.
- **Do not amend previous commits** unless the user explicitly asks. Create new commits.
- **Do not force-push** unless the user explicitly asks and confirms.
- **Never commit directly to the base branch.** If the current branch *is* the base, stop and
  ask.
