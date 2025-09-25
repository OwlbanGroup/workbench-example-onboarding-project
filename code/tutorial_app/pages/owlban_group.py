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
"""NVIDIA AI Workbench Team Onboarding Page."""

from pathlib import Path

import streamlit as st  # type: ignore

from common import localization, theme
from pages import owlban_group_tests as TESTS

# Load NVIDIA-focused onboarding content
MESSAGES = localization.load_messages(Path(__file__).parent / "owlban_group_nvidia.en_US.yaml")
NAME = Path(__file__).stem
COMPLETED_TASKS = 0

with theme.Theme():
    # Header with NVIDIA branding
    st.title(MESSAGES.get("title"))
    st.write(MESSAGES.get("welcome_msg"))
    st.header(MESSAGES.get("header"), divider="green")

    # NVIDIA-themed progress indicator
    if len(MESSAGES.get("tasks", [])) > 0:
        progress = COMPLETED_TASKS / len(MESSAGES.get("tasks", []))
        st.progress(progress, text=f"NVIDIA Onboarding Progress: {COMPLETED_TASKS}/{len(MESSAGES.get('tasks', []))}")

    # Print Tasks with NVIDIA branding
    for task in MESSAGES.get("tasks", []):
        if not theme.print_task(NAME, task, TESTS, MESSAGES):
            break
        COMPLETED_TASKS += 1
    else:
        # Print NVIDIA-themed completion message
        st.success(MESSAGES.get("closing_msg", None))
        st.balloons()  # Celebration effect
        theme.print_footer_nav(NAME)

    # Save state updates
    theme.ensure_state(f"{NAME}_completed", COMPLETED_TASKS)
    theme.ensure_state(f"{NAME}_total", len(MESSAGES.get("tasks", [])))

    # NVIDIA integration status
    if COMPLETED_TASKS == len(MESSAGES.get("tasks", [])):
        st.info(
            "🔗 **NVIDIA Integration Status**: All onboarding tasks completed. You are now fully integrated into the NVIDIA AI Workbench ecosystem!"
        )
