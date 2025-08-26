# Veeva Vault OpenAPI Specification

This repository contains the OpenAPI 3.0 specification for the Veeva Vault API.

## Repository Structure

The API specification is organized by version in the `api/` directory. Each version has its own subdirectory (e.g., `api/v25.1/`).

Inside each versioned directory, the specification is split into multiple files for better maintainability:

- `openapi.yaml`: The main entry point for the API specification. It contains the `info`, `servers`, and references to the path definitions.
- `paths/`: This directory contains the individual API path definitions, with each file corresponding to a specific endpoint.

This structure allows for easier navigation and management of the API specification, especially as it grows and evolves.

## Getting Started

To work with this repository, you will need a tool that supports OpenAPI 3.0 specification with file references. Some popular tools include:

- [Swagger Editor](https://editor.swagger.io/)
- [Redocly](https://redocly.com/)
- [Spectral](https://github.com/stoplightio/spectral) (for linting)

## Validation

It is recommended to use a linter like [Spectral](https://github.com/stoplightio/spectral) to validate the specification. You can run Spectral from the command line to check for errors and inconsistencies.

Example command:
```bash
spectral lint api/v25.1/openapi.yaml
```

This will help ensure the quality and consistency of the API specification.
