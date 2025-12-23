import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.department import Department

def test_department_initialization():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 50)
    assert dept.department_id == "DEP001"
    assert dept.name == "Engineering"
    assert dept.location == "San Francisco"
    assert dept.budget == 500000.0
    assert dept.employee_capacity == 50

def test_add_employee():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    result = dept.add_employee("EMP001")
    assert result == True
    assert "EMP001" in dept.employees

def test_add_employee_at_capacity():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 1)
    dept.add_employee("EMP001")
    result = dept.add_employee("EMP002")
    assert result == False

def test_remove_employee():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    dept.add_employee("EMP001")
    result = dept.remove_employee("EMP001")
    assert result == True
    assert "EMP001" not in dept.employees

def test_add_project():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    dept.add_project("PROJ001")
    assert "PROJ001" in dept.projects

def test_allocate_budget():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    result = dept.allocate_budget(100000.0)
    assert result == True
    assert dept.budget == 400000.0

def test_allocate_budget_insufficient():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 50000.0, 10)
    result = dept.allocate_budget(100000.0)
    assert result == False

def test_get_employee_count():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    dept.add_employee("EMP001")
    dept.add_employee("EMP002")
    assert dept.get_employee_count() == 2

def test_get_utilization_rate():
    dept = Department("DEP001", "Engineering", "San Francisco", "MGR001", 500000.0, 10)
    dept.add_employee("EMP001")
    utilization = dept.get_utilization_rate()
    assert utilization == 10.0