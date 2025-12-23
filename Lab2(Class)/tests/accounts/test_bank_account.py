import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.bank_account import BankAccount

def test_bank_account_initialization():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    assert account.account_id == "ACC001"
    assert account.account_holder == "John Doe"
    assert account.balance == 1000.0
    assert account.account_type == "checking"
    assert account.is_active == True

def test_deposit():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    result = account.deposit(500.0)
    assert result == True
    assert account.balance == 1500.0
    assert len(account.transactions) == 1

def test_withdraw():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    result = account.withdraw(300.0)
    assert result == True
    assert account.balance == 700.0
    assert len(account.transactions) == 1

def test_get_balance():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    assert account.get_balance() == 1000.0

def test_get_transaction_history():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    account.deposit(500.0)
    history = account.get_transaction_history()
    assert len(history) == 1
    assert history[0]['type'] == 'deposit'

def test_close_account():
    account = BankAccount("ACC001", "John Doe", "USD", 1000.0, "checking", "New York")
    account.close_account()
    assert account.is_active == False