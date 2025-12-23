import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.investment_transaction import InvestmentTransaction

def test_investment_transaction_initialization():
    investment = InvestmentTransaction("TXN006", "ACC005", 10000.0, "Stock investment", "USER001", "buy", "AAPL", 100)
    assert investment.transaction_id == "TXN006"
    assert investment.investment_type == "buy"
    assert investment.security_symbol == "AAPL"
    assert investment.quantity == 100
    assert investment.price_per_share == 100.0

def test_calculate_return():
    investment = InvestmentTransaction("TXN006", "ACC005", 10000.0, "Stock investment", "USER001", "buy", "AAPL", 100)
    returns = investment.calculate_return()
    assert returns == 500.0

def test_get_price_per_share():
    investment = InvestmentTransaction("TXN006", "ACC005", 10000.0, "Stock investment", "USER001", "buy", "AAPL", 100)
    assert investment.get_price_per_share() == 100.0