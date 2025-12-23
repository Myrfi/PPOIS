import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.employee import Employee

def test_employee_initialization():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    assert emp.employee_id == "EMP001"
    assert emp.first_name == "John"
    assert emp.last_name == "Doe"
    assert emp.salary == 75000.0
    assert emp.is_active == True

def test_get_full_name():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    assert emp.get_full_name() == "John Doe"

def test_update_salary():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    emp.update_salary(80000.0)
    assert emp.salary == 80000.0

def test_deactivate():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    emp.deactivate()
    assert emp.is_active == False

def test_assign_manager():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    emp.assign_manager("MGR001")
    assert emp.manager_id == "MGR001"

def test_change_location():
    emp = Employee("EMP001", "John", "Doe", "john@company.com", "2023-01-01", 75000.0, "DEP001")
    emp.change_location("London")
    assert emp.location == "London"