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
"""Tests for Owlban Group onboarding tasks."""
from pathlib import Path
import sys

try:
    from common import testing
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append("..")
    from common import testing


def check_environment_setup():
    """Check if the environment is set up correctly."""
    # Simple check: ensure requirements.txt exists
    req_file = Path("requirements.txt")
    if not req_file.exists():
        raise testing.TestFail("Requirements file not found.")
    # Add more checks if needed


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    # you can use this space for testing while you are
    # developing your tests
    check_environment_setup()
