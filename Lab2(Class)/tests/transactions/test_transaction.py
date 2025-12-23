import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.transaction import Transaction

def test_transaction_initialization():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    assert txn.transaction_id == "TXN001"
    assert txn.account_id == "ACC001"
    assert txn.amount == 1000.0
    assert txn.transaction_type == "deposit"
    assert txn.status == "pending"

def test_approve_transaction():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.approve_transaction("APPROVER001")
    assert txn.status == "completed"

def test_cancel_transaction():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.cancel_transaction()
    assert txn.status == "cancelled"

def test_add_fee():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.add_fee(5.0)
    assert txn.fees == 5.0

def test_get_total_amount():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.add_fee(5.0)
    assert txn.get_total_amount() == 1005.0

def test_is_completed():
    txn = Transaction("TXN001", "ACC001", 1000.0, "deposit", "Test transaction", "USER001")
    txn.approve_transaction("APPROVER001")
    assert txn.is_completed() == True