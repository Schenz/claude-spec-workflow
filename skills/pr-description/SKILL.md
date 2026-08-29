---
name: pr-description
description: Generate a concise, reviewer-friendly PR description for the current branch and save it to PR_DESCRIPTION.md in the item's spec folder. Use when the user is ready to open a PR or asks for a PR description.
---

# PR Description

Generate a PR description for the current branch. `$ARGUMENTS` may name the branch and,
optionally, the spec folder path.

**Read `.claude/workflow-config.md`** for the base branch, spec folder, commands and the
tracker's description length limit.

## Instructions

1. Detect the checked-out branch.

2. **Compute the diff against the base branch, resolving it rather than assuming.**
   `git symbolic-ref refs/remotes/origin/HEAD` is unreliable and can point at an abandoned
   branch. Compare the tips of the plausible bases by commit date, take the most recent, and
   **state which base you used.** Confirm with the user if the candidates differ by less than
   a day.

3. Read commit messages and file diffs to extract the **reviewer-relevant** changes — what
   behavior changed, not which files moved.

4. Produce a description that is concise and scannable. Target **800–1500 characters**, and
   never exceed the limit the config records for the tracker. A description a reviewer will
   not read is worse than a short one.

5. Write it to `PR_DESCRIPTION.md` in the item's spec folder. Resolve the item id from the
   branch using the config's branch-name shapes; ask the user if it cannot be determined.

6. In the **Testing** section, list the specific scenarios that were validated, drawing on
   the TESTING items in `PRE_PR_REVIEW.md` or `TASKS.md` when they exist. Prefer "what was
   run and what it showed" over "tests pass".

7. If `PR_DESCRIPTION.md` already exists, append the new description with a timestamp and
   author rather than overwriting.

8. When the branch is ready to merge, invoke `superpowers:finishing-a-development-branch` to
   coordinate the remaining branch-finishing steps.

## Output Format

No preface, no internal reasoning:

```
Title:
<one-line imperative summary>

Summary:
- <3-6 bullets describing functional changes users or systems will notice>
- <group by area; do not list many files>

Reviewer Notes:
- <important design decisions, trade-offs, edge cases>
- <breaking changes, migration notes, feature flags, config changes, dependency bumps>

Testing:
- <what was run and the key results>
- If unknown, write: "Not specified by author - please run: <recommended commands>"
```

## Always-on Rules

- **State the base branch you diffed against.**
- **Describe behavior, not file movement.** "Retries now defer on a busy renderer instead of
  failing the job" beats "updated conversion.py and 3 test files".
- **Name anything that changes how the thing is deployed or configured** — a flag, a new
  setting, a migration, a dependency bump. That is the part a reviewer cannot infer from the
  diff.
- **Keep formatting simple** — short bullets, no long paragraphs.
- Recommend commands from the config, invoked through the repo's documented entrypoint.
