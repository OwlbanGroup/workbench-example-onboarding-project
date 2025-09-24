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
"""Helpers for testing lab steps."""
import base64
from enum import Enum
from typing import cast, Any

from common import wb_svc_client


class TestFail(Exception):
    """Indicates a test failed."""


def run_test(fun) -> tuple[bool, None | str, None | Any]:
    """Cache the state of a test once it passes."""
    # importing streamlit outside of the toplevel to prevent
    # nuisance warnings while developing testing code.
    # pylint: disable-next=import-outside-toplevel
    import streamlit as st  # type: ignore

    mod_name = fun.__module__.split(".")[-1]
    idx = mod_name + "_" + fun.__name__

    # recall state from cache, if it exists
    cached_state = st.session_state.get(idx, None)
    if cached_state is not None:
        return cast(tuple[bool, None | str, None | Any], cached_state)

    # run the test to evaluate state
    try:
        result = fun()
        state = (True, None, result)
    except TestFail as exc:
        state = (False, str(exc), None)
    else:
        st.session_state[idx] = state

    return state


GQLDataType = dict[str, Any]


def get_project(project_name: str) -> GQLDataType:
    """Get a project, fail the test if it doesn't exist.

    Error message keys:
      - info_wait_for_project
    """
    project = wb_svc_client.get_project(project_name)
    if project is None:
        raise TestFail("info_wait_for_project")
    project = project.get("data", {}).get("project", None)
    if project is None:
        raise TestFail("info_wait_for_project")
    return project


class BuildState(Enum):
    """Possible values for the state of the build."""

    NO_BUILD = "NO_BUILD"
    FULL_BUILD = "FULL_BUILD"
    QUICK_BUILD = "QUICK_BUILD"
    BUILDING = "BUILDING"
    BUILD_ERROR = "BUILD_ERROR"
    IMAGE_DOES_NOT_EXIST = "IMAGE_DOES_NOT_EXIST"


def ensure_build_state(project: GQLDataType, target: BuildState):
    """Ensure that a project has desired build state.

    Error message keys:
      - info_build_ready -> state is ready and that is not desired
      - info_build_needed
      - info_build_running
      - info_build_error
    """
    try:
        state = BuildState(project["environment"]["buildState"])
    except ValueError:
        # this should never happen
        # if this happens, workbench is returning an unrecognized value
        raise TestFail("Unknown project build state.")

    # desired state has been reached
    if state == target:
        return

    # fail specific to the current state
    if state == BuildState.NO_BUILD:
        raise TestFail("info_build_ready")
    if state in [BuildState.QUICK_BUILD, BuildState.FULL_BUILD]:
        raise TestFail("info_build_needed")
    if state == BuildState.BUILDING:
        raise TestFail("info_build_running")
    if state in [BuildState.BUILD_ERROR, BuildState.IMAGE_DOES_NOT_EXIST]:
        raise TestFail("info_build_error")


class RunState(Enum):
    """Possible values for the project's run state."""

    CONTAINER_NOT_CREATED = "CONTAINER_NOT_CREATED"
    NOT_RUNNING = "NOT_RUNNING"
    RESTARTING = "RESTARTING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    OOM_KILLED = "OOM_KILLED"
    DEAD = "DEAD"


def ensure_run_state(project: GQLDataType, target: RunState):
    """Ensure that a project has desired run state.

    Error message keys:
      - info_container_not_running
      - info_container_running
      - info_container_paused
      - info_container_dead
    """
    try:
        state = RunState(project["environment"]["runState"])
    except ValueError:
        # this should never happen
        # if this happens, workbench is returning an unrecognized value
        raise TestFail("Unkown project run state")

    if not isinstance(target, list):
        target = [target]

    # return if desired state has been reached
    if state in target:
        return

    # throw state specific error
    if state in [RunState.CONTAINER_NOT_CREATED, RunState.NOT_RUNNING, RunState.RESTARTING]:
        raise TestFail("info_container_not_running")
    if state == RunState.RUNNING:
        raise TestFail("info_container_running")
    if state == RunState.PAUSED:
        raise TestFail("info_container_paused")
    if state in [RunState.OOM_KILLED, RunState.DEAD]:
        raise TestFail("info_container_dead")


def get_app(project: GQLDataType, app_name: str) -> GQLDataType:
    """Get the data for an application.

    Error message keys:
    - info_waiting_for_app
    """
    for app in project.get("applications", []):
        if app.get("name") == app_name:
            return app
    raise TestFail("info_wait_for_app")


class AppState(Enum):
    """Possible states for an application."""

    RUNNING = "RUNNING"
    NOT_RUNNING = "NOT_RUNNING"
    STOPPING = "STOPPING"
    STARTING = "STARTING"


def ensure_app_state(app: GQLDataType, target: RunState):
    """Ensure application is at desired state.

    Error Message Keys:
        - info_app_is_running
        - info_app_not_running
        - info_app_starting
    """
    try:
        state = AppState(app["info"]["runState"])
    except ValueError:
        # this should never happen
        # if this happens, workbench is returning an unrecognized value
        raise TestFail("Unkown app state")

    if state == target:
        return

    if state == AppState.RUNNING:
        raise TestFail("info_app_is_running")
    if state in [AppState.NOT_RUNNING, AppState.STOPPING]:
        raise TestFail("info_app_not_running")
    if state == AppState.STARTING:
        raise TestFail("info_app_starting")


def ensure_package(project_name: str, package_manager: str, package_name: str) -> dict[str, str]:
    """Ensure package is installed.

    Error message keys:
        - info_wait_for_package
    """
    # pull all package managers
    packages = wb_svc_client.get_packages(project_name) or {}
    packages = packages.get("data", {}).get("project", {}).get("environment", {}).get("packageManagers", [])

    # find the requested package manager
    installed_packages = []
    for manager in packages:
        if manager["name"] == package_manager:
            installed_packages = manager["installedPackages"]
            break

    # find the requested package
    for pkg in installed_packages:
        if pkg["name"] == package_name:
            return pkg

    raise TestFail("info_wait_for_package")


class ComposeState(Enum):
    """Representation of docker compose states."""

    RUNNING = "RUNNING"
    NOT_RUNNING = "NOT_RUNNING"
    STARTING = "STARTING"
    STOPPING = "STOPPING"
    ERROR = "ERROR"


def ensure_compose_state(project: GQLDataType, target: ComposeState):
    """Ensure compose is at desired state.

    Error Message Keys:
        - info_compose_is_running
        - info_compose_not_running
        - info_compose_starting
        - info_compose_error
    """
    try:
        state = ComposeState(project["compose"]["info"]["runState"])
    except ValueError:
        # this should never happen
        # if this happens, workbench is returning an unrecognized value
        raise TestFail("Unkown app state")
    except KeyError:
        state = ComposeState.NOT_RUNNING

    if state == target:
        return

    if state == ComposeState.RUNNING:
        raise TestFail("info_compose_is_running")
    if state in [ComposeState.NOT_RUNNING, ComposeState.STOPPING]:
        raise TestFail("info_compose_not_running")
    if state == ComposeState.STARTING:
        raise TestFail("info_compose_starting")
    if state == ComposeState.ERROR:
        raise TestFail("info_compose_error")


def get_file(project_name: str, directory: str, filename: str) -> bytes:
    """Retrieve a file from a project.

    Error message keys:
        - info_wait_for_file
    """
    response = wb_svc_client.get_file(project_name, directory, filename) or {}
    wb_file = response.get("data", {}).get("project", {}).get("file")
    if wb_file is None:
        raise TestFail("info_wait_for_file")

    return base64.b64decode(wb_file["contents"])


def get_folder(project_name: str, directory: str, folder_name: str) -> dict[str, Any]:
    """Retrieve a folder from a project.

    Error message keys:
        - info_wait_for_folder
    """
    response = wb_svc_client.get_file(project_name, directory, folder_name) or {}
    if response is None:
        raise TestFail("info_wait_for_folder")

    wb_file = response.get("data", {}).get("project", {}).get("file")
    if wb_file is None or not wb_file.get("isDirectory", False):
        raise TestFail("info_wait_for_folder")

    return wb_file


def ensure_gpu_count(project_name: str):
    """Ensure that a project has a valid GPU count (including 0).

    Error message keys:
        - info_wait_for_project
    """
    response = wb_svc_client.get_gpu_request(project_name) or {}
    gpu_count = response.get("data", {}).get("project", {}).get("resources", {}).get("gpusRequested")

    if gpu_count is None:
        raise TestFail("info_wait_for_project")

    return gpu_count


def ensure_changes_discarded(project_name: str):
    """Ensure the project has no uncommitted changes.

    Error message keys:
        - info_check_changes_discarded
        - info_wait_for_project
    """
    project = wb_svc_client.get_project(project_name) or {}
    project = project.get("data", {}).get("project")
    if project is None:
        raise TestFail("info_wait_for_project")

    repo_state = project.get("repoState", {})
    added = repo_state.get("addedFilesCount", 0)
    modified = repo_state.get("modifiedFilesCount", 0)
    deleted = repo_state.get("deletedFilesCount", 0)

    if (added + modified + deleted) > 0:
        raise TestFail("info_check_changes_discarded")
