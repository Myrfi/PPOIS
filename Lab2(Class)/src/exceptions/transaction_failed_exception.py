from .base_exception import TransnationalCompanyException

class TransactionFailedException(TransnationalCompanyException):
    """Exception raised when transaction fails."""
    def __init__(self, transaction_id: str, reason: str):
        super().__init__(f"Transaction {transaction_id} failed: {reason}", "TXN001")

