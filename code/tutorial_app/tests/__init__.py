# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Test utilities and shared testing infrastructure."""

import pytest
from typing import Any, Callable, Generator
from contextlib import contextmanager
import time
import functools
from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    """Performance metrics for benchmarking."""
    execution_time: float
    memory_usage: int  # in bytes
    function_name: str


class TestConfig:
    """Configuration for test execution."""

    # Performance thresholds
    MAX_EXECUTION_TIME = 1.0  # seconds
    MIN_TEST_COVERAGE = 85.0  # percentage

    # Test categories
    UNIT_TESTS = "unit"
    INTEGRATION_TESTS = "integration"
    PERFORMANCE_TESTS = "performance"
    PROPERTY_TESTS = "property"


def benchmark_performance(func: Callable) -> Callable:
    """Decorator to benchmark function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        start_memory = get_memory_usage()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        end_memory = get_memory_usage()

        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory

        metrics = PerformanceMetrics(
            execution_time=execution_time,
            memory_usage=memory_usage,
            function_name=func.__name__
        )

        # Log performance metrics
        print(f"Performance: {func.__name__} took {execution_time".4f"}s, "
              f"memory delta: {memory_usage} bytes")

        return result

    return wrapper


def get_memory_usage() -> int:
    """Get current memory usage (simplified for testing)."""
    import psutil
    process = psutil.Process()
    return process.memory_info().rss


@contextmanager
def mock_streamlit_session() -> Generator[None, None, None]:
    """Context manager to mock Streamlit session state."""
    import sys
    from unittest.mock import patch, MagicMock

    mock_session = MagicMock()
    mock_session.get.return_value = None
    mock_session.__setitem__ = MagicMock()

    with patch('streamlit.session_state', mock_session):
        yield


def assert_performance_threshold(func: Callable, max_time: float = 1.0) -> None:
    """Assert that a function executes within performance threshold."""
    execution_time = time.perf_counter()
    func()
    execution_time = time.perf_counter() - execution_time

    assert execution_time <= max_time, (
        f"Function {func.__name__} took {execution_time".4f"}s, "
        f"exceeding threshold of {max_time}s"
    )


def generate_test_data() -> dict[str, Any]:
    """Generate test data for property-based testing."""
    return {
        'valid_labels': ['Test', 'Tutorial', 'Exercise', 'Basic', 'Advanced'],
        'valid_targets': ['basic_01', 'basic_02', 'advanced_01', 'overview'],
        'invalid_labels': ['', '   ', None, 123],
        'invalid_targets': ['', '   ', None, 123],
        'edge_case_labels': ['A' * 100, 'Test\nWith\nNewlines', 'Test\tWith\tTabs'],
        'edge_case_targets': ['a' * 50, 'Test-With-Dashes', 'test_with_underscores']
    }
