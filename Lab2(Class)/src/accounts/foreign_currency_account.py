from .bank_account import BankAccount

class ForeignCurrencyAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, base_currency: str,
                 exchange_rate: float):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "foreign_currency", branch_location)
        self.base_currency = base_currency
        self.exchange_rate = exchange_rate
        self.converted_balance = opening_balance * exchange_rate

    def convert_to_base_currency(self) -> float:
        return self.balance * self.exchange_rate

    def update_exchange_rate(self, new_rate: float) -> None:
        self.exchange_rate = new_rate
        self.converted_balance = self.balance * new_rate

    def get_exchange_rate(self) -> float:
        return self.exchange_rate

