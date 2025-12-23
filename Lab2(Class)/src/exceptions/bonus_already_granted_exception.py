from .base_exception import TransnationalCompanyException

class BonusAlreadyGrantedException(TransnationalCompanyException):
    """Exception raised when bonus is already granted to employee."""
    def __init__(self, employee_id: str, bonus_type: str):
        super().__init__(f"Bonus {bonus_type} already granted to employee {employee_id}", "BON002")

