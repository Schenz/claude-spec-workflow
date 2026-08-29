<!--
  Copy to <repo>/docs/knowledge/README.md and fill in the surface list from
  .claude/workflow-config.md. The two must agree exactly — articles get tagged from
  one and searched from the other.

  Commit this empty. An empty indexed base is ready; an unindexed article is invisible.
-->

# Knowledge Base

Durable knowledge extracted from completed work by the `compound` skill, and consulted by the
`recall` skill. **Each article is independently readable** — you should not need the
originating item's spec to act on it.

## How to use this

- **Before planning an item:** `plan-with-spec` consults this automatically. To query it
  directly, invoke `recall <topic>`.
- **Before opening a PR:** `pre-pr-review` sweeps `trap` articles against the changed paths.
- **After work merges, or after real-world evidence arrives:** invoke `compound` to add what
  was learned. The second kind of run matters most.

## Authoring rules

- **Never cite a path inside the spec folder.** It is gitignored, so the citation points at a
  file no reader can open. Cite a commit, a `file:line`, a symbol, a query name, or a log path.

- **Prefer a symbol to a line number.** Line numbers rot within a day. Name the function; add
  the line only as a hint.

- **The index and the files must agree.** Both are text and merge as text, so a branch can
  carry an index row whose article never merged — which makes every trap sweep silently
  partial, because `recall` reads the index first and simply finds less than it lists. After
  any merge touching this directory, check that the file count matches the row count, and treat
  a mismatch as a broken sweep rather than cosmetic drift.

- **Merge the base branch before treating a trap sweep as complete.** A feature branch can be
  *behind* the base on this directory, so a sweep run there covers fewer articles than exist,
  with no signal at all. State the article count a sweep actually covered.

- **Consolidate rather than accumulate.** When new work hits a lesson an existing article
  covers, add the instance to that article — do not write a second one. The same lesson spread
  over nine files is nine reads to learn it once.

- **Provenance or it does not go in.** A commit, `file:line`, query, log path, or dated
  measurement. Knowledge without provenance is opinion.

## Retention rule

**Every article in this index is current guidance.** When an article is superseded it is
**deleted** — file and index row — rather than marked and kept, so no stale reading can be
surfaced by mistake. Anything from the old article still worth having is carried forward into
the superseding one before deletion, and inbound links from other articles are retargeted so
none points at a removed file. Git history remains the record of what was once believed.

`invalidation` is an article **type, not a status**. An invalidation article is live, current
guidance whose content happens to be "the team believed X; the evidence says otherwise" — it is
the guard that stops X being re-derived, and it must not be pruned as though it were stale.

## Article types

| Type | Captures |
|---|---|
| `decision` | A choice made, the alternatives rejected, and why |
| `trap` | Symptom → cause → guard for a defect worth never repeating |
| `behavior` | How the system actually acts under load or configuration |
| `evidence` | A re-runnable measurement recipe plus the numbers and the date they were true |
| `invalidation` | A previously-held belief the evidence overturned |

## Decision surfaces

Articles tag the surfaces they touch, so `recall` can filter without opening every file. These
must match `.claude/workflow-config.md` exactly.

`<surface-1>` · `<surface-2>` · `<surface-3>` · `<...>`

## Start here

<!--
  Once six or so articles accumulate, promote the ones carrying recurring lessons —
  especially any that consolidate what several items learned separately. This section
  is what a new team member reads first.
-->

*(Nothing yet. Populate once the base has articles worth leading with.)*

## Index

<!--
  Keep the count line accurate — it is how a partial sweep gets noticed.
  List each article once under its primary surface; the Also column names the others.
-->

0 articles.

### `<surface-1>`

| Article | Type | Item | Date | Also |
|---|---|---|---|---|
| | | | | |
