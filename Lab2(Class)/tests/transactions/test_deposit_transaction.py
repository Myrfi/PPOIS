import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.deposit_transaction import DepositTransaction

def test_deposit_transaction_initialization():
    deposit = DepositTransaction("TXN004", "ACC001", 2000.0, "Cash deposit", "USER001", "cash", "branch")
    assert deposit.transaction_id == "TXN004"
    assert deposit.deposit_type == "cash"
    assert deposit.deposit_method == "branch"

def test_verify_deposit():
    deposit = DepositTransaction("TXN004", "ACC001", 2000.0, "Cash deposit", "USER001", "cash", "branch")
    result = deposit.verify_deposit()
    assert result == True
    assert deposit.status == "completed"

def test_set_clearing_date():
    deposit = DepositTransaction("TXN004", "ACC001", 2000.0, "Cash deposit", "USER001", "cash", "branch")
    deposit.set_clearing_date("2024-01-02")
    assert deposit.clearing_date == "2024-01-02"

def test_get_clearing_date():
    deposit = DepositTransaction("TXN004", "ACC001", 2000.0, "Cash deposit", "USER001", "cash", "branch")
    deposit.set_clearing_date("2024-01-02")
    assert deposit.get_clearing_date() == "2024-01-02"