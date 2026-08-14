# Implementation Plan: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| Requirements | docs/requirements.md (approved 2026-08-14) |
| Architecture | docs/architecture.md (approved 2026-08-14) |
| Design review | docs/design-review.md (approved with conditions 2026-08-14) |
| Last updated | 2026-08-14 |

## Summary

Add three source files to the `initial/` Maven module under `com.example.restservice`: a `Greeting` record, a `GreetingController` with `GET /greeting` and an explicit `resolveName()` helper for blank/whitespace normalization, and `GreetingControllerTests` using `@SpringBootTest` and `RestTestClient`. Follow the Spring REST service guide and `complete/` reference for structure and test style, but implement `resolveName()` per architecture (DR-001) rather than copying the reference controller's `@RequestParam(defaultValue = "World")` approach. No `pom.xml` or bootstrap changes; existing `RestServiceApplicationTests.contextLoads()` must continue to pass.

## Scope reminder

### In scope

- `GET /greeting` with optional `name` query parameter
- JSON response `{ "id": <long>, "content": "Hello, {name}!" }` with HTTP 200
- Default and blank/whitespace normalization to `"World"`
- Unit tests: default, personalized, blank/whitespace normalization, and `id` presence
- Maven build verification from `initial/`

### Out of scope

- Authentication, database, UI, external integrations
- Additional endpoints beyond `/greeting`
- New Maven dependencies or changes to `RestServiceApplication`
- Modifications to `complete/`, Kotlin, or Gradle variants

## Preserved functionality

| Area | Current state | Must not regress |
|------|---------------|------------------|
| `initial/src/main/java/com/example/restservice/RestServiceApplication.java` | Spring Boot bootstrap only | Unchanged; application must start |
| `initial/src/test/java/com/example/restservice/RestServiceApplicationTests.java` | `contextLoads()` smoke test | Must pass after greeting feature is added |
| `initial/pom.xml` | Java 17, Spring Boot 4.0.7, `spring-boot-starter-webmvc`, test starter | No new dependencies (NFR-006) |
| Build tooling | Maven wrapper (`mvnw`, `mvnw.cmd`) | Standard `mvn test` lifecycle from `initial/` |

## Task breakdown

| ID | Task | Files / areas | Requirement refs | Depends on | Status |
|----|------|---------------|------------------|------------|--------|
| TASK-001 | Create `Greeting` Java record with `long id` and `String content` | `initial/src/main/java/com/example/restservice/Greeting.java` (new) | FR-006, FR-007, FR-008 | — | Complete |
| TASK-002 | Create `GreetingController` with `@GetMapping("/greeting")`, optional `@RequestParam(required = false) String name`, in-memory `AtomicLong` counter, greeting template `"Hello, %s!"`, and private `resolveName(String name)` that returns `"World"` when `name` is `null`, empty, or whitespace-only; use resolved name in `String.formatted` | `initial/src/main/java/com/example/restservice/GreetingController.java` (new) | FR-001–FR-005, FR-007, FR-008, SEC-003, DR-001 | TASK-001 | Complete |
| TASK-003 | Add `GreetingControllerTests` with `@SpringBootTest`, `@AutoConfigureRestTestClient`, and test methods for default greeting, personalized greeting, blank/whitespace normalization, and `id` field assertion | `initial/src/test/java/com/example/restservice/GreetingControllerTests.java` (new) | NFR-005, AC-006, DR-002, DR-003 | TASK-002 | Complete |
| TASK-004 | Run full Maven test suite from `initial/` and confirm all tests pass including existing `RestServiceApplicationTests.contextLoads()` | `initial/` (verify only) | FR-009, NFR-007, AC-007, AC-008 | TASK-003 | Complete |

## Test plan

| ID | Test | Verifies | Type | Requirement refs |
|----|------|----------|------|------------------|
| TEST-001 | `noParamGreetingShouldReturnDefaultMessage` — `GET /greeting` returns 200, `content` is `"Hello, World!"` | Default greeting when `name` omitted | Integration (RestTestClient) | FR-001, FR-003, FR-005, FR-006, FR-007, AC-001, AC-003, AC-004, AC-005 |
| TEST-002 | `paramGreetingShouldReturnTailoredMessage` — `GET /greeting?name=Spring Community` returns 200, `content` is `"Hello, Spring Community!"` | Personalized greeting with supplied name | Integration (RestTestClient) | FR-002, FR-004, FR-005, FR-006, FR-007, AC-001, AC-002, AC-004 |
| TEST-003 | `blankNameShouldNormalizeToWorld` — `GET /greeting?name=` and `GET /greeting?name=%20` (whitespace) return 200, `content` is `"Hello, World!"` | Blank/whitespace `name` normalization via `resolveName()` | Integration (RestTestClient) | FR-003, AC-003, DR-002 |
| TEST-004 | Assert `id` is present and numeric in at least one greeting test (e.g., `jsonPath("$.id").exists()` and `jsonPath("$.id").isNumber()` on TEST-001 or dedicated assertion) | JSON body includes monotonic `id` field | Integration (RestTestClient) | FR-008, AC-005, DR-003 |
| TEST-005 | Existing `RestServiceApplicationTests.contextLoads()` continues to pass | Application context loads after controller addition | Integration (SpringBootTest) | FR-009, AC-008 |

## Design-review conditions

| Condition | Addressed by |
|-----------|--------------|
| DR-001 — Implement `resolveName()` per architecture; do not copy `complete/GreetingController` verbatim | TASK-002 |
| DR-002 — Unit test for blank/whitespace name normalization | TASK-003, TEST-003 |
| DR-003 — Assert `id` is present in at least one test | TASK-003, TEST-004 |

## Requirement coverage

| Requirement ID | Task(s) | Test(s) |
|----------------|---------|---------|
| FR-001 | TASK-002 | TEST-001, TEST-002, TEST-003 |
| FR-002 | TASK-002 | TEST-002 |
| FR-003 | TASK-002 | TEST-001, TEST-003 |
| FR-004 | TASK-002 | TEST-002 |
| FR-005 | TASK-002 | TEST-001, TEST-002, TEST-003 |
| FR-006 | TASK-001, TASK-002 | TEST-001, TEST-002, TEST-003 |
| FR-007 | TASK-001, TASK-002 | TEST-001, TEST-002, TEST-003 |
| FR-008 | TASK-001, TASK-002 | TEST-004 |
| FR-009 | TASK-004 | TEST-005 |
| NFR-001 | TASK-001, TASK-002 | — |
| NFR-002 | TASK-002 | TEST-001–TEST-005 |
| NFR-003 | — (existing pom) | TEST-001–TEST-005 via TASK-004 |
| NFR-004 | TASK-001, TASK-002, TASK-003 | — |
| NFR-005 | TASK-003 | TEST-001, TEST-002, TEST-003, TEST-004 |
| NFR-006 | — (no pom changes) | TASK-004 |
| NFR-007 | TASK-004 | TEST-001–TEST-005 |
| SEC-001 | TASK-002 (public GET, no security config) | — |
| SEC-002 | TASK-002 (no persistence) | — |
| SEC-003 | TASK-002 (`resolveName` + string formatting only) | — |
| AC-001 | TASK-002, TASK-003 | TEST-001, TEST-002, TEST-003 |
| AC-002 | TASK-002, TASK-003 | TEST-002 |
| AC-003 | TASK-002, TASK-003 | TEST-001, TEST-003 |
| AC-004 | TASK-002, TASK-003 | TEST-001, TEST-002, TEST-003 |
| AC-005 | TASK-001, TASK-002, TASK-003 | TEST-001–TEST-004 |
| AC-006 | TASK-003 | TEST-001, TEST-002, TEST-003 |
| AC-007 | TASK-004 | TEST-001–TEST-005 |
| AC-008 | TASK-004 | TEST-005 |

## Implementation order

1. TASK-001 — Add `Greeting` record
2. TASK-002 — Add `GreetingController` with `resolveName()` (DR-001)
3. TASK-003 — Add `GreetingControllerTests` (TEST-001–TEST-004; DR-002, DR-003)
4. TASK-004 — Run `mvn test` in `initial/` (TEST-005 regression check)

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Copying `complete/GreetingController` verbatim misses blank-name normalization (DR-001) | TASK-002 explicitly requires private `resolveName()`; reference used for structure only |
| `?name=` treated as present empty string by Spring MVC | `resolveName()` checks `null`, empty, and `isBlank()` before formatting |
| Tests assert `content` only and miss `id` (DR-003) | TEST-004 adds explicit `id` jsonPath assertions |
| Regression in application startup | Preserve `RestServiceApplication`; verify with TEST-005 and TASK-004 |
| Accidental scope creep (validation, auth, extra endpoints) | Limit changes to three new files in `initial/`; no pom or bootstrap edits |

## Open questions

- None blocking. Empty-name and validation topics are resolved in approved architecture and design review.

## Implementation notes (for Implementation phase)

**Reference files (read-only guidance; do not modify):**

- `complete/src/main/java/com/example/restservice/Greeting.java` — record shape
- `complete/src/test/java/com/example/restservice/GreetingControllerTests.java` — test scaffolding and RestTestClient usage

**`resolveName()` contract (from architecture):**

```java
private static String resolveName(String name) {
  if (name == null || name.isBlank()) {
    return "World";
  }
  return name;
}
```

**Controller handler sketch (not verbatim copy of `complete/`):**

```java
@GetMapping("/greeting")
public Greeting greeting(@RequestParam(required = false) String name) {
  String effectiveName = resolveName(name);
  return new Greeting(counter.incrementAndGet(), template.formatted(effectiveName));
}
```

**Verification command:**

```bash
cd initial && ./mvnw test
```

(On Windows: `initial\mvnw.cmd test`)
