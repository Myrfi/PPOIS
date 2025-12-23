import pytest
from src.exceptions import AccountNotFoundException

class TestAccountNotFoundException:
    def test_exception_creation(self):
        exception = AccountNotFoundException("ACC001")
        assert exception.code == "ACC002"
        assert str(exception) == "ACC002: Account with ID ACC001 not found"

    def test_exception_inheritance(self):
        exception = AccountNotFoundException("ACC002")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = AccountNotFoundException("ACC003")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
