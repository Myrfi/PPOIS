import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.class_associations import demonstrate_associations

def test_class_associations():
    """Test that class associations work correctly."""
    associations = demonstrate_associations()

    # Test manager-employee association
    assert associations["employee"].manager_id == associations["manager"].employee_id

    # Test department-employee association
    assert associations["employee"].department_id == associations["department"].department_id

    # Test department-manager association
    assert associations["department"].manager_id == associations["manager"].employee_id

    # Test transaction-account association
    assert associations["transaction"].account_id == associations["account"].account_id

    # Test bonus-employee association
    assert associations["bonus"].employee_id == associations["employee"].employee_id

    # Test bonus-manager association
    assert associations["bonus"].granted_by == associations["manager"].employee_id

