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
from pages import settings_tests as TESTS

MESSAGES = localization.load_messages(__file__)
NAME = Path(__file__).stem

with theme.Theme(ephemeral=True):

    # reset progress
    with st.container(border=True):
        for task in MESSAGES.get("reset_progress_tasks", []):
            if not theme.print_task(NAME, task, TESTS, MESSAGES):
                break

    # break into two columns
    col_1, col_2 = st.columns([1, 1])

    # information on support logs
    with col_1:
        with st.container(border=True):
            st.header(MESSAGES.get("bundle_header"), divider="gray")
            st.markdown(MESSAGES.get("bundle_msg"))

    # information on developer forum
    with col_2:
        with st.container(border=True):

            st.header(MESSAGES.get("forum_header"), divider="gray")
            st.markdown(MESSAGES.get("forum_msg"))
