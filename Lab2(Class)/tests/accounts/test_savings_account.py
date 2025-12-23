import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.savings_account import SavingsAccount

def test_savings_account_initialization():
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    assert savings.account_id == "ACC002"
    assert savings.interest_rate == 0.025
    assert savings.minimum_balance == 500.0
    assert savings.withdrawals_this_month == 0

def test_calculate_interest():
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    interest = savings.calculate_interest()
    assert interest > 0

def test_apply_interest():
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    savings.apply_interest()
    assert savings.balance > 2000.0

def test_reset_monthly_withdrawals():
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    savings.withdrawals_this_month = 3
    savings.reset_monthly_withdrawals()
    assert savings.withdrawals_this_month == 0

def test_is_minimum_balance_maintained():
    savings = SavingsAccount("ACC002", "Jane Doe", "USD", 2000.0, "New York", 0.025, 500.0)
    assert savings.is_minimum_balance_maintained() == True