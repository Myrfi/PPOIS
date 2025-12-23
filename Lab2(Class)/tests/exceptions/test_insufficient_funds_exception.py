import pytest
from src.exceptions import InsufficientFundsException

class TestInsufficientFundsException:
    def test_exception_creation(self):
        exception = InsufficientFundsException("ACC001", 1000.0, 500.0)
        assert exception.code == "ACC001"
        assert str(exception) == "ACC001: Insufficient funds in account ACC001. Required: 1000.0, Available: 500.0"

    def test_exception_inheritance(self):
        exception = InsufficientFundsException("ACC002", 2000.0, 1000.0)
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = InsufficientFundsException("ACC003", 500.0, 200.0)
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
