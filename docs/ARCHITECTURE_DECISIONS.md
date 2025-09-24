# Architecture Decision Records (ADR)

## ADR 001: Project Structure
- Use a modular structure separating common utilities, pages, and tests.
- Common code in `code/tutorial_app/common/`
- Tutorial pages in `code/tutorial_app/pages/`
- Tests in `code/tutorial_app/tests/`

## ADR 002: State Management
- Use Streamlit session state with JSON persistence to disk.
- State file located at `/project/data/scratch/tutorial_state.json`.
- Use retry logic for file I/O to handle concurrency.

## ADR 003: Localization
- Use YAML files for localized messages.
- Load messages based on system locale with fallback to `en_US`.

## ADR 004: Testing Strategy
- Use pytest for unit and integration tests.
- Use hypothesis for property-based testing.
- Include performance benchmarks using custom decorators.

## ADR 005: Security
- Sanitize all user inputs and GraphQL queries.
- Implement rate limiting on GraphQL API calls.
- Manage secrets via environment variables.

## ADR 006: Documentation
- Use README for user and developer guides.
- Maintain ADRs in `docs/` folder.
- Use inline docstrings and type hints extensively.

## ADR 007: Development Workflow
- Use pre-commit hooks for linting and formatting.
- Use pytest for continuous integration testing.
- Use version control branching with feature branches.
