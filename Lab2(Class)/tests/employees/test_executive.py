import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.executive import Executive

def test_executive_initialization():
    executive = Executive("EXE001", "Grace", "Lee", "grace@company.com", "2015-01-01", 150000.0, "DEP001", "CTO", True, 10000)
    assert executive.employee_id == "EXE001"
    assert executive.executive_title == "CTO"

def test_make_strategic_decision():
    executive = Executive("EXE001", "Grace", "Lee", "grace@company.com", "2015-01-01", 150000.0, "DEP001", "CTO", True, 10000)
    executive.make_strategic_decision("New Product")
    assert executive.strategic_decisions == 1

def test_can_make_strategic_decisions():
    executive = Executive("EXE001", "Grace", "Lee", "grace@company.com", "2015-01-01", 150000.0, "DEP001", "CTO", True, 10000)
    assert executive.can_make_strategic_decisions() == True

def test_is_board_member():
    executive = Executive("EXE001", "Grace", "Lee", "grace@company.com", "2015-01-01", 150000.0, "DEP001", "CTO", True, 10000)
    assert executive.is_board_member() == True