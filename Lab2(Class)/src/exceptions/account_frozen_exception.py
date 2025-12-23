from .base_exception import TransnationalCompanyException

class AccountFrozenException(TransnationalCompanyException):
    """Exception raised when account is frozen."""
    def __init__(self, account_id: str):
        super().__init__(f"Account {account_id} is frozen and cannot be used", "ACC003")

