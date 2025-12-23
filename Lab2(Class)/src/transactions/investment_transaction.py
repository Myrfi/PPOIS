from .transaction import Transaction

class InvestmentTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, investment_type: str,
                 security_symbol: str, quantity: int):
        super().__init__(transaction_id, account_id, amount, "investment", description, initiated_by)
        self.investment_type = investment_type
        self.security_symbol = security_symbol
        self.quantity = quantity
        self.price_per_share = amount / quantity

    def calculate_return(self) -> float:
        return self.amount * 0.05

    def get_price_per_share(self) -> float:
        return self.price_per_share

