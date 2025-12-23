import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.it_administrator import ITAdministrator

def test_it_administrator_initialization():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    assert it_admin.employee_id == "ITA001"
    assert it_admin.technical_certifications == ["CCNA"]

def test_add_technical_certification():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    it_admin.add_technical_certification("AWS")
    assert "AWS" in it_admin.technical_certifications

def test_add_system_administered():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    it_admin.add_system_administered("Linux")
    assert "Linux" in it_admin.systems_administered

def test_increment_incidents_resolved():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    it_admin.increment_incidents_resolved()
    assert it_admin.incidents_resolved == 1

def test_update_uptime_maintained():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    it_admin.update_uptime_maintained(99.5)
    assert it_admin.uptime_maintained == 99.5

def test_can_access_critical_systems():
    it_admin = ITAdministrator("ITA001", "Alex", "Chen", "alex@company.com", "2020-06-01", 75000.0, "DEP001", ["CCNA"], ["Windows"], "elevated")
    assert it_admin.can_access_critical_systems() == True