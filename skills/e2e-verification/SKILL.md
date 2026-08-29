---
name: e2e-verification
description: End-to-end and integration verification — cross-repo contract scan, test planning, running the suite, style and assertions. Use any time E2E or integration tests are mentioned.
---

# E2E Verification

End-to-end tests verify that the system produces the expected **observable side-effects** when
run against real or emulated dependencies. They are the tests that catch a contract mismatch
no unit test can see.

**Read `.claude/workflow-config.md`** for the E2E command and its cost, the test layout, and
the cross-repo contracts table.

## Step 1: Offer the verification scan

Before planning or writing tests, ask:

> Would you like me to run a **verification scan** first — check for contract mismatches and
> edge cases across repos — or skip straight to **planning and implementing E2E tests**?

Wait for the answer.

The scan is worth it whenever the branch touched anything another repo consumes. It is the
cheapest way to find a break that would otherwise surface as a confusing E2E failure.

## Step 2: The scan (if chosen)

Examine `git diff <base>...HEAD` and cross-reference against the repos named in the config's
cross-repo contracts table. Focus on:

- **Persisted data shape** — did the branch change fields read or written to a shared store?
  Check that seed data and fixture helpers still match.
- **Storage and naming conventions** — container or bucket names, path prefixes, lifecycle
  expectations. Verify fixtures reflect any change.
- **Index or schema fields** — added, renamed or removed. Check emulator seed schemas and
  helpers align.
- **API and trigger contracts** — did an input or output schema change? Verify every external
  caller still passes valid input.
- **Error and retry semantics** — new error codes, changed failure behavior. Check whether E2E
  assertions account for them.
- **Anything on a decision surface** the config names.

### Report findings by severity

1. **Breaking** — contract mismatches that will cause runtime or test failures.
2. **Warning** — potential issues depending on usage, e.g. a newly required field the seed data
   omits.
3. **Info** — worth noting but not blocking, e.g. a deprecated field still referenced.

Then ask:

> I found [N] issue(s) that may need attention. Should I **address these first**, or **proceed
> to test planning** and note these as known gaps?

Wait for the answer.

## Step 3: Plan the tests

Before writing any test code.

### Gather context

From `git diff <base>...HEAD`, summarize:

- New or modified entry points and flows — name plus what changed
- New or modified units of work and the side-effects they produce
- Changes to persisted shapes, storage conventions or index fields
- New or changed error and retry behavior

### Ask the user, one question at a time

Do not skip this, and do not batch:

- **Which flows should be covered?** All changed ones, a subset, or specific scenarios.
- **Are there edge cases the diff does not make obvious?** Partial failures, empty input sets,
  races between steps.
- **Should existing tests be updated rather than new ones written?** Name the candidates you
  found and ask for confirmation.
- **What seed data is required?** Be specific about preconditions.
- **Should any scenarios be explicitly excluded?** Already covered by unit tests, or out of
  scope.

### Draft the plan

Once answered, produce a concise plan listing:

- The test file path, new or existing, per the config's test layout
- Each test function name and the scenario it covers
- Seed data required
- The trigger and its expected input
- Side-effects to verify after completion
- Any new fixture helpers needed

**Present the plan and wait for approval before writing tests.**

## Step 4: Running the suite

Use the config's E2E command.

**Prompt the user before running.** The config records what the suite costs — building images,
starting dependencies, minutes of wall time. The user may prefer to run it in CI.

## Test Style

### Structure: Seed → Trigger → Wait → Verify → Cleanup

Every E2E test follows this shape:

```
def test_<scenario>(client):
    run_id = unique_id()                    # unique per run

    try:
        # SEED: insert test data into the dependencies
        # TRIGGER: invoke the entry point
        #   assert the response status FIRST, with the body in the message
        # WAIT: poll until a terminal state, via the shared helper
        #   assert the terminal state before checking any output field
        # VERIFY: assert observable side-effects in the dependencies
    finally:
        # CLEANUP: remove everything seeded
```

### Rules that make these tests trustworthy

- **Unique identifiers per run.** A test that reuses a fixed id passes once and then interferes
  with itself.
- **Clean up in a `finally` block**, so teardown happens even when an assertion fails.
- **Assert the response status first**, with a descriptive message including the response body.
  **Verify what the implementation actually returns** rather than assuming a conventional code.
- **Assert the terminal state before reading output fields.** Reading output from a run that
  failed produces a confusing assertion error instead of a clear one.
- **Assert observable side-effects in the dependencies**, not internal state.
- **Use the shared polling helper**, never a hand-rolled sleep loop, and never instantiate a
  client directly when a session-scoped one exists.
- **A test that must observe work in flight records its measured timing window** next to the
  fixture, along with the dial that widens it, and asserts against a floor rather than an exact
  duration. Otherwise the next person shrinks the payload for speed and silently makes the test
  inert.

### Naming

Name test functions after the scenario. Lowercase with underscores.

| Pattern | Example |
|---|---|
| Happy path | `test_deletes_expired_documents` |
| Edge case | `test_skips_already_deleted_documents` |
| Partial failure | `test_continues_after_single_delete_failure` |
| Empty input | `test_no_op_when_nothing_expired` |
| Validation | `test_rejects_missing_cutoff_time` |

### What not to test here

- **Individual unit logic** — that belongs in unit tests.
- **Anything mocked.** E2E tests run against real or emulated dependencies. A mock in an E2E
  test means the test is a unit test wearing a costume.
- **Internal implementation details** — how many sub-steps were spawned, which branch ran. Test
  the observable outcome, or the test breaks on every refactor.
- **Do not add docstrings to test functions.** The name should carry it.

## A Note On Skip Reasons

A `skip` with a stated reason is a claim, and claims should be checked. Three reasons that
have repeatedly turned out to be false:

- *"Cannot guarantee the timing window"* — often means the fixture is too fast, not that the
  system cannot be observed. Find the dial that widens the window.
- *"Cannot identify which worker holds the resource"* — often the mechanism exists and was not
  looked for.
- *"No input takes long enough"* — often the relevant bound is environment-driven and can simply
  be lowered.

State the mechanism and test it before writing a skip.
