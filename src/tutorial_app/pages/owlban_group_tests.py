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
"""Tests for NVIDIA AI Workbench Team Onboarding Tasks."""
from pathlib import Path
import sys
import os
import subprocess

try:
    from common import testing
except ImportError:
    # this helps with debugging and allows direct importing or execution
    sys.path.append(str(Path(__file__).parent.parent))
    from common import testing


def check_environment_setup():
    """Check if the NVIDIA AI Workbench environment is set up correctly."""
    issues = []

    # Check for requirements.txt
    req_file = Path("requirements.txt")
    if not req_file.exists():
        issues.append("requirements.txt not found in project root.")
    else:
        # Verify it contains essential packages
        with open(req_file, "r") as f:
            content = f.read().lower()
            if "streamlit" not in content:
                issues.append("Streamlit not found in requirements.txt")
            if "pydantic" not in content:
                issues.append("Pydantic not found in requirements.txt")

    # Check for NVIDIA integration files
    nvidia_files = [
        "setup_nvidia_integration.sh",
        "setup_nvidia_integration.bat",
        "NVIDIA_INTEGRATION_README.md",
        "variables.env",
    ]
    for file in nvidia_files:
        if not Path(file).exists():
            issues.append(f"NVIDIA integration file missing: {file}")

    # Check for environment configuration
    env_files = ["variables.env", ".env", "deploy/environments/production.env"]
    env_configured = False
    for env_file in env_files:
        if Path(env_file).exists():
            env_configured = True
            break
    if not env_configured:
        issues.append("No environment configuration files found")

    # Check for security module
    security_file = Path("src/tutorial_app/common/security.py")
    if not security_file.exists():
        issues.append("Security module not found")
    else:
        # Basic check that security features are implemented
        with open(security_file, "r") as f:
            content = f.read()
            if "InputSanitizer" not in content:
                issues.append("InputSanitizer class not found in security module")
            if "initialize_security" not in content:
                issues.append("initialize_security function not found")

    # Check for documentation
    docs = ["docs/DEVELOPER_GUIDE.md", "docs/API_REFERENCE.md", "README.md"]
    for doc in docs:
        if not Path(doc).exists():
            issues.append(f"Documentation file missing: {doc}")

    if issues:
        raise testing.TestFail("Environment setup issues found:\n" + "\n".join(f"• {issue}" for issue in issues))

    print("SUCCESS: NVIDIA AI Workbench environment setup verified successfully!")


def check_nvidia_integration():
    """Check if NVIDIA integration is properly configured."""
    issues = []

    # Check environment variables
    required_vars = ["NVWB_API", "SECRET_KEY"]
    env_file = Path("variables.env")
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
            for var in required_vars:
                if var not in content:
                    issues.append(f"Required environment variable missing: {var}")

    # Check deployment configurations
    deploy_configs = [
        "deploy/environments/production.env",
        "docker-compose.yml",
        "deploy/kubernetes/deployment.yml",
    ]
    for config in deploy_configs:
        if not Path(config).exists():
            issues.append(f"Deployment configuration missing: {config}")

    # Check monitoring setup
    monitoring_files = [
        "deploy/monitoring/prometheus.yml",
        "deploy/monitoring/grafana/provisioning/datasources/prometheus.yml",
    ]
    for mon_file in monitoring_files:
        if not Path(mon_file).exists():
            issues.append(f"Monitoring configuration missing: {mon_file}")

    if issues:
        raise testing.TestFail("NVIDIA integration issues found:\n" + "\n".join(f"• {issue}" for issue in issues))

    print("SUCCESS: NVIDIA integration verified successfully!")


def check_development_workflow():
    """Check if development workflow tools are properly configured."""
    issues = []

    # Check for pre-commit configuration
    if not Path(".pre-commit-config.yaml").exists():
        issues.append("Pre-commit configuration missing")

    # Check for CI/CD pipeline
    if not Path(".github/workflows/ci-cd.yml").exists():
        issues.append("CI/CD pipeline configuration missing")

    # Check for testing configuration
    test_files = ["pyproject.toml", "run_all_tests.py"]
    for test_file in test_files:
        if not Path(test_file).exists():
            issues.append(f"Testing configuration missing: {test_file}")

    # Try to run a basic test to verify test environment
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import streamlit; print('Streamlit available')"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            issues.append("Streamlit not properly installed or accessible")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        issues.append("Cannot verify Streamlit installation")

    if issues:
        raise testing.TestFail("Development workflow issues found:\n" + "\n".join(f"• {issue}" for issue in issues))

    print("SUCCESS: Development workflow verified successfully!")


if __name__ == "__main__":
    sys.stdout.write("---------------\n")
    sys.stdout.write("NVIDIA AI Workbench Onboarding Tests\n")
    sys.stdout.write("---------------\n")

    try:
        check_environment_setup()
        check_nvidia_integration()
        check_development_workflow()
        sys.stdout.write("SUCCESS: All NVIDIA onboarding checks passed!\n")
    except testing.TestFail as e:
        sys.stdout.write(f"ERROR: Onboarding check failed: {e}\n")
        sys.exit(1)
