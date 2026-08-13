# Code Review: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| Requirements | docs/requirements.md (approved 2026-08-14) |
| Architecture | docs/architecture.md (approved 2026-08-14) |
| Implementation plan | docs/implementation-plan.md (approved 2026-08-14) |
| Implementation summary | docs/implementation-summary.md (approved 2026-08-14) |
| Last updated | 2026-08-14 |

## Summary

Implementation for SCRUM-3 matches the approved plan, requirements, and architecture. Three new source files in `initial/` add the `Greeting` record, `GreetingController` with explicit `resolveName()` blank/whitespace normalization (DR-001), and `GreetingControllerTests` covering default, personalized, blank/whitespace, and `id` field assertions (DR-002, DR-003). Preserved functionality is intact: `RestServiceApplication`, `RestServiceApplicationTests`, and `pom.xml` are unchanged. Maven test suite was re-run during this review (4 tests, 0 failures, BUILD SUCCESS), confirming implementation-summary claims. **Recommendation: Approved** — no blocking or major findings.

## Review checklist

| Area | Result | Notes |
|------|--------|-------|
| Plan adherence | Pass | TASK-001–TASK-004 scope delivered; three new source files only; no unauthorized pom or bootstrap changes |
| Requirement coverage | Pass | FR-001–FR-009, NFR-001–NFR-007, SEC-001–SEC-003 implemented per approved artifacts |
| Acceptance criteria | Pass | AC-001–AC-008 addressable from controller, record, and tests |
| Architecture alignment | Pass | Controller contract matches architecture; `resolveName()` used instead of `@RequestParam(defaultValue)` |
| Correctness | Pass | Default, personalized, empty, and whitespace `name` inputs produce expected `content`; monotonic `id` via `AtomicLong` |
| Preserved functionality | Pass | `RestServiceApplication.java` and existing smoke test unchanged; `contextLoads()` passes |
| Tests | Pass | TEST-001–TEST-005 coverage present; blank/whitespace and `id` assertions added beyond `complete/` reference |
| Security | Pass | Public GET only; no persistence; `name` used as display text via `String.formatted` and Jackson JSON encoding (SEC-003) |
| Code quality | Pass | Clear naming, minimal layering, consistent with `complete/` reference style |
| Scope alignment | Pass | Single `/greeting` endpoint; no auth, DB, UI, or extra dependencies |

## Findings

| ID | Severity | Finding | Location | Requirement refs | Recommendation | Status |
|----|----------|---------|----------|------------------|----------------|--------|
| CR-001 | Minor | Maven build output (`initial/target/`) is present and untracked; repository has no `.gitignore` entry for `initial/target/`. | Repository / git hygiene | NFR-003 | Add `initial/target/` (or root Maven ignore pattern) before PR to avoid committing build artifacts. | Open |
| CR-002 | Minor | New source files are untracked; `git diff HEAD -- initial/` shows no staged diff — review relied on direct file inspection. | Git working tree | — | Stage and commit implementation files during Pull Request phase; no code change required. | Open |

## Requirement verification

| Requirement ID | Implemented | Verified by tests | Notes |
|----------------|-------------|-------------------|-------|
| FR-001 | Yes | Yes | `@GetMapping("/greeting")` in `GreetingController` |
| FR-002 | Yes | Yes | `@RequestParam(required = false) String name` |
| FR-003 | Yes | Yes | `resolveName()` + TEST-001, TEST-003 |
| FR-004 | Yes | Yes | Non-blank name passed through; TEST-002 |
| FR-005 | Yes | Yes | HTTP 200 asserted in all greeting tests |
| FR-006 | Yes | Yes | `Greeting` record serialized to JSON |
| FR-007 | Yes | Yes | Template `"Hello, %s!"` with resolved name |
| FR-008 | Yes | Yes | `AtomicLong` counter; `$.id` assertions in TEST-001 |
| FR-009 | Yes | Yes | Additive components; TEST-005 `contextLoads()` passes |
| NFR-001 | Yes | — | Java 17 record; pom unchanged |
| NFR-002 | Yes | Yes | Spring Boot `@RestController`, existing starters |
| NFR-003 | Yes | Yes | Maven build succeeds |
| NFR-004 | Yes | — | Package `com.example.restservice` |
| NFR-005 | Yes | Yes | Default, personalized, and normalization tests |
| NFR-006 | Yes | Yes | No new dependencies in `pom.xml` |
| NFR-007 | Yes | Yes | `mvnw.cmd test` — 4 tests, BUILD SUCCESS (verified in review) |
| SEC-001 | Yes | — | No authentication on endpoint |
| SEC-002 | Yes | — | No persistence |
| SEC-003 | Yes | — | String formatting only; no code execution |
| AC-001 | Yes | Yes | GET `/greeting` returns JSON greeting |
| AC-002 | Yes | Yes | Optional `name` query parameter |
| AC-003 | Yes | Yes | Default and blank/whitespace → `"Hello, World!"` |
| AC-004 | Yes | Yes | HTTP 200 on success |
| AC-005 | Yes | Yes | JSON includes `content` and `id` |
| AC-006 | Yes | Yes | Default and personalized tests pass |
| AC-007 | Yes | Yes | Maven build succeeds |
| AC-008 | Yes | Yes | Application context loads |

## Files reviewed

| File | Assessment |
|------|------------|
| `initial/src/main/java/com/example/restservice/Greeting.java` | Correct record shape (`long id`, `String content`); matches architecture and TASK-001 |
| `initial/src/main/java/com/example/restservice/GreetingController.java` | Implements approved handler contract; `resolveName()` satisfies DR-001; differs appropriately from `complete/` reference |
| `initial/src/test/java/com/example/restservice/GreetingControllerTests.java` | Covers TEST-001–TEST-004; adds blank/whitespace test and `id` jsonPath assertions per DR-002/DR-003 |
| `initial/src/main/java/com/example/restservice/RestServiceApplication.java` | Unchanged (preserved functionality) |
| `initial/src/test/java/com/example/restservice/RestServiceApplicationTests.java` | Unchanged; `contextLoads()` passes (TEST-005) |
| `initial/pom.xml` | Unchanged; Java 17, Spring Boot 4.0.7, no new dependencies |

## Design-review conditions addressed

| Condition | Status | Evidence |
|-----------|--------|----------|
| DR-001 — `resolveName()` per architecture; no verbatim `complete/` controller copy | Done | `GreetingController.resolveName()` with `null`/blank check; no `defaultValue` on `@RequestParam` |
| DR-002 — Test blank/whitespace name normalization | Done | `blankNameShouldNormalizeToWorld` covers `?name=` and `?name=%20` |
| DR-003 — Assert `id` present in at least one test | Done | `noParamGreetingShouldReturnDefaultMessage` asserts `$.id` exists and is numeric |

## Test evidence cross-check

| Claim (implementation-summary) | Review evidence |
|--------------------------------|-----------------|
| 4 tests, 0 failures, BUILD SUCCESS | Confirmed by re-running `.\mvnw.cmd test` from `initial/` during Code Review |
| TEST-001–TEST-005 pass | Surefire: 3 tests in `GreetingControllerTests`, 1 in `RestServiceApplicationTests` |
| DR-001/DR-002/DR-003 addressed | Verified in source (see Design-review conditions table) |

## Accepted conditions

- CR-001 and CR-002 are repository/process hygiene items; acceptable to address during Pull Request without returning to Implementation.

## Open questions

- None

## Sign-off recommendation

| Disposition | Selected |
|-------------|----------|
| Approved | ☑ |
| Approved with conditions | ☐ |
| Not approved — return to Implementation | ☐ |

**Conditions (if applicable):**

- None blocking. Optional: add `.gitignore` for `initial/target/` before merge (CR-001).
