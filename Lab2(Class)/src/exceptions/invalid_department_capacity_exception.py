from .base_exception import TransnationalCompanyException

class InvalidDepartmentCapacityException(TransnationalCompanyException):
    """Exception raised when department capacity is invalid."""
    def __init__(self, department_id: str, capacity: int):
        super().__init__(f"Invalid capacity {capacity} for department {department_id}", "DEP002")

