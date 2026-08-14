# Requirements: Display personalized greeting message

## Traceability

| Field | Value |
|-------|-------|
| Jira issue | SCRUM-3 |
| User Story | As a user, I want to receive a greeting message using my name, so that I receive a personalized response. |
| Source | Jira SCRUM-3 — [Display personalized greeting message](https://gowri1020k-1784826767697.atlassian.net/rest/api/3/issue/10002); baseline app per repository README (Spring Boot REST service guide) |
| Last updated | 2026-08-14 |

## Summary

Add a REST endpoint to the existing Spring Boot baseline application that returns a personalized JSON greeting. Callers may supply an optional `name` query parameter; when omitted, the greeting defaults to `"World"`. The feature must not break existing application startup and must include unit tests. This capability serves as the reference feature for the Agentic SDLC demonstration across all downstream phases.

## Scope

### In scope

- REST GET endpoint exposing a greeting resource
- Optional `name` query parameter with default value `"World"`
- JSON response with HTTP 200 on success
- Unit tests for default and personalized greeting scenarios
- Preservation of existing application startup behavior
- Implementation using Java 17, Spring Boot, and Maven within the existing `com.example.restservice` package structure

### Out of scope

- Authentication and authorization
- Database persistence
- UI or front-end components
- External service integrations
- Additional endpoints beyond the greeting resource

## Functional requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| FR-001 | The system shall expose an HTTP GET endpoint at `/greeting`. | SCRUM-3 FR; AC-001 |
| FR-002 | The endpoint shall accept an optional query parameter named `name`. | SCRUM-3 FR; AC-002 |
| FR-003 | When the `name` parameter is omitted, the system shall use `"World"` as the default name in the greeting. | SCRUM-3 FR; AC-003 |
| FR-004 | When a `name` value is supplied, the greeting content shall include that name. | SCRUM-3 FR; AC-001 |
| FR-005 | The endpoint shall return HTTP status 200 for successful requests. | SCRUM-3 FR; AC-004 |
| FR-006 | The response body shall be JSON. | SCRUM-3 FR; AC-005 |
| FR-007 | The JSON response shall include a `content` field whose value follows the greeting format `Hello, {name}!`, where `{name}` is the supplied or default name. | SCRUM-3; README baseline |
| FR-008 | The JSON response shall include an `id` field identifying the greeting instance, consistent with the Spring REST service baseline pattern. | README baseline |
| FR-009 | The application shall continue to start successfully after the greeting endpoint is added; existing startup behavior shall not regress. | SCRUM-3 FR |

## Non-functional requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| NFR-001 | The implementation shall use Java 17. | SCRUM-3 NFR |
| NFR-002 | The implementation shall use the Spring Boot framework. | SCRUM-3 NFR |
| NFR-003 | The project shall build with Maven. | SCRUM-3 NFR; AC-007 |
| NFR-004 | New code shall follow the existing package structure (`com.example.restservice`). | SCRUM-3 NFR |
| NFR-005 | Unit tests shall verify the default greeting (no `name` parameter) and a personalized greeting (with `name` parameter), and all unit tests shall pass. | SCRUM-3 NFR; AC-006 |
| NFR-006 | No unnecessary third-party dependencies shall be introduced. | SCRUM-3 NFR |
| NFR-007 | The Maven build shall complete successfully (`mvn test` or equivalent). | SCRUM-3 AC |

## Security requirements

| ID | Requirement | Source / AC ref |
|----|-------------|-----------------|
| SEC-001 | The greeting endpoint shall not require authentication (authentication is explicitly out of scope for this story). | SCRUM-3 out of scope |
| SEC-002 | The endpoint shall not persist or transmit sensitive user data beyond the ephemeral greeting request/response. | SCRUM-3 scope |
| SEC-003 | The `name` parameter shall be treated as display text only; the system shall not execute or interpret it as code or commands. | Assumption — safe input handling |

## Acceptance criteria

| ID | Criterion | Maps to |
|----|-----------|---------|
| AC-001 | A GET request to `/greeting` returns a JSON greeting in the response body. | FR-001, FR-005, FR-006, FR-007 |
| AC-002 | The endpoint supports an optional `name` query parameter. | FR-002 |
| AC-003 | When `name` is not provided, the greeting content uses `"World"` (e.g., `"Hello, World!"`). | FR-003, FR-007 |
| AC-004 | Successful requests return HTTP 200. | FR-005 |
| AC-005 | The response body is valid JSON containing at least `content` (and `id` per baseline). | FR-006, FR-007, FR-008 |
| AC-006 | Unit tests pass for both default and personalized greeting scenarios. | NFR-005 |
| AC-007 | Maven build succeeds with no test failures. | NFR-003, NFR-007 |
| AC-008 | The Spring Boot application starts without errors after implementation. | FR-009 |

## Assumptions and dependencies

- The baseline application is the `initial` Maven/Spring Boot project in this repository (`RestServiceApplication` only; no greeting endpoint yet).
- Endpoint path `/greeting`, greeting template `Hello, {name}!`, and JSON shape `{ "id": <number>, "content": "<greeting>" }` follow the Spring REST service guide documented in the repository README.
- Default server port 8080 and standard Spring Boot conventions apply unless changed in a later phase.
- No database, message broker, or external API dependencies are required.
- Implementation work depends on completion and approval of this requirements artifact before Architecture begins.

## Open questions

- **Empty `name` parameter:** If a client sends `?name=` (empty string), should the system treat it as missing (default to `"World"`) or as an empty name in the greeting (e.g., `"Hello, !"`)? *Deferred to Architecture/Design Review; default assumption: treat blank/whitespace-only as `"World"` unless design decides otherwise.*
- **Name length or character validation:** No maximum length or character restrictions are specified in SCRUM-3. *Deferred; assume no validation beyond safe display handling unless NFR added later.*
