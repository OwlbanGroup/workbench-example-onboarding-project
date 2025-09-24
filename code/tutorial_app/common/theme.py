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
"""Common code that is used to render and style boilerplate streamlit objects."""

from dataclasses import dataclass
import json
from pathlib import Path
from types import ModuleType
from typing import Any

from jinja2 import Environment, BaseLoader
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_extras.stateful_button import button

from . import sidebar, testing

STATE_FILE = "/project/data/scratch/tutorial_state.json"
STYLESHEETS = [Path(__file__).parent.joinpath("style.css")]
PREVIOUS = "Previous"
NEXT = "Next"
AUTOREFRESH_DELAY = 2500


def ensure_state(key: str, value: Any):
    """Ensure a state variable is set to the specified value.

    Prevents unnecessary variable updates."""
    cur_value = st.session_state.get(key, None)
    if cur_value != value:
        st.session_state[key] = value


def slugify(name: str) -> str:
    """Convert a name into a slugged string."""

    def _is_valid(char: str) -> bool:
        """Only pass lowercase and underscores."""
        return (ord(char) > 96 and ord(char) < 123) or ord(char) == 95

    filtered_name = [x for x in name.lower().replace(" ", "_") if _is_valid(x)]
    return "".join(filtered_name)


def load_state():
    """Load the state from json file."""
    if "_loaded" in st.session_state:
        return

    try:
        with open(STATE_FILE, "r", encoding="UTF-8") as ptr:
            loaded_state = json.load(ptr)
    except (IOError, OSError):
        loaded_state = {}

    st.session_state.update(loaded_state)
    st.session_state["_loaded"] = True


def save_state():
    """Save the session state for all sessions."""
    # compare states
    state_dict = st.session_state.to_dict()
    last_state_json = state_dict.pop("last_state", "{}")  # dont recurse and save last state
    # dont save autorefresh runtime var
    # dont save session scoped variables (*_derived)
    remove_keys = ["autorefresh"] + [key for key in state_dict.keys() if key.endswith("_derived")]
    _ = [state_dict.pop(key, None) for key in remove_keys]
    state_json = json.dumps(state_dict)

    # save state when changed
    if state_json != last_state_json:
        with open(STATE_FILE, "w", encoding="UTF-8") as ptr:
            ptr.write(state_json)
        st.session_state["last_state"] = state_json


def print_task(parent: str, task: dict[str, str], test_suite: None | ModuleType, messages: dict[str, str]) -> bool:
    """Write tasks out to screen.

    Returns boolean to indicate if task printing should continue."""

    st.write("### " + task.get("name", "name"))
    st.write(task.get("msg", "msg"))

    # Lookup a test from the test module.
    test = None
    test_name = task.get("test", None)
    if test_name and test_suite is not None:
        test = getattr(test_suite, test_name, None)
    result: Any = None

    if test:
        # continue task based on test function
        st.write("***")
        st.write("**" + messages.get("testing_msg", "") + "**")
        success, msg, result = testing.run_test(test)
        if msg is not None:
            st.info(messages.get(msg, msg) or msg)
        if not success:
            return False

    else:
        # continue task based on user input
        slug = slugify(task.get("name", "name"))
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**" + messages.get("waiting_msg", "") + "**")
        with col2:
            done = button(messages.get("next"), key=f"{parent}_task_{slug}")
        if not done:
            return False

    # show success message after completion
    scs_msg = task.get("response")
    if scs_msg is not None:
        st.write(" ")
        rtemplate = Environment(loader=BaseLoader).from_string(task.get("response", ""))
        st.success(rtemplate.render(result=result))

    return True


def print_footer_nav(current: str):
    """Print the footer nav buttons for next and previous excercise."""
    # find the next and previous pages
    prev_page, next_page = sidebar.APP_SIDEBAR.prev_and_next_nav(current)

    # determine which buttons should be shown
    pills = []
    if prev_page is not None:
        pills.append(PREVIOUS)
    if next_page is not None:
        pills.append(NEXT)

    # render the buttons
    _, center, _ = st.columns([1, 1, 1])
    with center:
        next_steps = st.pills("", pills)

    # handle button presses
    if next_steps == PREVIOUS:
        st.switch_page(prev_page)
    elif next_steps == NEXT:
        st.switch_page(next_page)


def load_stylesheet():
    """Load and apply the stylesheet."""
    for stylesheet in STYLESHEETS:
        with open(stylesheet, "r", encoding="UTF-8") as ptr:
            style = ptr.read()

        # font awesome
        st.html(f"<style>{style}</style>")


@dataclass
class Theme:
    """Wrapper to simplify applying boilerplate theme."""

    autorefresh: bool = True
    ephemeral: bool = False

    def __enter__(self):
        """Initialize the theme."""
        load_state()
        if self.autorefresh:
            st_autorefresh(interval=AUTOREFRESH_DELAY, key="autorefresh")
        load_stylesheet()

        with st.sidebar:
            sidebar.APP_SIDEBAR.render()

    def __exit__(self, _, __, ___):
        """Cache data."""
        if not self.ephemeral:
            save_state()
