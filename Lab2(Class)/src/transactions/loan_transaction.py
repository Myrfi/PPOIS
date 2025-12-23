from .transaction import Transaction

class LoanTransaction(Transaction):
    def __init__(self, transaction_id: str, account_id: str, amount: float,
                 description: str, initiated_by: str, loan_type: str,
                 loan_term_months: int, interest_rate: float):
        super().__init__(transaction_id, account_id, amount, "loan", description, initiated_by)
        self.loan_type = loan_type
        self.loan_term_months = loan_term_months
        self.interest_rate = interest_rate

    def calculate_monthly_payment(self) -> float:
        return self.amount / self.loan_term_months

    def get_interest_rate(self) -> float:
        return self.interest_rate

