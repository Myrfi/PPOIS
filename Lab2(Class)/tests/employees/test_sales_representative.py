import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.sales_representative import SalesRepresentative

def test_sales_representative_initialization():
    sales = SalesRepresentative("SAL001", "David", "Brown", "david@company.com", "2022-01-15", 65000.0, "DEP001", "North America", 0.05, 0.0)
    assert sales.employee_id == "SAL001"
    assert sales.sales_region == "North America"

def test_record_sale():
    sales = SalesRepresentative("SAL001", "David", "Brown", "david@company.com", "2022-01-15", 65000.0, "DEP001", "North America", 0.05, 0.0)
    sales.record_sale(10000.0)
    assert sales.total_sales == 10000.0

def test_update_target_achievement():
    sales = SalesRepresentative("SAL001", "David", "Brown", "david@company.com", "2022-01-15", 65000.0, "DEP001", "North America", 0.05, 0.0)
    sales.update_target_achievement(0.85)
    assert sales.target_achievement == 0.85

def test_calculate_commission():
    sales = SalesRepresentative("SAL001", "David", "Brown", "david@company.com", "2022-01-15", 65000.0, "DEP001", "North America", 0.05, 10000.0)
    commission = sales.calculate_commission()
    assert commission == 500.0