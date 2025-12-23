import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.exceptions.base_exception import TransnationalCompanyException

def test_exception_initialization_default_code():
    exc = TransnationalCompanyException("Test error")
    assert exc.message == "Test error"
    assert exc.code == "GENERAL_ERROR"

def test_exception_initialization_custom_code():
    exc = TransnationalCompanyException("Custom error", "CUSTOM_ERROR")
    assert exc.message == "Custom error"
    assert exc.code == "CUSTOM_ERROR"

def test_exception_str_representation():
    exc = TransnationalCompanyException("Test error", "TEST_ERROR")
    assert str(exc) == "TEST_ERROR: Test error"

def test_exception_inheritance():
    exc = TransnationalCompanyException("Test error")
    assert isinstance(exc, Exception)