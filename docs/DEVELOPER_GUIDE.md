# Developer Guide for NVIDIA AI Workbench Tutorial

## Overview
This guide provides instructions for developers contributing to the NVIDIA AI Workbench Tutorial application.

## Project Structure
```
code/tutorial_app/
├── common/           # Shared utilities and modules
│   ├── sidebar.py    # Navigation and progress tracking
│   ├── theme.py      # UI theming and state management
│   ├── localization.py # Internationalization support
│   ├── testing.py    # Test utilities and validation
│   ├── wb_svc_client.py # AI Workbench API client
│   └── icons.py      # Icon definitions
├── pages/            # Tutorial page implementations
│   ├── overview.py   # Tutorial overview page
│   ├── basic_01.py   # Basic tutorial 1
│   └── ...
└── tests/            # Test suite
    ├── test_integration.py
    ├── test_property_based.py
    └── test_performance.py
```

## Development Setup

### Prerequisites
- Python 3.8+
- NVIDIA AI Workbench
- Git

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install development dependencies: `pip install pytest hypothesis psutil`

### Running the Application
```bash
streamlit run code/tutorial_app/streamlit_app.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest code/tutorial_app/tests/test_integration.py
pytest code/tutorial_app/tests/test_property_based.py
pytest code/tutorial_app/tests/test_performance.py

# Run with coverage
pytest --cov=code/tutorial_app
```

## Adding New Tutorials

### 1. Create Page File
Create a new file in `code/tutorial_app/pages/` following this template:

```python
from pathlib import Path
import streamlit as st

from ..common import localization, theme
from . import your_tutorial_tests as TESTS

MESSAGES = localization.load_messages(__file__)
NAME = Path(__file__).stem
COMPLETED_TASKS = 0

with theme.Theme():
    # Header
    st.title(MESSAGES.get("title"))
    st.write(MESSAGES.get("welcome_msg"))
    st.header(MESSAGES.get("header"), divider="gray")

    # Print Tasks
    for task in MESSAGES.get("tasks", []):
        if not theme.print_task(NAME, task, TESTS, MESSAGES):
            break
        COMPLETED_TASKS += 1
    else:
        # Print footer after last task
        st.success(MESSAGES.get("closing_msg", None))
        theme.print_footer_nav(NAME)

    # save state updates
    theme.ensure_state(f"{NAME}_completed", COMPLETED_TASKS)
    theme.ensure_state(f"{NAME}_total", len(MESSAGES.get("tasks", [])))
```

### 2. Create Localization File
Create `your_tutorial.en_US.yaml`:

```yaml
title: "Your Tutorial Title"
welcome_msg: "Welcome to this tutorial!"
header: "Tutorial Content"
tasks:
  - name: "Task 1"
    msg: "Complete this task"
    test: "check_task_1"
    response: "Task 1 completed successfully!"
closing_msg: "Tutorial completed!"
```

### 3. Create Test Functions
Create `your_tutorial_tests.py`:

```python
def check_task_1():
    """Check if task 1 is completed."""
    # Your validation logic here
    return True, "Task completed", None
```

### 4. Update Navigation
Add your tutorial to `code/tutorial_app/pages/sidebar.yaml`:

```yaml
navbar:
  - label: "Your Section"
    children:
      - label: "Your Tutorial"
        target: "your_tutorial"
```

## Code Standards

### Python Style
- Follow PEP 8
- Use type hints
- Write comprehensive docstrings
- Maximum line length: 120 characters

### Testing
- Write tests for all new functionality
- Include property-based tests for critical functions
- Add performance benchmarks for slow operations
- Aim for >80% code coverage

### Documentation
- Update this guide for significant changes
- Document API changes in README.md
- Add ADRs for architectural decisions

## Deployment
The application is deployed as part of NVIDIA AI Workbench. No additional deployment steps are required for developers.

## Contributing
1. Create a feature branch
2. Make your changes
3. Run tests: `pytest`
4. Run linting: `pylint code/tutorial_app/`
5. Submit a pull request

## Troubleshooting
- **Import errors**: Ensure you're in the correct directory
- **Test failures**: Check that AI Workbench is running
- **Performance issues**: Run performance benchmarks to identify bottlenecks
