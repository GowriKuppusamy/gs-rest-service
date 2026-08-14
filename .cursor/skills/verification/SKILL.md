---
name: verification
description: Runs the Agentic SDLC Verification phase — executes tests and acceptance checks against approved artifacts, records evidence, and produces docs/verification.md. Use after Code Review approval, or when the user invokes /verification or the Verification phase.
disable-model-invocation: true
---

# Verification Phase

Execute only the Verification phase. Run tests and checks to produce evidence. Do not start the Pull Request phase or open a PR.

## Prerequisites

Before starting:

1. Confirm `docs/code-review.md` is **human-approved** with disposition **Approved** or **Approved with conditions**.
2. Confirm prior artifacts exist: `docs/requirements.md`, `docs/implementation-summary.md`, `docs/implementation-plan.md`.
3. If code review is **Not approved**, stop and return to Implementation / Code Review.
4. If any approval is missing or unclear, stop and ask the user to complete the prior phase first.

Read acceptance criteria (`AC-*`) and the test plan (`TEST-*`) from prior artifacts.

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/requirements.md` | Acceptance criteria to verify |
| `docs/implementation-plan.md` | Planned tests and requirement mappings |
| `docs/implementation-summary.md` | Tests previously run and files changed |
| `docs/code-review.md` | Sign-off conditions to satisfy |
| Application codebase | Target of test and build commands |

Run verification commands yourself. Do not modify application source code unless a code-review condition requires a fix and the user explicitly authorizes it in this phase.

## Workflow

Copy and track progress:

```
Verification Progress:
- [ ] Step 1: Ingest artifacts and define verification scope
- [ ] Step 2: Execute automated checks
- [ ] Step 3: Verify acceptance criteria
- [ ] Step 4: Clarify with user (if needed)
- [ ] Step 5: Write docs/verification.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest artifacts and define verification scope

Capture:

- Jira issue ID and story summary
- Every `AC-*` criterion from requirements
- Every `TEST-*` entry from the implementation plan
- Code-review conditions that require verification evidence
- Commands appropriate for this project (build, unit tests, integration tests, lint)

List what will be run vs what cannot be run in this environment.

### Step 2: Execute automated checks

1. Run the project build and test commands (e.g., `./mvnw test`, `./gradlew test`, `npm test`).
2. Record the **exact command**, **exit code**, and **outcome** for each run.
3. If a command fails, document the failure; do not claim success.
4. If a command was not run, list it under **Not verified** — do not infer results from earlier phases.

Re-run tests even if `docs/implementation-summary.md` reports them passing; this phase produces independent evidence.

### Step 3: Verify acceptance criteria and documentation quality

For each `AC-*`:

1. Identify how it is verified (automated test, manual step, or inspection).
2. Record evidence linking the criterion to a test result or observed outcome.
3. Mark each criterion **Pass**, **Fail**, or **Not verified**.

Also verify the final output documentation:
- Required SDLC artifacts exist.
- Documents are internally consistent.
- Requirement IDs are traceable through the workflow.
- Acceptance criteria are reflected in verification evidence.
- No required sections are missing.
- No unsupported claims or unverified results are presented.

Perform manual checks only when automated tests cannot cover a criterion; describe exactly what was done.

### Step 4: Clarify with user

When verification is blocked (missing setup, credentials, environment, or ambiguous expected behavior):

1. Describe the blocker and affected `AC-*` items.
2. Ask a focused question. **Stop and wait** for answers.
3. Incorporate responses and re-run checks if needed.

Record unresolved items in the verification artifact.

### Step 5: Write docs/verification.md

Create or update `docs/verification.md` using this structure:

```markdown
# Verification: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Requirements | docs/requirements.md (approved [YYYY-MM-DD]) |
| Code review | docs/code-review.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph: overall verification outcome]

## Automated checks

| Command | Exit code | Result | Notes |
|---------|-----------|--------|-------|
| `[exact command]` | 0 / non-zero | Pass / Fail / Not run | … |

## Acceptance criteria verification

| ID | Criterion | Method | Evidence | Result |
|----|-----------|--------|----------|--------|
| AC-001 | … | Test / Manual / Inspection | TEST-… or description | Pass / Fail / Not verified |

## Code-review conditions verified

| Condition | Evidence | Result |
|-----------|----------|--------|
| … | … | Pass / Fail / Not verified |

## Regression check

[Confirmation that existing tests still pass, or documented failures]

## Not verified

- … (empty if none)

## Open items

- … (empty if none)

## Recommendation

| Outcome | Selected |
|---------|----------|
| Verified — ready for Pull Request | ☐ |
| Not verified — return to Implementation | ☐ |
```

Update existing files in place when revising; keep **Last updated** current.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Verification phase complete

**Artifact:** docs/verification.md
**Jira:** [issue ID or N/A]
**Acceptance criteria:** [N] pass, [N] fail, [N] not verified
**Automated checks:** [N] pass, [N] fail, [N] not run
**Open items:** [list or "None"]

Ready for human review. Pull Request must not begin until this evidence is approved.
```

**Stop here.** Do not proceed to Pull Request or any later phase until the user explicitly approves `docs/verification.md`.

If any blocking `AC-*` fails, recommend **Not verified — return to Implementation** and stop.
