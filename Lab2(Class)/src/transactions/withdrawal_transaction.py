from .transaction import Transaction

class WithdrawalTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, withdrawal_type: str,
                 withdrawal_method: str):
        super().__init__(transaction_id, account_id, amount, "withdrawal", description, initiated_by)
        self.withdrawal_type = withdrawal_type
        self.withdrawal_method = withdrawal_method
        self.atm_location = ""

    def authorize_withdrawal(self) -> bool:
        self.approve_transaction("SYSTEM")
        return True

    def set_atm_location(self, location: str) -> None:
        self.atm_location = location

    def get_atm_location(self) -> str:
        return self.atm_location