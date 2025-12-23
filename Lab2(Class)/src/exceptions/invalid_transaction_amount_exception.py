from .base_exception import TransnationalCompanyException

class InvalidTransactionAmountException(TransnationalCompanyException):
    """Exception raised when transaction amount is invalid."""
    def __init__(self, amount: float):
        super().__init__(f"Invalid transaction amount: {amount}", "TXN002")

