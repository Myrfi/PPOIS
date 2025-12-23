import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.bonuses.bonus import Bonus

def test_bonus_initialization():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    assert bonus.bonus_id == "BON001"
    assert bonus.employee_id == "EMP001"
    assert bonus.bonus_type == "performance"
    assert bonus.base_amount == 5000.0
    assert bonus.status == "pending"

def test_approve_bonus():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.approve_bonus()
    assert bonus.status == "approved"

def test_pay_bonus():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.approve_bonus()
    bonus.pay_bonus("2023-12-01")
    assert bonus.status == "paid"

def test_cancel_bonus():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.cancel_bonus()
    assert bonus.status == "cancelled"

def test_apply_tax_withholding():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.apply_tax_withholding(0.25)
    assert bonus.net_amount == 3750.0

def test_is_paid():
    bonus = Bonus("BON001", "EMP001", "performance", 5000.0, "Performance bonus", "MGR001")
    bonus.approve_bonus()
    bonus.pay_bonus()
    assert bonus.is_paid() == True