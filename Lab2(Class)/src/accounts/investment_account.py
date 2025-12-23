from .bank_account import BankAccount

class InvestmentAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, investment_type: str,
                 risk_tolerance: str):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "investment", branch_location)
        self.investment_type = investment_type
        self.risk_tolerance = risk_tolerance
        self.portfolio = {}
        self.returns_percentage = 0.0

    def add_investment(self, symbol: str, amount: float) -> None:
        self.portfolio[symbol] = amount

    def remove_investment(self, symbol: str) -> None:
        if symbol in self.portfolio:
            del self.portfolio[symbol]

    def update_returns_percentage(self, percentage: float) -> None:
        self.returns_percentage = percentage

    def get_portfolio_value(self) -> float:
        return sum(self.portfolio.values())

