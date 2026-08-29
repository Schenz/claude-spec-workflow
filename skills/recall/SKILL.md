---
name: recall
description: Surface durable knowledge from docs/knowledge/ relevant to a topic, work item, or set of changed paths. Use before planning an item, when a design question feels previously answered, or to check changed code against known traps.
---

# Recall

Return prior knowledge relevant to `$ARGUMENTS` — a topic, an item id, or
`--paths <path> [<path>...]` for a diff-driven sweep. Optional `--type <type>` narrows to one
article type.

**This skill is the single definition of how knowledge is selected.** Other skills invoke it
rather than implementing their own selection, so that improving retrieval improves it
everywhere at once.

**Read `.claude/workflow-config.md`** for this project's decision surfaces — they are the
primary selection axis.

## Instructions

1. **Read `docs/knowledge/README.md` first.** The index is the cheap filter. Do not open
   every article.

2. **Select candidates**, in descending order of strength:
   - **Surface overlap** — the topic or the changed paths map to a tagged decision surface.
   - **Path overlap** — for `--paths`, an article's Evidence cites a changed file.
   - **Item adjacency** — the requested item's epic, or an item cited in an article.
   - **Keyword match** on article titles and summaries.

3. **Open only the selected articles**, and read them fully. A half-read article produces a
   confident wrong summary.

4. **Report each hit as:** relative path, type, date, and **one sentence on what it means for
   the work at hand** — its consequence, not a summary of its contents. The caller needs to
   know what to do differently, not what the article says.

5. **Flag staleness.** When an `evidence` article's measurements are older than 90 days, say
   so and note that re-measuring may be warranted. Measured figures expire; structure does
   not.

6. **State the coverage.** Say how many articles the index listed and how many you opened. For
   a `--paths` sweep this matters especially: if the branch is behind the base branch on
   `docs/knowledge/`, the sweep covers fewer articles than exist, with no other signal. Advise
   merging the base branch when the index looks short.

7. **If nothing is relevant, output exactly `No relevant prior knowledge.` and stop.** Do not
   pad with loosely-related articles. **A false hit costs more than a miss**, because it gets
   cited in a plan and then trusted.

## Selection Rules

- **Never filter by type unless asked.** All types are eligible. A `trap` is as
  planning-relevant as a `decision` — excluding traps from planning is a known failure of
  this pattern, and the reason step 2 ranks by surface rather than by type.

- **Prefer few strong hits to many weak ones.** Three articles that change the work beat ten
  that merely touch the topic.

- **An `invalidation` that overturns a belief the caller is relying on is always relevant.
  Lead with it.** The caller may be about to plan work premised on something now known to be
  false.

- **Honour supersession.** Superseded articles are deleted from this base rather than kept, so
  everything the index lists is current guidance. If you encounter an article referencing a
  file that no longer exists, report that as an index/file mismatch — it means a sweep
  somewhere is silently partial.

## Output Format

```
## Prior knowledge

Index lists 41 articles; opened 3.

- `docs/knowledge/2026-07-23-instance-cap-not-needed-yet.md` (invalidation, 2026-07-23)
  The admission gate's defaults were shown unnecessary at observed production levels — do
  not re-tune them without re-running the baseline query first.

- `docs/knowledge/2026-07-23-activity-not-registered.md` (trap, 2026-07-23)
  New handler functions must be registered in the app entrypoint or they fail at runtime
  with "does not exist" — check registration for anything this work adds.
```

When invoked with `--paths`, group by article and name the specific changed file that
triggered each hit.

## Notes

This skill reads markdown and git. It runs no tests and no linters, so it is safe to invoke
at any point, including mid-implementation when a question starts to feel familiar.
