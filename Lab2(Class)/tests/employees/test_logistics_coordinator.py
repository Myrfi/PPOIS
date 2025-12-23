import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.employees.logistics_coordinator import LogisticsCoordinator

def test_logistics_coordinator_initialization():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    assert logistics.employee_id == "LOG001"
    assert logistics.transportation_modes == ["road"]

def test_add_transportation_mode():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    logistics.add_transportation_mode("sea")
    assert "sea" in logistics.transportation_modes

def test_increment_shipments_coordinated():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    logistics.increment_shipments_coordinated()
    assert logistics.shipments_coordinated == 1

def test_update_on_time_delivery_rate():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    logistics.update_on_time_delivery_rate(95.5)
    assert logistics.on_time_delivery_rate == 95.5

def test_can_handle_international_logistics():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    assert logistics.can_handle_international_logistics() == True

def test_can_handle_hazardous_materials():
    logistics = LogisticsCoordinator("LOG001", "Mike", "Davis", "mike@company.com", "2019-07-01", 65000.0, "DEP001", ["road"], 5, True)
    assert logistics.can_handle_hazardous_materials() == True