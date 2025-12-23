from .bank_account import BankAccount

class CheckingAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, overdraft_limit: float,
                 atm_fee: float):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "checking", branch_location)
        self.overdraft_limit = overdraft_limit
        self.atm_fee = atm_fee
        self.checks_written = 0
        self.atm_transactions = 0

    def write_check(self, amount: float) -> bool:
        self.balance -= amount
        self.checks_written += 1
        return True

    def use_atm(self, amount: float) -> None:
        self.balance -= amount
        self.atm_transactions += 1

    def get_atm_fee(self) -> float:
        return self.atm_fee

