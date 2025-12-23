import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.transactions.payment_transaction import PaymentTransaction

def test_payment_transaction_initialization():
    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    assert payment.transaction_id == "TXN002"
    assert payment.recipient_id == "REC001"
    assert payment.payment_method == "wire_transfer"

def test_process_payment():
    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    result = payment.process_payment()
    assert result == True
    assert payment.status == "completed"

def test_generate_receipt():
    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    payment.generate_receipt("RCP001")
    assert payment.receipt_number == "RCP001"

def test_get_receipt_number():
    payment = PaymentTransaction("TXN002", "ACC001", 500.0, "Payment for services", "USER001", "REC001", "wire_transfer")
    payment.generate_receipt("RCP001")
    assert payment.get_receipt_number() == "RCP001"