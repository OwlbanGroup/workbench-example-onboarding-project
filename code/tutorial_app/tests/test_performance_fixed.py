# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Performance benchmarks for critical functions."""

import pytest
import time
import psutil
import os
from typing import Dict, Any, Callable
from unittest.mock import patch
from pathlib import Path

# Add the parent directory to the path for imports
import sys

sys.path.append(str(Path(__file__).parent.parent))

from common.sidebar import Sidebar, MenuItem, Menu, Links
from common.theme import load_state, save_state, ensure_state, slugify
from common.localization import load_messages
from tests import TestConfig, benchmark_performance, PerformanceMetrics


class TestPerformanceBenchmarks:
    """Performance benchmarks for critical functions."""

    def get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss

    def benchmark_function(self, func: Callable, *args, **kwargs) -> PerformanceMetrics:
        """Benchmark a function and return performance metrics."""
        start_time = time.perf_counter()
        start_memory = self.get_memory_usage()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        end_memory = self.get_memory_usage()

        return PerformanceMetrics(
            execution_time=end_time - start_time, memory_usage=end_memory - start_memory, function_name=func.__name__
        )

    def test_sidebar_loading_performance(self) -> None:
        """Benchmark sidebar loading performance."""
        metrics = self.benchmark_function(Sidebar.from_yaml)

        # Assert performance requirements
        assert metrics.execution_time < TestConfig.MAX_EXECUTION_TIME, (
            f"Sidebar loading took {metrics.execution_time:.4f}s, "
            f"exceeding threshold of {TestConfig.MAX_EXECUTION_TIME}s"
        )

        # Memory usage should be reasonable
        assert metrics.memory_usage < 50 * 1024 * 1024, (  # 50MB
            f"Sidebar loading used {metrics.memory_usage} bytes, " "exceeding reasonable memory limit"
        )

        print(f"Sidebar loading: {metrics.execution_time:.4f}s, " f"{metrics.memory_usage} bytes")

    def test_theme_state_operations_performance(self) -> None:
        """Benchmark theme state operations performance."""
        # Test load_state performance
        load_metrics = self.benchmark_function(load_state)

        # Test save_state performance
        save_metrics = self.benchmark_function(save_state)

        # Test ensure_state performance
        ensure_metrics = self.benchmark_function(ensure_state, "test_key", "test_value")

        # Assert performance requirements
        for metrics in [load_metrics, save_metrics, ensure_metrics]:
            assert metrics.execution_time < TestConfig.MAX_EXECUTION_TIME, (
                f"State operation {metrics.function_name} took {metrics.execution_time:.4f}s, "
                f"exceeding threshold of {TestConfig.MAX_EXECUTION_TIME}s"
            )

        print(
            f"State operations - Load: {load_metrics.execution_time:.4f}s, "
            f"Save: {save_metrics.execution_time:.4f}s, "
            f"Ensure: {ensure_metrics.execution_time:.4f}s"
        )

    def test_slugify_performance(self) -> None:
        """Benchmark slugify function performance."""
        test_strings = [
            "Simple String",
            "Complex String With Special Characters!@#$%^&*()",
            "Very Long String " * 100,
            "String\nWith\nNewlines",
            "String\tWith\tTabs",
        ]

        total_time = 0
        for test_string in test_strings:
            metrics = self.benchmark_function(slugify, test_string)
            total_time += metrics.execution_time

            assert metrics.execution_time < 0.1, (  # 100ms should be plenty
                f"Slugify took {metrics.execution_time:.4f}s for string of length {len(test_string)}, "
                "exceeding reasonable time"
            )

        avg_time = total_time / len(test_strings)
        print(f"Slugify average: {avg_time:.4f}s per operation")

    def test_menuitem_creation_performance(self) -> None:
        """Benchmark MenuItem creation performance."""
        test_cases = [
            ("Simple Label", "simple_target"),
            ("Very Long Label " * 50, "very_long_target_" * 20),
            ("Label With Special Chars !@#$%", "target_with_special_chars"),
        ]

        for label, target in test_cases:
            metrics = self.benchmark_function(MenuItem, label=label, target=target)

            assert metrics.execution_time < 0.1, (
                f"MenuItem creation took {metrics.execution_time:.4f}s, " "exceeding reasonable time"
            )

        print(f"MenuItem creation: ~{metrics.execution_time:.4f}s per item")

    def test_navigation_performance(self) -> None:
        """Benchmark navigation operations performance."""
        sidebar = Sidebar.from_yaml()

        # Test navigation for all pages
        navigation_times = []
        for menu in sidebar.navbar:
            for item in menu.children:
                metrics = self.benchmark_function(sidebar.prev_and_next_nav, item.target)
                navigation_times.append(metrics.execution_time)

                assert metrics.execution_time < 0.01, (  # 10ms should be plenty
                    f"Navigation took {metrics.execution_time:.4f}s, " "exceeding reasonable time"
                )

        avg_navigation_time = sum(navigation_times) / len(navigation_times)
        print(f"Navigation average: {avg_navigation_time:.4f}s per operation")

    def test_progress_calculation_performance(self) -> None:
        """Benchmark progress calculation performance."""
        sidebar = Sidebar.from_yaml()

        # Test progress calculation for all items
        progress_times = []
        for menu in sidebar.navbar:
            for item in menu.children:
                metrics = self.benchmark_function(lambda: item.progress_string)
                progress_times.append(metrics.execution_time)

                assert metrics.execution_time < 0.01, (
                    f"Progress calculation took {metrics.execution_time:.4f}s, " "exceeding reasonable time"
                )

        avg_progress_time = sum(progress_times) / len(progress_times)
        print(f"Progress calculation average: {avg_progress_time:.4f}s per operation")

    def test_localization_loading_performance(self) -> None:
        """Benchmark localization loading performance."""
        test_files = [
            "code/tutorial_app/pages/basic_01.py",
            "code/tutorial_app/pages/basic_02.py",
            "code/tutorial_app/pages/overview.py",
        ]

        for file_path in test_files:
            if os.path.exists(file_path):
                metrics = self.benchmark_function(load_messages, file_path)

                assert metrics.execution_time < 0.5, (  # 500ms should be plenty
                    f"Localization loading took {metrics.execution_time:.4f}s, " "exceeding reasonable time"
                )

        print(f"Localization loading: ~{metrics.execution_time:.4f}s per file")

    def test_complete_workflow_performance(self) -> None:
        """Benchmark complete application workflow performance."""

        @benchmark_performance
        def complete_workflow():
            # Simulate complete workflow
            sidebar = Sidebar.from_yaml()
            load_state()
            save_state()

            # Navigate through all pages
            for menu in sidebar.navbar:
                for item in menu.children:
                    _ = item.progress_string
                    _ = sidebar.prev_and_next_nav(item.target)

            # Test slugify operations
            for i in range(100):
                slugify(f"test_string_{i}")

        metrics = self.benchmark_function(complete_workflow)

        # Complete workflow should still be fast
        assert metrics.execution_time < 5.0, (
            f"Complete workflow took {metrics.execution_time:.4f}s, "
            "exceeding reasonable time for full application workflow"
        )

        print(f"Complete workflow: {metrics.execution_time:.4f}s, " f"{metrics.memory_usage} bytes")

    def test_memory_efficiency(self) -> None:
        """Test memory efficiency of operations."""
        initial_memory = self.get_memory_usage()

        # Create multiple sidebar instances
        sidebars = []
        for i in range(10):
            sidebar = Sidebar.from_yaml()
            sidebars.append(sidebar)

        peak_memory = self.get_memory_usage()
        memory_increase = peak_memory - initial_memory

        # Memory increase should be reasonable
        assert memory_increase < 100 * 1024 * 1024, f"Memory increase of {memory_increase} bytes is too high"  # 100MB

        print(f"Memory efficiency: {memory_increase} bytes for 10 sidebar instances")

        # Clean up
        del sidebars

    def test_concurrent_operations_performance(self) -> None:
        """Test performance under concurrent operations."""
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def create_sidebar():
            return Sidebar.from_yaml()

        def calculate_progress(sidebar):
            for menu in sidebar.navbar:
                for item in menu.children:
                    _ = item.progress_string

        # Test concurrent sidebar creation
        start_time = time.perf_counter()

        with ThreadPoolExecutor(max_workers=5) as executor:
            sidebar_futures = [executor.submit(create_sidebar) for _ in range(5)]
            progress_futures = []

            for future in as_completed(sidebar_futures):
                sidebar = future.result()
                progress_futures.append(executor.submit(calculate_progress, sidebar))

            # Wait for all progress calculations to complete
            for future in as_completed(progress_futures):
                future.result()

        end_time = time.perf_counter()
        concurrent_time = end_time - start_time

        # Concurrent operations should still be reasonably fast
        assert concurrent_time < 10.0, (
            f"Concurrent operations took {concurrent_time:.4f}s, " "exceeding reasonable time"
        )

        print(f"Concurrent operations: {concurrent_time:.4f}s for 5 parallel workflows")

    def test_scalability_performance(self) -> None:
        """Test performance scalability with larger datasets."""
        # Test with larger menu structures
        items = []
        for i in range(100):
            item = MenuItem(label=f"Item {i}", target=f"item_{i}")
            items.append(item)

        menu = Menu(label="Large Menu", children=items)
        sidebar = Sidebar(header="Large Sidebar", navbar=[menu], links=Links())

        # Test navigation performance with large menu
        start_time = time.perf_counter()

        for item in items:
            _ = sidebar.prev_and_next_nav(item.target)
            _ = item.progress_string

        end_time = time.perf_counter()
        scalability_time = end_time - start_time

        # Should scale reasonably well
        assert scalability_time < 5.0, (
            f"Large menu operations took {scalability_time:.4f}s, " "performance does not scale well"
        )

        print(f"Scalability test: {scalability_time:.4f}s for 100 menu items")

    def test_cold_start_performance(self) -> None:
        """Test cold start performance (first-time operations)."""
        # Clear any caches
        import sys

        modules_to_clear = [k for k in sys.modules.keys() if k.startswith("common")]
        for module in modules_to_clear:
            del sys.modules[module]

        # Re-import and test
        from common.sidebar import Sidebar
        from common.theme import load_state, save_state

        # Cold start should still be fast
        cold_start_metrics = self.benchmark_function(Sidebar.from_yaml)
        assert cold_start_metrics.execution_time < TestConfig.MAX_EXECUTION_TIME * 2, (
            f"Cold start took {cold_start_metrics.execution_time:.4f}s, " "too slow for initial load"
        )

        print(f"Cold start: {cold_start_metrics.execution_time:.4f}s")
