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
"""Tests for auto continuing associated tasks."""
from pathlib import Path
import sys

import streamlit as st

try:
    from common import testing, theme
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common import testing, theme

PROJECTS = ["my-first-project", "custom-application-project", "multi-container-project"]
INFO_MSG = ["info_first_project", "info_custom_app_proj", "info_multi_container_proj"]


def wait_for_clean():
    """Wait for the projects to be deleted."""
    # wait for user to delete projects
    for idx, project in enumerate(PROJECTS):
        try:
            _ = testing.get_project(project)
        except testing.TestFail:
            continue
        raise testing.TestFail(INFO_MSG[idx])

    # remove the cached state
    try:
        Path(theme.STATE_FILE).unlink()
    except FileNotFoundError:
        pass

    # clear the state
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
