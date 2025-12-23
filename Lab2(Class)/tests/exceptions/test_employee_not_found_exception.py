import pytest
from src.exceptions import EmployeeNotFoundException

class TestEmployeeNotFoundException:
    def test_exception_creation(self):
        exception = EmployeeNotFoundException("EMP001")
        assert exception.code == "EMP001"
        assert str(exception) == "EMP001: Employee with ID EMP001 not found"

    def test_exception_inheritance(self):
        exception = EmployeeNotFoundException("EMP002")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = EmployeeNotFoundException("EMP003")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
