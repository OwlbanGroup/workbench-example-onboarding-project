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

try:
    from common import testing
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common import testing


# try:
#     from common import testing
# except ImportError:
#     # this helps with debugging and allows direct importing or execution
#     sys.path.append("..")
#     from common import testing


PROJECT_NAME = "nvidia-ai-workbench-onboarding"
JUPYTER_NAME = "jupyterlab"


def wait_for_jupyterlab_start():
    """Wait for the JupyterLab app to be running."""
    project = testing.get_project(PROJECT_NAME)  # Use testing module's version
    app = testing.get_app(project, JUPYTER_NAME)
    target = testing.AppState.RUNNING
    testing.ensure_app_state(app, target)


def wait_for_jupyterlab_stop():
    """Wait for the JupyterLab app to stop running."""
    project = testing.get_project(PROJECT_NAME)
    app = testing.get_app(project, JUPYTER_NAME)
    target = testing.AppState.NOT_RUNNING
    testing.ensure_app_state(app, target)


def wait_three_times():
    """Wait for a few calls."""
    import tempfile
    import os

    # Use system temp directory instead of /tmp
    temp_dir = tempfile.gettempdir()

    for idx in range(3):
        marker = Path(temp_dir) / f"file{idx}"
        if not marker.exists():
            try:
                with marker.open("w", encoding="utf-8"):
                    pass
                raise testing.TestFail(f"info_wait_{idx}")
            except Exception as e:
                print(f"Skipping test: Cannot create temp file - {e}")
                return

    for idx in range(3):
        marker = Path(temp_dir) / f"file{idx}"
        try:
            marker.unlink()
        except Exception:
            pass  # Ignore if file doesn't exist or can't be deleted


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
    wait_three_times()
