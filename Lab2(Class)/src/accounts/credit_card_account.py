from .bank_account import BankAccount

class CreditCardAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, credit_limit: float,
                 apr: float):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "credit_card", branch_location)
        self.credit_limit = credit_limit
        self.apr = apr
        self.available_credit = credit_limit - opening_balance

    def make_purchase(self, amount: float) -> bool:
        if amount <= self.available_credit:
            self.balance += amount
            self.available_credit -= amount
            return True
        return False

    def make_payment(self, amount: float) -> None:
        self.balance -= amount
        self.available_credit += amount

    def get_available_credit(self) -> float:
        return self.available_credit

