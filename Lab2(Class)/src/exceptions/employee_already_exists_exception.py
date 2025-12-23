from .base_exception import TransnationalCompanyException

class EmployeeAlreadyExistsException(TransnationalCompanyException):
    """Exception raised when trying to create employee that already exists."""
    def __init__(self, employee_id: str):
        super().__init__(f"Employee with ID {employee_id} already exists", "EMP002")

