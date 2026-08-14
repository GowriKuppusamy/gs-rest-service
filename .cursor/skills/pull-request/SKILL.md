---
name: pull-request
description: Runs the Agentic SDLC Pull Request phase — prepares a traceable PR from approved verification evidence using gh, and produces docs/pull-request.md. Use after Verification approval, or when the user invokes /pull-request or the Pull Request phase.
disable-model-invocation: true
---

# Pull Request Phase

Execute only the Pull Request phase. Prepare and open a pull request with full SDLC traceability. This is the final workflow phase.

## Prerequisites

Before starting:

1. Confirm `docs/verification.md` is **human-approved** with recommendation **Verified — ready for Pull Request**.
2. Confirm prior artifacts exist: `docs/requirements.md`, `docs/architecture.md`, `docs/design-review.md`, `docs/implementation-plan.md`, `docs/implementation-summary.md`, `docs/code-review.md`.
3. If verification is **Not verified**, stop and return to Implementation / Verification.
4. If any approval is missing or unclear, stop and ask the user to complete the prior phase first.

## Inputs

| Source | Purpose |
|--------|---------|
| `docs/verification.md` | Approved test evidence and acceptance-criteria results |
| `docs/requirements.md` | Jira issue ID, story summary, and acceptance criteria |
| `docs/implementation-summary.md` | Files changed and implementation scope |
| All prior `docs/*.md` artifacts | Traceability links for the PR description |
| Git state | Branch, commits, and diff to be submitted |

Do not create commits unless the user explicitly requests them. Do not push unless the user has approved publishing the branch.

## Workflow

Copy and track progress:

```
Pull Request Progress:
- [ ] Step 1: Ingest artifacts and git state
- [ ] Step 2: Prepare branch and PR content
- [ ] Step 3: Clarify with user (if needed)
- [ ] Step 4: Push branch and open PR
- [ ] Step 5: Write docs/pull-request.md
- [ ] Step 6: Report completion
```

### Step 1: Ingest artifacts and git state

Capture:

- Jira issue ID and story title
- Current branch name and base branch (default: `main` or project default)
- Commits and files included in the change set
- Verification summary (pass/fail counts)
- Key requirement IDs satisfied

Run `git status`, `git log`, and `git diff [base]...HEAD` to understand what will be in the PR.

### Step 2: Prepare branch and PR content

Draft the PR using this structure:

```markdown
## Summary
- [1–3 bullets: what changed and why]

## SDLC traceability
| Phase | Artifact |
|-------|----------|
| Requirements | docs/requirements.md |
| Architecture | docs/architecture.md |
| Design review | docs/design-review.md |
| Implementation plan | docs/implementation-plan.md |
| Implementation | docs/implementation-summary.md |
| Code review | docs/code-review.md |
| Verification | docs/verification.md |

**Jira:** [PROJ-123 or N/A]

## Test plan
- [ ] [Verification command or check from docs/verification.md]
- [ ] [Acceptance criterion AC-… verified]

## Verification evidence
[Brief summary from docs/verification.md — only include checks that passed]
```

Ensure the PR description does not claim tests passed that verification did not confirm.
## Changes Made
- [File/component] — [what changed and why]

## Test Evidence
- [Exact verification command/result]
- [Acceptance criterion verified]

## Known Limitations
- [Known limitation, Not Found item, or "None"]

## Reviewer Checklist
- [ ] Requirements approved and satisfied
- [ ] Architecture and design review approved
- [ ] Implementation plan completed
- [ ] Code review approved
- [ ] Verification evidence reviewed
- [ ] Tests passed
- [ ] No known security issues
- [ ] Known limitations reviewed

### Step 3: Clarify with user

Before pushing or opening the PR, confirm with the user when:

- The branch is not pushed or tracking remote is unset
- Uncommitted changes exist and the user has not requested a commit
- Base branch, PR title, or scope is ambiguous
- Credentials or `gh` auth may be missing

**Stop and wait** for confirmation on push, commit, and PR creation actions.

### Step 4: Push branch and open PR

1. Push the branch: `git push -u origin HEAD` (only with user approval).
2. Create the PR with `gh pr create`, passing the drafted body via HEREDOC.
3. Capture the returned PR URL.

If `gh` is unavailable or auth fails, document the blocker and provide the prepared title/body for manual submission.

### Step 5: Write docs/pull-request.md

Create or update `docs/pull-request.md` using this structure:

```markdown
# Pull Request: [Story title]

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | [PROJ-123 or N/A] |
| Verification | docs/verification.md (approved [YYYY-MM-DD]) |
| PR URL | [https://github.com/… or "Not created"] |
| Branch | [feature/…] → [main] |
| Last updated | [YYYY-MM-DD] |

## Summary

[One short paragraph describing the delivered change]

## PR details

| Field | Value |
|-------|-------|
| Title | … |
| Base branch | … |
| Head branch | … |

## Artifacts included

- docs/requirements.md
- docs/architecture.md
- docs/design-review.md
- docs/implementation-plan.md
- docs/implementation-summary.md
- docs/code-review.md
- docs/verification.md

## Verification summary

[Copied from approved docs/verification.md — pass/fail counts only]

## Open items

- … (empty if none)
```

### Step 6: Report completion

End the workflow with a completion report:

```markdown
## Pull Request phase complete

**Artifact:** docs/pull-request.md
**PR URL:** [url or "Pending — see open items"]
**Jira:** [issue ID or N/A]
**Branch:** [head] → [base]
**Open items:** [list or "None"]

SDLC workflow complete pending PR merge and any post-merge follow-up.
```

**Stop here.** The Agentic SDLC workflow ends when the PR is opened (or documented for manual creation) and the user approves completion.

Do not start new SDLC phases or modify scope without a new user story and a fresh Requirements phase.
