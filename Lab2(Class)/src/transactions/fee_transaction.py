from .transaction import Transaction

class FeeTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, fee_type: str,
                 fee_category: str):
        super().__init__(transaction_id, account_id, amount, "fee", description, initiated_by)
        self.fee_type = fee_type
        self.fee_category = fee_category

    def apply_fee(self) -> bool:
        self.approve_transaction("SYSTEM")
        return True

    def get_fee_category(self) -> str:
        return self.fee_category

