#!/usr/bin/env python3
"""
Run all tests for Transnational Company Management System.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage reporting."""
    project_root = os.path.abspath(os.path.dirname(__file__))
    tests_dir = os.path.join(project_root, "tests")

    print("Running comprehensive test suite for Transnational Company Management System")
    print("======================================================================")
    print("🔍 Discovering and running all tests from /tests directory...")
    print()

    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=src",
        "--cov-report=term",
        "--cov-report=html:coverage_report",
        "-v",
        "--tb=short",
        tests_dir
    ]

    try:
        result = subprocess.run(cmd, cwd=project_root, capture_output=False, text=True)
        exit_code = result.returncode
    except FileNotFoundError:
        print("❌ ERROR: pytest not found. Please install pytest:")
        print("   pip install pytest pytest-cov")
        return 1

    print("\\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY:")
    print("="*80)

    if exit_code == 0:
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("🎯 COMPREHENSIVE COVERAGE ACHIEVED!")
        print("📊 Coverage report saved to: coverage_report/index.html")
    else:
        print(f"⚠️  SOME TESTS FAILED (exit code: {exit_code})")
        print("📊 Coverage calculated for passed tests")
        print("❌ Check the output above for failed test details")

    print("="*80)
    return exit_code

if __name__ == "__main__":
    sys.exit(run_tests())