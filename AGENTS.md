# Guidelines for AI Agents

Welcome! If you are an AI agent working on `pymonzo`, please follow these instructions.

For additional context about the project, refer to the [README.md](./README.md) and [CONTRIBUTING.md](./CONTRIBUTING.md) files.

## General Information
- The project is written in Python 3.9+.
- The codebase is heavily typed and uses `pydantic` for API schema validation.

## Tools
- `make` is used for running various common tasks (see `Makefile` for available commands).
- `nox` is used to run tests across different python versions, and for linting/type-checking.

## Code Style and Formatting
- The project uses `black`, `isort`, and `ruff` for code style and linting.
- To format the code, run: `make format`

## Testing
- Tests are written with `pytest`.
- Run tests via `make test` or `nox`.

## Type Checking
- Run type checks using `mypy`. This is available via the `nox` configuration.

## Submitting Changes
- Always make sure `make format` and `make test` are passing before finalizing your changes.
- Remember to update documentation if you modify API signatures or behavior.
