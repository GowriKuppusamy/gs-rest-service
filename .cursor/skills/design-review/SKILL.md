---
name: design-review
description: Runs the Agentic SDLC Design Review phase — validates docs/architecture.md against approved docs/requirements.md, records findings, and produces docs/design-review.md sign-off. Use after Architecture approval, or when the user invokes /design-review or the Design Review phase.
disable-model-invocation: true
---

# Design Review Phase

Execute only the Design Review phase. Do not start Implementation Planning, modify application source code, or produce implementation-plan artifacts.

## Prerequisites

Before starting:

1. Confirm `docs/requirements.md` exists and is **human-approved**.
2. Confirm `docs/architecture.md` exists and is **human-approved**.
3. If either approval is missing or unclear, stop and ask the user to complete the prior phase first.

Read both artifacts and note all requirement IDs (`FR-*`, `NFR-*`, `SEC-*`, `AC-*`) and architecture decision references.

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/requirements.md` | Approved scope, requirements, and acceptance criteria |
| `docs/architecture.md` | Proposed design, decisions, and requirement coverage |
| Existing codebase | Read-only check of feasibility and alignment with current patterns |

Do not change application source files during this phase.

## Workflow

Copy and track progress:

```
Design Review Progress:
- [ ] Step 1: Ingest requirements and architecture
- [ ] Step 2: Perform structured review
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Draft review findings and recommendation
- [ ] Step 5: Write docs/design-review.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest requirements and architecture

Capture from the approved artifacts:

- Jira issue ID and story summary
- In-scope vs out-of-scope boundaries
- Every requirement ID and acceptance criterion
- Architecture components, interfaces, data design, security, and NFR approach
- Open questions and assumptions carried from prior phases

### Step 2: Perform structured review

Evaluate the architecture against requirements and feasibility:

| Review area | Check |
|-------------|-------|
| Coverage | Every in-scope `FR-*`, `NFR-*`, and `SEC-*` has an architectural response |
| Acceptance criteria | Each `AC-*` is achievable from the proposed design |
| Consistency | Components, interfaces, and data design align without contradictions |
| Scope | Design stays within approved requirements; no silent scope expansion |
| Feasibility | Design fits the existing codebase and stated dependencies |
| Security | Controls address `SEC-*` requirements; no obvious gaps |
| Non-functional | `NFR-*` approaches are concrete enough to implement and verify |
| Risks | Technical, integration, and operational risks are identified |
| Testability | Design supports verification of acceptance criteria |

Classify each finding:

- **Blocking** — must resolve before sign-off
- **Major** — should resolve; may proceed with documented conditions
- **Minor** — recommendation only

List findings as **Pass** vs **Issue found**.

### Step 3: Clarify with user

When a finding needs a product or technical decision:

1. Describe the issue, impact, and options tied to requirement IDs.
2. Ask focused questions. **Stop and wait** for answers.
3. Incorporate responses into findings and recommendations.
4. Repeat until blocking items are resolved, deferred with explicit acceptance, or referred back to Architecture.

If blocking issues require architecture changes, document them and recommend updating `docs/architecture.md` before sign-off. Do not edit `docs/architecture.md` unless the user explicitly asks you to apply approved corrections during this phase.

### Step 4: Draft review findings and recommendation

Summarize:

- Overall assessment (ready / ready with conditions / not ready)
- Finding counts by severity
- Requirement coverage gaps
- Accepted risks and deferred items
- Recommended sign-off disposition: **Approved**, **Approved with conditions**, or **Not approved — return to Architecture**

### Step 5: Write docs/design-review.md

Create or update `docs/design-review.md` using this structure:

```markdown
# Design Review: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Requirements | docs/requirements.md (approved [YYYY-MM-DD]) |
| Architecture | docs/architecture.md (approved [YYYY-MM-DD]) |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph: overall review outcome and recommendation]

## Review checklist

| Area | Result | Notes |
|------|--------|-------|
| Requirement coverage | Pass / Fail | … |
| Acceptance criteria achievability | Pass / Fail | … |
| Internal consistency | Pass / Fail | … |
| Scope alignment | Pass / Fail | … |
| Feasibility | Pass / Fail | … |
| Security | Pass / Fail | … |
| Non-functional approach | Pass / Fail | … |
| Testability | Pass / Fail | … |

## Findings

| ID | Severity | Finding | Requirement refs | Recommendation | Status |
|----|----------|---------|------------------|----------------|--------|
| DR-001 | Blocking / Major / Minor | … | FR-… | … | Open / Resolved / Accepted |

## Requirement coverage verification

| Requirement ID | Covered | Evidence / gap |
|----------------|---------|----------------|
| FR-001 | Yes / No / Partial | … |

## Accepted risks and conditions

- … (empty if none)

## Open questions

- … (empty if none)

## Sign-off recommendation

| Disposition | Selected |
|-------------|----------|
| Approved | ☐ |
| Approved with conditions | ☐ |
| Not approved — return to Architecture | ☐ |

**Conditions (if applicable):**
- …
```

Update existing files in place when revising; keep **Last updated** current.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Design Review phase complete

**Artifact:** docs/design-review.md
**Jira:** [issue ID or N/A]
**Review result:** [Approved / Approved with conditions / Not approved]
**Findings:** [N] blocking, [N] major, [N] minor
**Coverage gaps:** [list or "None"]
**Open items:** [list or "None"]

Ready for human review. Implementation Planning must not begin until this sign-off is approved.
```

**Stop here.** Do not proceed to Implementation Planning or any later phase until the user explicitly approves `docs/design-review.md`.

If the recommendation is **Not approved**, stop after reporting and wait for Architecture to be revised and re-reviewed.
