---
name: execute-task-checklist
description: Execute TASKS.md items in the project's spec folder in strict order, with evidence, verification, checklist updates and auditable commits. Use when the user is ready to start delivering tasks for a work item.
model: sonnet
---

# Execute Task Checklist

Execute `TASKS.md` items. `$ARGUMENTS` should be the path to the tasks file and the task or
task group to execute, e.g. `specs/1234/TASKS.md T2`. When omitted, default to the current
item's spec folder.

**Read `.claude/workflow-config.md` first** for the commands, test layout, lint baseline and
definition-of-done rules.

## Model

This skill declares `model: sonnet`, overriding the session model for its turn only; the
session model resumes afterwards.

The reasoning: task execution here is well-scoped and prescriptive — each task arrives with
explicit acceptance criteria, verification steps, rollback and traceability already decided —
so a capable mid-tier model is the right cost and latency fit. The expensive thinking
happened at the planning rungs.

Override it when a specific task is genuinely hard (non-trivial algorithm design, a subtle
concurrency question): the user can select a stronger model before running it. Set
`model: inherit` to always follow the session model instead. If an organisation's model
allowlist disallows `sonnet`, the session model is kept.

## Execution Engine

`superpowers:subagent-driven-development` (SDD) **is** the delivery engine for steps 5–10.
This skill is the project adapter: it owns scope and validation (steps 1–4) and the audit
record (`TASKS.md`). SDD owns delivery — a fresh implementer subagent per task, a task
review after each, and a final whole-branch review at the end of a group.

Invoke SDD once for the in-scope work and give it this adapter block, so its conventions map
onto this project:

- **Plan = the in-scope tasks file.** Each `T#` section is one SDD task, delivered in the
  documented order.

- **Hand each implementer only its own `T#` section** as the brief — never the whole tasks
  file, never other specs. Add the one-line "where this fits" context and any interfaces
  decided by earlier tasks. Giving an implementer the whole file invites it to solve the next
  task too.

- **Tell the implementer the task id is context for *them*, not content for the code.** The
  delivered source and tests must not cite the task, item, plan or guide. The task review
  rejects any such reference as a finding.

- **Serial only. No parallel implementers, no worktrees.** Execute one task at a time even
  when the dependency map shows independence — that map encodes *ordering*, not concurrency.
  Parallel implementers in one tree collide.

- **Already on the item's branch.** Do not start work on the base branch.

- **Verification is the task's own stated command.** The implementer, and any fix subagent,
  runs it and reports the command plus trimmed output. No "complete" without passing
  evidence.

- **Commit per task**, in the implementer, in the format below.

- **`TASKS.md` is the audit artifact and the controller owns it.** After a task's review
  comes back clean, *you* — not the subagent — mark the `T#` section complete with trimmed
  verification evidence and the full traceability chain. Keep SDD's own progress ledger as
  compaction-recovery scratch; `TASKS.md` remains the human-facing record.

- **Single vs group.** Single-task scope → run SDD's per-task loop once, skip the final
  whole-branch review. Group scope → the full per-task loop for each, then the final
  whole-branch review on the most capable available model.

- **Stop conditions.** Strict order; stop on the first failed or blocked task; record the
  reason in `TASKS.md` and mark it `Blocked`. A reviewer's unresolved Critical or Important
  finding blocks the next task.

### What the subagents apply per task

- **Writing code:** invoke `superpowers:test-driven-development`. Write the failing test
  first, confirm it fails *for the right reason*, then the minimal code to pass.
- **A task fails verification:** invoke `superpowers:systematic-debugging`. Reproduce,
  isolate the root cause, then fix. No speculative patches.
- **Before marking complete:** invoke `superpowers:verification-before-completion`. Every
  acceptance criterion needs passing executable evidence, not a code skim.

## Execution Order

1. **Resolve scope.** Identify the tasks file(s) and the target mode — single task or group.

2. **Reload the checklist.** Load the latest file content and verify task status before
   coding. **Never trust an in-context copy** — a prior session may have advanced it.

3. **Validate task shape.** For each incomplete task in scope, confirm it has acceptance
   criteria, verification steps, a rollback note and traceability. **Reject malformed tasks
   back to the user** — do not silently proceed on a task that cannot be audited.

4. **Check dependencies.** If a blocking task is incomplete, clarify with the user whether to
   wait or proceed with a stated assumption. Record the chosen path.

5. **Deliver the task** via SDD. Implement **only the required changes** — no opportunistic
   refactors, no scope creep into adjacent files.

6. **Run all verification steps before updating the checklist.** Follow the task's own stated
   commands: the unit-test command for the relevant tests, the lint/format check, and any
   schema validation when a spec changed. Invoke tooling through the repo's documented
   entrypoint.

7. **Collect verification evidence** appropriate to the task: trimmed test output, the
   initial failure message that proves test-first, mutation output for a guard task,
   validation summaries, or manual notes when no automated check exists.

8. **Update the checklist** with completion status, evidence and the full traceability chain.

9. **Commit task-related changes:**

   ```
   Task <ID>: <Short Description> (Plan <ItemId> → Guide → Task <ID>)
   ```

   Stage code, tests, docs, schema/spec files, pipeline config **and the updated tasks file
   in the same commit**, so the audit trail cannot drift from the code.

10. **If a task is blocked or fails verification**, record the reason in `TASKS.md`, mark it
    `Blocked`, and stop the current scope.

11. **End with a concise run summary** — what changed, verification results, blockers, next
    actions.

## Required Output Structure

- Task validation results, including any malformed task rejected
- Dependency check results and decisions
- Verification evidence per completed task
- Updated checklist entries with the full traceability chain
- Commit messages
- Run summary with blockers, verification status and next actions

## Always-on Rules

- **A task is complete only when:** acceptance criteria met **and** verification steps pass
  **and** the checklist is marked **and** the commit exists. Four conjuncts, no shortcuts.

- **Never mark complete without verification evidence.** If verification is ambiguous, ask
  the user rather than deciding.

- **In group mode, execute strictly in the documented order** and stop on the first failure
  or block.

- **Reject malformed tasks** — missing acceptance criteria, verification, rollback or
  traceability — and report them.

- **Avoid unrelated edits and refactors.** The task's scope is the task's scope.

- **No spec references in source.** Code and test files focus on functionality, not on the
  spec that produced them. Never add comments, docstrings, test names or identifiers citing a
  task id, item number, plan, guide or design-doc section. Traceability lives in the commit
  message and the tasks file only.

  Comments explaining *why* the code behaves as it does are encouraged — write the reason
  itself, stripped of the citation. When editing a file that already carries such
  references, remove the citation from lines you touch; do not sweep the whole file.

  The reason this matters: the spec folder is gitignored, so a comment citing it points at a
  file no reader can open.

- **Stage and commit all task-related changes by default** — code, tests, docs, schema
  files, pipeline config and the updated checklist.

- **Invoke tooling through the repo's documented entrypoint.** Never activate an environment
  in the shell; it does not survive between tool calls.

- **Exclude integration tests by default** using the config's mechanism. Opt in only when
  the task explicitly requires them.
