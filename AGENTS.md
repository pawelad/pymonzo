# AI Agent Instructions (`AGENTS.md`)

This document defines the strict, non-negotiable guidelines for any AI agent interacting with the `pymonzo` codebase. Read it fully before performing any work.

## Project References

Always consult these files first for context, standards, and setup instructions:

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview, high-level architecture, and installation. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Coding standards, tooling reference, and CI details. |
| [`CHANGELOG.md`](CHANGELOG.md) | Change history. |
| [`Makefile`](Makefile) | Source of truth for all dev automation - always prefer `make` over raw commands. |
| [`pyproject.toml`](pyproject.toml) | Dependency groups, build definitions, and tool config (`black`, `isort`, `ruff`, `mypy`, `pytest`, `interrogate`). |
| [`noxfile.py`](noxfile.py) | Nox sessions run by CI: `tests`, `coverage_report`, `code_style_checks`, `type_checks`, `docs`. |

## Project Context & Toolchain

- **Core Identity**: `pymonzo` is a modern Python API client for the Monzo public API.
- **Python Version**: Python 3.9+.
- **Typing & Validation**: The codebase is strictly typed and utilizes `pydantic` extensively for defining and validating API schemas.
- **`make` is the Source of Truth**: Never run raw tool commands when a `make` target exists. Run `make help` for the full list.
- **Formatting**: Always use `make format` (`black` + `isort` + `ruff check --fix`). Never run formatters directly.
- **Testing**: Always use `make test` which invokes `nox`.

## The "Do Not" List

- **Do not hallucinate files or states.** Verify paths exist before reading or writing.
- **Do not run raw formatters.** Always use `make format`.
- **Do not skip tests.** New functionality without tests will be rejected.
- **Do not forget to update types/schemas.** If a Monzo API signature changes, the associated `pydantic` schemas must be updated.
- **Do not commit without formatting.** `make format` must pass cleanly.

## Pre-flight Checklist

Before concluding any task, verify each item:

- [ ] Did I run `make format` and does it pass cleanly?
- [ ] Did I run `make test` and do the relevant core tests pass?
- [ ] If I modified API behavior, did I update the corresponding `pydantic` schemas?
- [ ] If I modified API signatures, did I ensure that typing and docstrings were updated?
