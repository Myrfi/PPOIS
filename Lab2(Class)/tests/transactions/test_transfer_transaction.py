import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.transfer_transaction import TransferTransaction

def test_transfer_transaction_initialization():
    transfer = TransferTransaction("TXN003", "ACC001", "ACC002", 1000.0, "Transfer between accounts", "USER001", "internal")
    assert transfer.transaction_id == "TXN003"
    assert transfer.to_account_id == "ACC002"
    assert transfer.transfer_type == "internal"

def test_execute_transfer():
    transfer = TransferTransaction("TXN003", "ACC001", "ACC002", 1000.0, "Transfer between accounts", "USER001", "internal")
    result = transfer.execute_transfer()
    assert result == True
    assert transfer.status == "completed"

def test_set_exchange_rate():
    transfer = TransferTransaction("TXN003", "ACC001", "ACC002", 1000.0, "Transfer between accounts", "USER001", "internal")
    transfer.set_exchange_rate(1.2)
    assert transfer.exchange_rate == 1.2

def test_get_exchange_rate():
    transfer = TransferTransaction("TXN003", "ACC001", "ACC002", 1000.0, "Transfer between accounts", "USER001", "internal")
    assert transfer.get_exchange_rate() == 1.0