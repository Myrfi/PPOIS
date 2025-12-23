import pytest
from src.exceptions import EmployeeAlreadyExistsException

class TestEmployeeAlreadyExistsException:
    def test_exception_creation(self):
        exception = EmployeeAlreadyExistsException("EMP001")
        assert exception.code == "EMP002"
        assert str(exception) == "EMP002: Employee with ID EMP001 already exists"

    def test_exception_inheritance(self):
        exception = EmployeeAlreadyExistsException("EMP002")
        assert isinstance(exception, Exception)

    def test_exception_attributes(self):
        exception = EmployeeAlreadyExistsException("EMP003")
        assert hasattr(exception, 'message')
        assert hasattr(exception, 'code')
