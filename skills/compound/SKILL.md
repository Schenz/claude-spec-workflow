---
name: compound
description: Extract durable knowledge from completed work into docs/knowledge/ — decisions, traps, measured behavior, evidence recipes, and invalidated beliefs. Use after pre-pr-review or pr-description, and again whenever real-world validation produces new evidence.
---

# Compound

Extract lasting knowledge from this item's work and write it to `docs/knowledge/`.

Run this after `pre-pr-review` or `pr-description`, and **again** whenever real-world
validation produces evidence — a staging or production run, a measured baseline, an incident.

**The second kind of run matters most.** The sharpest lessons arrive days after a merge, and
a review-time-only extraction cannot see them.

**Read `.claude/workflow-config.md`** for the base branch, spec folder and decision surfaces.

## Resolution

1. **Item id** — from the branch, using the config's branch-name shapes. Ask the user if it
   cannot be resolved.
2. **Base branch** — do not trust `git symbolic-ref refs/remotes/origin/HEAD`; it can point at
   an abandoned branch. Compare the tips of the plausible bases by commit date, choose the most
   recent, and **state the chosen base in your output** so a wrong guess is visible
   immediately. Confirm with the user if the candidates differ by less than a day.

## Inputs

Read all of these before writing anything:

| Source | What to look for |
|---|---|
| `PLAN.md` | Decisions, scope boundaries, explicitly rejected alternatives |
| `PRE_PR_REVIEW.md` | Findings, verification matrix, MUST-FIX / SHOULD-FIX |
| `TASKS.md` | What was planned versus what was delivered |
| `git log <base>..HEAD` and `git diff <base>...HEAD --stat` | Commit progression, course corrections |
| **This conversation** | Pasted logs, query results, measurements, links, and conclusions stated only out loud |
| `recall <subject>` | Prior art — do not re-derive it; supersede it |

**The conversation is a first-class input, not a fallback.** Evidence the user gathered by
hand frequently exists nowhere else.

**When there is no spec folder.** Not every project uses one. Work from git history, the diff
and the conversation, and **say which inputs were available** — so a thin extraction is
understood as thin evidence rather than a thin item.

**When `docs/knowledge/` does not exist.** Create it and its index, seeding the index with the
format header before adding rows.

## The Delta Hunt

Knowledge lives in three gaps. Work them in order:

1. **Planned versus shipped** — what changed during implementation, and why.
2. **Review versus plan** — what the review surfaced that the plan did not anticipate.
3. **Predicted versus measured** — what the plan asserted about real-world behavior versus
   what the environment actually showed.

The third gap is the highest-value one, and the reason this skill runs after validation
rather than only at review time.

## Article Types

| Type | Use when |
|---|---|
| `decision` | A choice was made and alternatives rejected for reasons worth preserving |
| `trap` | A defect was hit whose symptom, cause and guard should outlive the fix |
| `behavior` | The system's real behavior under load or configuration was established |
| `evidence` | A measurement was taken that future work should be able to reproduce |
| `invalidation` | Something the team believed turned out to be wrong |

`invalidation` is a **type, not a status.** An invalidation article is live, current guidance
whose content happens to be "the team believed X; the evidence says otherwise" — it is the
guard that stops X being re-derived, and it must never be pruned as though it were stale.

## File Format

Write to `docs/knowledge/YYYY-MM-DD-short-slug.md`:

```
---
type: decision | trap | behavior | evidence | invalidation
item: 1234
date: 2026-01-15
surfaces: [<from the config's decision surfaces>]
supersedes: 2026-01-02-earlier-article.md   # omit when not applicable
repos: [<this repo, plus any other repo the knowledge affects>]
---

# <Descriptive title, memorable enough to recall by name>

## What
<The knowledge itself, stated plainly. Two to four sentences.>

## Why it matters
<The consequence for future work. One or two sentences.>

## Evidence
<Provenance: commit SHA, file:line or symbol, query name, log path, or dated measurement.
For `evidence` articles, the full re-runnable recipe.>

## What to do with it
<The actionable instruction for someone hitting this area next.>
```

**Name traps and behaviors memorably.** "Fail-open admits the whole waiting cohort" is
recallable; "the concurrency thing" is not.

**Prefer a symbol to a line number.** Line numbers rot within a day — an article citing
`writers.py:555-557` is wrong as soon as unrelated work moves that code. Name the function;
add the line only as a hint.

**Never cite a path inside the spec folder.** It is gitignored, so the citation points at a
file no reader can open. Cite a commit, a `file:line`, a query name, or a log path instead.

## Evidence Articles Carry Recipes

An `evidence` article that records only a conclusion is half-written. Include what someone
needs to re-measure: the exact query, the CLI invocation, the settings, the test cohort.

**Record the numbers and the window they describe**, because they expire.

`p50 3, p95 12, p99 19, max 47` over a named 6-day window *after* a specific fix shipped is
knowledge. "Concurrency is low" is not.

**Never pool windows that straddle a fix.** The same work measured over 14 days — mostly
*pre*-fix — can read nearly 4× higher, and recording that as the current baseline sends the
next item to a threshold the system has already outgrown. When a fix lands mid-window, report
each side separately and say which one decisions rest on.

## Supersession Is Deletion

When new knowledge overturns an existing article:

1. Carry forward anything in the old article still worth having.
2. Retarget any inbound links from other articles so none points at a removed file.
3. **Delete the old article — the file and its index row.** Set `supersedes:` in the new one.

Superseded articles are **not** marked and kept. Everything the index lists is current
guidance, so no stale reading can be surfaced by mistake. Git history remains the record of
what was once believed.

Two live articles giving contradictory guidance is worse than none.

## Consolidate Rather Than Accumulate

When this item hits a lesson an existing article already covers, **add the instance to that
article** — do not write a second one. The same lesson spread over nine files is nine reads to
learn it once.

A consolidated article naming several items in its `item:` field is a sign the base is
working, not a sign of sloppiness.

## When Knowledge Implies Work

Some findings describe the system; others imply work that needs doing. For the second kind,
**invoke `write-story`** to draft it. That skill owns the format, the size ceiling and the
acceptance-criteria quality gate.

Cite the knowledge article by relative path in the draft, in place of restating its evidence.
The evidence belongs in the article; repeating it is what makes drafts unusable.

## Self-Gate

Before writing any article, check it against all four. **Fail any one, and do not write it:**

- **Provenance** — it cites a commit, `file:line` or symbol, query, log path, or dated
  measurement. *Knowledge without provenance is opinion.*
- **Non-obvious** — a competent engineer new to the repo would not already assume it. "Tests
  should pass" and "handle errors" are not knowledge.
- **Standalone** — actionable without reading the originating item's spec.
- **Not already known** — `recall` did not surface an article saying this. If one exists and
  this refines it, consolidate or supersede rather than duplicate.

**Emitting nothing is a valid and common outcome.** Say
`No durable knowledge extracted from this item.` and stop.

A knowledge base padded with filler is worse than a small one, because `recall` starts
returning noise and callers stop trusting it.

## Extraction Context

**Dispatch a fresh-context subagent to perform the extraction.** Give it the spec artifact
paths, the resolved base branch, the `recall` output, and any evidence the user supplied in
conversation — but **not a narrative summary of the session.**

Rationale: extracting inline means summarizing your own account of the work, which preserves
your own blind spots. The gaps worth recording are frequently the ones you did not notice at
the time.

**Where the subagent's reading and this session's memory disagree, the artifacts win — and
the disagreement is itself a candidate article,** because it usually means the record is
incomplete.

If the user declines the subagent, extract inline, but re-read the artifacts and the diff
first, before consulting memory of the session.

## Hard Constraints

- **Write to `docs/` only.** Never add item numbers, task ids or plan citations to source or
  test files — traceability lives in commits and the tasks file.
- **Keep articles terse.** Document the what and the how, not the reasoning that produced them.
- **Record cross-repo impact** in `repos:` when the knowledge affects another repo.
- **Environment and machine-level facts** — local setup, proxies, host quirks — belong in
  personal memory, not here. This directory is for project knowledge that every teammate
  needs.
- **Update `docs/knowledge/README.md` in the same run that adds an article.** `recall` reads
  the index first, so an unindexed article is invisible. After any merge touching this
  directory, check that the row count matches the file count and treat a mismatch as a broken
  sweep rather than cosmetic drift.
