# Copilot Instructions for AI Coding Agents

## Project Overview

## References

- Read `docs/design.md` for comprehensive architecture documentation, including
  data flow diagrams and refactoring improvements.
- See `Makefile` for developer commands (test, lint, venv setup, etc.).

## Developer Guidelines

### Goals

- Ensure that the tool is easy for a non-technical user to configure, extend, and use.
- Make the codebase easy to understand and maintain.
- Ensure new features can be added with minimal code changes.
- Keep configuration separate from code logic.
- Only load and parse configuration files once at initialization.

### Code Style and Documentation

- Follow PEP 8 for all Python code.
- DO NOT HARDCODE values; use configuration the files. Before adding a new config
  parameter, see if it exists in an existing config file.
- Use f-strings for string formatting.
- Use type hints throughout the codebase.
- Add docstrings to all public functions, classes, and modules (Google or NumPy
  style recommended).
- Write meaningful and descriptive names for variables, functions, classes, and
  modules.
- Keep documentation updated when introducing or modifying features.
- Use Markdown for all documentation files.
- Avoid emojis in code comments and documentation.
- Include usage examples in docstrings when helpful.
- Keep modules focused and coherent; avoid excessively long modules.

### Architecture and Design

- Maintain a clear separation of responsibilities:
- Refactor when helpful; remove deprecated code, unused comments, and unused
  files.

### Configuration Management

- Never hardcode configuration values.
- Store them under conf/ and access them through the config loader.
- Do not modify data in data/ directly—especially target_state.csv.This file is
  the ground truth for accuracy evaluation. Only the project maintainer may
  update it.
- Keep environment-specific values in environment variables or .env files when
  appropriate.
- Ensure configuration files remain readable and well-organized.

### Testing and Quality Assurance

- Write tests for all new features (unit, integration where applicable).
- Ensure existing tests pass before merging PRs.
- Prefer small, deterministic test inputs.
- Include a minimal test dataset under tests/data/.
- Keep test names descriptive; test one thing per test.

### Development Workflow

- Use pytest for tests and integrate coverage reporting.
- Maintain a consistent commit style (short summary + clear body when needed).
- Avoid code duplication; extract helpers or shared utilities where appropriate.
- Keep PRs small and focused; large refactors should be coordinated.
- Ensure logging is clear, meaningful, and helpful for debugging.

### Maintenance and Governance

- Remove deprecated features or dead code aggressively.
- Keep dependency versions current and pin them in the appropriate file.
- Avoid unnecessary dependencies; prefer standard library solutions when
  suitable.
