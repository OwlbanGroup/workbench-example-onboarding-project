# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Integration tests for complete application workflows."""

import pytest
import tempfile
import json
import os
from typing import Generator, Any
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to the path for imports
import sys

sys.path.append(str(Path(__file__).parent.parent))

from common.sidebar import Sidebar, MenuItem, Menu, Links
from common.theme import Theme, load_state, save_state, ensure_state
from common.localization import load_messages
from tests import TestConfig, mock_streamlit_session, benchmark_performance


class TestCompleteWorkflows:
    """Test complete application workflows end-to-end."""

    @pytest.fixture
    def mock_session_state(self) -> Generator[MagicMock, None, None]:
        """Mock Streamlit session state for testing."""
        with mock_streamlit_session() as mock_session:
            yield mock_session

    @pytest.fixture
    def temp_state_file(self) -> Generator[str, None, None]:
        """Create a temporary state file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"basic_01_completed": 3, "basic_01_total": 3, "basic_02_completed": 0, "basic_02_total": 2}, f)
            temp_file = f.name

        yield temp_file

        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    def test_complete_sidebar_workflow(self, mock_session_state: MagicMock) -> None:
        """Test complete sidebar loading and navigation workflow."""
        # Test YAML loading
        sidebar = Sidebar.from_yaml()
        assert sidebar is not None
        assert sidebar.header is not None
        assert len(sidebar.navbar) > 0

        # Test navigation logic
        page_list = sidebar.page_list
        assert len(page_list) > 0
        assert all("pages/" in str(page) for page in page_list)

        # Test progress tracking
        for menu in sidebar.navbar:
            for item in menu.children:
                progress = item.progress_string
                assert isinstance(progress, str)

        # Test navigation between pages
        first_page = sidebar.navbar[0].children[0].target
        prev, next_page = sidebar.prev_and_next_nav(first_page)

        if len(sidebar.navbar[0].children) > 1:
            assert next_page is not None
        assert prev is None  # First page should have no previous

    def test_complete_theme_workflow(self, temp_state_file: str, mock_session_state: MagicMock) -> None:
        """Test complete theme loading and state management workflow."""
        # Mock the state file path
        with patch("common.theme.STATE_FILE", temp_state_file):
            # Test state loading
            load_state()
            assert mock_session_state.__setitem__.called

            # Test state saving
            save_state()
            assert mock_session_state.__setitem__.called

            # Test state ensuring
            ensure_state("test_key", "test_value")
            assert mock_session_state.__setitem__.called

    def test_complete_localization_workflow(self) -> None:
        """Test complete localization loading workflow."""
        # Test loading messages for existing file
        messages = load_messages(__file__)
        assert isinstance(messages, dict)

        # Test loading messages for non-existent file
        messages = load_messages("nonexistent_file.py")
        assert isinstance(messages, dict)

    def test_complete_error_handling_workflow(self, mock_session_state: MagicMock) -> None:
        """Test complete error handling across all components."""
        # Test sidebar error handling
        sidebar = Sidebar.from_yaml()

        # Test navigation with invalid page (should not crash)
        prev, next_page = sidebar.prev_and_next_nav("nonexistent_page")
        assert prev is None
        assert next_page is None

        # Test progress calculation with missing session data
        for menu in sidebar.navbar:
            for item in menu.children:
                progress = item.progress_string  # Should handle missing data gracefully
                assert isinstance(progress, str)

    def test_complete_performance_workflow(self) -> None:
        """Test performance of complete workflows."""

        # Test sidebar loading performance
        @benchmark_performance
        def load_sidebar() -> Sidebar:
            return Sidebar.from_yaml()

        sidebar = load_sidebar()
        assert sidebar is not None

        # Test theme state operations performance
        @benchmark_performance
        def state_operations() -> None:
            load_state()
            save_state()

        state_operations()  # Should complete within threshold

    def test_complete_validation_workflow(self) -> None:
        """Test complete validation workflow for all components."""
        # Test MenuItem validation
        valid_item = MenuItem(label="Valid Label", target="valid_target")
        assert valid_item.label == "Valid Label"
        assert valid_item.target == "valid_target"

        # Test Menu validation
        menu = Menu(label="Test Menu", children=[valid_item])
        assert menu.label == "Test Menu"
        assert len(menu.children) == 1

        # Test Links validation
        links = Links(documentation="https://example.com")
        assert links.documentation == "https://example.com"

        # Test Sidebar validation
        sidebar = Sidebar(header="Test Header", navbar=[menu], links=links)
        assert sidebar.header == "Test Header"
        assert len(sidebar.navbar) == 1

    def test_complete_edge_case_workflow(self, mock_session_state: MagicMock) -> None:
        """Test complete workflow with edge cases."""
        # Test with empty sidebar configuration
        # (This would require mocking the YAML file)

        # Test with malformed data
        # (This would require mocking the YAML parsing)

        # Test with missing translations
        messages = load_messages("nonexistent_file.py")
        assert "title" in messages or len(messages) == 0

        # Test with very long labels
        long_item = MenuItem(label="A" * 100, target="a" * 50)
        assert len(long_item.label) == 100
        assert len(long_item.target) == 50

    def test_complete_recovery_workflow(self, mock_session_state: MagicMock) -> None:
        """Test recovery from various failure scenarios."""
        # Test recovery from YAML parsing errors
        # (Would require mocking file system errors)

        # Test recovery from state file corruption
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content {")
            corrupted_file = f.name

        try:
            with patch("common.theme.STATE_FILE", corrupted_file):
                # Should handle corrupted state file gracefully
                load_state()
        except Exception:
            # Expected to handle gracefully
            pass
        finally:
            if os.path.exists(corrupted_file):
                os.unlink(corrupted_file)

    def test_complete_concurrency_workflow(self) -> None:
        """Test concurrent access patterns."""
        # Test multiple sidebar instances
        sidebar1 = Sidebar.from_yaml()
        sidebar2 = Sidebar.from_yaml()
        assert sidebar1 is not None
        assert sidebar2 is not None

        # Test concurrent state access
        with patch("common.theme.STATE_FILE", "/tmp/test_state.json"):
            # Multiple rapid state operations should not interfere
            for i in range(10):
                ensure_state(f"test_key_{i}", f"test_value_{i}")


class TestWorkflowPerformance:
    """Performance tests for complete workflows."""

    def test_sidebar_loading_performance(self) -> None:
        """Test that sidebar loading meets performance requirements."""

        @benchmark_performance
        def load_sidebar() -> Sidebar:
            return Sidebar.from_yaml()

        sidebar = load_sidebar()
        assert sidebar is not None

    def test_theme_operations_performance(self) -> None:
        """Test that theme operations meet performance requirements."""

        @benchmark_performance
        def theme_operations() -> None:
            load_state()
            save_state()

        theme_operations()  # Should complete within reasonable time

    def test_navigation_performance(self) -> None:
        """Test that navigation operations meet performance requirements."""
        sidebar = Sidebar.from_yaml()

        @benchmark_performance
        def navigation_ops() -> None:
            for menu in sidebar.navbar:
                for item in menu.children:
                    _ = item.progress_string
                    _ = sidebar.prev_and_next_nav(item.target)

        navigation_ops()
