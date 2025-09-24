# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES.
# All rights reserved.
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

"""Code to automate loading location specific messages from a file."""

import os
import locale
import logging

import yaml

DEFAULT_LOCALE = "en_US.yaml"
_LOGGER = logging.getLogger(__file__)


def load_messages(form_path: str) -> dict[str, str]:
    """Load the messages from a message catalog."""
    # find the yaml file
    base_path = os.path.splitext(form_path)[0]
    here = locale.getlocale()[0]
    catalog = ".".join([base_path, here, "yaml"])
    if not os.path.isfile(catalog):
        _LOGGER.info("Message file %s not found. Falling back to %s", catalog, DEFAULT_LOCALE)
        catalog = ".".join([base_path, DEFAULT_LOCALE, "yaml"])
    if not os.path.isfile(catalog):
        _LOGGER.critical("Cannot find the preferred or default language messages file in %s.", catalog)

    # read the yaml file
    with open(catalog, "r", encoding="UTF-8") as ptr:
        data = yaml.safe_load(ptr)
    return data
