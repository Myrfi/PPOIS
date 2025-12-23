import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.finance_department import FinanceDepartment

def test_finance_department_initialization():
    finance = FinanceDepartment("DEP004", "Finance", "HQ", "MGR004", 400000.0, 12)
    assert finance.department_id == "DEP004"
    assert finance.name == "Finance"

def test_generate_financial_report():
    finance = FinanceDepartment("DEP004", "Finance", "HQ", "MGR004", 400000.0, 12)
    report = finance.generate_financial_report("Q4")
    assert report["type"] == "Q4"
    assert report["date"] == "2024-01-01"

def test_complete_audit():
    finance = FinanceDepartment("DEP004", "Finance", "HQ", "MGR004", 400000.0, 12)
    finance.complete_audit()
    assert finance.audits_completed == 1

def test_get_reports_count():
    finance = FinanceDepartment("DEP004", "Finance", "HQ", "MGR004", 400000.0, 12)
    finance.generate_financial_report("Q1")
    finance.generate_financial_report("Q2")
    assert finance.get_reports_count() == 2