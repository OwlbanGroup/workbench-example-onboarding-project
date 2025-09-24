#!/usr/bin/env python3
"""Simple test runner to avoid pytest naming conflicts."""

import sys
import os
import importlib.util
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())


def run_test_file(test_file_path):
    """Run a single test file."""
    try:
        # Load the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file_path)
        if spec is None or spec.loader is None:
            print(f"Could not load {test_file_path}")
            return False

        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        # Run test classes/methods if they exist
        success = True
        for attr_name in dir(test_module):
            attr = getattr(test_module, attr_name)
            if attr_name.startswith("test_") and callable(attr):
                try:
                    print(f"Running {attr_name}...")
                    attr()
                    print(f"✓ {attr_name} passed")
                except Exception as e:
                    print(f"✗ {attr_name} failed: {e}")
                    success = False
            elif hasattr(attr, "__bases__") and any("Test" in str(base) for base in attr.__bases__):
                # It's a test class
                try:
                    print(f"Running test class {attr_name}...")
                    # Try to instantiate and run
                    instance = attr()
                    for method_name in dir(instance):
                        if method_name.startswith("test_") and callable(getattr(instance, method_name)):
                            try:
                                print(f"  Running {method_name}...")
                                getattr(instance, method_name)()
                                print(f"  ✓ {method_name} passed")
                            except Exception as e:
                                print(f"  ✗ {method_name} failed: {e}")
                                success = False
                except Exception as e:
                    print(f"✗ {attr_name} failed: {e}")
                    success = False

        return success

    except Exception as e:
        print(f"Error running {test_file_path}: {e}")
        return False


def main():
    """Run all tests in the tests directory."""
    tests_dir = Path("code/tutorial_app/tests")
    if not tests_dir.exists():
        print(f"Tests directory {tests_dir} not found")
        return 1

    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        print("No test files found")
        return 1

    print(f"Found {len(test_files)} test files")
    all_passed = True

    for test_file in test_files:
        print(f"\nRunning tests in {test_file.name}")
        if not run_test_file(test_file):
            all_passed = False

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
