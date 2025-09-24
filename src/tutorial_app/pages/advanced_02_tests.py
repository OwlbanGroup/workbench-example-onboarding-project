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
import sys

try:
    from common import testing
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common import testing

PROJECT_NAME = "custom-application-project"
PYTHON_PACKAGE = "gradio"
JUPYTER_NAME = "jupyterlab"
CODE_DIR = "/code"
CODE_FILE = "gradio-hello-world.py"
APP_NAME = "simple-gradio"


def create_project():
    """Wait for the project to be created."""
    project = testing.get_project(PROJECT_NAME)
    build_target = testing.BuildState.NO_BUILD
    testing.ensure_build_state(project, build_target)
    # run_target = testing.RunState.RUNNING
    # testing.ensure_run_state(project, run_target)


def package_setup():
    """Wait for python packages."""
    testing.ensure_package(PROJECT_NAME, "pip", PYTHON_PACKAGE)


def create_web_app():
    """Wait for the web app code to probably exist."""
    project = testing.get_project(PROJECT_NAME)

    # start jupyter
    app = testing.get_app(project, JUPYTER_NAME)
    target = testing.AppState.RUNNING
    testing.ensure_app_state(app, target)

    # write code
    contents = testing.get_file(PROJECT_NAME, CODE_DIR, CODE_FILE)
    if b"demo.launch" not in contents:
        raise testing.TestFail("info_wait_for_code")


def wait_for_custom_app():
    """Wait for the custom application to be created."""
    project = testing.get_project(PROJECT_NAME)
    _ = testing.get_app(project, APP_NAME)


def wait_for_custom_app_start():
    """Wait for the custom application to be started."""
    project = testing.get_project(PROJECT_NAME)
    app = testing.get_app(project, APP_NAME)
    target = testing.AppState.RUNNING
    testing.ensure_app_state(app, target)


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
