# Developer Workflow Guide

## Overview

This guide provides comprehensive instructions for developers working on the NVIDIA AI Workbench tutorial application. It covers development setup, coding standards, testing procedures, and deployment workflows.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- NVIDIA AI Workbench installed
- Git for version control
- VS Code with Python extension (recommended)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd workbench-example-onboarding-project
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Set up development environment:**
   ```bash
   # Copy environment template
   cp variables.env.template variables.env
   # Edit variables.env with your configuration
   ```

### IDE Configuration

#### VS Code Setup

1. **Install recommended extensions:**
   - Python
   - Pylance
   - Python Docstring Generator
   - YAML
   - GitLens

2. **Configure Python interpreter:**
   - Select the virtual environment: `.venv`
   - Set Python path to include `src/tutorial_app`

3. **Configure linting and formatting:**
   ```json
   {
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.linting.flake8Enabled": true,
     "python.formatting.provider": "black",
     "python.formatting.blackArgs": ["--line-length", "100"],
     "editor.formatOnSave": true
   }
   ```

## Project Structure

```
workbench-example-onboarding-project/
├── src/tutorial_app/           # Main application code
│   ├── common/                 # Shared utilities
│   │   ├── sidebar.py         # Navigation management
│   │   ├── theme.py           # Theme and state management
│   │   ├── testing.py         # Testing utilities
│   │   ├── localization.py    # i18n support
│   │   └── security.py        # Security utilities
│   ├── pages/                 # Tutorial pages
│   │   ├── basic_01.py        # Basic tutorials
│   │   ├── advanced_01.py     # Advanced tutorials
│   │   └── *_tests.py         # Page-specific tests
│   ├── tests/                 # Test suite
│   │   ├── test_property_based.py
│   │   ├── test_performance.py
│   │   └── test_integration.py
│   └── streamlit_app.py       # Main application
├── docs/                      # Documentation
├── app/                       # Production app
├── code/                      # Development code
├── data/                      # Data files
└── models/                    # Model files
```

## Development Workflow

### 1. Creating a New Tutorial Page

#### Step 1: Create the Page File

Create `src/tutorial_app/pages/new_tutorial.py`:

```python
"""New tutorial page implementation."""

import streamlit as st
from common.sidebar import APP_SIDEBAR
from common.localization import load_messages

# Load localized messages
messages = load_messages(__file__)

def main():
    """Main page content."""
    st.title(messages.get('title', 'New Tutorial'))

    st.markdown(messages.get('description', 'Tutorial description'))

    # Tutorial content goes here
    with st.expander("Step 1: Getting Started"):
        st.write("Step content...")

if __name__ == "__main__":
    main()
```

#### Step 2: Create Localization File

Create `src/tutorial_app/pages/new_tutorial.en_US.yaml`:

```yaml
title: "New Tutorial"
description: "Learn about new tutorial topic"
steps:
  - "Complete step 1"
  - "Complete step 2"
  - "Complete step 3"
messages:
  step1_title: "Step 1: Getting Started"
  step1_content: "Content for step 1"
  step2_title: "Step 2: Advanced Concepts"
  step2_content: "Content for step 2"
```

#### Step 3: Create Tests

Create `src/tutorial_app/pages/new_tutorial_tests.py`:

```python
"""Tests for new tutorial page."""

from common import testing

def check_step1_completed():
    """Verify step 1 completion."""
    # Add validation logic
    pass

def check_step2_completed():
    """Verify step 2 completion."""
    # Add validation logic
    pass

def check_tutorial_completed():
    """Verify entire tutorial completion."""
    # Add validation logic
    pass
```

#### Step 4: Update Navigation

Update `src/tutorial_app/pages/sidebar.yaml`:

```yaml
navbar:
  - label: "Existing Section"
    children:
      - label: "New Tutorial"
        target: "new_tutorial"
        show_progress: true
```

#### Step 5: Update Test Runner

Update `run_all_tests.py`:

```python
test_files = [
    # ... existing tests
    "src/tutorial_app/pages/new_tutorial_tests.py",
]
```

### 2. Adding New Common Utilities

#### Step 1: Create Utility Module

Create `src/tutorial_app/common/new_utility.py`:

```python
"""New utility module."""

from typing import Any, Optional

def new_utility_function(param: str) -> Optional[dict]:
    """Perform new utility operation.

    Args:
        param: Input parameter

    Returns:
        Result dictionary or None
    """
    # Implementation
    pass
```

#### Step 2: Add Tests

Create `src/tutorial_app/tests/test_new_utility.py`:

```python
"""Tests for new utility module."""

import pytest
from common.new_utility import new_utility_function

class TestNewUtility:
    """Test cases for new utility."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = new_utility_function("test")
        assert result is not None

    def test_edge_cases(self):
        """Test edge cases."""
        # Test various edge cases
        pass
```

#### Step 3: Update Documentation

Update `docs/API_REFERENCE.md` with new module documentation.

### 3. Security Considerations

#### Input Validation

Always validate and sanitize user inputs:

```python
from common.security import InputSanitizer

def process_user_input(user_input: str) -> str:
    """Process user input with security checks."""
    sanitized = InputSanitizer.sanitize_text_input(user_input)
    # Process sanitized input
    return sanitized
```

#### Rate Limiting

Implement rate limiting for API calls:

```python
from common.security import RateLimiter

def api_call_with_rate_limit(user_id: str, data: dict) -> dict:
    """Make API call with rate limiting."""
    if not RateLimiter.check_rate_limit(user_id):
        raise ValueError("Rate limit exceeded")

    # Make API call
    return {"result": "success"}
```

## Testing Procedures

### Running Tests

#### Run All Tests
```bash
python run_all_tests.py
```

#### Run Specific Test Suite
```bash
# Unit tests
python -m pytest src/tutorial_app/tests/ -v

# Property-based tests
python -m pytest src/tutorial_app/tests/test_property_based.py -v

# Performance tests
python -m pytest src/tutorial_app/tests/test_performance.py -v
```

#### Run Page Tests
```bash
python src/tutorial_app/pages/basic_01_tests.py
```

### Test Coverage

Aim for >85% test coverage:

```bash
python -m pytest --cov=src/tutorial_app --cov-report=html
```

### Performance Testing

Run performance benchmarks:

```bash
python -m pytest src/tutorial_app/tests/test_performance.py::TestPerformanceBenchmarks::test_complete_workflow_performance -v
```

## Code Quality Standards

### Type Hints

Use comprehensive type hints:

```python
from typing import List, Dict, Optional, Any

def process_data(data: List[Dict[str, Any]]) -> Optional[str]:
    """Process list of dictionaries.

    Args:
        data: List of data dictionaries

    Returns:
        Processed result or None
    """
    pass
```

### Documentation

#### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """Brief description of function.

    More detailed description of what the function does,
    including any important notes or warnings.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this is raised

    Examples:
        >>> function_name("test", 1)
        True
    """
    pass
```

#### Inline Comments

Use inline comments for complex logic:

```python
# Calculate weighted average with boundary checks
if total_weight > 0:
    average = sum(values) / total_weight  # Avoid division by zero
else:
    average = 0.0
```

### Naming Conventions

- **Functions/Methods**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Modules**: `snake_case`
- **Private members**: `_leading_underscore`

### Error Handling

Implement comprehensive error handling:

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    # Handle specific error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle general error
finally:
    # Cleanup code
    pass
```

## Performance Optimization

### Profiling

Use profiling tools to identify bottlenecks:

```python
import cProfile
import pstats

def profile_function():
    """Profile function execution."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Code to profile
    expensive_operation()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
```

### Caching

Implement caching for expensive operations:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def cached_expensive_operation(param: str) -> dict:
    """Expensive operation with caching."""
    # Simulate expensive operation
    time.sleep(1)
    return {"result": f"processed_{param}"}
```

### Memory Management

Monitor memory usage:

```python
import psutil
import os

def get_memory_usage() -> float:
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024
```

## Deployment

### Local Development

```bash
# Run development server
streamlit run src/tutorial_app/streamlit_app.py

# Run with security features
streamlit run src/tutorial_app/streamlit_app_secure.py
```

### Production Deployment

#### Docker Deployment

```bash
# Build Docker image
docker build -t tutorial-app .

# Run container
docker run -p 8501:8501 tutorial-app
```

#### AI Workbench Deployment

1. Open NVIDIA AI Workbench
2. Import project
3. Click "Open Tutorial" button

### Environment Configuration

#### Development
```bash
export ENVIRONMENT=development
export DEBUG=true
export LOG_LEVEL=DEBUG
```

#### Production
```bash
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO
export PROXY_PREFIX=/tutorial-app
```

## Debugging

### Logging

Configure logging for debugging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Common Issues

#### Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Add to path if needed
export PYTHONPATH="${PYTHONPATH}:src/tutorial_app"
```

#### Streamlit Issues
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit

# Run with debug mode
streamlit run app.py --logger.level=debug
```

#### Test Failures
```bash
# Run tests with verbose output
python -m pytest -v -s

# Run specific failing test
python -m pytest src/tutorial_app/tests/test_property_based.py::TestPropertyBased::test_menuitem_label_properties -v
```

## Contributing

### Pull Request Process

1. **Create feature branch:**
   ```bash
   git checkout -b feature/new-tutorial
   ```

2. **Make changes and add tests**

3. **Run full test suite:**
   ```bash
   python run_all_tests.py
   ```

4. **Update documentation**

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add new tutorial feature"
   ```

6. **Push and create PR:**
   ```bash
   git push origin feature/new-tutorial
   ```

### Code Review Checklist

- [ ] Type hints added
- [ ] Docstrings complete
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Security considerations addressed
- [ ] Performance impact assessed
- [ ] Cross-platform compatibility verified

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

## Support

### Getting Help

1. **Check documentation:** `docs/` directory
2. **Review existing issues:** GitHub Issues
3. **Ask in forums:** NVIDIA Developer Forums
4. **Contact maintainers:** Through GitHub

### Reporting Bugs

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Environment**
- OS: [e.g., Windows 10]
- Python: [e.g., 3.9]
- Streamlit: [e.g., 1.25.0]

**Additional Context**
Any other relevant information
```

## Security

### Security Checklist

- [ ] Input validation implemented
- [ ] XSS prevention in place
- [ ] Rate limiting configured
- [ ] Secrets properly managed
- [ ] Dependencies updated
- [ ] Security headers applied

### Reporting Security Issues

Email security@nvidia.com with details. Do not create public GitHub issues for security vulnerabilities.
