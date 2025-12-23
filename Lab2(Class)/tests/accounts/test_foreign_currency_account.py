import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.foreign_currency_account import ForeignCurrencyAccount

def test_foreign_currency_account_initialization():
    fca = ForeignCurrencyAccount("ACC006", "Global Trader", "EUR", 25000.0, "London", "USD", 1.1)
    assert fca.account_id == "ACC006"
    assert fca.currency == "EUR"
    assert fca.base_currency == "USD"
    assert fca.exchange_rate == 1.1

def test_convert_to_base_currency():
    fca = ForeignCurrencyAccount("ACC006", "Global Trader", "EUR", 25000.0, "London", "USD", 1.1)
    converted = fca.convert_to_base_currency()
    assert abs(converted - 27500.0) < 0.01

def test_update_exchange_rate():
    fca = ForeignCurrencyAccount("ACC006", "Global Trader", "EUR", 25000.0, "London", "USD", 1.1)
    fca.update_exchange_rate(1.2)
    assert fca.exchange_rate == 1.2
    assert fca.converted_balance == 30000.0

def test_get_exchange_rate():
    fca = ForeignCurrencyAccount("ACC006", "Global Trader", "EUR", 25000.0, "London", "USD", 1.1)
    assert fca.get_exchange_rate() == 1.1