import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.accountant import Accountant

def test_accountant_initialization():
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    assert accountant.employee_id == "ACC001"
    assert accountant.accounting_standards == ["GAAP"]

def test_add_accounting_standard():
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    accountant.add_accounting_standard("IFRS")
    assert "IFRS" in accountant.accounting_standards

def test_conduct_audit():
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    accountant.conduct_audit("internal")
    assert accountant.audits_conducted == 1

def test_prepare_financial_statement():
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    accountant.prepare_financial_statement("balance_sheet")
    assert accountant.financial_statements_prepared == 1

def test_is_cpa_certified():
    accountant = Accountant("ACC001", "Emma", "Taylor", "emma@company.com", "2019-03-01", 85000.0, "DEP001", ["GAAP"], True, 7)
    assert accountant.is_cpa_certified() == True