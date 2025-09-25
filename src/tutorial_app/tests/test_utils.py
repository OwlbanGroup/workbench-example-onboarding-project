# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Test utilities and shared testing infrastructure."""

import pytest
import tempfile
import json
import os
from typing import Any, Dict, List, Generator, Callable
from unittest.mock import MagicMock, patch
from pathlib import Path
import time

# Add the parent directory to the path for imports
import sys

sys.path.append(str(Path(__file__).parent.parent))

from common.sidebar import Sidebar, MenuItem, Menu, Links
from common.theme import load_state, save_state, ensure_state
from common.localization import load_messages
from tests import TestConfig


class TestDataGenerator:
    """Generate test data for various testing scenarios."""

    @staticmethod
    def create_valid_menu_items(count: int = 5) -> List[MenuItem]:
        """Create valid menu items for testing."""
        return [MenuItem(label=f"Test Item {i}", target=f"test_target_{i}") for i in range(count)]

    @staticmethod
    def create_nested_menu_structure() -> Menu:
        """Create a nested menu structure for testing."""
        # Create child items
        child_items = TestDataGenerator.create_valid_menu_items(3)

        # Create parent items
        parent_items = [
            MenuItem(label="Parent Item 1", target="parent_1"),
            MenuItem(label="Parent Item 2", target="parent_2"),
        ]

        # Create nested menu
        child_menu = Menu(label="Child Menu", children=child_items)
        parent_items.append(child_menu)

        return Menu(label="Parent Menu", children=parent_items)

    @staticmethod
    def create_sidebar_with_progress_data() -> Sidebar:
        """Create a sidebar with mock progress data."""
        items = TestDataGenerator.create_valid_menu_items(4)
        menu = Menu(label="Test Menu", children=items)
        links = Links(documentation="https://example.com")

        return Sidebar(header="Test Header", navbar=[menu], links=links)

    @staticmethod
    def create_mock_session_state(progress_data: Dict[str, Any]) -> MagicMock:
        """Create a mock session state with progress data."""
        mock_session = MagicMock()
        mock_session.get.side_effect = lambda key, default=None: progress_data.get(key, default)
        mock_session.__setitem__ = MagicMock()
        return mock_session


class TestFixtures:
    """Reusable test fixtures."""

    @staticmethod
    @pytest.fixture
    def temp_state_file() -> Generator[str, None, None]:
        """Create a temporary state file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                {
                    "basic_01_completed": 3,
                    "basic_01_total": 3,
                    "basic_02_completed": 1,
                    "basic_02_total": 2,
                    "advanced_01_completed": 0,
                    "advanced_01_total": 5,
                },
                f,
            )
            temp_file = f.name

        yield temp_file

        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    @staticmethod
    @pytest.fixture
    def mock_streamlit_session() -> Generator[MagicMock, None, None]:
        """Mock Streamlit session state for testing."""
        with patch("streamlit.session_state") as mock_session:
            mock_session.get.return_value = None
            mock_session.__setitem__ = MagicMock()
            yield mock_session

    @staticmethod
    @pytest.fixture
    def sample_sidebar() -> Sidebar:
        """Create a sample sidebar for testing."""
        return TestDataGenerator.create_sidebar_with_progress_data()

    @staticmethod
    @pytest.fixture
    def performance_monitor() -> "PerformanceMonitor":
        """Create a performance monitor for benchmarking."""
        return PerformanceMonitor()


class PerformanceMonitor:
    """Monitor and assert performance requirements."""

    def __init__(self):
        self.baselines: Dict[str, float] = {}

    def benchmark_function(self, func: Callable, *args, **kwargs) -> float:
        """Benchmark a function and return execution time."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print(f"Function {func.__name__} executed in {execution_time:.4f}s")
        return execution_time

    def assert_performance(self, func: Callable, max_time: float, *args, **kwargs) -> None:
        """Assert that a function executes within performance threshold."""
        execution_time = self.benchmark_function(func, *args, **kwargs)
        assert execution_time <= max_time, (
            f"Function {func.__name__} took {execution_time:.4f}s, " f"exceeding threshold of {max_time}s"
        )

    def set_baseline(self, name: str, func: Callable, *args, **kwargs) -> None:
        """Set a performance baseline for a function."""
        execution_time = self.benchmark_function(func, *args, **kwargs)
        self.baselines[name] = execution_time
        print(f"Baseline set for {name}: {execution_time:.4f}s")

    def assert_not_regression(self, name: str, func: Callable, threshold: float = 2.0, *args, **kwargs) -> None:
        """Assert that performance hasn't regressed beyond threshold."""
        if name not in self.baselines:
            raise ValueError(f"No baseline set for {name}")

        execution_time = self.benchmark_function(func, *args, **kwargs)
        baseline = self.baselines[name]

        if execution_time > baseline * threshold:
            raise AssertionError(
                f"Performance regression detected for {name}: "
                f"{execution_time:.4f}s vs baseline {baseline:.4f}s "
                f"(threshold: {threshold}x)"
            )

        print(f"Performance check passed for {name}: {execution_time:.4f}s")


class TestValidator:
    """Validate test results and provide detailed feedback."""

    @staticmethod
    def validate_sidebar_structure(sidebar: Sidebar) -> List[str]:
        """Validate sidebar structure and return any issues."""
        issues = []

        if not sidebar.header:
            issues.append("Sidebar missing header")

        if not sidebar.navbar:
            issues.append("Sidebar missing navbar")
        else:
            for menu in sidebar.navbar:
                if not menu.label:
                    issues.append(f"Menu missing label: {menu}")
                if not menu.children:
                    issues.append(f"Menu missing children: {menu.label}")

        if not sidebar.links:
            issues.append("Sidebar missing links")

        return issues

    @staticmethod
    def validate_menu_item(item: MenuItem) -> List[str]:
        """Validate menu item and return any issues."""
        issues = []

        if not item.label:
            issues.append("MenuItem missing label")

        if not item.target:
            issues.append("MenuItem missing target")

        if not item.filepath.endswith(".py"):
            issues.append(f"MenuItem filepath doesn't end with .py: {item.filepath}")

        return issues

    @staticmethod
    def validate_progress_data(progress_data: Dict[str, Any]) -> List[str]:
        """Validate progress data structure."""
        issues = []

        for key, value in progress_data.items():
            if not isinstance(value, (int, float)):
                issues.append(f"Progress value not numeric for {key}: {value}")

            if isinstance(value, (int, float)) and value < 0:
                issues.append(f"Negative progress value for {key}: {value}")

        return issues


class TestRunner:
    """Run comprehensive test suites."""

    def __init__(self):
        self.results: Dict[str, Any] = {}

    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        print("Running integration tests...")

        try:
            # Test sidebar loading
            sidebar = Sidebar.from_yaml()
            assert sidebar is not None

            # Test theme operations
            load_state()
            save_state()
            ensure_state("test_key", "test_value")

            # Test localization
            messages = load_messages("code/tutorial_app/pages/basic_01.py")
            assert isinstance(messages, dict)

            self.results["integration"] = {"status": "PASSED", "tests": 3}
            print("SUCCESS: Integration tests passed")

        except Exception as e:
            self.results["integration"] = {"status": "FAILED", "error": str(e)}
            print(f"ERROR: Integration tests failed: {e}")

        return self.results["integration"]

    def run_property_tests(self) -> Dict[str, Any]:
        """Run property-based tests."""
        print("Running property-based tests...")

        try:
            # Test MenuItem properties
            item = MenuItem(label="Test Label", target="test_target")
            assert item.label == "Test Label"
            assert item.target == "test_target"
            assert isinstance(item.progress_string, str)

            # Test Menu properties
            menu = Menu(label="Test Menu", children=[item])
            assert menu.label == "Test Menu"
            assert len(menu.children) == 1

            # Test Links properties
            links = Links(documentation="https://example.com")
            assert links.documentation == "https://example.com"

            self.results["property"] = {"status": "PASSED", "tests": 3}
            print("SUCCESS: Property-based tests passed")

        except Exception as e:
            self.results["property"] = {"status": "FAILED", "error": str(e)}
            print(f"ERROR: Property-based tests failed: {e}")

        return self.results["property"]

    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests."""
        print("Running performance tests...")

        try:
            monitor = PerformanceMonitor()

            # Test critical operations
            monitor.assert_performance(Sidebar.from_yaml, TestConfig.MAX_EXECUTION_TIME)
            monitor.assert_performance(load_state, TestConfig.MAX_EXECUTION_TIME)
            monitor.assert_performance(save_state, TestConfig.MAX_EXECUTION_TIME)

            self.results["performance"] = {"status": "PASSED", "tests": 3}
            print("SUCCESS: Performance tests passed")

        except Exception as e:
            self.results["performance"] = {"status": "FAILED", "error": str(e)}
            print(f"ERROR: Performance tests failed: {e}")

        return self.results["performance"]

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites."""
        print("RUNNING: Running comprehensive test suite...")

        self.run_integration_tests()
        self.run_property_tests()
        self.run_performance_tests()

        # Summary
        total_tests = sum(suite.get("tests", 0) for suite in self.results.values() if suite.get("status") == "PASSED")

        failed_suites = [name for name, result in self.results.items() if result.get("status") == "FAILED"]

        print("\n📊 Test Summary:")
        print(f"   Total test suites: {len(self.results)}")
        print(f"   Passed: {len(self.results) - len(failed_suites)}")
        print(f"   Failed: {len(failed_suites)}")
        print(f"   Total tests: {total_tests}")

        if failed_suites:
            print(f"   Failed suites: {', '.join(failed_suites)}")
            return {"status": "FAILED", "failed_suites": failed_suites}

        return {"status": "PASSED", "total_tests": total_tests}


# Convenience functions for common testing patterns
def assert_valid_sidebar(sidebar: Sidebar) -> None:
    """Assert that a sidebar has valid structure."""
    issues = TestValidator.validate_sidebar_structure(sidebar)
    assert len(issues) == 0, f"Sidebar validation failed: {issues}"


def assert_valid_menu_item(item: MenuItem) -> None:
    """Assert that a menu item is valid."""
    issues = TestValidator.validate_menu_item(item)
    assert len(issues) == 0, f"MenuItem validation failed: {issues}"


def assert_performance_threshold(func: Callable, max_time: float, *args, **kwargs) -> None:
    """Assert that a function executes within performance threshold."""
    monitor = PerformanceMonitor()
    monitor.assert_performance(func, max_time, *args, **kwargs)
