from .base_exception import TransnationalCompanyException

class BonusNotEligibleException(TransnationalCompanyException):
    """Exception raised when employee is not eligible for bonus."""
    def __init__(self, employee_id: str, bonus_type: str):
        super().__init__(f"Employee {employee_id} is not eligible for {bonus_type} bonus", "BON001")

