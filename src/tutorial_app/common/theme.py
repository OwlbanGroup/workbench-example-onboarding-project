# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common code that is used to render and style boilerplate streamlit objects.

This module provides the core theming and state management functionality for the
NVIDIA AI Workbench tutorial application. It handles session state persistence,
stylesheet loading, and common UI components.

Key Features:
- Session state management with JSON persistence
- Automatic UI refresh functionality
- Common task rendering and navigation
- Stylesheet loading and application
- Sidebar integration

Example:
    >>> with Theme():
    ...     st.title("My Tutorial Page")
    ...     # Your tutorial content here
"""

from dataclasses import dataclass
import json
import logging
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Union, Tuple
from functools import lru_cache
import time

from jinja2 import Environment, BaseLoader, Template
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_extras.stateful_button import button

from . import sidebar, testing

# Constants
STATE_FILE: str = "/project/data/scratch/tutorial_state.json"
STYLESHEETS: List[Path] = [Path(__file__).parent.joinpath("style.css")]
PREVIOUS: str = "Previous"
NEXT: str = "Next"
AUTOREFRESH_DELAY: int = 2500
MAX_RETRY_ATTEMPTS: int = 3
RETRY_DELAY: float = 1.0

# Configure logging
logger = logging.getLogger(__name__)


def ensure_state(key: str, value: Any) -> None:
    """Ensure a state variable is set to the specified value.

    Prevents unnecessary variable updates by only setting the value if it differs
    from the current value.

    Args:
        key: The session state key to set
        value: The value to assign to the key

    Example:
        >>> ensure_state("user_name", "John")
        >>> ensure_state("user_name", "Jane")  # Only updates if different
    """
    if not isinstance(key, str):
        raise ValueError("State key must be a string")

    cur_value = st.session_state.get(key, None)
    if cur_value != value:
        st.session_state[key] = value
        logger.debug(f"Updated session state: {key} = {value}")


def slugify(name: str) -> str:
    """Convert a name into a slugged string.

    Converts a human-readable name into a URL-safe slug by:
    1. Converting to lowercase
    2. Replacing spaces with underscores
    3. Keeping only lowercase letters and underscores

    Args:
        name: The name to convert to a slug

    Returns:
        A slugified string safe for use in URLs and identifiers

    Raises:
        ValueError: If name is not a string

    Example:
        >>> slugify("My Task Name")
        'my_task_name'
        >>> slugify("Test 123!")
        'test_'
    """
    if not isinstance(name, str):
        raise ValueError("Name must be a string")

    def _is_valid(char: str) -> bool:
        """Check if character is valid for slug (lowercase letters or underscore)."""
        return (ord(char) > 96 and ord(char) < 123) or ord(char) == 95

    filtered_name = [x for x in name.lower().replace(" ", "_") if _is_valid(x)]
    return "".join(filtered_name)


@lru_cache(maxsize=1)
def _get_cached_state_file() -> Path:
    """Get the cached state file path.

    Returns:
        Path object for the state file
    """
    return Path(STATE_FILE)


def load_state() -> None:
    """Load the state from JSON file with retry logic.

    Loads the tutorial state from the JSON file and updates the session state.
    Uses caching to avoid repeated file system checks.

    Raises:
        RuntimeError: If state file cannot be loaded after retries
    """
    if "_loaded" in st.session_state:
        return

    state_file = _get_cached_state_file()

    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            if state_file.exists():
                with open(state_file, "r", encoding="UTF-8") as ptr:
                    loaded_state = json.load(ptr)
                    st.session_state.update(loaded_state)
                    logger.info(f"Successfully loaded state from {state_file}")
            else:
                logger.info(f"State file {state_file} does not exist, starting with empty state")
                loaded_state = {}

            st.session_state["_loaded"] = True
            return

        except (IOError, OSError, json.JSONDecodeError) as e:
            if attempt < MAX_RETRY_ATTEMPTS - 1:
                logger.warning(f"Failed to load state (attempt {attempt + 1}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to load state after {MAX_RETRY_ATTEMPTS} attempts: {e}")
                raise RuntimeError(f"Could not load state file: {e}")


def save_state() -> None:
    """Save the session state for all sessions with error handling.

    Compares current state with previous state and only saves if changed.
    Excludes certain keys from persistence for performance and security.

    Raises:
        RuntimeError: If state cannot be saved after retries
    """
    try:
        # Get current state and prepare for saving
        state_dict = st.session_state.to_dict()
        last_state_json = state_dict.pop("last_state", "{}")

        # Remove keys that shouldn't be persisted
        excluded_keys = ["autorefresh"] + [key for key in state_dict.keys() if key.endswith("_derived")]
        for key in excluded_keys:
            state_dict.pop(key, None)

        state_json = json.dumps(state_dict, indent=2, ensure_ascii=False)

        # Only save if state has changed
        if state_json != last_state_json:
            state_file = _get_cached_state_file()

            for attempt in range(MAX_RETRY_ATTEMPTS):
                try:
                    # Ensure directory exists
                    state_file.parent.mkdir(parents=True, exist_ok=True)

                    with open(state_file, "w", encoding="UTF-8") as ptr:
                        ptr.write(state_json)

                    st.session_state["last_state"] = state_json
                    logger.info(f"Successfully saved state to {state_file}")
                    return

                except (IOError, OSError) as e:
                    if attempt < MAX_RETRY_ATTEMPTS - 1:
                        logger.warning(f"Failed to save state (attempt {attempt + 1}): {e}")
                        time.sleep(RETRY_DELAY)
                    else:
                        logger.error(f"Failed to save state after {MAX_RETRY_ATTEMPTS} attempts: {e}")
                        raise RuntimeError(f"Could not save state file: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in save_state: {e}")
        raise


def print_task(parent: str, task: Dict[str, str], test_suite: Optional[ModuleType], messages: Dict[str, str]) -> bool:
    """Write tasks out to screen with enhanced error handling.

    Renders a tutorial task with either automated testing or manual user input.
    Handles both test-based progression and user interaction-based progression.

    Args:
        parent: The parent module name for key generation
        task: Dictionary containing task information (name, msg, test, response)
        test_suite: Optional test module containing validation functions
        messages: Dictionary of localized messages

    Returns:
        True if task should continue, False if task is incomplete

    Raises:
        ValueError: If required task parameters are missing

    Example:
        >>> task = {"name": "Create Project", "msg": "Create a new project", "test": "check_project"}
        >>> print_task("basic_01", task, test_module, messages)
    """
    if not isinstance(task, dict):
        raise ValueError("Task must be a dictionary")

    task_name = task.get("name", "Unnamed Task")
    task_msg = task.get("msg", "No description available")

    if not task_name or not task_msg:
        logger.warning(f"Task missing required fields: {task}")
        return False

    st.write(f"### {task_name}")
    st.write(task_msg)

    # Lookup a test from the test module
    test = None
    test_name = task.get("test")
    if test_name and test_suite is not None:
        test = getattr(test_suite, test_name, None)

    result: Any = None

    if test:
        # Continue task based on test function
        st.write("***")
        st.write(f"**{messages.get('testing_msg', 'Running validation...')}**")

        try:
            success, msg, result = testing.run_test(test)
            if msg is not None:
                display_msg = messages.get(msg, msg) or msg
                st.info(display_msg)

            if not success:
                logger.debug(f"Test failed for task '{task_name}': {msg}")
                return False

        except Exception as e:
            logger.error(f"Error running test '{test_name}' for task '{task_name}': {e}")
            st.error(f"Test error: {e}")
            return False

    else:
        # Continue task based on user input
        try:
            slug = slugify(task_name)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{messages.get('waiting_msg', 'Click Next when ready')}**")
            with col2:
                done = button(messages.get("next", "Next"), key=f"{parent}_task_{slug}")
            if not done:
                return False

        except Exception as e:
            logger.error(f"Error in user input handling for task '{task_name}': {e}")
            st.error(f"Input error: {e}")
            return False

    # Show success message after completion
    response_template = task.get("response")
    if response_template:
        try:
            template = Environment(loader=BaseLoader).from_string(response_template)
            rendered_message = template.render(result=result)
            st.success(rendered_message)
        except Exception as e:
            logger.error(f"Error rendering response template for task '{task_name}': {e}")
            st.success("Task completed successfully!")

    return True


def print_footer_nav(current: str) -> None:
    """Print the footer navigation buttons for next and previous exercises.

    Renders navigation buttons to move between tutorial pages with proper
    error handling and user feedback.

    Args:
        current: The current page identifier

    Raises:
        RuntimeError: If navigation fails
    """
    if not isinstance(current, str):
        raise ValueError("Current page must be a string")

    try:
        # Find the next and previous pages
        prev_page, next_page = sidebar.APP_SIDEBAR.prev_and_next_nav(current)

        # Determine which buttons should be shown
        pills: List[str] = []
        if prev_page is not None:
            pills.append(PREVIOUS)
        if next_page is not None:
            pills.append(NEXT)

        if not pills:
            logger.debug(f"No navigation available from page '{current}'")
            return

        # Render the buttons
        _, center, _ = st.columns([1, 1, 1])
        with center:
            next_steps = st.pills("Navigate", pills, selection_mode="single")

        # Handle button presses
        if next_steps == PREVIOUS and prev_page:
            logger.info(f"Navigating from '{current}' to '{prev_page}'")
            st.switch_page(prev_page)
        elif next_steps == NEXT and next_page:
            logger.info(f"Navigating from '{current}' to '{next_page}'")
            st.switch_page(next_page)

    except Exception as e:
        logger.error(f"Error in footer navigation for page '{current}': {e}")
        st.error(f"Navigation error: {e}")


@lru_cache(maxsize=len(STYLESHEETS))
def _load_stylesheet_cached(stylesheet_path: str) -> str:
    """Load a stylesheet with caching.

    Args:
        stylesheet_path: Path to the stylesheet file

    Returns:
        The stylesheet content as a string

    Raises:
        FileNotFoundError: If stylesheet file doesn't exist
        IOError: If stylesheet cannot be read
    """
    path = Path(stylesheet_path)
    if not path.exists():
        raise FileNotFoundError(f"Stylesheet not found: {stylesheet_path}")

    with open(path, "r", encoding="UTF-8") as ptr:
        return ptr.read()


def load_stylesheet() -> None:
    """Load and apply stylesheets with error handling and caching.

    Loads all configured stylesheets and applies them to the Streamlit app.
    Uses caching to avoid repeated file I/O operations.

    Raises:
        RuntimeError: If stylesheets cannot be loaded
    """
    for stylesheet in STYLESHEETS:
        try:
            style = _load_stylesheet_cached(str(stylesheet))
            st.html(f"<style>{style}</style>")
            logger.debug(f"Successfully loaded stylesheet: {stylesheet}")

        except Exception as e:
            logger.error(f"Failed to load stylesheet {stylesheet}: {e}")
            st.error(f"Failed to load stylesheet: {e}")
            # Continue with other stylesheets even if one fails


@dataclass
class Theme:
    """Context manager for applying the tutorial application theme.

    Provides a clean interface for setting up the tutorial environment with
    proper state management, auto-refresh, and styling.

    Attributes:
        autorefresh: Whether to enable automatic UI refresh
        ephemeral: Whether to skip state persistence (for testing)

    Example:
        >>> with Theme():
        ...     st.title("Tutorial Page")
        ...     # Tutorial content here
    """

    autorefresh: bool = True
    ephemeral: bool = False

    def __enter__(self) -> "Theme":
        """Initialize the theme context.

        Sets up state management, auto-refresh, stylesheets, and sidebar.

        Returns:
            Self for context manager compatibility

        Raises:
            RuntimeError: If theme initialization fails
        """
        try:
            logger.info("Initializing theme context")
            load_state()

            if self.autorefresh:
                st_autorefresh(interval=AUTOREFRESH_DELAY, key="autorefresh")
                logger.debug("Auto-refresh enabled")

            load_stylesheet()
            logger.debug("Stylesheets loaded")

            with st.sidebar:
                sidebar.APP_SIDEBAR.render()
                logger.debug("Sidebar rendered")

            return self

        except Exception as e:
            logger.error(f"Failed to initialize theme: {e}")
            raise RuntimeError(f"Theme initialization failed: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Clean up the theme context.

        Saves the session state if not in ephemeral mode.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if exc_type is not None:
            logger.warning(f"Theme context exited with exception: {exc_type.__name__}: {exc_val}")

        if not self.ephemeral:
            try:
                save_state()
                logger.debug("Session state saved")
            except Exception as e:
                logger.error(f"Failed to save state on theme exit: {e}")
                # Don't raise here to avoid masking the original exception
