import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.analyst import Analyst

def test_analyst_initialization():
    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    assert analyst.employee_id == "ANA001"
    assert analyst.analysis_tools == ["Excel"]

def test_add_analysis_tool():
    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    analyst.add_analysis_tool("Tableau")
    assert "Tableau" in analyst.analysis_tools

def test_update_accuracy_rating():
    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    analyst.update_accuracy_rating(4.5)
    assert analyst.accuracy_rating == 4.5

def test_increment_reports_generated():
    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    analyst.increment_reports_generated()
    assert analyst.reports_generated == 1

def test_can_access_confidential_data():
    analyst = Analyst("ANA001", "Bob", "Wilson", "bob@company.com", "2021-05-01", 78000.0, "DEP001", ["Excel"], "financial", "medium")
    assert analyst.can_access_confidential_data() == True