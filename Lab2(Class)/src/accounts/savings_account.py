from .bank_account import BankAccount

class SavingsAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, interest_rate: float,
                 minimum_balance: float):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "savings", branch_location)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.withdrawals_this_month = 0

    def calculate_interest(self) -> float:
        return self.balance * (self.interest_rate / 12)

    def apply_interest(self) -> None:
        interest = self.calculate_interest()
        self.balance += interest

    def reset_monthly_withdrawals(self) -> None:
        self.withdrawals_this_month = 0

    def is_minimum_balance_maintained(self) -> bool:
        return self.balance >= self.minimum_balance

