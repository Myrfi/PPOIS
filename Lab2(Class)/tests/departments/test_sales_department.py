import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.sales_department import SalesDepartment

def test_sales_department_initialization():
    sales = SalesDepartment("DEP006", "Sales", "HQ", "MGR006", 350000.0, 25)
    assert sales.department_id == "DEP006"
    assert sales.name == "Sales"

def test_set_sales_target():
    sales = SalesDepartment("DEP006", "Sales", "HQ", "MGR006", 350000.0, 25)
    result = sales.set_sales_target(1000000.0)
    assert result == True
    assert 1000000.0 in sales.sales_targets

def test_record_revenue():
    sales = SalesDepartment("DEP006", "Sales", "HQ", "MGR006", 350000.0, 25)
    sales.record_revenue(50000.0)
    assert sales.revenue_generated == 50000.0

def test_get_targets_count():
    sales = SalesDepartment("DEP006", "Sales", "HQ", "MGR006", 350000.0, 25)
    sales.set_sales_target(1000000.0)
    sales.set_sales_target(2000000.0)
    assert sales.get_targets_count() == 2