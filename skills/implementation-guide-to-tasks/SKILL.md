---
name: implementation-guide-to-tasks
description: Convert IMPLEMENTATION_GUIDE.md into TASKS.md in the project's spec folder — execution-ready, traceable, required-only scope. Use when the guide exists and the user is ready to break delivery work into auditable tasks.
---

# Implementation Guide To Tasks

Convert an implementation guide into tasks. `$ARGUMENTS` should be the path to
`IMPLEMENTATION_GUIDE.md`, and optionally `PLAN.md`. When omitted, default to the current
item's spec folder.

**Read `.claude/workflow-config.md` first** for commands, test layout, lint baseline,
definition-of-done rules and the spec folder convention.

## Execution Order

1. Use `IMPLEMENTATION_GUIDE.md` as the source of truth; read `PLAN.md` only for missing
   context.

2. Create or update `TASKS.md` in the same item folder. Split into `TASKS_1.md`,
   `TASKS_2.md`, … **only** when a genuine phase boundary exists — a separate migration
   phase, a separate observability phase, an operator-run phase. Splitting by size alone
   makes the chain harder to follow.

3. Analyse the guide items for dependencies, parallelization opportunities and sequencing.
   Identify task-specific questions that remain unresolved.

4. **Present each sequencing question to the user ONE AT A TIME:**
   - **Question:** about sequencing, granularity, verification scope, or rollback
   - **Options:** a labelled list of realistic execution approaches
   - **Recommendation:** the best-practice choice and a one-sentence reason

   Wait for the user's answer before asking the next. **Do not batch questions.**

5. Map required guide items into task groups and a strict execution order, informed by the
   confirmed answers.

6. **For each task, include all seven fields:**
   - **Task ID** — stable, e.g. `T1`, `T2.1`, so commits and reviews can cite it
   - **Title**
   - **Files affected** — markdown links to repo paths
   - **Description**
   - **Acceptance criteria**
   - **Verification steps** — concrete commands from the config, invoked through the repo's
     documented entrypoint. Scope lint to the paths the task changes when the config records
     a pre-existing lint backlog.
   - **Rollback note** — which commit or file to revert, and whether downstream contracts
     must be unwound first
   - **Traceability** — `Item → Plan section → Guide section → Task ID`

7. **Draw the dependency map explicitly**, and state that it encodes *ordering*, not
   concurrency:

   ```
   T1 ─┬─► T3 ──► T5 ─┐
   T2 ─┘             ├─► T6 (full-suite gate) ──► T7 (operator verification)
   T4 ────────────────┘
   ```

   Annotate which tasks are independent — different files, no shared symbols — and which
   are strictly serial, naming the dependency in each case.

8. If the tasks file already exists, append or update without removing still-relevant
   tasks; clearly mark additions and changes.

9. Run a final pass for self-contained execution, clarity and independence.

## Task Design Rules

These are what make a task auditable rather than merely written down.

- **Test-first, failing for the right reason.** Each task states the assertion to write
  first, and that the initial run must fail *for the expected reason* before implementing.
  A test that fails for the wrong reason proves nothing about the change.

- **Any task that adds a guard gets a mutation step.** Break the guard, confirm red,
  restore, re-confirm green — and record the mutation's output as evidence. A guard that was
  never seen to fail is not known to work.

- **Assert a collected count, not just a pass**, wherever a test file's existence is itself
  in question — after a rename, a merge, or a branch switch. A suite that collects zero
  tests exits successfully.

- **Label agent-run versus operator-run tasks**, and order them so no human time is spent
  on a branch the automated suites already know is broken. Put a full-suite gate immediately
  before the first operator-run task.

- **One task, one logical change.** If the rollback note has to explain two unwindings, it
  is two tasks.

## Required Output Structure

- Task groups and recommended implementation order
- The dependency map
- For each task: ID, title, files, description, acceptance criteria, verification steps,
  rollback note, traceability
- Independence annotations
- Change notes for appended or updated tasks when the file already exists

## Always-on Rules

- **Analyse dependencies and surface sequencing questions before drafting.** Do not skip
  this — the assumptions about parallelization, verification scope and rollback are exactly
  what goes wrong later.
- **One question at a time**, with options and a recommendation. Never batch.
- **Each task must be independently testable and verifiable.**
- **Each task must carry explicit traceability** to the guide section and plan item it
  fulfils.
- **Include only required work.** Exclude optional and speculative items unless explicitly
  requested.
- **Do not duplicate completed work** from `IMPLEMENTATION_GUIDE.md`.
- **Keep language concise and execution-focused.**
- **Verification commands come from the config**, invoked through the repo's documented
  entrypoint — never by activating an environment in the shell.
