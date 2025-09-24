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
"""This module serves as the client to the graphql unix socket.

The reason this was custom made is because python-gql doesn't support unix sockets.
Also requests_unixsocket doesn't seem to play nicely with POSTs."""

import json
import os
from typing import Any

import requests
from httpunixsocketconnection import HTTPUnixSocketConnection

GQL_SOCKET = "/wb-svc-ro.socket"
QUERY_TIMEOUT = 3


def query(query_str: str):
    """Send a GraphQL query over a Unix socket."""
    api_host = os.getenv("NVWB_API")
    if api_host:
        req = requests.post(
            f"http://{api_host}/v1/query",
            json={"query": query_str},
            headers={"Content-Type": "application/json"},
        )
        return req.json()

    else:
        conn = HTTPUnixSocketConnection(unix_socket=GQL_SOCKET, timeout=QUERY_TIMEOUT)
        request_data = json.dumps({"query": query_str})
        conn.request("POST", "/v1/query", body=request_data, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        body = response.read().decode("UTF-8")
        return json.loads(body)  # type: ignore


def list_projects() -> dict[str, Any]:
    """List the projects and return the name, id, and path."""
    return query(
        """query {
            projects {
                edges {
                    node {
                        name
                        id
                        path
                    }
                }
            }
        }"""
    )


def get_project_path(project_name: str) -> None | str:
    """Find the project path."""
    projects = list_projects()["data"]["projects"]["edges"]
    for project in projects:
        if project["node"]["name"] == project_name:
            return project["node"]["path"]
    return None


def get_project(project_name: str) -> None | dict[str, Any]:
    """Get a project's details."""
    project_path = get_project_path(project_name)
    if project_path is None:
        return None

    return query(
        f"""query {{
                project(projectPath: "{project_path}") {{
                    name
                    path
                    remoteUrl
                    hasCompose
                    compose {{
                        fileLocation
                        availableProfiles
                        info {{
                            enabledProfiles
                            runState
                        }}
                    }}
                    gitBranches {{
                        name
                    }}
                    repoState {{
                        commitsAhead
                        commitsBehind
                        addedFilesCount
                        modifiedFilesCount
                        deletedFilesCount
                        changes {{
                            file
                            fileStatus
                        }}
                    }}
                    environment {{
                        buildState
                        runState
                        id
                    }}
                    applications {{
                        name
                        info {{
                            runState
                            url
                        }}
                    }}
                }}
            }}"""
    )


def get_file(project_name: str, relative_path: str, filename: str) -> dict[str, Any]:
    """Find a file in the project."""
    project_path = get_project_path(project_name)
    if project_path is None:
        return None

    return query(
        f"""query {{
            project(projectPath: "{project_path}") {{
                file(relativePath: "{relative_path}", fileName: "{filename}") {{
                    contents
                    modifiedAt
                    isDirectory
                }}
            }}
        }}"""
    )


def get_packages(project_name: str) -> dict[str, Any]:
    """List the packages installed in a project."""
    project_path = get_project_path(project_name)
    if project_path is None:
        return None
    return query(
        f"""query {{
            project(projectPath: "{project_path}") {{
                    environment {{
                        packageManagers {{
                            name
                            installedPackages {{
                                name
                            }}
                        }}
                    }}
                }}
            }}"""
    )


def get_gpu_request(project_name: str) -> dict[str, Any] | None:
    """Query project for GPU assignment."""
    project_path = get_project_path(project_name)
    if project_path is None:
        return None

    return query(
        f"""query {{
            project(projectPath: "{project_path}") {{
                resources {{
                    gpusRequested
                }}
            }}
        }}"""
    )
