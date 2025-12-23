from .transaction import Transaction

class TransferTransaction(Transaction):
    def __init__(self, transaction_id: str, from_account_id: str, to_account_id: str,
                 amount: float, description: str, initiated_by: str, transfer_type: str):
        super().__init__(transaction_id, from_account_id, amount, "transfer", description, initiated_by)
        self.to_account_id = to_account_id
        self.transfer_type = transfer_type
        self.exchange_rate = 1.0

    def execute_transfer(self) -> bool:
        self.approve_transaction("SYSTEM")
        return True

    def set_exchange_rate(self, rate: float) -> None:
        self.exchange_rate = rate

    def get_exchange_rate(self) -> float:
        return self.exchange_rate