import pytest
from src.exceptions import BonusNotEligibleException

class TestBonusNotEligibleException:
    def test_exception_creation(self):
        exception = BonusNotEligibleException("EMP001", "performance")
        assert exception.code == "BON001"
        assert str(exception) == "BON001: Employee EMP001 is not eligible for performance bonus"

    def test_exception_inheritance(self):
        exception = BonusNotEligibleException("EMP002", "referral")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = BonusNotEligibleException("EMP003", "signing")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
