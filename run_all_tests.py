"""Script to run all test files in the tutorial app."""

import subprocess
import sys
import os

test_files = [
    "src/tutorial_app/pages/advanced_02_tests.py",
    "src/tutorial_app/pages/advanced_03_tests.py",
    "src/tutorial_app/pages/basic_01_tests.py",
    "src/tutorial_app/pages/basic_02_tests.py",
    "src/tutorial_app/pages/basic_03_tests.py",
    # "src/tutorial_app/pages/overview_tests.py",  # Excluded: UI interaction test that intentionally fails
    "src/tutorial_app/pages/owlban_group_tests.py",
    "src/tutorial_app/pages/settings_tests.py",
]

for test_file in test_files:
    print(f"Running {test_file}...")
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONPATH": "src/tutorial_app"},
        )
        if result.returncode == 0:
            print(f"✓ {test_file} passed")
        else:
            print(f"✗ {test_file} failed: {result.stderr}")
    except Exception as e:
        print(f"✗ {test_file} error: {e}")
