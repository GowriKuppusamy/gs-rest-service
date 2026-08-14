---
name: implementation
description: Runs the Agentic SDLC Implementation phase — executes approved docs/implementation-plan.md tasks, modifies application source code, adds tests, and produces docs/implementation-summary.md. Use after Implementation Planning approval, or when the user invokes /implementation or the Implementation phase.
disable-model-invocation: true
---

# Implementation Phase

Execute only the Implementation phase. Modify application source code and tests as defined in the approved plan. Do not start Code Review or produce code-review artifacts.

## Prerequisites

Before starting:

1. Confirm `docs/implementation-plan.md` is **human-approved**.
2. Confirm prior artifacts exist and were approved: `docs/requirements.md`, `docs/architecture.md`, `docs/design-review.md`.
3. If any approval is missing or unclear, stop and ask the user to complete the prior phase first.

Read the implementation plan and follow its task order (`TASK-*`) and test plan (`TEST-*`).

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/implementation-plan.md` | Approved tasks, file targets, order, and test plan |
| `docs/requirements.md` | Requirement IDs and acceptance criteria to satisfy |
| `docs/architecture.md` | Design decisions to follow |
| `docs/design-review.md` | Conditions that must be addressed |
| Existing codebase | Patterns, conventions, and code to extend or preserve |

Before editing any file, read its current contents and surrounding context.

## Workflow

Copy and track progress:

```
Implementation Progress:
- [ ] Step 1: Ingest plan and codebase context
- [ ] Step 2: Execute tasks in order
- [ ] Step 3: Clarify with user (if blocked)
- [ ] Step 4: Implement tests and run verification
- [ ] Step 5: Update docs/implementation-plan.md statuses
- [ ] Step 6: Write docs/implementation-summary.md
- [ ] Step 7: Report and request approval
```

### Step 1: Ingest plan and codebase context

Capture:

- Jira issue ID and story summary
- Task list in dependency order
- Files and areas to modify
- Preserved functionality that must not regress
- Design-review conditions assigned to tasks
- Test plan entries and their requirement mappings

### Step 2: Execute tasks in order

For each `TASK-*` in the plan's implementation order:

1. Confirm prerequisite tasks are complete.
2. Read target files before editing.
3. Implement only what the task and requirement refs authorize — do not expand scope.
4. Follow existing project conventions and the approved architecture.
5. Mark the task **In progress**, then **Complete** or **Blocked** in your working notes.

**Preserve existing functionality** unless the plan explicitly authorizes a breaking change. When modifying shared code, verify callers and tests still behave as documented.

### Step 3: Clarify with user

When blocked by ambiguity, missing information, or a conflict with existing code:

1. Describe the blocker tied to the task and requirement ID.
2. Ask a focused question. **Stop and wait** for answers.
3. Incorporate the response and continue.
4. Do not guess or silently change scope.

Record unresolved blockers in the summary artifact.

### Step 4: Implement tests and run verification

For each `TEST-*` in the test plan:

1. Add or update tests for new functionality.
2. Run the relevant test, build, or lint commands for this project.
3. Record **only results you actually executed** — include the exact command and outcome.
4. If a test was not run, list it under **Not verified**; do not claim it passed.

Fix failures within approved scope before completing the phase. If a failure requires plan changes, stop and ask the user rather than improvising.

### Step 5: Update docs/implementation-plan.md statuses

Update the **Status** column for each `TASK-*` and note any deviations:

| Status | Meaning |
|--------|---------|
| Complete | Task implemented as planned |
| Blocked | Could not finish — reason documented |
| Deferred | Explicitly postponed with user approval |

Do not rewrite the plan's scope or add unauthorized tasks.

### Step 6: Write docs/implementation-summary.md

Create or update `docs/implementation-summary.md` using this structure:

```markdown
# Implementation Summary: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Implementation plan | docs/implementation-plan.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph describing what was implemented]

## Tasks completed

| ID | Task | Status | Notes |
|----|------|--------|-------|
| TASK-001 | … | Complete / Blocked / Deferred | … |

## Files changed

| File | Change |
|------|--------|
| `path/to/file` | … |

## Tests

| ID | Test | Command run | Result |
|----|------|-------------|--------|
| TEST-001 | … | `[exact command]` | Pass / Fail / Not run |

## Requirement coverage

| Requirement ID | Implemented by | Verified by |
|----------------|----------------|-------------|
| FR-001 | TASK-… | TEST-… |

## Design-review conditions addressed

| Condition | Addressed by | Status |
|-----------|--------------|--------|
| … | TASK-… | Done / Partial / Not done |

## Preserved functionality

[Confirmation that existing behavior was maintained, or documented exceptions]

## Not verified

- … (commands or tests not run — empty if none)

## Open items

- … (empty if none)
```

### Step 7: Report and request approval

End the phase with a completion report:

```markdown
## Implementation phase complete

**Artifact:** docs/implementation-summary.md
**Jira:** [issue ID or N/A]
**Tasks:** [N] complete, [N] blocked/deferred
**Files changed:** [N]
**Tests run:** [N] pass, [N] fail, [N] not verified
**Open items:** [list or "None"]

Ready for human review. Code Review must not begin until this implementation is approved.
```

**Stop here.** Do not proceed to Code Review or any later phase until the user explicitly approves the implementation.
