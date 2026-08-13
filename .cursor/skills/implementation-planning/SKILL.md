---
name: implementation-planning
description: Runs the Agentic SDLC Implementation Planning phase — reads approved design review sign-off and prior artifacts, breaks work into traceable tasks, and produces docs/implementation-plan.md. Use after Design Review approval, or when the user invokes /implementation-planning or the Implementation Planning phase.
disable-model-invocation: true
---

# Implementation Planning Phase

Execute only the Implementation Planning phase. Do not start Implementation, modify application source code, or write production code.

## Prerequisites

Before starting:

1. Confirm `docs/requirements.md` is **human-approved**.
2. Confirm `docs/architecture.md` is **human-approved**.
3. Confirm `docs/design-review.md` is **human-approved** with disposition **Approved** or **Approved with conditions**.
4. If design review is **Not approved**, stop and return to Architecture / Design Review.
5. If any approval is missing or unclear, stop and ask the user to complete the prior phase first.

Read all three artifacts and note requirement IDs (`FR-*`, `NFR-*`, `SEC-*`, `AC-*`), architecture components, and any design-review conditions.

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/requirements.md` | Scope, requirements, and acceptance criteria to implement |
| `docs/architecture.md` | Components, interfaces, and design decisions to follow |
| `docs/design-review.md` | Sign-off conditions and findings to address during implementation |
| Existing codebase | Read-only inventory of files, patterns, and tests to extend |

Survey the codebase read-only to identify concrete files, modules, and test locations. Do not change source files during this phase.

## Workflow

Copy and track progress:

```
Implementation Planning Progress:
- [ ] Step 1: Ingest approved artifacts and codebase
- [ ] Step 2: Decompose work and identify gaps
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Draft implementation plan
- [ ] Step 5: Write docs/implementation-plan.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest approved artifacts and codebase

Capture:

- Jira issue ID and story summary
- In-scope requirements and acceptance criteria
- Architecture components and interfaces to build or extend
- Design-review conditions that must be satisfied
- Existing code paths that must be **preserved** unless a prior phase authorized breaking changes
- Current test layout and conventions

### Step 2: Decompose work and identify gaps

Break implementation into ordered, traceable tasks:

- Map each task to requirement IDs and architecture components
- Identify files or modules to create or modify (paths only — no edits yet)
- Define test tasks for new functionality (unit, integration, or acceptance-level as appropriate)
- Sequence tasks by dependency (e.g., model → service → controller → tests)
- Flag design-review conditions not yet assigned to a task
- Note risks, unknowns, or missing information

List findings as **Resolved from artifacts/codebase** vs **Needs clarification**.

### Step 3: Clarify with user

When task breakdown or approach is ambiguous:

1. Ask focused questions tied to requirement IDs or design decisions.
2. **Stop and wait** for answers. Do not assume or expand scope silently.
3. Incorporate responses into the plan.
4. Repeat until blocking ambiguities are resolved or explicitly deferred.

Record deferred items under **Open questions** in the artifact.

### Step 4: Draft implementation plan

The plan must:

- Cover all in-scope requirements without exceeding approved scope
- Address design-review conditions explicitly
- Preserve existing functionality; call out regression-sensitive areas
- Include a test task for every new behavior
- Be executable step-by-step during the Implementation phase

Assign stable task IDs (e.g., `TASK-001`).

### Step 5: Write docs/implementation-plan.md

Create or update `docs/implementation-plan.md` using this structure:

```markdown
# Implementation Plan: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Requirements | docs/requirements.md (approved [YYYY-MM-DD]) |
| Architecture | docs/architecture.md (approved [YYYY-MM-DD]) |
| Design review | docs/design-review.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph describing the implementation approach]

## Scope reminder

### In scope
- …

### Out of scope
- …

## Preserved functionality

[Existing behavior that must not regress]

## Task breakdown

| ID | Task | Files / areas | Requirement refs | Depends on | Status |
|----|------|---------------|------------------|------------|--------|
| TASK-001 | … | `path/to/file` | FR-…, AC-… | — | Planned |

## Test plan

| ID | Test | Verifies | Type | Requirement refs |
|----|------|----------|------|------------------|
| TEST-001 | … | … | Unit / Integration / Manual | AC-… |

## Design-review conditions

| Condition | Addressed by |
|-----------|--------------|
| … | TASK-… |

## Requirement coverage

| Requirement ID | Task(s) | Test(s) |
|----------------|---------|---------|
| FR-001 | TASK-… | TEST-… |

## Implementation order

1. TASK-…
2. TASK-…

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| … | … |

## Open questions

- … (empty if none)
```

Update existing files in place when revising; keep **Last updated** current.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Implementation Planning phase complete

**Artifact:** docs/implementation-plan.md
**Jira:** [issue ID or N/A]
**Tasks defined:** [N]
**Tests planned:** [N]
**Requirements covered:** [N]/[total]
**Open items:** [list or "None"]

Ready for human review. Implementation must not begin until this artifact is approved.
```

**Stop here.** Do not proceed to Implementation or any later phase until the user explicitly approves `docs/implementation-plan.md`.
