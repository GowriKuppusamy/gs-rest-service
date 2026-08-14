---
name: code-review
description: Runs the Agentic SDLC Code Review phase — reviews implementation changes against approved artifacts, records findings, and produces docs/code-review.md sign-off. Use after Implementation approval, or when the user invokes /code-review or the Code Review phase.
disable-model-invocation: true
---

# Code Review Phase

Execute only the Code Review phase. Do not start Verification, modify application source code, or produce verification artifacts.

## Prerequisites

Before starting:

1. Confirm `docs/implementation-summary.md` exists and the implementation is **human-approved**.
2. Confirm prior artifacts exist and were approved: `docs/requirements.md`, `docs/architecture.md`, `docs/design-review.md`, `docs/implementation-plan.md`.
3. If implementation is incomplete or approval is missing, stop and ask the user to complete the prior phase first.

Read all artifacts and note requirement IDs (`FR-*`, `NFR-*`, `SEC-*`, `AC-*`), task IDs (`TASK-*`), and test IDs (`TEST-*`).

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/implementation-summary.md` | What was built, files changed, and test results claimed |
| `docs/implementation-plan.md` | Planned tasks, tests, and requirement mappings |
| `docs/requirements.md` | Scope, requirements, and acceptance criteria |
| `docs/architecture.md` | Design decisions the code should follow |
| Code changes | `git diff` and modified files (read-only review) |

Inspect the actual code diff. Do not change source files during this phase unless the user explicitly asks you to apply approved fixes.

## Workflow

Copy and track progress:

```
Code Review Progress:
- [ ] Step 1: Ingest artifacts and code changes
- [ ] Step 2: Perform structured review
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Draft findings and recommendation
- [ ] Step 5: Write docs/code-review.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest artifacts and code changes

Capture:

- Jira issue ID and story summary
- Files changed vs `docs/implementation-summary.md`
- Tasks marked complete, blocked, or deferred
- Tests reported as run, passed, failed, or not verified
- Requirement and acceptance-criteria coverage claimed in the summary

Run `git diff` (or review the user's indicated change set) to inspect the actual implementation.

### Step 2: Perform structured review

Evaluate the code against approved artifacts:

| Review area | Check |
|-------------|-------|
| Plan adherence | Changes match `TASK-*` scope; no unauthorized work |
| Requirement coverage | In-scope `FR-*`, `NFR-*`, and `SEC-*` are implemented |
| Acceptance criteria | Each `AC-*` is addressable from the code and tests |
| Architecture alignment | Code follows approved components, interfaces, and decisions |
| Correctness | Logic, error handling, and edge cases are sound |
| Preserved functionality | Existing behavior not broken unless explicitly authorized |
| Tests | New functionality has tests; existing tests not weakened |
| Security | No secrets exposed; `SEC-*` controls implemented |
| Code quality | Readable, consistent with project conventions |
| Scope | No silent scope expansion beyond approved requirements |
| Error Handling | API failures, missing files, empty repositories, invalid input, and unexpected failures are handled gracefully |
| Test Coverage | Happy paths and Not Found / missing-field / edge cases are covered |
| Code Clarity | Names and logic are clear and maintainable |
| DRY Principle | Identify duplicated logic that should be refactored |
| Dependency Safety | Check dependency versions and flag known security/vulnerability concerns |

Classify each finding:

- **Blocking** — must fix before sign-off
- **Major** — should fix; may proceed with documented conditions
- **Minor** — recommendation only

Cross-check `docs/implementation-summary.md` claims against the diff. Flag unverified test results the summary marks as passed without evidence you can confirm from this review.

### Step 3: Clarify with user

When intent or a finding needs a decision:

1. Describe the issue, file/line context, and requirement refs.
2. Ask a focused question. **Stop and wait** for answers.
3. Incorporate responses into findings.
4. Repeat until blocking items are resolved, accepted, or referred back to Implementation.

If blocking issues require code changes, document them and recommend returning to Implementation. Do not edit source files unless the user explicitly requests fixes during this phase.

### Step 4: Draft findings and recommendation

Summarize:

- Overall assessment (ready / ready with conditions / not ready)
- Finding counts by severity
- Gaps between plan, requirements, and actual code
- Discrepancies in reported vs reviewable test evidence
- Recommended sign-off disposition: **Approved**, **Approved with conditions**, or **Not approved — return to Implementation**

### Step 5: Write docs/code-review.md

Create or update `docs/code-review.md` using this structure:

```markdown
# Code Review: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Requirements | docs/requirements.md (approved [YYYY-MM-DD]) |
| Architecture | docs/architecture.md (approved [YYYY-MM-DD]) |
| Implementation plan | docs/implementation-plan.md (approved [YYYY-MM-DD]) |
| Implementation summary | docs/implementation-summary.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph: overall review outcome and recommendation]

## Review checklist

| Area | Result | Notes |
|------|--------|-------|
| Plan adherence | Pass / Fail | … |
| Requirement coverage | Pass / Fail | … |
| Acceptance criteria | Pass / Fail | … |
| Architecture alignment | Pass / Fail | … |
| Correctness | Pass / Fail | … |
| Preserved functionality | Pass / Fail | … |
| Tests | Pass / Fail | … |
| Security | Pass / Fail | … |
| Code quality | Pass / Fail | … |
| Scope alignment | Pass / Fail | … |

## Findings

| ID | Severity | Finding | Location | Requirement refs | Recommendation | Status |
|----|----------|---------|----------|------------------|----------------|--------|
| CR-001 | Blocking / Major / Minor | … | `path:line` | FR-… | … | Open / Resolved / Accepted |

## Requirement verification

| Requirement ID | Implemented | Verified by tests | Notes |
|----------------|-------------|-------------------|-------|
| FR-001 | Yes / No / Partial | Yes / No | … |

## Files reviewed

| File | Assessment |
|------|------------|
| `path/to/file` | … |

## Accepted conditions

- … (empty if none)

## Open questions

- … (empty if none)

## Sign-off recommendation

| Disposition | Selected |
|-------------|----------|
| Approved | ☐ |
| Approved with conditions | ☐ |
| Not approved — return to Implementation | ☐ |

**Conditions (if applicable):**
- …
```

Update existing files in place when revising; keep **Last updated** current.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Code Review phase complete

**Artifact:** docs/code-review.md
**Jira:** [issue ID or N/A]
**Review result:** [Approved / Approved with conditions / Not approved]
**Findings:** [N] blocking, [N] major, [N] minor
**Coverage gaps:** [list or "None"]
**Open items:** [list or "None"]

Ready for human review. Verification must not begin until this sign-off is approved.
```

**Stop here.** Do not proceed to Verification or any later phase until the user explicitly approves `docs/code-review.md`.

If the recommendation is **Not approved**, stop after reporting and wait for Implementation to address findings and be re-reviewed.
