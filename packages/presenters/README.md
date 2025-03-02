# Presenters

The **Presenters** package is a core component of the Agents Service, responsible for exposing processed data and interfacing with external clients. It provides multiple presentation layers—including REST APIs and WebSocket interfaces—to facilitate real-time communication and control of the Agents Service.

## Overview

The presenters package decouples presentation logic from the underlying business logic, ensuring a clean and maintainable codebase. It is divided into two main modules:
- **REST API Module:** Handles HTTP requests and responses, providing endpoints for managing agents, retrieving reports, and configuring the service.
- **WebSocket Module:** Enables real-time, bidirectional communication, streaming updates and notifications to connected clients.

Both modules leverage a set of controllers and dependency management utilities to ensure consistency and ease of integration with the overall service architecture.

## Usage

### Controllers & Use Cases

Each controller within the REST and WebSocket modules is designed to handle a specific set of operations. They typically:
- Validate incoming requests.
- Invoke the appropriate use case from the usecases library.
- Format and return responses.

### Dependency Management

Both the REST and WebSocket modules use dedicated dependency files (`dependencies.py`) to manage configuration and dependencies. This design promotes modularity and eases testing. Ensure that any changes to external integrations are reflected in these files.
