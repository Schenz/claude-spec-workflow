---
name: write-story
description: Draft a work item for something found but not yet filed — a defect, a gap, a follow-up. Owns the work-item format, the size ceiling and the acceptance-criteria quality gate. Use whenever work is discovered that does not belong in the current item, or when a knowledge article implies work.
---

# Write Story

Draft a work item for `$ARGUMENTS` — a finding, a gap, a follow-up, or the implication of a
knowledge article.

**This skill is the single definition of the work-item format.** `compound` invokes it for
work its findings imply; triage and review skills invoke it for remediation items; you invoke
it directly whenever something surfaces that needs capturing. Nothing else should carry its
own copy of the format.

**Read `.claude/workflow-config.md`** for the estimate unit, the size ceiling, the scratch
directory and the tracker field mapping.

## Why This Exists

Work found while doing other work does not get fixed inline — that is how an item's scope
becomes unreviewable. It gets captured, sized, and filed as its own item.

The failure mode this prevents is not forgetting. It is capturing badly: a wall of
investigation prose that nobody can act on, or an item so large it never gets picked up.

## Where Drafts Go

Write each draft to a **scratch file outside the repo**, at the path the config names:

```
<scratch>/story-draft-<slug>.md
```

Outside the repo, for a specific reason: a draft is dated narrative prose about work, and it
must never be caught by a pull request and reviewed as though it were code. Say where you put
it so the user can find it.

## The Format

**Emit exactly these five fields, in this order, and nothing else.** The same format is kept as
a standalone reference at `templates/story-draft.md`, with the quality checklist inline.

```
**Title**
<one line>

**Description**
As a {}, I want {} so that {}

**Proposed Fix**
<what and where. Not how.>

**Acceptance Criteria**
GIVEN {}
WHEN {}
THEN {}

**Estimate**
<in the config's unit>
```

No backing-evidence section. No "why this matters" preamble. No re-runnable query appendix.
No tables. **The evidence belongs in the knowledge article or the investigation the item came
from; repeating it here is what makes drafts unusable.**

## The Rules That Make A Draft Usable

### Description and Proposed Fix are one line each

A short paragraph is acceptable where a single sentence genuinely cannot carry it. More than
that is a signal the item is **too big**, not that the field needs more prose.

Name the file, the symptom, or the surface. Do not restage the investigation that found it.

### Acceptance criteria must be checkable by an outsider

`GIVEN` / `WHEN` / `THEN` each on their own line, one blank line between criteria, **two to
four criteria** total.

Each must be verifiable by someone who was not in the conversation. Prefer a named artifact or
a measurable threshold to "is improved" or "works correctly".

- **Weak:** `THEN the error rate is better`
- **Strong:** `THEN each event carries a non-null positive duration_ms`
- **Strong:** `THEN the stage-duration query returns rows for the wrapper stages with no path filter`

If you cannot write a checkable `THEN`, the item is not understood well enough to file. Say so
rather than filing a vague one.

### The size ceiling is a ceiling, not a target to negotiate

The config names the unit and the ceiling. **If the work will not fit, split it into multiple
items** rather than raising the estimate.

A diagnosis and the remediation it implies are usually **two items, not one** — the
remediation cannot be scoped until the diagnosis lands, so bundling them produces an item
whose second half has no acceptance criteria anyone can write yet.

### Cite, do not restate

When the item comes from a knowledge article, cite it by relative path. When it comes from a
measurement, name the measurement and its date. One line either way.

## Execution Order

1. **Check the scratch directory for existing drafts** covering the same finding. Extend or
   replace rather than adding a near-duplicate — the same problem filed twice gets triaged
   twice and fixed once.

2. **Establish what is actually known.** Separate the symptom from the suspected cause. If the
   cause is unproven, the item is a diagnosis item and its acceptance criteria are about
   *establishing* the cause, not fixing it.

3. **Size it.** If it exceeds the ceiling, split now and draft each piece. State the split and
   the dependency between the pieces.

4. **Draft the five fields.**

5. **Run the self-gate** below.

6. **Write the file** and report its path, plus a one-line summary of each item drafted.

7. **Do not file it.** Filing is a separate, deliberate step — see
   `reference/tracker-integration.md`. The user assigns the tracker id.

## Self-Gate

Before writing, check all five. Fail any one, and fix it rather than filing:

- **One item, one outcome.** If the Title needs an "and", consider splitting.
- **Every `THEN` is checkable by an outsider**, against a named artifact or a threshold.
- **Description and Proposed Fix are one line each** — or the item is too big.
- **Within the size ceiling**, without the estimate having been stretched to fit.
- **No restated evidence.** A path or a dated measurement, not a narrative.

## Always-on Rules

- **Five fields, in order, nothing else.**
- **Proposed Fix says what and where, never how.** The how is decided at planning time by
  `plan-with-spec`, with the knowledge base consulted — deciding it here skips that.
- **Drafts live outside the repo.**
- **Do not invent an item id.** The tracker assigns it.
- **Emitting nothing is valid.** If the finding is not actually work — it is a knowledge
  article, or it is already filed — say so and stop.
