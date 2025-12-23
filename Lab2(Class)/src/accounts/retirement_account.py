from .bank_account import BankAccount

class RetirementAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, retirement_age: int,
                 current_age: int):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "retirement", branch_location)
        self.retirement_age = retirement_age
        self.current_age = current_age
        self.years_until_retirement = retirement_age - current_age

    def calculate_retirement_readiness(self) -> float:
        return self.balance / (self.retirement_age - self.current_age)

    def update_current_age(self, new_age: int) -> None:
        self.current_age = new_age
        self.years_until_retirement = self.retirement_age - new_age

    def get_years_until_retirement(self) -> int:
        return self.years_until_retirement

