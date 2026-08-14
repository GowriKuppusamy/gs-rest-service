# Verification: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| Requirements | docs/requirements.md (approved 2026-08-14) |
| Code review | docs/code-review.md (approved 2026-08-14) |
| Last updated | 2026-08-14 |

## Summary

Independent verification of SCRUM-3 re-ran the full Maven test suite from `initial/` on Windows. All 4 tests passed with BUILD SUCCESS (exit code 0). Every acceptance criterion AC-001 through AC-008 is satisfied with automated test evidence. Design-review conditions DR-001–DR-003 are confirmed via passing tests and source inspection. Existing application startup behavior (`RestServiceApplicationTests.contextLoads()`) shows no regression. Code-review hygiene items CR-001 and CR-002 are deferred to the Pull Request phase and do not block verification.

## Automated checks

| Command | Exit code | Result | Notes |
|---------|-----------|--------|-------|
| `cd initial && .\mvnw.cmd test` | — | Not run | PowerShell on this host does not support `&&` as a statement separator |
| `.\mvnw.cmd test` (cwd: `initial/`) | 0 | Pass | Tests run: 4, Failures: 0, Errors: 0, Skipped: 0 — BUILD SUCCESS (7.353 s). Surefire: 3 tests in `GreetingControllerTests`, 1 test in `RestServiceApplicationTests` |

## Acceptance criteria verification

| ID | Criterion | Method | Evidence | Result |
|----|-----------|--------|----------|--------|
| AC-001 | A GET request to `/greeting` returns a JSON greeting in the response body. | Test | TEST-001 (`noParamGreetingShouldReturnDefaultMessage`), TEST-002 (`paramGreetingShouldReturnTailoredMessage`), TEST-003 (`blankNameShouldNormalizeToWorld`) — all assert HTTP 200 and `$.content` JSON field; suite pass (4/4) | Pass |
| AC-002 | The endpoint supports an optional `name` query parameter. | Test | TEST-002 sends `?name=Spring Community` and receives tailored greeting; controller uses `@RequestParam(required = false) String name` | Pass |
| AC-003 | When `name` is not provided, the greeting content uses `"World"` (e.g., `"Hello, World!"`). | Test | TEST-001 asserts `$.content` equals `"Hello, World!"`; TEST-003 asserts blank (`?name=`) and whitespace (`?name= `) normalize to `"Hello, World!"` | Pass |
| AC-004 | Successful requests return HTTP 200. | Test | TEST-001, TEST-002, TEST-003 each call `.expectStatus().isOk()` | Pass |
| AC-005 | The response body is valid JSON containing at least `content` (and `id` per baseline). | Test | TEST-001 asserts `$.id` exists and is numeric, and `$.content` equals `"Hello, World!"` (TEST-004) | Pass |
| AC-006 | Unit tests pass for both default and personalized greeting scenarios. | Test | TEST-001 (default) and TEST-002 (personalized) both pass in this verification run | Pass |
| AC-007 | Maven build succeeds with no test failures. | Test | `.\mvnw.cmd test` exit code 0; Surefire summary: 4 tests, 0 failures, BUILD SUCCESS | Pass |
| AC-008 | The Spring Boot application starts without errors after implementation. | Test | TEST-005 (`RestServiceApplicationTests.contextLoads()`) passes; Spring Boot context started successfully in test output | Pass |

## Code-review conditions verified

| Condition | Evidence | Result |
|-----------|----------|--------|
| DR-001 — `resolveName()` per architecture; no verbatim `complete/` controller copy | `GreetingController.resolveName()` uses `null`/blank check; no `defaultValue` on `@RequestParam`; TEST-003 confirms normalization | Pass |
| DR-002 — Test blank/whitespace name normalization | TEST-003 (`blankNameShouldNormalizeToWorld`) passes for `?name=` and `?name= ` | Pass |
| DR-003 — Assert `id` present in at least one test | TEST-001 asserts `$.id` exists and is numeric | Pass |
| CR-001 — Add `.gitignore` for `initial/target/` before PR | Repository hygiene; not executed in Verification phase | Not verified |
| CR-002 — Stage and commit implementation files during Pull Request | Git workflow; not executed in Verification phase | Not verified |

## Regression check

Existing smoke test `RestServiceApplicationTests.contextLoads()` passes (1 test, 0 failures). `RestServiceApplication.java` and `initial/pom.xml` remain unchanged per code review. Full suite result: 4 tests, 0 failures — no regression detected.

## Not verified

- `cd initial && .\mvnw.cmd test` — command syntax invalid in PowerShell; equivalent run from `initial/` directory used instead
- CR-001 (`.gitignore` for `initial/target/`) — deferred to Pull Request phase
- CR-002 (git staging/commit) — deferred to Pull Request phase
- Manual HTTP request against a running server on port 8080 — not required; `@SpringBootTest` + `RestTestClient` integration tests cover endpoint behavior

## Open items

- CR-001: Add `.gitignore` entry for `initial/target/` during Pull Request (minor hygiene, non-blocking)
- CR-002: Stage and commit new source files during Pull Request (process item, non-blocking)

## Recommendation

| Outcome | Selected |
|---------|----------|
| Verified — ready for Pull Request | ☑ |
| Not verified — return to Implementation | ☐ |
