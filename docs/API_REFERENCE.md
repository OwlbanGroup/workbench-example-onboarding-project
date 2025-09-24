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

###### `InputSanitizer`
Input validation and sanitization.

**Methods:**
- `sanitize_text_input(text, max_length)` -> str: Sanitize text input
- `validate_file_upload(content, filename)` -> bool: Validate file uploads
- `sanitize_url(url)` -> str: Sanitize URLs

###### `RateLimiter`
API rate limiting functionality.

**Methods:**
- `check_rate_limit(identifier, requests, window)` -> bool: Check rate limit
- `get_remaining_requests(identifier)` -> int: Get remaining requests

###### `SecretManager`
Secure secret storage and retrieval.

**Methods:**
- `get_secret(key, default)` -> Optional[str]: Get secret value
- `hash_sensitive_data(data, salt)` -> str: Hash sensitive data

###### `SecurityHeaders`
Security header management.

**Methods:**
- `apply_security_headers()`: Apply security headers
- `validate_request_origin(headers)` -> bool: Validate request origin

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
