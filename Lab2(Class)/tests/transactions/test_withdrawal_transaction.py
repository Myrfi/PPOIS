import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.withdrawal_transaction import WithdrawalTransaction

def test_withdrawal_transaction_initialization():
    withdrawal = WithdrawalTransaction("TXN005", "ACC001", 500.0, "ATM withdrawal", "USER001", "atm", "cash")
    assert withdrawal.transaction_id == "TXN005"
    assert withdrawal.withdrawal_type == "atm"
    assert withdrawal.withdrawal_method == "cash"

def test_authorize_withdrawal():
    withdrawal = WithdrawalTransaction("TXN005", "ACC001", 500.0, "ATM withdrawal", "USER001", "atm", "cash")
    result = withdrawal.authorize_withdrawal()
    assert result == True
    assert withdrawal.status == "completed"

def test_set_atm_location():
    withdrawal = WithdrawalTransaction("TXN005", "ACC001", 500.0, "ATM withdrawal", "USER001", "atm", "cash")
    withdrawal.set_atm_location("Downtown Branch")
    assert withdrawal.atm_location == "Downtown Branch"

def test_get_atm_location():
    withdrawal = WithdrawalTransaction("TXN005", "ACC001", 500.0, "ATM withdrawal", "USER001", "atm", "cash")
    withdrawal.set_atm_location("Downtown Branch")
    assert withdrawal.get_atm_location() == "Downtown Branch"