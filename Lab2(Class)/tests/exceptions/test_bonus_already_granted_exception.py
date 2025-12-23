import pytest
from src.exceptions import BonusAlreadyGrantedException

class TestBonusAlreadyGrantedException:
    def test_exception_creation(self):
        exception = BonusAlreadyGrantedException("EMP001", "performance")
        assert exception.code == "BON002"
        assert str(exception) == "BON002: Bonus performance already granted to employee EMP001"

    def test_exception_inheritance(self):
        exception = BonusAlreadyGrantedException("EMP002", "referral")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = BonusAlreadyGrantedException("EMP003", "signing")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
