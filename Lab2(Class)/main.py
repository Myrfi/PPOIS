import pytest
import os
import sys
import shutil

def clean_pycache(project_root):
    """Удаляем __pycache__ и .pyc файлы"""
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    sys.path.insert(0, project_root)

    clean_pycache(project_root)

    print("Running comprehensive test suite for Transnational Company Management System")
    print("="*80)
    print("🔍 Discovering and running all tests from /tests directory...\n")

    # Запуск всех тестов с coverage
    pytest_args = [
        "--cov=src",
        "--cov-report=term",
        "--cov-report=html:coverage_report",
        "-v",
        "--tb=short",
        "--maxfail=0",
        "--disable-warnings",
        "tests/"
    ]

    # Результат pytest
    result = pytest.main(pytest_args)

    print("\n" + "="*80)
    print("📊 TEST RESULTS SUMMARY:")
    print("="*80)

    if result == 0:
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print(f"⚠️  SOME TESTS FAILED (return code: {result})")

    print("="*80)
    print("📈 COVERAGE REPORT:")
    print("📁 HTML report saved to: coverage_report/index.html")
    print("="*80)
    print("🔹 To see coverage % and details, check the terminal output above or open the HTML report.")

