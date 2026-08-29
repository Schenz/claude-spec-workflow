# Harness Setup

Claude Code configuration that makes this workflow work. Everything here is optional in the
sense that the skills run without it — and each item earns its place by removing friction or
preventing a class of mistake.

## The one idea to take away

**When a rule must hold regardless of what any session decides, it belongs in a hook, not in
guidance.**

Guidance in `CLAUDE.md` or memory can be read and rationalized past — a session can be told
something and still not do it, especially a long session under context pressure. A `PreToolUse`
hook is enforced by the harness. Before writing a standing rule as prose, ask whether it is
actually a hook.

`hooks/block_compound_bash.py` in this pack is a worked example.

## Permissions: broad on reading, narrow on destruction

The shape that matters is the split, not the specific entries.

**Allow generously for anything that reads, inspects or reports.** Every permission prompt on a
`git log` or a `ls` is friction on the verification-heavy work this pipeline is made of — and
the pipeline runs a *lot* of commands. Reading is cheap to permit and expensive to interrupt.

```jsonc
{
  "permissions": {
    "allow": [
      // inspection
      "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)",
      "Bash(grep:*)", "Bash(rg:*)", "Bash(find:*)", "Bash(wc:*)",
      "Bash(sort:*)", "Bash(uniq:*)", "Bash(cut:*)", "Bash(diff:*)",
      "Bash(file:*)", "Bash(stat:*)", "Bash(du:*)", "Bash(jq:*)",
      "Bash(pwd)", "Bash(which:*)", "Bash(env)",

      // version control and code review
      "Bash(git *)",
      "Bash(gh pr *)", "Bash(gh repo *)", "Bash(gh api:*)",

      // the project's own toolchain — name the entrypoints from
      // .claude/workflow-config.md explicitly
      "Bash(<TEST_RUNNER> *)", "Bash(<LINTER> *)", "Bash(<BUILD_TOOL> *)",

      // documentation domains only
      "WebFetch(domain:docs.python.org)"
    ],

    "deny": [
      "Bash(rm -rf /)", "Bash(rm -rf /*)", "Bash(rm -rf ~)",
      "Bash(sudo rm *)",
      "Bash(git push --force*)",
      "Bash(git reset --hard*)",
      "Bash(mkfs*)", "Bash(dd if=*)"
    ]
  }
}
```

**Deny the irreversibles outright** — not "ask", deny. The deny list should be short and
consist only of things you would never want, so that its presence never has to be reasoned
about. Note `git push --force` and `git reset --hard` sitting alongside `rm -rf`: rewriting
history destroys work exactly as thoroughly as deleting files.

Two habits worth keeping:

- **Allow the toolchain by its documented entrypoint**, matching what
  `.claude/workflow-config.md` says. If the config says `.venv/bin/pytest`, allow that — not a
  bare `pytest` that may resolve elsewhere.
- **Scope `WebFetch` to documentation domains.** Useful for consulting a vendor's docs mid-task,
  and narrow enough not to be a general web-browsing grant.

## The compound-bash hook

`hooks/block_compound_bash.py` blocks, at the `PreToolUse` boundary:

- unquoted `&&`, `;` and newline separators — one command per call
- inline heredocs
- a newline-then-`#` inside a quoted argument

Wire it in:

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 <repo>/.claude/hooks/block_compound_bash.py",
            "statusMessage": "Checking Bash command for compound/heredoc"
          }
        ]
      }
    ]
  }
}
```

**The rationale is throughput, not safety.** Simple single commands match an allowlist entry and
auto-approve; compound commands, heredoc bodies and commented multi-line blobs do not, so they
prompt every time. Blocking them forces the split-into-separate-calls or write-a-file pattern,
where each step auto-approves. On a long verification-heavy session this is the difference
between a flow and a stream of confirmation dialogs.

The scan is quote- and escape-aware, so operators inside quotes or after a backslash are
ignored — no false positives on URLs, `echo` strings, line continuations or
`find ... -exec ... \;`.

It copies verbatim. There is nothing project-specific in it.

## Model and effort

```jsonc
{
  "model": "<a large-context model>",
  "effortLevel": "xhigh"
}
```

Context size matters more here than in most workflows: a `TASKS.md` with evidence recorded
inline runs to hundreds of lines, and `pre-pr-review` reads four spec artifacts plus a diff plus
knowledge articles before it writes anything.

Two per-phase overrides worth knowing:

- **`execute-task-checklist` declares `model: sonnet`.** Task execution is prescriptive — the
  acceptance criteria, verification and rollback are already decided — so a mid-tier model fits.
  The expensive thinking happened at the planning rungs. Override upward for a genuinely hard
  task.
- **Run the final whole-branch review on the most capable model available.** It is the last
  gate before a PR.

## Transcript retention

```jsonc
{ "cleanupPeriodDays": 365 }
```

Worth raising deliberately. Session transcripts are the only record of *how* work was done — and
they are how you audit whether the workflow is actually being followed, which stages get
skipped, and where questions are being batched that should not be. The default retention is
short enough that this evidence is gone before you think to look for it.

## Commit attribution

```jsonc
{ "includeCoAuthoredBy": false }
```

Set this if the commit trail feeds a compliance or audit process that expects a single author
per commit. Harmless either way; just decide rather than inherit.

## `CLAUDE.md`

Keep it short and factual. What the project is, key directories, the commands, testing
conventions.

**Do not restate the workflow** — the skills carry it, and a second copy in `CLAUDE.md` drifts
from them. What belongs here is the ambient project knowledge every session needs regardless of
which skill is running:

```markdown
# <Project>

<One or two sentences: what it is, what it runs on.>

Base branch: `<base>`

## Key Directories
- `<dir>/` — <what lives here>

## Commands
- `<command>` — <what it does>

## Testing Conventions
- <where tests live, how they are named, how integration tests are marked>
- <fixture and helper conventions a test author must know>
```

Anything you find yourself wanting to write in the imperative — *always*, *never* — is a
candidate for a hook instead. Check before writing it as prose.
