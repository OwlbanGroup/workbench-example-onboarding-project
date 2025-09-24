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
from typing import Any

try:
    from common.testing import TestFail
    from common import wb_svc_client
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common.testing import TestFail
    from common import wb_svc_client

PROJECT_NAME = "my-first-project"
BRANCH_NAME = "my-first-branch"

# TODO: add step to setup git server integration


def get_project() -> dict[str, Any]:
    """Get the working project."""
    return wb_svc_client.get_project(PROJECT_NAME) or {}


def wait_for_commit():
    """Wait for the repo changes to be committed."""
    proj = get_project()
    changes = proj.get("data", {}).get("project", {}).get("repoState", {}).get("changes")
    num_changes = len(changes) if changes else 0

    if num_changes > 0:
        raise TestFail("info_wait_for_commit")


def wait_for_publish() -> str:
    """Wait for the repo to be published."""
    proj = get_project()
    url = proj.get("data", {}).get("project", {}).get("remoteUrl")

    if url is None:
        raise TestFail("info_wait_for_publish")

    return url


def wait_for_remote_changes():
    """Wait for the repo to be published."""
    proj = get_project()
    behind = proj.get("data", {}).get("project", {}).get("repoState", {}).get("commitsBehind")

    if behind == 0:
        raise TestFail("info_wait_for_remote_changes")


def wait_for_remote_changes_sync():
    """Wait for the repo to be synced."""
    proj = get_project()
    behind = proj.get("data", {}).get("project", {}).get("repoState", {}).get("commitsBehind")

    if behind > 0:
        raise TestFail("info_wait_for_remote_changes_sync")


def wait_for_branch():
    """Wait for branch to exist."""
    proj = get_project()
    branches = proj.get("data", {}).get("project", {}).get("gitBranches", [])

    if {"name": BRANCH_NAME} not in branches:
        raise TestFail("info_wait_for_branch")


def wait_for_no_proj():
    """Wait for the project to be deleted."""
    proj = get_project()
    if proj != {}:
        raise TestFail("info_wait_for_no_proj")


def wait_for_proj():
    """Wait for the project to be deleted."""
    try:
        proj = get_project()
        if proj == {}:
            raise TestFail("info_wait_for_proj")
    except OSError as e:
        if "Socket" in str(e) or "does not exist" in str(e):
            print("Skipping test: Workbench service not available in local environment")
            return
        raise


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
    wait_for_proj()
