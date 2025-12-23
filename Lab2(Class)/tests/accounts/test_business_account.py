import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.accounts.business_account import BusinessAccount

def test_business_account_initialization():
    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    assert business.account_id == "ACC004"
    assert business.business_type == "LLC"
    assert business.tax_id == "123456789"

def test_add_authorized_signer():
    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    business.add_authorized_signer("John Doe")
    assert "John Doe" in business.authorized_signers

def test_remove_authorized_signer():
    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    business.add_authorized_signer("John Doe")
    business.remove_authorized_signer("John Doe")
    assert "John Doe" not in business.authorized_signers

def test_update_monthly_transaction_volume():
    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    business.update_monthly_transaction_volume(100)
    assert business.monthly_transaction_volume == 100

def test_get_authorized_signers_count():
    business = BusinessAccount("ACC004", "ABC Corp", "USD", 10000.0, "Chicago", "LLC", "123456789")
    business.add_authorized_signer("John Doe")
    business.add_authorized_signer("Jane Smith")
    assert business.get_authorized_signers_count() == 2