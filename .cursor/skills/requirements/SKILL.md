---
name: requirements
description: Runs the Agentic SDLC Requirements phase — reads user stories from Jira, Confluence, or document files, clarifies ambiguities, and produces docs/requirements.md. Use when starting requirements analysis, working on a Jira story, or when the user invokes /requirements or the Requirements phase.
disable-model-invocation: true
---

# Requirements Phase

Execute only the Requirements phase. Do not start Architecture, modify application source code, or produce architecture or implementation artifacts.

## Inputs

Obtain the User Story from one of:

1. **Jira** — issue key, summary, description, acceptance criteria, links (via MCP, API, or user-provided export)
2. **Confluence** — page URL or exported content
3. **Document** — Word (`.docx`), PDF, or plain text the user provides or attaches

If the source is missing or inaccessible, ask the user to paste the story or grant access. Do not invent requirements.

## Workflow

Copy and track progress:

```
Requirements Progress:
- [ ] Step 1: Ingest User Story
- [ ] Step 2: Analyze gaps and ambiguities
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Draft requirements
- [ ] Step 5: Write docs/requirements.md
- [ ] Step 6: Report and request approval
```

### Step 1: Ingest User Story

Capture verbatim where possible:

- Jira issue ID and title
- User Story text (As a… I want… So that…)
- Stated acceptance criteria
- Links, attachments, or related issues mentioned in the source

### Step 2: Analyze gaps and ambiguities

Review the story for missing or unclear information:

- Scope boundaries (in scope / out of scope)
- Actors, triggers, and expected outcomes
- Data inputs, outputs, and validation rules
- Error and edge-case behavior
- Non-functional expectations (performance, availability, usability)
- Security and privacy constraints
- Dependencies, integrations, and assumptions
- Testability — can each requirement be verified?

List findings as **Resolved from source** vs **Needs clarification**.

### Step 3: Clarify with user

When information is missing or ambiguous:

1. Ask focused questions (group related items; avoid overwhelming the user).
2. **Stop and wait** for answers. Do not assume or fill gaps silently.
3. Incorporate responses into the requirements draft.
4. Repeat until blocking ambiguities are resolved or explicitly deferred.

Record deferred items under **Open questions / assumptions** in the artifact.

### Step 4: Draft requirements

Define requirements that are **clear, testable, and traceable**:

| Category | Content |
|----------|---------|
| Functional | Behaviors the system must perform |
| Non-functional | Quality attributes (performance, scalability, reliability, etc.) |
| Security | Auth, authorization, data protection, compliance |
| Acceptance criteria | Verifiable conditions of done, mapped to requirements |

Assign stable IDs (e.g., `FR-001`, `NFR-001`, `SEC-001`, `AC-001`). Every requirement must trace back to the User Story and, when available, the Jira issue ID and source acceptance criteria.

### Step 5: Write docs/requirements.md

Create or update `docs/requirements.md` using this structure:

```markdown
# Requirements: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| User Story | [Full story text] |
| Source | [Jira / Confluence / document — link or filename] |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph describing the capability being built]

## Scope

### In scope
- …

### Out of scope
- …

## Functional requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| FR-001 | … | AC-… |

## Non-functional requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| NFR-001 | … | … |

## Security requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| SEC-001 | … | … |

## Acceptance criteria

| ID | Criterion | Maps to |
|----|-----------|---------|
| AC-001 | … | FR-… |

## Assumptions and dependencies

- …

## Open questions

- … (empty if none)
```

Update existing files in place when revising a story; preserve traceability history in the **Last updated** field.

### Step 6: Report and request approval

End the phase with a completion report:

```markdown
## Requirements phase complete

**Artifact:** docs/requirements.md
**Jira:** [issue ID or N/A]
**Requirements count:** [N] functional, [N] non-functional, [N] security, [N] acceptance criteria
**Open items:** [list or "None"]

Ready for human review. Architecture must not begin until this artifact is approved.
```

**Stop here.** Do not proceed to Architecture or any later phase until the user explicitly approves `docs/requirements.md`.
