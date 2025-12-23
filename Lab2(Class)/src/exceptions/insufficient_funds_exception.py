from .base_exception import TransnationalCompanyException

class InsufficientFundsException(TransnationalCompanyException):
    """Exception raised when account has insufficient funds."""
    def __init__(self, account_id: str, required: float, available: float):
        super().__init__(
            f"Insufficient funds in account {account_id}. Required: {required}, Available: {available}",
            "ACC001"
        )

