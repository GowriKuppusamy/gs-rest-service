# Pull Request Description

## Summary

Implement Jira story SCRUM-3 by adding a personalized greeting endpoint to the Spring Boot application in the initial folder. The change introduces a lightweight REST endpoint with an optional name parameter and a default greeting of World when no name is supplied.

## Changes

- Added a new greeting endpoint at /greeting.
- Implemented greeting business logic in a dedicated service class.
- Introduced a simple response model for the greeting payload.
- Added automated tests covering the default and personalized greeting scenarios.
- Documented the feature through the requirements, architecture, implementation plan, verification, review, and design review documents.

## Testing

Verified the implementation by running:

- mvn clean test

Result:

- 3 tests run
- 0 failures
- 0 errors
- 0 skipped

## Risks

- The current implementation uses a minimal endpoint contract and may need clarification if the API format is expanded later.
- Blank or whitespace-only name input is currently handled by the default fallback logic, which is acceptable for the current scope but may need explicit documentation if the feature evolves.

## Rollback Plan

If needed, the change can be rolled back by removing the newly added controller, service, response model, and tests from the initial folder.

## Related Jira Story

- SCRUM-3: Display personalized greeting message
