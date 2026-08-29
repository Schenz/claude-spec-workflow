---
name: pre-pr-review
description: Systematically verify an implemented work item against its spec, run validation, and write a structured review to PRE_PR_REVIEW.md in the item's spec folder. Use before opening a PR, or when the user asks for a pre-PR review.
---

# Pre-PR Review

Perform a pre-PR code review. `$ARGUMENTS` may name the branch and the concern areas, e.g.
`feature/1234, bugs, performance, security, testing`. When omitted, use the current branch
and review all standard concern areas.

The workflow is systematic and produces an actionable, evidence-backed deliverable — not a
narrative impression of the diff.

**Read `.claude/workflow-config.md` first** for the base branch, spec folder, commands,
definition-of-done rules, decision surfaces, cross-repo contracts and observability notes.

## Instructions

1. **Establish the spec context before reviewing any code.**
   - Resolve the item id from the branch using the config's branch-name shapes. Ask the user
     if it cannot be resolved.
   - Load `PLAN.md`, `IMPLEMENTATION_GUIDE.md`, `TASKS.md` and any existing
     `PRE_PR_REVIEW.md` from the item's spec folder.
   - Extract the work item, acceptance criteria, explicit scope boundaries and task-level
     verification expectations.

   Reviewing the diff before reading the spec produces a review of the code that was
   written, not of the item that was asked for.

2. **Compare the branch against the base branch.**
   - **Resolve the base rather than assuming it.** `git symbolic-ref
     refs/remotes/origin/HEAD` is unreliable — it can point at an abandoned branch. Compare
     the tips of the plausible bases by commit date, take the most recent, and **state which
     base you used** so a wrong guess is visible immediately. Confirm with the user if the
     candidates differ by less than a day.
   - Get the branch overview: commits, files changed, scope.
   - Review the diff for new, changed and removed code.
   - **Inspect the implementation files that satisfy each acceptance criterion**, not just
     the spec documents.
   - Categorize findings: **MUST-FIX**, **SHOULD-FIX**, **TESTING**, **DOCUMENTATION**.
   - Assess overall risk: **LOW / MEDIUM / HIGH**.

3. **Build a Story Verification Matrix** mapping every acceptance criterion to:
   - the relevant code paths, as markdown links
   - the validating test, command or other executable evidence
   - a status: `VERIFIED`, `PARTIALLY VERIFIED`, `NOT VERIFIED`, `NOT IMPLEMENTED`
   - any gap or risk preventing full confidence

4. **Run focused validation** for the touched behavior whenever the environment allows.
   Narrowest relevant checks first, using the config's commands:
   - Unit tests for the changed modules
   - The lint/format check, scoped to changed paths if the config records a lint backlog
   - Schema or spec validation when a definition changed
   - Targeted integration or E2E tests **only when the change requires them**, noting their
     cost
   - Invoke tooling through the repo's documented entrypoint

   **Where no automated check exists for an acceptance criterion, say so explicitly** and
   state what manual verification remains. **Never mark a criterion `VERIFIED` from spec
   documents or a code skim when executable evidence is feasible.**

   Two things that make a green result meaningless, both worth checking for:
   - **A suite that collected zero tests exits successfully.** Assert a collected count
     after any rename, move or branch switch.
   - **A guard nothing exercises is untested.** If the diff adds a guard, confirm a test
     would fail without it.

5. **Run a known-trap sweep.** Invoke `recall --paths <changed paths> --type trap` and check
   the diff against each article returned.
   - **A reintroduced trap is a MUST-FIX, not a SHOULD-FIX** — it is a defect the team has
     already paid for once.
   - When an article names a *pattern* rather than a single site, sweep every changed file
     for the pattern, not only the file the article cites.
   - **State the number of articles the sweep actually covered.** If the branch is behind
     the base on `docs/knowledge/`, the sweep is silently partial — merge the base branch
     first, or say the coverage was incomplete.

6. **For each finding**, give actionable recommendations, code excerpts with file path and
   line range, and a rough effort estimate where useful.

7. **Build detailed tables** for Story Completion, Correctness, Security, Code Quality,
   Testing and Observability, each with status and detail.

   - **Observability deserves disproportionate attention** wherever the config records a
     telemetry contract — because failures in that area are usually silent, and a broken
     contract will not announce itself in tests.
   - Under **Code Quality**, flag any **spec references left in source**: comments,
     docstrings, test names or identifiers in changed files that cite a task id, item number,
     plan, guide or design-doc section. Raise each as a SHOULD-FIX. A comment stating the
     functional *why* without a citation is fine and must not be flagged.

8. **Get an independent pass.** Invoke `superpowers:requesting-code-review` for a fresh-eyes
   review alongside this workflow, and fold its findings in — noting where the two
   disagree rather than silently reconciling.

9. **Write the review** to `PRE_PR_REVIEW.md` in the item's spec folder. If the item id
   cannot be determined, ask the user for the correct location.

10. **If `PRE_PR_REVIEW.md` already exists**, append the new review with a timestamp and
    reviewer name rather than overwriting. The history of what a review missed is useful.

11. **End with an explicit conclusion:** `GOALS SATISFIED`, `GOALS PARTIALLY SATISFIED`, or
    `GOALS NOT YET SATISFIED` — justified by the verification matrix and the validation
    evidence, not by overall impression.

## Always-on Rules

- **State the base branch you compared against.**
- **State the article count the trap sweep covered.**
- **Executable evidence beats assertion.** Every `VERIFIED` needs a command and its output.
- **Prefer naming a symbol to citing a line number** in findings that will outlive the diff.
- Keep the review focused, structured and traceable.
