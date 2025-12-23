from .base_exception import TransnationalCompanyException

class DepartmentNotFoundException(TransnationalCompanyException):
    """Exception raised when department is not found."""
    def __init__(self, department_id: str):
        super().__init__(f"Department with ID {department_id} not found", "DEP001")

