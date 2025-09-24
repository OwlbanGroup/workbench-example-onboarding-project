# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Property-based tests for critical functions."""

import pytest
from hypothesis import given, strategies as st, settings
from typing import Any, Dict, List
import string
import re

# Add the parent directory to the path for imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from common.sidebar import MenuItem, Menu, Links, Sidebar
from common.theme import slugify, ensure_state
from tests import generate_test_data


class TestPropertyBased:
    """Property-based tests using Hypothesis."""

    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_menuitem_label_properties(self, label: str) -> None:
        """Test properties of MenuItem labels."""
        # Property: Label should be preserved exactly
        item = MenuItem(label=label, target="test_target")
        assert item.label == label

        # Property: Progress string should always be a string
        progress = item.progress_string
        assert isinstance(progress, str)

        # Property: Full label should contain original label
        full_label = item.full_label
        assert label in full_label

    @given(st.text(min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_menuitem_target_properties(self, target: str) -> None:
        """Test properties of MenuItem targets."""
        # Property: Target should be preserved exactly
        item = MenuItem(label="test_label", target=target)
        assert item.target == target

        # Property: Filepath should contain target
        filepath = item.filepath
        assert target in filepath
        assert filepath.endswith(".py")

        # Property: Markdown should contain label
        markdown = item.markdown
        assert "test_label" in markdown

    @given(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=10))
    @settings(max_examples=50)
    def test_menu_children_properties(self, labels: List[str]) -> None:
        """Test properties of Menu with children."""
        # Create menu items from labels
        children = [MenuItem(label=label, target=f"target_{i}") for i, label in enumerate(labels)]

        # Property: Menu should preserve all children
        menu = Menu(label="test_menu", children=children)
        assert len(menu.children) == len(children)
        assert all(child in menu.children for child in children)

        # Property: Menu label should be preserved
        assert menu.label == "test_menu"

    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_slugify_properties(self, text: str) -> None:
        """Test properties of slugify function."""
        result = slugify(text)

        # Property: Result should only contain lowercase letters and underscores
        assert all(c.islower() or c == "_" for c in result)

        # Property: Result should not contain original spaces
        assert " " not in result

        # Property: Result should be shorter than or equal to original
        assert len(result) <= len(text)

        # Property: Empty string should produce empty result
        if text.strip() == "":
            assert result == ""

        # Property: Result should be stable (same input produces same output)
        result2 = slugify(text)
        assert result == result2

    @given(
        st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.integers(min_value=0, max_value=100),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    def test_progress_calculation_properties(self, progress_data: Dict[str, int]) -> None:
        """Test properties of progress calculations."""
        # Create a mock MenuItem with progress data
        item = MenuItem(label="test", target="test")

        # Mock session state with progress data
        import streamlit as st

        for key, value in progress_data.items():
            st.session_state[key] = value

        # Property: Progress string should always be a string
        progress = item.progress_string
        assert isinstance(progress, str)

        # Property: Progress string should not be None
        assert progress is not None

        # Property: Progress string should be non-empty
        assert len(progress.strip()) > 0

    @given(st.text(min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_filepath_generation_properties(self, target: str) -> None:
        """Test properties of filepath generation."""
        item = MenuItem(label="test", target=target)

        # Property: Filepath should always end with .py
        filepath = item.filepath
        assert filepath.endswith(".py")

        # Property: Filepath should contain target
        assert target in filepath

        # Property: Filepath should start with pages/
        assert filepath.startswith("pages/")

        # Property: Filepath should not contain invalid characters
        assert all(c not in filepath for c in ["<", ">", ":", '"', "|", "?", "*"])

    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_markdown_generation_properties(self, label: str) -> None:
        """Test properties of markdown generation."""
        item = MenuItem(label=label, target="test_target")

        # Property: Markdown should contain label
        markdown = item.markdown
        assert label in markdown

        # Property: Markdown should be valid markdown format
        assert markdown.startswith("[")
        assert markdown.endswith(")")

        # Property: Markdown should contain target
        assert "test_target" in markdown

    @given(st.lists(st.text(min_size=1, max_size=20), min_size=2, max_size=5))
    @settings(max_examples=50)
    def test_navigation_properties(self, targets: List[str]) -> None:
        """Test properties of navigation between pages."""
        # Create menu items
        children = [MenuItem(label=f"label_{i}", target=target) for i, target in enumerate(targets)]
        menu = Menu(label="test_menu", children=children)
        sidebar = Sidebar(header="test", navbar=[menu], links=Links())

        # Property: Navigation should work for all valid targets
        for target in targets:
            prev, next_page = sidebar.prev_and_next_nav(target)
            assert isinstance(prev, (str, type(None)))
            assert isinstance(next_page, (str, type(None)))

        # Property: First target should have no previous
        first_target = targets[0]
        prev, next_page = sidebar.prev_and_next_nav(first_target)
        assert prev is None

        # Property: Last target should have no next
        last_target = targets[-1]
        prev, next_page = sidebar.prev_and_next_nav(last_target)
        assert next_page is None

    @given(st.text(min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_sidebar_validation_properties(self, header: str) -> None:
        """Test properties of sidebar validation."""
        # Create valid sidebar components
        item = MenuItem(label="test_label", target="test_target")
        menu = Menu(label="test_menu", children=[item])
        links = Links(documentation="https://example.com")

        # Property: Sidebar should accept valid components
        sidebar = Sidebar(header=header, navbar=[menu], links=links)
        assert sidebar.header == header
        assert len(sidebar.navbar) == 1
        assert sidebar.links.documentation == "https://example.com"

        # Property: Page list should be generated correctly
        page_list = sidebar.page_list
        assert len(page_list) > 0
        assert all("pages/" in str(page) for page in page_list)

    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_error_handling_properties(self, invalid_input: str) -> None:
        """Test properties of error handling with invalid inputs."""
        # Property: Invalid navigation should not crash
        sidebar = Sidebar.from_yaml()
        prev, next_page = sidebar.prev_and_next_nav(invalid_input)
        assert isinstance(prev, (str, type(None)))
        assert isinstance(next_page, (str, type(None)))

        # Property: Progress calculation should handle missing data gracefully
        item = MenuItem(label="test", target="test")
        progress = item.progress_string
        assert isinstance(progress, str)

    @given(st.text(min_size=1, max_size=50), st.text(min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_menu_hierarchy_properties(self, menu_label: str, item_label: str) -> None:
        """Test properties of menu hierarchy."""
        # Create nested menu structure
        child_item = MenuItem(label=item_label, target="child_target")
        child_menu = Menu(label="child_menu", children=[child_item])
        parent_item = MenuItem(label="parent_item", target="parent_target")
        parent_menu = Menu(label=menu_label, children=[parent_item, child_item])

        # Property: Menu should preserve hierarchy
        assert parent_menu.label == menu_label
        assert len(parent_menu.children) == 2

        # Property: Child menu should be independent
        assert child_menu.label == "child_menu"
        assert len(child_menu.children) == 1

    @given(st.booleans())
    @settings(max_examples=50)
    def test_progress_display_properties(self, show_progress: bool) -> None:
        """Test properties of progress display."""
        item = MenuItem(label="test", target="test", show_progress=show_progress)

        # Property: Progress string should reflect show_progress setting
        progress = item.progress_string

        if show_progress:
            # Should attempt to show progress (may be default if no data)
            assert isinstance(progress, str)
        else:
            # Should be empty if progress is disabled
            assert progress == ""

        # Property: Full label should always contain original label
        full_label = item.full_label
        assert "test" in full_label
