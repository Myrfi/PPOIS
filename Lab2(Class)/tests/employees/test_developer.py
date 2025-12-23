import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.developer import Developer

def test_developer_initialization():
    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    assert dev.employee_id == "DEV001"
    assert dev.programming_languages == ["Python"]
    assert dev.experience_years == 3

def test_add_programming_language():
    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    dev.add_programming_language("Java")
    assert "Java" in dev.programming_languages

def test_update_code_quality_score():
    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    dev.update_code_quality_score(8.5)
    assert dev.code_quality_score == 8.5

def test_increment_projects_completed():
    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    dev.increment_projects_completed()
    assert dev.projects_completed == 1

def test_get_experience_level():
    dev = Developer("DEV001", "Alice", "Johnson", "alice@company.com", "2022-03-01", 85000.0, "DEP001", ["Python"], 3, "backend")
    assert dev.get_experience_level() == "mid"