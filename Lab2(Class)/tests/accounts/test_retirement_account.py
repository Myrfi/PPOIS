import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.retirement_account import RetirementAccount

def test_retirement_account_initialization():
    retirement = RetirementAccount("ACC007", "Retiree Smith", "USD", 100000.0, "Denver", 65, 45)
    assert retirement.account_id == "ACC007"
    assert retirement.retirement_age == 65
    assert retirement.current_age == 45
    assert retirement.years_until_retirement == 20

def test_calculate_retirement_readiness():
    retirement = RetirementAccount("ACC007", "Retiree Smith", "USD", 100000.0, "Denver", 65, 45)
    readiness = retirement.calculate_retirement_readiness()
    assert readiness == 5000.0

def test_update_current_age():
    retirement = RetirementAccount("ACC007", "Retiree Smith", "USD", 100000.0, "Denver", 65, 45)
    retirement.update_current_age(46)
    assert retirement.current_age == 46
    assert retirement.years_until_retirement == 19

def test_get_years_until_retirement():
    retirement = RetirementAccount("ACC007", "Retiree Smith", "USD", 100000.0, "Denver", 65, 45)
    assert retirement.get_years_until_retirement() == 20