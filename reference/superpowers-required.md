# Superpowers: Required, Not Optional

This pack depends on the `superpowers` plugin. The skills invoke it directly and carry **no
fallbacks**.

```
/plugin marketplace add claude-plugins-official
/plugin install superpowers
```

## Why it is a hard dependency here

An earlier version of these skills treated superpowers as optional — each one carried an
"if available, invoke it; otherwise do this instead" section, because not every teammate could
be assumed to have it installed.

That is the right call when you are retrofitting a workflow onto a team that already exists. It
is the wrong call when you are defining the workflow up front, for three reasons:

1. **The fallbacks were inferior restatements.** "Otherwise apply TDD directly — write a failing
   test first" is a one-line gesture at a skill that has an actual procedure behind it. Shipping
   both means shipping one good path and one thin one, and not knowing which ran.

2. **Two paths cannot be reasoned about.** A review finding traced back to an execution that may
   or may not have gone through a subagent with a review gate is a finding you cannot act on.

3. **It was roughly 15% of the text** for a branch almost never taken.

The cost of requiring it is one install step during bootstrap. That is cheaper than maintaining
a second-class path forever.

## Which plugin skills are load-bearing

| Superpowers skill | Invoked by | What it carries |
|---|---|---|
| `brainstorming` | `plan-with-spec`; and directly, for any work that is not item-shaped | Classifies work as spike / bounded / architectural and scales ceremony to it. The front door for investigations, spikes and environment work — anything with no work item behind it. |
| `subagent-driven-development` | `execute-task-checklist` | **The delivery engine.** Fresh implementer subagent per task, task review after each, final whole-branch review. Without it, task execution falls back to implementing inline in an increasingly polluted context. |
| `test-driven-development` | the SDD implementer, per task | Failing test first, confirmed failing for the right reason, then minimal code. |
| `systematic-debugging` | `execute-task-checklist` on a verification failure; `address-comments` when a comment points at a bug | Reproduce, isolate root cause, then fix. The guard against speculative patching. |
| `verification-before-completion` | the SDD implementer, before marking a task complete | Every acceptance criterion needs passing executable evidence, not a code skim. Directly enforces the four-conjunct definition of done. |
| `requesting-code-review` | `pre-pr-review` | The independent fresh-eyes pass alongside the spec-driven review. |
| `receiving-code-review` | `address-comments` | Triage before implementing. Guards against both performative agreement and dismissing a valid point. |
| `finishing-a-development-branch` | `pr-description` | Coordinates the remaining branch-finishing steps. |
| `using-superpowers` | the plugin's own `SessionStart` hook | Establishes that a relevant skill is invoked before any response — including before clarifying questions. |

## Skills in the plugin this pack does not wire in

Available and useful, just not on the critical path:

- **`writing-plans`** — the ladder skills define their own output structures, which are more
  specific. Reach for this when planning something the ladder does not cover.
- **`writing-skills`** — use it when authoring domain skills. See
  `skills/DOMAIN-SKILL-TEMPLATE.md`.
- **`using-git-worktrees`** — useful for isolating work, but note that
  `execute-task-checklist` deliberately runs **serial with no worktrees**: parallel implementers
  in one tree collide, and the task dependency map encodes ordering rather than concurrency.
- **`dispatching-parallel-agents`** — for breadth-first investigation, which is genuinely
  valuable and sits outside this pipeline. A read-only analysis question fans out well; task
  delivery does not.
- **`executing-plans`** — superseded here by the `TASKS.md` chain, which adds rollback notes and
  traceability.

## What degrades if one is missing

If the plugin is absent or a skill is unavailable, the pack does not fail loudly — it quietly
runs a weaker version. Worth knowing which:

| Missing | Effect |
|---|---|
| `subagent-driven-development` | Tasks implement inline; no per-task review gate; context accumulates across a group and later tasks get worse |
| `test-driven-development` | Tests get written after the code, and stop being evidence the code was needed |
| `verification-before-completion` | "Complete" starts meaning "looks right" |
| `systematic-debugging` | Speculative patches at the symptom |
| `requesting-code-review` | `pre-pr-review` reviews its own work, with its own blind spots |
| `brainstorming` | Non-item work loses its front door and starts arriving as unscoped requests |

If an organisation genuinely cannot install the plugin, the honest move is to fork this pack and
write the procedures inline — not to leave the invocations in place and hope.
