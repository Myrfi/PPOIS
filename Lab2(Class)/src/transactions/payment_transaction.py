from .transaction import Transaction

class PaymentTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, recipient_id: str, payment_method: str):
        super().__init__(transaction_id, account_id, amount, "payment", description, initiated_by)
        self.recipient_id = recipient_id
        self.payment_method = payment_method
        self.receipt_number = ""

    def process_payment(self) -> bool:
        self.approve_transaction("SYSTEM")
        return True

    def generate_receipt(self, receipt_num: str) -> None:
        self.receipt_number = receipt_num

    def get_receipt_number(self) -> str:
        return self.receipt_number