<!--
  The work-item draft format. Owned by the write-story skill.

  Copy this file only if you want it on hand as a reference — write-story emits it
  directly. Drafts belong in the scratch directory OUTSIDE the repo, named
  story-draft-<slug>.md, because they are dated narrative prose about work and must
  never be reviewed as part of a code change.

  Five fields, in this order, nothing else. No evidence section, no preamble,
  no query appendix, no tables. Cite the source; do not restate it.
-->

**Title**
{One line. If it needs an "and", consider splitting the item.}

**Description**
As a {role}, I want {capability} so that {outcome}

**Proposed Fix**
{What and where. Not how. Name the file, the symptom, or the surface — do not restage the
investigation that found it. One line; a short paragraph only where a sentence genuinely
cannot carry it. More than that means the item is too big.}

**Acceptance Criteria**
GIVEN {precondition}
WHEN {action}
THEN {checkable outcome}

GIVEN {precondition}
WHEN {action}
THEN {checkable outcome}

**Estimate**
{In the unit from `.claude/workflow-config.md`. If it exceeds the ceiling, split the item
rather than raising the estimate.}

<!--
  Acceptance criteria checklist:

  - Two to four criteria. Each GIVEN / WHEN / THEN on its own line, blank line between.
  - Every THEN checkable by someone who was not in the conversation.
    Weak:   THEN the error rate is better
    Strong: THEN each event carries a non-null positive duration_ms
    Strong: THEN the query returns rows for the wrapper stages with no path filter
  - If you cannot write a checkable THEN, the item is not understood well enough to file.

  Sizing:
  - The ceiling is a ceiling. Split rather than inflate.
  - A diagnosis and the remediation it implies are usually two items — the remediation
    cannot be scoped until the diagnosis lands.

  Provenance:
  - Cite the knowledge article by relative path, or name the measurement and its date.
    One line. The evidence lives where it was recorded.
-->
