import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.legal_counsel import LegalCounsel

def test_legal_counsel_initialization():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    assert legal.employee_id == "LEG001"
    assert legal.jurisdictions == ["USA"]

def test_add_jurisdiction():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    legal.add_jurisdiction("EU")
    assert "EU" in legal.jurisdictions

def test_add_practice_area():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    legal.add_practice_area("employment")
    assert "employment" in legal.practice_areas

def test_increment_cases_handled():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    legal.increment_cases_handled()
    assert legal.cases_handled == 1

def test_update_success_rate():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    legal.update_success_rate(0.85)
    assert legal.success_rate == 0.85

def test_get_years_of_practice():
    legal = LegalCounsel("LEG001", "Sarah", "Johnson", "sarah@company.com", "2018-03-01", 95000.0, "DEP001", ["USA"], 2015, ["corporate"])
    years = legal.get_years_of_practice()
    assert years >= 0