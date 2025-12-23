import pytest
from src.exceptions import InvalidEmployeeStatusException

class TestInvalidEmployeeStatusException:
    def test_exception_creation(self):
        exception = InvalidEmployeeStatusException("EMP001", "invalid_status")
        assert exception.code == "EMP003"
        assert str(exception) == "EMP003: Invalid status 'invalid_status' for employee EMP001"

    def test_exception_inheritance(self):
        exception = InvalidEmployeeStatusException("EMP002", "terminated")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = InvalidEmployeeStatusException("EMP003", "suspended")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
