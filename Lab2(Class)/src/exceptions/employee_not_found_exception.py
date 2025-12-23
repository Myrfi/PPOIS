from .base_exception import TransnationalCompanyException

class EmployeeNotFoundException(TransnationalCompanyException):
    """Exception raised when employee is not found."""
    def __init__(self, employee_id: str):
        super().__init__(f"Employee with ID {employee_id} not found", "EMP001")

