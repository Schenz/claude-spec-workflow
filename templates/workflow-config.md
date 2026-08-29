# Workflow Config

<!--
  Copy to <repo>/.claude/workflow-config.md and fill in every field.
  Every skill in this pack reads this file instead of carrying its own copy of
  these values. Do not edit project specifics into skill bodies.

  Leave nothing as a placeholder. A skill that reads <TEST_COMMAND> will run it.
  Delete a whole section only if it genuinely does not apply, and say so in one line
  rather than leaving it blank — a blank section reads as an oversight.
-->

## Project

- **Name:** `<PROJECT_NAME>`
- **What it is:** `<one sentence — enough for a reviewer to orient>`
- **Primary language / runtime:** `<e.g. Python 3.11, .NET 8, TypeScript/Node 20>`

## Branch and item resolution

- **Base branch:** `<e.g. main>`
- **Base-branch caveats:** `<none, or: an abandoned branch that origin/HEAD still points
  at, and which to prefer>`
- **Branch-name shapes an item id can be parsed from:**
  - `<e.g. feature/{id}-description>`
  - `<e.g. {id}/description>`
  - `<add every shape actually in use; skills ask rather than guess when parsing fails>`

## Spec folder

- **Convention:** `<specs/{itemId}/ | none>`
- **Tracked?** `<gitignored — expected | tracked, and why>`
- **Scratch directory, outside the repo,** for story drafts and tracker payloads:
  `<e.g. /path/to/scratch>`

## Commands

Invoke tooling through the repo's documented entrypoint. Do **not** activate an
environment in the shell — it does not survive between tool calls. If the runner needs a
variable set at import time, include it in the command string.

- **Unit tests, full suite:** `<COMMAND>`
- **Unit tests, single path:** `<COMMAND with a <path> placeholder>`
- **Lint / format check:** `<COMMAND with a <paths> placeholder>`
- **Lint baseline:** `<clean | N pre-existing errors as of DATE — scope lint to changed
  paths only>`
- **Integration tests:** `<COMMAND, or "none">`
- **How integration tests are marked / excluded:** `<e.g. a marker, a category, a
  directory>`
- **E2E tests:** `<COMMAND, or "none">` — **cost to run:** `<e.g. builds images, needs
  Docker, ~8 min>`
- **Schema / spec validation:** `<OpenAPI lint, migration dry-run, codegen check, or
  "none">`
- **Build:** `<COMMAND, or "none">`

## Test layout

- **Unit tests live in:** `<path>`
- **Integration tests live in:** `<path>`
- **E2E tests live in:** `<path>`
- **File naming convention:** `<e.g. source my_file.py → tests/unit/test_my_file.py>`
- **Grouping convention within a file:** `<e.g. classes named Test<Scenario>>`
- **Shared fixture/helper conventions:** `<anything a test author must know>`

## Definition of Done, by file type

Keyed to what actually changed, not one checklist for everything. Adapt the rows; keep the
shape.

| What changed | What is required |
|---|---|
| Runtime behavior | `<unit tests in the location above + the lint command>` |
| API / schema definition | `<its validation command>` |
| Documentation only | `<no new tests>` |
| Pipeline / deployment config | `<explicit reviewer note describing deployment impact>` |
| Generated file | `<generator ran + the generated-matches-committed check>` |
| `<other file type this repo has>` | `<requirement>` |

## Decision surfaces

The recurring areas where this project makes non-obvious choices. These become knowledge
article tags and the axis `recall` filters on.

Aim for six to twelve, derived from where recent work actually made arguable decisions —
not from directory names. Retire a surface no article uses; split one that swallows
everything.

- `<surface-1>` — `<one line: what kind of decision lives here>`
- `<surface-2>` — `<...>`
- `<surface-3>` — `<...>`
- `<...>`

## Tracker

- **Tracker:** `<Azure DevOps | GitHub Issues | Jira | other>`
- **Where work items live:** `<org/project, repo, or board>`
- **Work item type used for stories:** `<type name>`
- **Estimate unit:** `<business days | points | t-shirt>` — **size ceiling:**
  `<e.g. 3 business days; split rather than exceed>`
- **Field mapping** — see `reference/tracker-integration.md` for the portable field set:

  | Portable field | This tracker's field |
  |---|---|
  | Title | `<field>` |
  | Description | `<field>` |
  | Proposed Fix | `<field, or "fold into Description">` |
  | Acceptance Criteria | `<field>` |
  | Estimate | `<field(s)>` |

- **Description length limit, if any:** `<e.g. 4000 characters>`
- **Known tracker quirks:** `<link to a dated quirks doc, or "none recorded yet">`

## Cross-repo contracts

Repos this one shares a contract with — a data schema, a queue message shape, an API
surface, an index definition. `e2e-verification` scans these.

| Repo | Shared contract | Where it is defined |
|---|---|---|
| `<repo>` | `<what is shared>` | `<file or path>` |

`<or: "none — this repo has no cross-repo contracts">`

## Observability

What a reviewer should check when behavior changes. Leave as "none" if the project has no
telemetry contract.

- **Structured events / metrics this project emits:** `<names, or "none">`
- **Where they land:** `<system>`
- **What must stay true when they change:** `<contract notes>`
