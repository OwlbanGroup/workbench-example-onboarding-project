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
from typing import Any
import sys

try:
    from common import testing
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common import testing


PROJECT_NAME = "my-first-project"
PROJECT_DIR = "/project"
JUPYTER_NAME = "jupyterlab"
IPYNB_DIR = "/code"
IPYNB_FILE = "my-new-notebook.ipynb"
PYTHON_PACKAGE_1 = "plotly"
PYTHON_PACKAGE_2 = "numpy"
UBUNTU_PACKAGE = "jq"


def create_a_brand_new_project():
    """Ensure my-first-project is created."""
    _ = testing.get_project(PROJECT_NAME)


def wait_for_project_build():
    """Wait for the project to finish building."""
    project = testing.get_project(PROJECT_NAME)
    target = testing.BuildState.NO_BUILD
    testing.ensure_build_state(project, target)


def wait_for_project_start():
    """Wait for the project to finish starting."""
    project = testing.get_project(PROJECT_NAME)
    target = testing.RunState.RUNNING
    testing.ensure_run_state(project, target)


def wait_for_jupyterlab_to_exist() -> dict[str, Any]:
    """Wait for the JupyterLab application to exist."""
    project = testing.get_project(PROJECT_NAME)
    _ = testing.get_app(project, JUPYTER_NAME)


def wait_for_jupyterlab_start():
    """Wait for the JupyterLab app to be running."""
    project = testing.get_project(PROJECT_NAME)
    app = testing.get_app(project, JUPYTER_NAME)
    target = testing.AppState.RUNNING
    testing.ensure_app_state(app, target)


def create_a_new_notebook() -> dict[str, Any]:
    """Ensure my-first-project is created."""
    _ = testing.get_file(PROJECT_NAME, IPYNB_DIR, IPYNB_FILE)


def write_some_code():
    """Wait for some code plotly code to be in the notebook."""
    contents = testing.get_file(PROJECT_NAME, IPYNB_DIR, IPYNB_FILE)
    if "plotly" not in contents.decode("UTF-8"):
        raise testing.TestFail("info_wait_for_code")


def add_python_packages():
    """Wait for the package to be added."""
    pkg = testing.ensure_package(PROJECT_NAME, "pip", PYTHON_PACKAGE_1)
    pkg = testing.ensure_package(PROJECT_NAME, "pip", PYTHON_PACKAGE_2)
    return pkg


def add_ubuntu_package():
    """Check if 'jq' appears in the file."""
    import os

    file_path = os.path.join(PROJECT_DIR, "apt.txt")

    content = testing.get_file(PROJECT_NAME, ".", "apt.txt").decode("UTF-8")

    if "jq" not in content:
        raise testing.TestFail("info_wait_for_package")

    return None


def rebuild_environment():
    """Wait for the environment to rebuild and restart."""
    wait_for_project_build()
    wait_for_project_start()


def wait_for_project_stop():
    """Wait for the project to stop."""
    project = testing.get_project(PROJECT_NAME)
    target = [testing.RunState.NOT_RUNNING, testing.RunState.CONTAINER_NOT_CREATED]
    testing.ensure_run_state(project, target)


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
