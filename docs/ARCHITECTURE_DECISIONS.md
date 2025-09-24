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

## ADR 008: Security Implementation
**Date:** 2024
**Status:** Accepted

### Context
The application handles user inputs, file operations, and API calls that require security measures to prevent common web vulnerabilities and ensure safe operation.

### Decision
Implement comprehensive security measures including:
- Input sanitization for all user inputs
- Rate limiting for API calls
- Security headers configuration
- Secure secret management via environment variables and Streamlit secrets
- Audit logging for security events

### Consequences
- **Positive:** Enhanced security posture, protection against common attacks
- **Negative:** Slight performance overhead from validation and logging
- **Risks:** Overly aggressive validation could break legitimate inputs

### Alternatives Considered
- External security proxy (rejected due to complexity)
- Minimal security (rejected due to risk exposure)

## ADR 009: Rate Limiting Strategy
**Date:** 2024
**Status:** Accepted

### Context
API calls to the NVIDIA AI Workbench GraphQL service need protection against abuse while maintaining usability.

### Decision
Implement in-memory rate limiting with:
- 100 requests per minute default limit
- 60-second sliding window
- Per-client identification via IP/request context
- Graceful degradation with user-friendly error messages

### Consequences
- **Positive:** Prevents API abuse, maintains service availability
- **Negative:** May impact legitimate high-frequency users
- **Mitigation:** Configurable limits, clear error messaging

## ADR 010: Secret Management
**Date:** 2024
**Status:** Accepted

### Context
Application requires secure storage of sensitive configuration like API keys, database credentials, and proxy settings.

### Decision
Use a hierarchical secret management approach:
1. Environment variables (primary)
2. Streamlit secrets (fallback)
3. Default values (development only)

Implement SecretManager class for centralized access.

### Consequences
- **Positive:** Secure, flexible configuration management
- **Negative:** Requires proper environment setup
- **Risks:** Misconfiguration could expose secrets

## ADR 011: Error Handling Strategy
**Date:** 2024
**Status:** Accepted

### Context
Application needs robust error handling for user experience and debugging.

### Decision
Implement multi-layer error handling:
- Graceful degradation for missing dependencies
- User-friendly error messages in UI
- Detailed logging for debugging
- Custom exceptions for domain-specific errors
- Retry logic for transient failures

### Consequences
- **Positive:** Better user experience, easier debugging
- **Negative:** Increased code complexity
- **Mitigation:** Consistent error handling patterns

## ADR 012: Performance Optimization
**Date:** 2024
**Status:** Accepted

### Context
Application needs to maintain responsive UI while handling complex operations.

### Decision
Implement performance optimizations:
- Caching for expensive operations (file I/O, API calls)
- Lazy loading for heavy components
- State management optimization
- Connection pooling for external services
- Performance benchmarks and monitoring

### Consequences
- **Positive:** Improved user experience, scalability
- **Negative:** Increased memory usage, complexity
- **Mitigation:** Configurable cache sizes, monitoring tools

## ADR 013: Type Safety Implementation
**Date:** 2024
**Status:** Accepted

### Context
Python's dynamic typing can lead to runtime errors and maintenance issues.

### Decision
Implement comprehensive type safety:
- Type hints for all functions and methods
- Strict type checking where beneficial
- Pydantic models for data validation
- Runtime type checking for critical paths

### Consequences
- **Positive:** Better code reliability, IDE support, documentation
- **Negative:** Development overhead, potential false positives
- **Mitigation:** Gradual adoption, tool configuration
