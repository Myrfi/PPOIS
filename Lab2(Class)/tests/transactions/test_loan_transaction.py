import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.loan_transaction import LoanTransaction

def test_loan_transaction_initialization():
    loan = LoanTransaction("TXN007", "ACC010", 50000.0, "Business loan", "USER001", "business", 60, 0.08)
    assert loan.transaction_id == "TXN007"
    assert loan.loan_type == "business"
    assert loan.loan_term_months == 60
    assert loan.interest_rate == 0.08

def test_calculate_monthly_payment():
    loan = LoanTransaction("TXN007", "ACC010", 50000.0, "Business loan", "USER001", "business", 60, 0.08)
    payment = loan.calculate_monthly_payment()
    assert abs(payment - 833.33) < 0.01

def test_get_interest_rate():
    loan = LoanTransaction("TXN007", "ACC010", 50000.0, "Business loan", "USER001", "business", 60, 0.08)
    assert loan.get_interest_rate() == 0.08