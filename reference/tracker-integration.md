# Tracker Integration

Reading and writing work items from the shell, so drafting and filing are separate steps and
neither requires clicking through a web UI.

`write-story` owns the **format**. This document covers the **mechanics** of filing.

## The separation, and why it matters

Drafting is judgment; filing is mechanics.

```
finding ──► write-story ──► draft file (scratch dir, outside the repo)
                                │
                                ▼
                          payload files ──► apply, dry-run first ──► tracker
```

Keeping them apart means you can draft with no tracker configured at all, review a batch of
drafts as prose before any of them exists as an item, and re-run a failed filing without
re-deciding what the item says.

## Nine principles

These hold across trackers. The per-tracker specifics come after.

### 1. Reuse the identity the developer already has

No personal access tokens in files or environment variables. Every major tracker has a CLI that
already holds a session, and a way to mint a token for the tracker's own audience rather than
for the cloud provider's API.

A PAT is a long-lived secret that ends up in a dotfile. The identity the developer already
authenticated is better in every respect.

### 2. Order writes by reversibility

**The single most useful rule here.**

```
1. a comment      deletable, burns no id — use it to prove write access
2. a create       consumes an id permanently; deletion usually only recycle-bins
3. an update      touches something that already exists and has history
```

Prove access with a comment first. If credentials or field validation are wrong, you find out on
the cheapest possible operation instead of on a create that permanently consumes an item number.

### 3. Optimistic concurrency on every update

Include a revision or version test with any update, so the write **rejects rather than
clobbers** if someone edited in between. This is not hypothetical — it happens the first time two
people triage the same board.

### 4. Dry-run by default

Generate payloads as files, apply them as an explicit second step:

```
<tool> payloads/                     # dry run — prints what would be sent
<tool> payloads/ --only 05 --write   # send one step
<tool> payloads/ --write             # send all
```

Name payloads `NN-<verb>-<target>` so they sort into execution order, and so a partially-applied
batch can be resumed from a known point.

### 5. Payloads and drafts stay out of version control

Both are narrative prose about work. Gitignore the payload directory; keep drafts outside the
repo entirely. Neither should ever be reviewed as part of a code change.

### 6. Author once in Markdown, convert at the boundary

Write the prose once, in Markdown, and convert to whatever the target field expects. **Never
maintain two copies** — they drift, and the drift is invisible until someone reads the wrong one.

### 7. Preflight before sending

Validate locally, before any request:

- Required fields present — including fields the API reports as optional but a process rule
  requires
- Picklist values are exact members of the allowed set
- Escaping is correct for the target field's format
- Length limits respected

A preflight that catches a bad picklist value saves a round trip and an error message that names
the wrong thing.

### 8. Append, never overwrite

When adding to a field that already has content, concatenate onto the current value at send
time — read the current value, append, write. Never send a field's new content assuming you know
what is already there.

### 9. Keep a dated tracker-quirks doc

The highest-value artifact in this whole area. Each entry: **symptom → cause → what to do**,
with the date it was measured.

Tracker quirks are not discoverable from field definitions, they differ per organisation because
of process customization, and they cost real time every single time they are rediscovered. This
is the same reasoning as `docs/knowledge/`, applied to the tracker.

## Per-tracker notes

### Azure DevOps

- **Auth:** `az rest` with the Azure DevOps resource id, which mints a token for
  `dev.azure.com` rather than for ARM. `az boards` needs the `azure-devops` extension added once.
- **Narrative field format is per-item and effectively immutable.** Each work item carries a
  top-level property mapping each multi-line field to `markdown` or `html`. It is not a field, so
  searching the field definitions for a format marker finds nothing. API-created items tend to
  get `html`; items touched in the newer UI carry `markdown`. **Match the target rather than
  fighting it** — every route to changing it fails, and several fail *silently* with HTTP 200.
- **Comments are a separate endpoint**, and `format` must be a **query parameter**. Passing it in
  the body returns 200 and is ignored. Adding a comment through the work-item patch's history
  field forces HTML.
- **Process rules can require a field the API says is optional.** A rule conditioned on the
  first save requires fields that report `alwaysRequired: false`. Later state transitions add
  more. Discover these by reading the process, not the field definitions.
- **Picklist values containing `&` must arrive raw.** Escaped, they fail validation with an error
  naming the field rather than the escaping.
- **Watch for parallel size fields.** A transition gate may require one size field while the team
  populates a different one. Set both to the same value and no transition can be blocked.

### GitHub Issues

- **Auth:** `gh` CLI, which already holds a session. `gh issue create`, `gh issue edit`,
  `gh api` for anything the porcelain does not cover.
- **Markdown throughout** — principle 6 is nearly free; no format negotiation.
- **The five fields map onto body sections**, since GitHub has one body rather than several
  narrative fields. Use consistent `##` headings so they can be parsed back out.
- **Estimates live in Projects**, not on the issue, as a custom number field — reachable through
  the GraphQL API rather than the issues REST endpoint.
- **Labels are the main structured axis.** Decide a convention early; retrofitting labels across
  a populated repo is tedious.
- **Optimistic concurrency is weaker.** There is no revision test on issue edits, so read
  immediately before writing and keep the window short.

### Jira

- **Auth:** an API token with basic auth, or OAuth for a real integration. Closest of the three
  to needing a stored secret — scope it narrowly.
- **Description format depends on the deployment.** Cloud uses a structured document format;
  Server and Data Center use wiki markup. Principle 6 matters most here: author Markdown, convert
  at the boundary, and confirm which format the instance expects before generating a batch.
- **Custom fields are opaque ids.** Acceptance Criteria and Story Points are almost always
  custom fields with ids like `customfield_10021`. Record the mapping in
  `.claude/workflow-config.md`; the ids differ per instance.
- **Screens and workflows gate which fields are settable in which state** — the same class of
  surprise as ADO's process rules, from a different mechanism. A field can exist, be required,
  and not be on the create screen.
- **Version-check on update** via the issue's `updated` timestamp, since there is no revision
  counter.

## The portable field set

`write-story` emits these five. Map them in `.claude/workflow-config.md`.

| Portable field | Azure DevOps | GitHub Issues | Jira |
|---|---|---|---|
| Title | `System.Title` | issue title | Summary |
| Description | `System.Description` | body `## Description` | Description |
| Proposed Fix | a `ProposedFix` field | body `## Proposed Fix` | custom field |
| Acceptance Criteria | an `AcceptanceCriteria` field | body `## Acceptance Criteria` | custom field |
| Estimate | story-points **and** size fields | Projects number field | Story Points custom field |

Where a tracker has no distinct field, fold the content into the body under a heading. Do not
drop it — Proposed Fix is what makes an item pickup-able by someone who did not find the problem.

## A minimal adapter

If you build tooling rather than filing by hand, this is the shape that has proven durable:

| Piece | Responsibility |
|---|---|
| Library | Read, write, op builders, format conversion, preflight |
| Read CLI | Show an item, list children of an epic, list comments, show field formats. Read-only apart from adding a comment. |
| Payload applier | Applies a payload directory in sorted order. **Dry-run by default**, `--write` to send, `--only NN` for one step. |
| Payload builder | A copyable template — write the item content once, generate the payloads |
| `payloads/` | Gitignored |

Keep the read CLI genuinely read-only apart from comments. It gets used casually, and casual use
should not be able to mutate a board.
