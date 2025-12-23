from .base_exception import TransnationalCompanyException

class InvalidEmployeeStatusException(TransnationalCompanyException):
    """Exception raised when employee status is invalid."""
    def __init__(self, employee_id: str, status: str):
        super().__init__(f"Invalid status '{status}' for employee {employee_id}", "EMP003")

