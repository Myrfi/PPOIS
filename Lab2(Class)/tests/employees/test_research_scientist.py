import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.research_scientist import ResearchScientist

def test_research_scientist_initialization():
    rs = ResearchScientist("RS001", "Dr", "Smith", "dr@company.com", "2016-01-01", 95000.0, "DEP001", "AI", 2010, 25)
    assert rs.employee_id == "RS001"
    assert rs.research_field == "AI"

def test_increment_publications():
    rs = ResearchScientist("RS001", "Dr", "Smith", "dr@company.com", "2016-01-01", 95000.0, "DEP001", "AI", 2010, 25)
    rs.increment_publications()
    assert rs.publications_count == 26

def test_increment_patents_filed():
    rs = ResearchScientist("RS001", "Dr", "Smith", "dr@company.com", "2016-01-01", 95000.0, "DEP001", "AI", 2010, 25)
    rs.increment_patents_filed()
    assert rs.patents_filed == 1

def test_increment_research_grants_secured():
    rs = ResearchScientist("RS001", "Dr", "Smith", "dr@company.com", "2016-01-01", 95000.0, "DEP001", "AI", 2010, 25)
    rs.increment_research_grants_secured()
    assert rs.research_grants_secured == 1