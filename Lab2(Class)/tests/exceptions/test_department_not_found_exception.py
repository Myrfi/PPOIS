import pytest
from src.exceptions import DepartmentNotFoundException

class TestDepartmentNotFoundException:
    def test_exception_creation(self):
        exception = DepartmentNotFoundException("DEP001")
        assert exception.code == "DEP001"
        assert str(exception) == "DEP001: Department with ID DEP001 not found"

    def test_exception_inheritance(self):
        exception = DepartmentNotFoundException("DEP002")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = DepartmentNotFoundException("DEP003")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
