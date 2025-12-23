import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.checking_account import CheckingAccount

def test_checking_account_initialization():
    checking = CheckingAccount("ACC003", "Alice Smith", "USD", 1500.0, "Boston", 500.0, 2.50)
    assert checking.account_id == "ACC003"
    assert checking.overdraft_limit == 500.0
    assert checking.atm_fee == 2.50

def test_write_check():
    checking = CheckingAccount("ACC003", "Alice Smith", "USD", 1500.0, "Boston", 500.0, 2.50)
    result = checking.write_check(100.0)
    assert result == True
    assert checking.balance == 1400.0
    assert checking.checks_written == 1

def test_use_atm():
    checking = CheckingAccount("ACC003", "Alice Smith", "USD", 1500.0, "Boston", 500.0, 2.50)
    checking.use_atm(100.0)
    assert checking.balance == 1400.0
    assert checking.atm_transactions == 1

def test_get_atm_fee():
    checking = CheckingAccount("ACC003", "Alice Smith", "USD", 1500.0, "Boston", 500.0, 2.50)
    assert checking.get_atm_fee() == 2.50