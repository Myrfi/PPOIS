import pytest
from src.exceptions import TransactionFailedException

class TestTransactionFailedException:
    def test_exception_creation(self):
        exception = TransactionFailedException("TXN001", "Network error")
        assert exception.code == "TXN001"
        assert str(exception) == "TXN001: Transaction TXN001 failed: Network error"

    def test_exception_inheritance(self):
        exception = TransactionFailedException("TXN002", "Timeout")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = TransactionFailedException("TXN003", "Invalid data")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
