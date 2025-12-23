import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.investment_account import InvestmentAccount

def test_investment_account_initialization():
    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    assert investment.account_id == "ACC005"
    assert investment.investment_type == "stocks"
    assert investment.risk_tolerance == "moderate"

def test_add_investment():
    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    investment.add_investment("AAPL", 1000.0)
    assert "AAPL" in investment.portfolio

def test_remove_investment():
    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    investment.add_investment("AAPL", 1000.0)
    investment.remove_investment("AAPL")
    assert "AAPL" not in investment.portfolio

def test_update_returns_percentage():
    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    investment.update_returns_percentage(10.5)
    assert investment.returns_percentage == 10.5

def test_get_portfolio_value():
    investment = InvestmentAccount("ACC005", "Bob Investor", "USD", 50000.0, "San Francisco", "stocks", "moderate")
    investment.add_investment("AAPL", 1000.0)
    investment.add_investment("GOOGL", 2000.0)
    assert investment.get_portfolio_value() == 3000.0