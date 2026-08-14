# Pull Request: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| Verification | docs/verification.md (approved 2026-08-14) |
| PR URL | https://github.com/GowriKuppusamy/gs-rest-service/pull/1 |
| Branch | feature/cursor-agentic-sdlc → main |
| Last updated | 2026-08-14 |

## Summary

Adds a `GET /greeting` REST endpoint to the `initial/` Spring Boot module with optional `name` query parameter (default `"World"`), JSON response via a `Greeting` record, and integration tests. Includes full Agentic SDLC documentation (Requirements through Verification) and Maven `target/` gitignore hygiene (CR-001).

## PR details

| Field | Value |
|-------|-------|
| Title | SCRUM-3: Display personalized greeting message |
| Base branch | main |
| Head branch | feature/cursor-agentic-sdlc |
| Commit | 7affea3 — SCRUM-3: Add personalized greeting endpoint and SDLC artifacts |

## Artifacts included

- docs/requirements.md
- docs/architecture.md
- docs/design-review.md
- docs/implementation-plan.md
- docs/implementation-summary.md
- docs/code-review.md
- docs/verification.md

## Verification summary

- **Automated checks:** 1 pass, 0 fail
- **Acceptance criteria:** AC-001 through AC-008 — all Pass
- **Full suite:** `.\mvnw.cmd test` (from `initial/`) — 4 tests, 0 failures, BUILD SUCCESS

## Changes committed

| File | Change |
|------|--------|
| `initial/src/main/java/com/example/restservice/Greeting.java` | New — JSON response record |
| `initial/src/main/java/com/example/restservice/GreetingController.java` | New — `GET /greeting` with `resolveName()` |
| `initial/src/test/java/com/example/restservice/GreetingControllerTests.java` | New — integration tests |
| `initial/.gitignore` | New — ignore `target/` (CR-001) |
| `docs/*.md` | New — SDLC phase artifacts |

## Prepared PR description

Use this body when opening the pull request:

```markdown
## Summary
- Add `GET /greeting` REST endpoint with optional `name` query parameter and default `"World"` greeting (SCRUM-3)
- Add `Greeting` record, `GreetingController` with explicit `resolveName()` blank/whitespace normalization, and integration tests
- Include full Agentic SDLC documentation and Maven `target/` gitignore (CR-001, CR-002)

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
 **Jira:** SCRUM-3

## Test plan
- [x] `.\mvnw.cmd test` from `initial/` — 4 tests, 0 failures, BUILD SUCCESS
- [x] AC-001 — GET `/greeting` returns JSON greeting in response body
- [x] AC-002 — Optional `name` query parameter supported
- [x] AC-003 — Default greeting uses `"World"` when `name` omitted or blank
- [x] AC-004 — Successful requests return HTTP 200
- [x] AC-005 — Response is valid JSON with `content` and `id`
- [x] AC-006 — Unit tests pass for default and personalized scenarios
- [x] AC-007 — Maven build succeeds with no test failures
- [x] AC-008 — Spring Boot application starts without errors

## Verification evidence
Independent verification re-ran the full Maven test suite from `initial/` on Windows. All 4 tests passed (3 in `GreetingControllerTests`, 1 in `RestServiceApplicationTests`). Design-review conditions DR-001–DR-003 confirmed via passing tests. No regression in `RestServiceApplicationTests.contextLoads()`.

## Changes Made
- `Greeting.java` — JSON response record with `id` and `content`
- `GreetingController.java` — `GET /greeting` endpoint with `resolveName()` normalization
- `GreetingControllerTests.java` — integration tests for default, personalized, and blank-name scenarios
- `initial/.gitignore` — exclude Maven `target/` build output
- `docs/*.md` — Agentic SDLC phase artifacts

## Known Limitations
- Manual HTTP request against a running server on port 8080 was not verified (covered by `@SpringBootTest` + `RestTestClient` integration tests)

## Reviewer Checklist
- [x] Requirements approved and satisfied
- [x] Architecture and design review approved
- [x] Implementation plan completed
- [x] Code review approved
- [x] Verification evidence reviewed
- [x] Tests passed
- [x] No known security issues
- [x] Known limitations reviewed

```
## Pull Request Status

Pull Request successfully created:

https://github.com/GowriKuppusamy/gs-rest-service/pull/1

Status: Open
Base Branch: main
Feature Branch: feature/cursor-agentic-sdlc