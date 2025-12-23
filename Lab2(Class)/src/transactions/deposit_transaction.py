from .transaction import Transaction

class DepositTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, deposit_type: str,
                 deposit_method: str):
        super().__init__(transaction_id, account_id, amount, "deposit", description, initiated_by)
        self.deposit_type = deposit_type
        self.deposit_method = deposit_method
        self.clearing_date = ""

    def verify_deposit(self) -> bool:
        self.approve_transaction("SYSTEM")
        return True

    def set_clearing_date(self, date: str) -> None:
        self.clearing_date = date

    def get_clearing_date(self) -> str:
        return self.clearing_date

