import pytest
from src.exceptions import AccountFrozenException

class TestAccountFrozenException:
    def test_exception_creation(self):
        exception = AccountFrozenException("ACC001")
        assert exception.code == "ACC003"
        assert str(exception) == "ACC003: Account ACC001 is frozen and cannot be used"

    def test_exception_inheritance(self):
        exception = AccountFrozenException("ACC002")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = AccountFrozenException("ACC003")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
