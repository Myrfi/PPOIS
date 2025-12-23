import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.project_manager import ProjectManager

def test_project_manager_initialization():
    pm = ProjectManager("PM001", "Lisa", "Wang", "lisa@company.com", "2017-09-01", 85000.0, "DEP001", True, "agile", 8)
    assert pm.employee_id == "PM001"
    assert pm.pmp_certified == True

def test_increment_projects_completed():
    pm = ProjectManager("PM001", "Lisa", "Wang", "lisa@company.com", "2017-09-01", 85000.0, "DEP001", True, "agile", 8)
    pm.increment_projects_completed()
    assert pm.projects_completed == 1

def test_update_on_time_delivery_rate():
    pm = ProjectManager("PM001", "Lisa", "Wang", "lisa@company.com", "2017-09-01", 85000.0, "DEP001", True, "agile", 8)
    pm.update_on_time_delivery_rate(90.5)
    assert pm.on_time_delivery_rate == 90.5