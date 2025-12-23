import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.hr_department import HRDepartment

def test_hr_department_initialization():
    hr = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    assert hr.department_id == "DEP002"
    assert hr.name == "Human Resources"

def test_recruit_employee():
    hr = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    result = hr.recruit_employee("New Employee")
    assert result == True

def test_add_training_program():
    hr = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    hr.add_training_program("Leadership Training")
    assert "Leadership Training" in hr.training_programs

def test_get_recruitment_count():
    hr = HRDepartment("DEP002", "Human Resources", "HQ", "MGR002", 200000.0, 15)
    hr.recruit_employee("Employee 1")
    hr.recruit_employee("Employee 2")
    assert hr.get_recruitment_count() == 2