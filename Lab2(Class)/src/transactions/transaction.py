class Transaction:
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 transaction_type: str, description: str, initiated_by: str):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.initiated_by = initiated_by
        self.status = "pending"
        self.fees = 0.0

    def approve_transaction(self, approver_id: str) -> None:
        self.status = "completed"

    def cancel_transaction(self) -> None:
        self.status = "cancelled"

    def add_fee(self, fee_amount: float) -> None:
        self.fees += fee_amount

    def get_total_amount(self) -> float:
        return self.amount + self.fees

    def is_completed(self) -> bool:
        return self.status == "completed"

