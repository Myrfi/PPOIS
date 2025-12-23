import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.it_department import ITDepartment

def test_it_department_initialization():
    it = ITDepartment("DEP003", "Information Technology", "HQ", "MGR003", 300000.0, 20)
    assert it.department_id == "DEP003"
    assert it.name == "Information Technology"

def test_deploy_system():
    it = ITDepartment("DEP003", "Information Technology", "HQ", "MGR003", 300000.0, 20)
    result = it.deploy_system("New CRM")
    assert result == True
    assert "New CRM" in it.systems_deployed

def test_report_security_incident():
    it = ITDepartment("DEP003", "Information Technology", "HQ", "MGR003", 300000.0, 20)
    it.report_security_incident()
    assert it.security_incidents == 1

def test_get_systems_count():
    it = ITDepartment("DEP003", "Information Technology", "HQ", "MGR003", 300000.0, 20)
    it.deploy_system("System 1")
    it.deploy_system("System 2")
    assert it.get_systems_count() == 2