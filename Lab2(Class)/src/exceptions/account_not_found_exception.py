from .base_exception import TransnationalCompanyException

class AccountNotFoundException(TransnationalCompanyException):
    """Exception raised when account is not found."""
    def __init__(self, account_id: str):
        super().__init__(f"Account with ID {account_id} not found", "ACC002")

