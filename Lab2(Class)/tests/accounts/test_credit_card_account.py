import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.credit_card_account import CreditCardAccount

def test_credit_card_account_initialization():
    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 0.0, "Miami", 5000.0, 0.15)
    assert credit.account_id == "ACC008"
    assert credit.credit_limit == 5000.0
    assert credit.apr == 0.15
    assert credit.available_credit == 5000.0

def test_make_purchase():
    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 0.0, "Miami", 5000.0, 0.15)
    result = credit.make_purchase(1000.0)
    assert result == True
    assert credit.balance == 1000.0
    assert credit.available_credit == 4000.0

def test_make_purchase_over_limit():
    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 0.0, "Miami", 5000.0, 0.15)
    result = credit.make_purchase(6000.0)
    assert result == False
    assert credit.balance == 0.0
    assert credit.available_credit == 5000.0

def test_make_payment():
    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 1000.0, "Miami", 5000.0, 0.15)
    credit.make_payment(500.0)
    assert credit.balance == 500.0
    assert credit.available_credit == 4500.0

def test_get_available_credit():
    credit = CreditCardAccount("ACC008", "Card Holder", "USD", 1000.0, "Miami", 5000.0, 0.15)
    assert credit.get_available_credit() == 4000.0