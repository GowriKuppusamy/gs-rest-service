---
name: architecture
description: Runs the Agentic SDLC Architecture phase — reads approved docs/requirements.md, analyzes the codebase, defines system design, and produces docs/architecture.md. Use when starting architecture design, after Requirements approval, or when the user invokes /architecture or the Architecture phase.
disable-model-invocation: true
---

# Architecture Phase

Execute only the Architecture phase. Do not start Design Review, modify application source code, or produce implementation-plan artifacts.

## Prerequisites

Before starting:

1. Confirm `docs/requirements.md` exists and is **human-approved**.
2. If approval is missing or unclear, stop and ask the user to approve Requirements first.

Read the full requirements artifact and note all requirement IDs (`FR-*`, `NFR-*`, `SEC-*`, `AC-*`).

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/requirements.md` | Approved functional, non-functional, security, and acceptance criteria |
| Existing codebase | Current components, patterns, constraints, and extension points |
| Project docs | README, ADRs, or conventions that constrain design choices |

Review the codebase read-only to understand what exists. Do not change source files during this phase.

## Workflow

Copy and track progress:

```
Architecture Progress:
- [ ] Step 1: Ingest requirements and codebase context
- [ ] Step 2: Identify design decisions and gaps
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Draft architecture
- [ ] Step 5: Write docs/architecture.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest requirements and codebase context

From `docs/requirements.md`, capture:

- Jira issue ID and story summary
- In-scope capabilities and explicit out-of-scope items
- All requirement IDs and acceptance criteria
- Assumptions, dependencies, and open questions carried forward

From the codebase, capture:

- Existing layers, modules, and entry points
- Data stores, external integrations, and deployment context (if present)
- Patterns already in use that new design should follow or consciously extend

### Step 2: Identify design decisions and gaps

Determine what the architecture must resolve:

- System boundaries and major components
- Component responsibilities and interactions
- Data model and persistence approach
- API or interface contracts (high level)
- Security controls mapped to `SEC-*` requirements
- How each `NFR-*` requirement is addressed (performance, reliability, etc.)
- Technology choices and rationale where not already fixed
- Trade-offs, alternatives considered, and recommended approach

List findings as **Decided from requirements/codebase** vs **Needs clarification**.

### Step 3: Clarify with user

When a design decision is ambiguous or has meaningful trade-offs:

1. Present options with concise pros/cons tied to requirements.
2. Ask focused questions. **Stop and wait** for answers.
3. Incorporate responses into the architecture draft.
4. Repeat until blocking decisions are resolved or explicitly deferred.

Record deferred decisions under **Open questions / pending decisions** in the artifact.

### Step 4: Draft architecture

Produce a design that:

- Satisfies approved requirements without expanding scope
- Maps every significant decision to one or more requirement IDs
- Fits the existing codebase unless a justified structural change is documented
- Addresses security and non-functional requirements explicitly
- Is implementable — clear enough for Design Review and Implementation Planning

Use diagrams (mermaid or ASCII) when they clarify component or data flow.

### Step 5: Write docs/architecture.md

Create or update `docs/architecture.md` using this structure:

```markdown
# Architecture: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Requirements | docs/requirements.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph describing the proposed system design]

## Context

[Problem space, actors, external systems — C4-style context if helpful]

## Components

| Component | Responsibility | Requirement refs |
|-----------|----------------|------------------|
| … | … | FR-…, NFR-… |

## Data design

[Entities, storage, key relationships — or "N/A" if none]

## Interfaces

[APIs, events, or integration points at a contract level]

## Security architecture

| Control | Approach | Requirement refs |
|---------|----------|------------------|
| … | … | SEC-… |

## Non-functional approach

| Requirement | Design approach |
|-------------|-----------------|
| NFR-001 | … |

## Key decisions

| Decision | Choice | Rationale | Alternatives considered |
|----------|--------|-----------|-------------------------|
| … | … | … | … |

## Requirement coverage

| Requirement ID | Architectural response |
|----------------|------------------------|
| FR-001 | … |

## Assumptions and dependencies

- …

## Open questions

- … (empty if none)
```

Update existing files in place when revising; keep **Last updated** current.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Architecture phase complete

**Artifact:** docs/architecture.md
**Jira:** [issue ID or N/A]
**Components defined:** [N]
**Requirements covered:** [N]/[total] FR, [N]/[total] NFR, [N]/[total] SEC
**Open items:** [list or "None"]

Ready for human review. Design Review must not begin until this artifact is approved.
```

**Stop here.** Do not proceed to Design Review or any later phase until the user explicitly approves `docs/architecture.md`.
