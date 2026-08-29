# Domain Skill Template

The skills in this pack are process skills — they work in any repo. The skills that end up
most valuable are the ones you write yourself: **domain skills**, which encode how *this*
system actually works.

They are the highest-return thing in the whole setup, and they cannot be shipped with a pack
because their content is the thing that is specific.

## What a domain skill is for

Three kinds pay off consistently.

### 1. Established patterns for a subsystem

*"How we design, debug and extend the thing at the centre of this codebase."* The patterns a
new contributor gets wrong, written down once.

Signals you need one: the same review comment recurring across items; a subsystem where the
obvious approach is wrong for a non-obvious reason; a component people avoid touching.

### 2. A recurring analysis or report

*"Compute this number correctly, from the right source, avoiding the traps that make naive
answers wrong."*

These are worth their weight the moment two people compute the same figure differently. The
critical content is not the query — it is **which source is authoritative and why the obvious
one is wrong**, and what the number does *not* include.

Signals: a metric someone asks for repeatedly; a figure that has been reported wrong before; a
question that takes 40 minutes of rediscovery each time.

### 3. A periodic review with a decision gate

*"Generate a dated snapshot, apply the gate, produce the outputs."* A triage review, a capacity
check, a dependency audit.

These pair naturally with `write-story`: the review produces findings, `write-story` turns the
actionable ones into items.

## Template

```markdown
---
name: <kebab-case-name>
description: <What it does, then the trigger conditions. Write the description as
  the condition under which it should fire, not as a summary — that is what makes
  automatic invocation work. Name the specific words a user would say.>
---

# <Title>

## What this covers
<One paragraph. What part of the system, and what question it answers.>

## Prerequisites
<Access, credentials, tools, environment. Be specific — a skill that fails at step
one because of an unstated prerequisite wastes more time than no skill.>

## The correct source
<For an analysis skill, this is the most important section.
 Which source is authoritative, and — explicitly — which plausible-looking source
 is wrong and by roughly how much. Someone will reach for the wrong one.>

## Steps
1. <...>
2. <...>

## Traps
<Symptom → cause → what to do. The reason this skill exists rather than a
 paragraph in CLAUDE.md. Each entry should have cost someone real time.
 Date any measured figure.>

## Output
<What the user gets, and where it goes.>
```

## Rules that keep a domain skill useful

- **The description is a trigger, not a summary.** Compare *"Information about the ingestion
  pipeline"* with *"Use this before quoting an ingestion count or failure rate — the obvious
  source overstates job counts and understates the failure rate by the same factor."* Only the
  second one fires when it should.

- **State what is authoritative and what is wrong.** For anything that produces a number, the
  most valuable line is the one that says *don't use X, use Y, here's the size of the error*.

- **Date every measured figure, and prefer structure to magnitude.** Numbers expire; the shape
  of the system usually does not. Where a figure must be recorded, say what window it describes.

- **Traps earn their place.** Each entry should trace to something that actually went wrong.
  A speculative trap list is documentation; a real one is a skill.

- **Version it when the contract underneath changes.** If a data contract changes such that the
  old method is now wrong, a `-v2` skill that states what drifted and refuses out-of-range
  windows is better than silently editing the original — people have old outputs to reconcile.

- **Cross-reference the knowledge base rather than duplicating it.** A `trap` article and a
  domain skill can point at each other. Two copies of the same lesson drift.

- **Delete it when it stops being true.** An unused or stale domain skill is worse than none,
  because it will be trusted.

## Where domain skills fit the flow

| Skill kind | Invoked by | Feeds |
|---|---|---|
| Subsystem patterns | `plan-with-spec`, `plan-to-implementation-guide`, `pre-pr-review` | Better plans; fewer review findings |
| Analysis / report | The user, directly | Baselines that `compound` writes up as `evidence` |
| Periodic review | The user, on a schedule | Findings that `write-story` turns into items |

The last row is the loop worth building deliberately: a review skill that produces findings, a
`write-story` invocation that captures them, and a knowledge base that records what the review
learned. That is what turns the pack from a delivery pipeline into something that improves.
