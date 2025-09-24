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
"""Excercise page layout."""

from pathlib import Path

import streamlit as st

from common import localization, theme

TESTS = None

MESSAGES = localization.load_messages(__file__)
NAME = Path(__file__).stem
COMPLETED_TASKS = 0

with theme.Theme():
    # Header
    st.title(MESSAGES.get("title"))
    st.write(MESSAGES.get("welcome_msg"))

    # Print Onetime Tasks
    st.header(MESSAGES.get("header_onetime"), divider="gray")
    for task in MESSAGES.get("tasks_onetime", []):
        if not theme.print_task(NAME, task, None, MESSAGES):
            break
        COMPLETED_TASKS += 1

    # Print everytime tasks
    if COMPLETED_TASKS == len(MESSAGES.get("tasks_onetime", [])):
        st.header(MESSAGES.get("header_everytime"), divider="gray")
        for task in MESSAGES.get("tasks_everytime", []):
            if not theme.print_task(NAME, task, TESTS, MESSAGES):
                break
            COMPLETED_TASKS += 1

        else:
            # Print footer after last task
            st.success(MESSAGES.get("closing_msg", None))
            theme.print_footer_nav(NAME)

    # save state updates
    theme.ensure_state(f"{NAME}_completed", COMPLETED_TASKS)
    total_length = len(MESSAGES.get("tasks_onetime", [])) + len(MESSAGES.get("tasks_everytime", []))
    theme.ensure_state(f"{NAME}_total", total_length)
