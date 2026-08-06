# Architecture Document

## Current Architecture

The application in the initial folder is a minimal Spring Boot service built with Java 17 and Maven. The entry point is the Spring Boot application class, which boots the web application and exposes the service through the embedded Spring runtime. At this stage, the project does not yet contain a dedicated controller, service, or data model for the greeting feature, so the architecture is intentionally simple and follows the default Spring Boot structure.

The current solution is a single-service application with no persistence layer, no external integrations, and no user interface. Its purpose is to provide a lightweight REST service foundation that can grow to support the requirements of SCRUM-3.

## Proposed Architecture

For SCRUM-3, the architecture should remain lightweight and layered while introducing the minimum components needed to support a personalized greeting endpoint.

The proposed design follows a standard Spring MVC style:

1. A web controller receives incoming HTTP requests.
2. A service component handles the greeting logic.
3. A simple response model represents the greeting payload.
4. The application remains a single Spring Boot service with no database dependency.

This approach keeps the solution easy to test, easy to understand, and consistent with the existing Spring Boot structure.

## Components

### 1. Application Bootstrap
- Responsible for starting the Spring Boot application.
- Initializes the web context and configures the application runtime.

### 2. REST Controller
- Handles incoming HTTP requests for the greeting endpoint.
- Parses the optional name parameter.
- Returns a greeting response to the client.

### 3. Greeting Service
- Encapsulates the business logic for creating the message.
- Applies the default value of World when no name is supplied.
- Keeps the controller thin and focused on request handling.

### 4. Response Model
- Represents the payload returned by the endpoint.
- Contains the greeting message in a simple structure suitable for JSON responses.

### 5. Test Layer
- Verifies that the application starts correctly and that the greeting behavior is working as expected.
- Confirms the endpoint behavior for both provided and default values.

## Responsibilities

- The controller is responsible for HTTP concerns such as request mapping and response formatting.
- The service is responsible for business rules and greeting generation.
- The model is responsible for representing API output.
- The test layer is responsible for validating behavior without changing production code.

## Technology Stack

- Java 17
- Spring Boot 4.0.7
- Spring Web MVC
- Maven
- JUnit 5 for testing

## REST Endpoint Design

### Proposed Endpoint
- Method: GET
- Path: /greeting

### Request Parameters
- name: optional query parameter

### Example Requests
- /greeting
- /greeting?name=Alice

### Example Responses
- Without name: Hello, World!
- With name: Hello, Alice!

### Status Codes
- 200 OK for successful requests

## Request Flow

1. A client sends an HTTP GET request to /greeting.
2. The controller receives the request and extracts the optional name parameter.
3. The controller delegates to the greeting service.
4. The service constructs the greeting message using the provided name or the default value World.
5. The controller returns the message as a JSON response.
6. The client receives the greeting payload with an HTTP 200 response.

## Data Model

The feature does not require persistence or a database model. A simple response object is sufficient.

### Greeting Response
- message: string

This object contains the final greeting text that is returned to the client.

## Package Structure

The proposed package organization is aligned with the current project layout:

- com.example.restservice
  - RestServiceApplication
  - controller
    - GreetingController
  - service
    - GreetingService
  - model
    - GreetingResponse

This structure keeps the application organized without introducing unnecessary complexity.

## Risks

- The current project is a minimal scaffold, so the feature must be introduced carefully to avoid over-engineering.
- The endpoint design could become ambiguous if naming conventions are not kept consistent.
- The default handling for blank or empty names should be defined clearly to avoid inconsistent behavior.
- If additional features are introduced later, the simple structure may need to evolve into a more formal layered design.

## Assumptions

- The goal of SCRUM-3 is limited to implementing a simple personalized greeting endpoint.
- No database or external service integration is required for this story.
- The solution should remain compatible with the current Spring Boot application setup.
- The implementation should remain focused on the greeting feature and avoid unrelated architectural changes.
