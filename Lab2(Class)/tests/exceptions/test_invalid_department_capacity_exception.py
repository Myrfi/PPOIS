import pytest
from src.exceptions import InvalidDepartmentCapacityException

class TestInvalidDepartmentCapacityException:
    def test_exception_creation(self):
        exception = InvalidDepartmentCapacityException("DEP001", 100)
        assert exception.code == "DEP002"
        assert str(exception) == "DEP002: Invalid capacity 100 for department DEP001"

    def test_exception_inheritance(self):
        exception = InvalidDepartmentCapacityException("DEP002", 50)
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = InvalidDepartmentCapacityException("DEP003", 200)
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
