import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.manager import Manager

def test_manager_initialization():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    assert mgr.employee_id == "MGR001"
    assert mgr.management_level == "senior"
    assert mgr.subordinates == []
    assert mgr.budget_limit == 0.0

def test_add_subordinate():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.add_subordinate("EMP001")
    assert "EMP001" in mgr.subordinates

def test_remove_subordinate():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.add_subordinate("EMP001")
    mgr.remove_subordinate("EMP001")
    assert "EMP001" not in mgr.subordinates

def test_get_subordinates_count():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.add_subordinate("EMP001")
    mgr.add_subordinate("EMP002")
    assert mgr.get_subordinates_count() == 2

def test_set_budget_limit():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.set_budget_limit(50000.0)
    assert mgr.budget_limit == 50000.0

def test_approve_expense():
    mgr = Manager("MGR001", "Jane", "Smith", "jane@company.com", "2020-01-01", 95000.0, "DEP001", "senior")
    mgr.set_budget_limit(50000.0)
    assert mgr.approve_expense(30000.0) == True
    assert mgr.approve_expense(60000.0) == False