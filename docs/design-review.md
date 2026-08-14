# Design Review: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| Requirements | docs/requirements.md (approved 2026-08-14) |
| Architecture | docs/architecture.md (approved 2026-08-14) |
| Last updated | 2026-08-14 |

## Summary

The proposed architecture for SCRUM-3 is sound, complete, and feasible against the approved requirements and the existing `initial/` Spring Boot baseline. All functional, non-functional, security, and acceptance-criteria requirements have explicit architectural responses. The design correctly targets the `initial/` Maven module, follows the repository README and `complete/` reference patterns, and resolves the requirements open question on empty `name` values by normalizing blank/whitespace input to `"World"`. Codebase inspection confirms Java 17, Spring Boot 4.0.7, required starters, and test infrastructure are already present; only additive source files are needed. **Recommendation: Approved with conditions** — two minor implementation conditions below; no blocking or major design defects.

## Review checklist

| Area | Result | Notes |
|------|--------|-------|
| Requirement coverage | Pass | All FR-*, NFR-*, and SEC-* have mapped architectural responses |
| Acceptance criteria achievability | Pass | Each AC-* is achievable from controller + record + tests design |
| Internal consistency | Pass | Components, interfaces, and data design align; no contradictions |
| Scope alignment | Pass | Single GET endpoint; no auth, DB, UI, or extra endpoints introduced |
| Feasibility | Pass | `initial/` pom.xml, package structure, and reference `complete/` module support the design |
| Security | Pass | SEC-001–SEC-003 addressed; no auth, no persistence, display-only handling |
| Non-functional approach | Pass | Java 17, Spring Boot, Maven, package layout, and zero new deps are concrete |
| Testability | Pass | `@SpringBootTest` + `RestTestClient` pattern validated in `complete/`; minor test-gap notes in findings |

## Findings

| ID | Severity | Finding | Requirement refs | Recommendation | Status |
|----|----------|---------|------------------|----------------|--------|
| DR-001 | Minor | Architecture refines blank/whitespace `name` handling via `resolveName()`, but `complete/GreetingController.java` uses `@RequestParam(defaultValue = "World")` only — `?name=` would yield `"Hello, !"` in the reference, not `"Hello, World!"`. | FR-003, AC-003 | During implementation, implement `resolveName()` per architecture contract; do not copy the reference controller verbatim without normalization logic. | Open |
| DR-002 | Minor | NFR-005 and the architecture test plan specify default (no param) and personalized scenarios only; blank/whitespace `name` normalization is an explicit architecture decision without a corresponding test requirement. | NFR-005, AC-003 | Add a unit test for `?name=` and/or whitespace-only `name` during Implementation to lock in the normalization behavior. | Open |
| DR-003 | Minor | Reference tests in `complete/GreetingControllerTests.java` assert `content` only; AC-005 also requires an `id` field in the JSON body. | AC-005, FR-008 | Assert `id` is present and numeric in at least one test during Implementation for stronger AC-005 traceability. | Open |

## Requirement coverage verification

| Requirement ID | Covered | Evidence / gap |
|----------------|---------|----------------|
| FR-001 | Yes | `GreetingController` with `@GetMapping("/greeting")` |
| FR-002 | Yes | Optional `@RequestParam(required = false) String name` |
| FR-003 | Yes | `resolveName()` returns `"World"` when parameter absent |
| FR-004 | Yes | Non-blank `name` used verbatim in `Hello, {name}!` template |
| FR-005 | Yes | Spring MVC default 200 on successful handler return |
| FR-006 | Yes | `Greeting` record serialized by Jackson |
| FR-007 | Yes | `content` set via `String.formatted("Hello, %s!", effectiveName)` |
| FR-008 | Yes | Monotonic `AtomicLong` counter assigns `id` |
| FR-009 | Yes | Additive components; `RestServiceApplication` unchanged |
| NFR-001 | Yes | `initial/pom.xml` sets `<java.version>17</java.version>` |
| NFR-002 | Yes | Existing Spring Boot 4.x + `spring-boot-starter-webmvc` |
| NFR-003 | Yes | Maven build via existing `pom.xml` and wrapper |
| NFR-004 | Yes | All new types in `com.example.restservice` |
| NFR-005 | Yes | `GreetingControllerTests` with default + personalized methods planned |
| NFR-006 | Yes | No new dependencies required |
| NFR-007 | Yes | Standard `mvn test` lifecycle from `initial/` |
| SEC-001 | Yes | Public endpoint; no Spring Security |
| SEC-002 | Yes | No persistence; ephemeral request/response |
| SEC-003 | Yes | String interpolation + Jackson JSON encoding only |
| AC-001 | Yes | GET `/greeting` → JSON greeting (FR-001, FR-005–FR-007) |
| AC-002 | Yes | Optional `name` query parameter on controller |
| AC-003 | Yes | Default/normalized name → `"Hello, World!"` |
| AC-004 | Yes | HTTP 200 on success |
| AC-005 | Yes | JSON body with `content` and `id` fields |
| AC-006 | Yes | Unit tests for default and personalized paths |
| AC-007 | Yes | Maven build/test pipeline unchanged in structure |
| AC-008 | Yes | Existing `RestServiceApplicationTests.contextLoads()` + component scan |

## Accepted risks and conditions

**Conditions for Implementation (from findings DR-001–DR-003):**

- Implement `resolveName()` normalization logic as specified in architecture; do not rely solely on `@RequestParam(defaultValue = "World")`.
- Add a unit test covering blank/whitespace `name` normalization (recommended, not blocking for sign-off).
- Assert `id` field presence in at least one test (recommended, not blocking for sign-off).

**Accepted risks (deferred by design, non-blocking):**

- No maximum length or character-set validation on `name` — acceptable per architecture key decision; revisit only if product adds an NFR later.
- Greeting `id` values are ephemeral and non-persistent — consistent with Spring guide baseline and requirements scope.

## Open questions

- None blocking. Empty-name and validation topics from requirements are resolved in architecture **Key decisions**.

## Sign-off recommendation

| Disposition | Selected |
|-------------|----------|
| Approved | ☐ |
| Approved with conditions | ☑ |
| Not approved — return to Architecture | ☐ |

**Conditions (if applicable):**

- Implementation must follow the architecture's `resolveName()` contract for blank/whitespace `name` values (DR-001); copying `complete/GreetingController` without this refinement would diverge from the approved design.
- Implementation Planning should include the recommended tests noted in DR-002 and DR-003 to strengthen traceability for normalization and `id` field presence.
