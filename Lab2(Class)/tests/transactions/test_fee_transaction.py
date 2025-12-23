import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.fee_transaction import FeeTransaction

def test_fee_transaction_initialization():
    fee = FeeTransaction("TXN008", "ACC001", 25.0, "Monthly maintenance fee", "SYSTEM", "maintenance", "monthly")
    assert fee.transaction_id == "TXN008"
    assert fee.fee_type == "maintenance"
    assert fee.fee_category == "monthly"

def test_apply_fee():
    fee = FeeTransaction("TXN008", "ACC001", 25.0, "Monthly maintenance fee", "SYSTEM", "maintenance", "monthly")
    result = fee.apply_fee()
    assert result == True
    assert fee.status == "completed"

def test_get_fee_category():
    fee = FeeTransaction("TXN008", "ACC001", 25.0, "Monthly maintenance fee", "SYSTEM", "maintenance", "monthly")
    assert fee.get_fee_category() == "monthly"