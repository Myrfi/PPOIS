import pytest
from src.exceptions import InvalidTransactionAmountException

class TestInvalidTransactionAmountException:
    def test_exception_creation(self):
        exception = InvalidTransactionAmountException(1000.0)
        assert exception.code == "TXN002"
        assert str(exception) == "TXN002: Invalid transaction amount: 1000.0"

    def test_exception_inheritance(self):
        exception = InvalidTransactionAmountException(500.0)
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = InvalidTransactionAmountException(2000.0)
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
