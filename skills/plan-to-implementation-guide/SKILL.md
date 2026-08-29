---
name: plan-to-implementation-guide
description: Generate or update IMPLEMENTATION_GUIDE.md from PLAN.md in the project's spec folder. Focuses on required delivery work and how it will be verified. Use after PLAN.md exists, or when the user asks to translate a plan into a guide.
---

# Plan To Implementation Guide

Generate an implementation guide from an item's plan. `$ARGUMENTS` should be the path to
`PLAN.md`, or provide `PLAN.md` as context.

**Read `.claude/workflow-config.md` first** for the spec folder convention, branch-name
shapes, commands, test layout, definition-of-done rules and decision surfaces.

## Item Folder Resolution

- Default location: `PLAN.md` and `IMPLEMENTATION_GUIDE.md` in the configured spec folder
  for the item.
- Resolve the item id from the branch using the config's branch-name shapes. If it cannot be
  resolved, ask the user before doing anything else.

## Execution Order

1. Use `PLAN.md` as the **source of truth**. Read it fully before writing.

2. Create or update `IMPLEMENTATION_GUIDE.md` in the same item folder.

3. Review the plan and its accepted decisions, then identify **implementation-specific**
   questions the plan did not address. The recurring classes:
   - **Where the change lives** — which module or layer, per the repo's structure.
   - **Extend or introduce** — grow an existing module, or add a new one.
   - **Test scope** — unit only (the default), or unit plus targeted integration.
   - **Migration strategy** for any persisted shape — dual-write, or cutover.
   - **Contract shape** for anything other code depends on — an API surface, an event
     schema, a queue message, a generated artifact.
   - Anything touching a **decision surface** named in the config.

4. **Present each implementation question to the user ONE AT A TIME:**
   - **Question:** clear and concise, focused on the *how*
   - **Options:** a labelled list of realistic technical choices
   - **Recommendation:** the best-practice choice and a one-sentence reason

   Wait for the user's answer before asking the next. **Do not batch questions.**

5. Translate each **required** plan item into implementation instructions using this
   structure:
   - **Goal** — one sentence
   - **Approach** — the implementation *and* verification strategy, informed by the
     confirmed answers
   - **Files to edit/create** — markdown links, relative to repo root
   - **Effort and priority**
   - **Checklist**
   - **Definition of Done** — per the config's file-type table

6. If the guide already exists, append or update without deleting still-relevant content.

7. End with direct next actions that map to required delivery work.

8. Perform a final pass for clarity, completeness and strict scope control.

## Required Output Structure

- **Context Reference** — links to `PLAN.md` and the work item
- **Delivery Strategy**, by required item
- **For each item:** Goal, Approach, Files, Effort/Priority, Checklist, Definition of Done
- **Actionable Next Steps**

## Always-on Rules

- **Identify implementation questions before drafting.** Do not skip this — surface the
  assumptions about technical approach, testing strategy and verification.
- **One question at a time**, with options and a recommendation. Never batch.
- **Weave confirmed answers in naturally.** No Q&A section.
- **Include only required work from `PLAN.md`.** Exclude optional, speculative and
  alternative paths unless explicitly requested.
- **Resolve every optional plan item into a decision:** committed now, or excluded from this
  item. Do not carry an "if we have time" into a guide.
- **Do not duplicate completed work** already recorded in `PLAN.md`.
- **Keep the guide concise**, readable in about one screen.
- **Verification requirements match file type and committed scope**, per the config's
  definition-of-done table. Name the actual command, and invoke tooling through the repo's
  documented entrypoint rather than activating an environment in the shell.
- **Every item states how it will be proven, not just what will change.** An approach with
  no verification strategy is a guess about how long the work will take.
- **Prefer naming a symbol to citing a line number** in file references.
