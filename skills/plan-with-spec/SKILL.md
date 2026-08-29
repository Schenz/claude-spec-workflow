---
name: plan-with-spec
description: Create or update a concise PLAN.md for a work item under the project's spec folder, focused on intent, scope decisions, and acceptance criteria — not implementation steps. Use when the user provides a tracker work item or asks to plan an item.
---

# Plan With Spec

Create or update the plan for the current work item. `$ARGUMENTS` should be the work item —
title, description and acceptance criteria. If not provided, ask the user for it.

**Read `.claude/workflow-config.md` first.** It holds this project's base branch, spec
folder convention, branch-name shapes, commands, definition-of-done rules and decision
surfaces. Never guess a value it defines, and never edit project specifics into this file.

## Item Folder Resolution

1. Derive the item id from the current branch, using the branch-name shapes in the config.
   If it cannot be resolved, **ask the user before doing anything else** — do not guess.
2. Open or create `PLAN.md` in the configured spec folder for that item. Existing peers may
   include `IMPLEMENTATION_GUIDE.md`, `TASKS.md`, `PRE_PR_REVIEW.md`, `PR_DESCRIPTION.md`
   and per-item notes.
3. If the config says this project has no spec folder, ask the user where the plan should
   live before writing.

## Execution Order

1. Resolve the item folder per the rules above.

2. **Consult prior knowledge before forming questions.** Invoke `recall` with the item's
   subject area, and read what it returns before drafting anything. Prior knowledge changes
   the plan in three ways:
   - A question it already answers is **not asked**. Fold the answer into the plan instead.
   - A `trap` touching this item's area becomes an **explicit plan item** to avoid it.
   - An `invalidation` overturning an assumption in the item itself is **raised with the
     user before planning proceeds** — the item may be premised on something now known to
     be false.

   Cite the articles you used by relative path inside **Approach & Decisions**.

3. **Surface open questions.** Invoke `superpowers:brainstorming` to explore intent and
   constraints, then analyse the work item, its acceptance criteria and your codebase
   findings to identify what is ambiguous, has multiple valid approaches, or carries risk
   if assumed incorrectly.

   Pay particular attention to questions touching this project's **decision surfaces** as
   listed in the config — those are the areas where a wrong assumption is most expensive.

4. **Present each open question to the user ONE AT A TIME** in this format:
   - **Question:** clear and concise
   - **Options:** a labelled list of realistic choices
   - **Recommendation:** the best-practice choice and a one-sentence reason

   Wait for the user's answer before asking the next question. **Do not batch questions.**

5. Build or update the plan from the work item, its acceptance criteria and the confirmed
   answers — weaving the decisions in naturally, as if they had always been part of the
   plan.

6. If updating an existing plan, append a brief **Completed Work Summary** and add
   **Remaining Work** only when work is still open.

7. Run a final quality pass: remove ambiguity, remove optional and speculative items, and
   confirm every item answers *why* rather than *how*.

## Required Output Structure

- **Item Id Source** — the branch it came from, and whether the spec folder is tracked
- **Work Item** — title and description as given
- **Acceptance Criteria**
- **Current Codebase Findings** — link concrete files as markdown links, relative to repo
  root. Prefer naming a symbol to citing a line number; line numbers rot within a day.
- **Approach & Decisions** — scope boundaries, design choices, constraints, non-obvious
  rationale, and an explicit **Out of scope** list
- **Implementation Checklist**
- **Definition of Done** — per the config's file-type table, for the file types this item
  actually touches
- **Completed Work Summary** *(update mode only)*
- **Remaining Work** *(only when applicable)*

## Always-on Rules

- **Consult the knowledge base before generating questions.** Never re-derive knowledge the
  base already holds, and never ask the user something a prior article answers.
- **Identify open questions before drafting.** Do not skip this even when the item seems
  clear — the purpose is to surface assumptions, and an item that seems clear is where
  unexamined assumptions hide.
- **One question at a time**, with options and a recommendation. Never batch.
- **Weave confirmed answers in naturally.** Do not create a Q&A or Decisions section
  recording the interrogation — the plan must read as one coherent decision.
- **Focus on intent and decisions:** what is in scope, what is explicitly out of scope,
  and why.
- **Do not describe implementation steps.** Those belong in `IMPLEMENTATION_GUIDE.md`. A
  plan that has drifted into steps cannot be reviewed as a scope decision.
- **Do not add optional paths** — nice-to-haves, alternatives — unless the user explicitly
  asks.
- **Keep the plan concise**, readable in about one screen.
- **Convert uncertainty into a decision.** Any uncertain item becomes explicit: committed
  now, or excluded from this item. An open question left in the plan is a decision deferred
  to implementation time, which is the worst moment to make it.
- **Findings are dated measurements, not impressions.** When a finding rests on a
  measurement, record the number, its source and the date. When it rests on a file, name
  the symbol.
- **Mark corrections as corrections.** If a re-review overturns something an earlier draft
  of this plan asserted, say so explicitly rather than silently editing — the correction is
  often the most useful line in the document.
