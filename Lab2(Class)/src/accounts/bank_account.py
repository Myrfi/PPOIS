class BankAccount:
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, account_type: str, branch_location: str):
        self.account_id = account_id
        self.account_holder = account_holder
        self.currency = currency
        self.balance = opening_balance
        self.account_type = account_type
        self.branch_location = branch_location
        self.is_active = True
        self.transactions = []

    def deposit(self, amount: float) -> bool:
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})
        return True

    def withdraw(self, amount: float) -> bool:
        self.balance -= amount
        self.transactions.append({'type': 'withdrawal', 'amount': amount})
        return True

    def get_balance(self) -> float:
        return self.balance

    def get_transaction_history(self) -> list:
        return self.transactions.copy()

    def close_account(self) -> None:
        self.is_active = False

