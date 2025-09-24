# NVIDIA AI Workbench Tutorial Application - API Reference

## Overview

This document provides comprehensive API reference for the NVIDIA AI Workbench tutorial application, a Streamlit-based interactive learning platform.

## Architecture

The application follows a modular architecture with the following key components:

- **Streamlit App** (`streamlit_app.py`): Main application entry point
- **Common Modules** (`common/`): Shared utilities and services
- **Pages** (`pages/`): Tutorial content and interactive exercises
- **Tests** (`tests/`): Comprehensive test suite

## Core Modules

### Common Modules

#### sidebar.py

Navigation and UI structure management.

##### Classes

###### `MenuItem`
Represents a single menu item in the navigation.

**Attributes:**
- `label` (str): Display name
- `target` (str): Target page identifier
- `show_progress` (bool): Whether to display progress indicator

**Properties:**
- `progress_string` (str): Current progress status
- `full_label` (str): Label with progress indicator
- `filepath` (str): Full path to page file
- `markdown` (str): Markdown link format

**Methods:**
- `progress_string` -> str: Get formatted progress string
- `full_label` -> str: Get label with progress
- `filepath` -> str: Get file path
- `markdown` -> str: Get markdown link

###### `Menu`
Represents a menu section containing multiple items.

**Attributes:**
- `label` (str): Menu section name
- `children` (list[MenuItem]): Menu items in this section

###### `Links`
External links configuration.

**Attributes:**
- `documentation` (Optional[str]): Documentation URL
- `gethelp` (Optional[str]): Help URL
- `about` (Optional[str]): About page URL
- `bugs` (Optional[str]): Bug reporting URL
- `settings` (Optional[str]): Settings URL

###### `Sidebar`
Main sidebar configuration and rendering.

**Attributes:**
- `header` (Optional[str]): Sidebar header text
- `navbar` (list[Menu]): Navigation menu sections
- `links` (Links): External links

**Methods:**
- `from_yaml()` -> Sidebar: Load configuration from YAML
- `page_list` -> List[str]: Get list of page objects
- `prev_and_next_nav(page_name)` -> Tuple[Optional[str], Optional[str]]: Get navigation links
- `render()`: Render the complete sidebar

#### theme.py

Theme and state management.

##### Functions

###### `load_state()`
Load application state from persistent storage.

**Returns:** None

###### `save_state()`
Save current application state to persistent storage.

**Returns:** None

###### `ensure_state(key, value)`
Ensure a state key has a specific value.

**Parameters:**
- `key` (str): State key
- `value` (Any): Value to set

**Returns:** None

###### `slugify(text)`
Convert text to URL-safe slug.

**Parameters:**
- `text` (str): Input text

**Returns:** str: Slugified text

#### testing.py

Testing utilities and validation functions.

##### Classes

###### `TestFail(Exception)`
Exception raised when a test fails.

##### Functions

###### `run_test(fun)`
Execute a test function with caching.

**Parameters:**
- `fun` (Callable): Test function to execute

**Returns:** tuple[bool, Optional[str], Optional[Any]]: (passed, error_message, result)

###### `get_project(project_name)`
Retrieve project information.

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** dict: Project data

###### `ensure_build_state(project, target)`
Verify project build state.

**Parameters:**
- `project` (dict): Project data
- `target` (BuildState): Desired build state

**Returns:** None

**Raises:** TestFail: If state doesn't match

#### localization.py

Internationalization and localization support.

##### Functions

###### `load_messages(file_path)`
Load localized messages for a file.

**Parameters:**
- `file_path` (str): Path to the file

**Returns:** dict: Localized messages

#### security.py

Security utilities and best practices.

##### Classes

###### `SecurityError(Exception)`
Custom exception for security violations.

**Attributes:**
- Standard Exception attributes

###### `InputSanitizer`
Input validation and sanitization.

**Methods:**
- `sanitize_text_input(text, max_length)` -> str: Sanitize text input by removing dangerous content
- `validate_file_upload(file_content, filename)` -> bool: Validate uploaded file content and filename
- `sanitize_url(url)` -> str: Sanitize and validate URLs

**Raises:** SecurityError for dangerous patterns or invalid inputs

###### `RateLimiter`
API rate limiting functionality with in-memory storage.

**Methods:**
- `check_rate_limit(identifier, requests, window)` -> bool: Check if request is within rate limits
- `get_remaining_requests(identifier)` -> int: Get remaining requests for an identifier

**Parameters:**
- `identifier` (str): Unique client identifier
- `requests` (int): Max requests allowed (default: 100)
- `window` (int): Time window in seconds (default: 60)

###### `SecretManager`
Secure secret storage and retrieval from environment variables and Streamlit secrets.

**Methods:**
- `get_secret(key, default)` -> Optional[str]: Get secret from env vars or Streamlit secrets
- `hash_sensitive_data(data, salt)` -> str: Hash sensitive data using SHA256

**Parameters:**
- `key` (str): Secret key name
- `default` (Optional[str]): Default value if not found
- `data` (str): Data to hash
- `salt` (Optional[str]): Optional salt for hashing

###### `SecurityHeaders`
Security header management for web applications.

**Methods:**
- `apply_security_headers()`: Log security headers for manual web server configuration
- `validate_request_origin(request_headers)` -> bool: Validate request origin for CORS-like protection

##### Functions

###### `initialize_security()`
Initialize security measures for the application.

**Returns:** None

###### `secure_file_operation(filepath, operation)`
Check if file operation is secure.

**Parameters:**
- `filepath` (str): File path to check
- `operation` (str): Operation type ('read', 'write', 'execute')

**Returns:** bool: True if operation is allowed

###### `audit_log(action, user_id, details)`
Log security-related actions for audit purposes.

**Parameters:**
- `action` (str): Action performed
- `user_id` (Optional[str]): User identifier
- `details` (Optional[Dict[str, Any]]): Additional details

**Returns:** None

#### wb_svc_client.py

Client for NVIDIA AI Workbench GraphQL API with Unix socket and HTTP support.

##### Functions

###### `query(query_str)`
Send a GraphQL query over Unix socket or HTTP.

**Parameters:**
- `query_str` (str): GraphQL query string

**Returns:** dict: Query response data

**Raises:** Exception if rate limit exceeded

###### `list_projects()`
List all projects with name, id, and path.

**Returns:** dict[str, Any]: Projects data

###### `get_project_path(project_name)`
Find the file system path for a project.

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** Optional[str]: Project path or None if not found

###### `get_project(project_name)`
Get detailed project information.

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** Optional[dict[str, Any]]: Project details or None if not found

###### `get_file(project_name, relative_path, filename)`
Retrieve file contents from a project.

**Parameters:**
- `project_name` (str): Name of the project
- `relative_path` (str): Relative path within project
- `filename` (str): Name of the file

**Returns:** dict[str, Any]: File data including contents

###### `get_packages(project_name)`
List installed packages in a project environment.

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** Optional[dict[str, Any]]: Package information or None

###### `get_gpu_request(project_name)`
Query GPU resource allocation for a project.

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** Optional[dict[str, Any]]: GPU request data or None

## Page Modules

### Tutorial Pages

Each tutorial page follows a consistent structure:

#### Basic Structure
```python
import streamlit as st
from common.sidebar import APP_SIDEBAR
from common.localization import load_messages

# Load localized messages
messages = load_messages(__file__)

def main():
    st.title(messages.get('title', 'Tutorial Title'))

    # Tutorial content and exercises
    # ...

if __name__ == "__main__":
    main()
```

#### Available Pages

1. **basic_01.py** - Getting Started with AI Workbench
2. **basic_02.py** - Environment Customization
3. **basic_03.py** - Project Structure and Management
4. **overview.py** - Tutorial Overview
5. **advanced_01.py** - Advanced Environment Configuration
6. **advanced_02.py** - Custom Container Usage
7. **advanced_03.py** - Advanced RAG Applications
8. **settings.py** - Application Settings

## Testing Framework

### Test Categories

#### Unit Tests
Located in `src/tutorial_app/tests/`
- `test_property_based.py`: Property-based tests using Hypothesis
- `test_performance.py`: Performance benchmarks
- `test_integration.py`: Integration tests

#### Page Tests
Located in `src/tutorial_app/pages/`
- `{page_name}_tests.py`: Page-specific validation tests

### Test Utilities

#### `benchmark_performance(func)`
Decorator for performance benchmarking.

**Parameters:**
- `func` (Callable): Function to benchmark

**Returns:** Callable: Wrapped function

#### `mock_streamlit_session()`
Context manager for mocking Streamlit session state.

**Returns:** Generator: Mock session context

#### `assert_performance_threshold(func, max_time)`
Assert function executes within time threshold.

**Parameters:**
- `func` (Callable): Function to test
- `max_time` (float): Maximum execution time

**Returns:** None

## Configuration

### Environment Variables

- `PROXY_PREFIX`: URL prefix for proxy deployments
- Security-related secrets (managed via SecretManager)

### YAML Configuration

#### Sidebar Configuration (`pages/sidebar.yaml`)
```yaml
header: "Tutorial App"
navbar:
  - label: "Basics"
    children:
      - label: "Getting Started"
        target: "basic_01"
        show_progress: true
links:
  documentation: "https://docs.nvidia.com/ai-workbench"
  gethelp: "https://forums.developer.nvidia.com"
```

#### Localization Files (`pages/*.en_US.yaml`)
```yaml
title: "Getting Started"
description: "Learn the basics of NVIDIA AI Workbench"
steps:
  - "Create your first project"
  - "Explore the interface"
```

## Error Handling

The application implements comprehensive error handling:

### Error Types

- `TestFail`: Tutorial validation failures
- `SecurityError`: Security violations
- Standard Python exceptions with graceful degradation

### Error Recovery

- Graceful fallbacks for missing dependencies
- User-friendly error messages
- Logging for debugging and monitoring

## Performance Characteristics

### Benchmarks

- Sidebar loading: < 1.0s
- Theme operations: < 0.1s per operation
- Navigation: < 0.01s per operation
- Memory usage: < 100MB for typical operations

### Caching

- State persistence with file-based caching
- Test result caching to avoid redundant operations
- Lazy loading for heavy components

## Security Features

### Input Validation
- XSS prevention through input sanitization
- File upload validation
- URL validation and sanitization

### Rate Limiting
- API call rate limiting (100 requests per minute default)
- Configurable limits per endpoint/user

### Security Headers
- Content Security Policy (CSP)
- X-Frame-Options, X-Content-Type-Options
- Referrer Policy, HSTS

### Secret Management
- Environment variable-based secrets
- Streamlit secrets integration
- Sensitive data hashing

## Development Workflow

### Adding New Tutorials

1. Create page file: `pages/new_tutorial.py`
2. Create localization: `pages/new_tutorial.en_US.yaml`
3. Create tests: `pages/new_tutorial_tests.py`
4. Update sidebar configuration
5. Add to test runner

### Testing

```bash
# Run all tests
python run_all_tests.py

# Run specific test
python -m pytest src/tutorial_app/tests/test_property_based.py

# Run with coverage
python -m pytest --cov=src/tutorial_app
```

### Deployment

The application supports multiple deployment scenarios:

- Local development with `streamlit run`
- Docker containerization
- Proxy deployment with `PROXY_PREFIX`
- Production deployment with security hardening

## API Stability

### Version Compatibility

- Python 3.8+
- Streamlit 1.0+
- Pydantic v1/v2 compatibility
- Cross-platform support (Windows, Linux, macOS)

### Deprecation Policy

- APIs marked as deprecated will be supported for 2 major versions
- Breaking changes announced in release notes
- Migration guides provided for major updates

## Troubleshooting

### Common Issues

1. **Import Errors**: Check PYTHONPATH includes `src/tutorial_app`
2. **YAML Parsing Errors**: Validate YAML syntax
3. **Security Violations**: Check input sanitization
4. **Performance Issues**: Review benchmark results

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Checks

The application provides health check endpoints for monitoring:
- Test suite execution status
- Performance benchmark results
- Security validation status
