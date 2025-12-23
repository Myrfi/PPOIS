from .bank_account import BankAccount

class BusinessAccount(BankAccount):
    def __init__(self, account_id: str, account_holder: str, currency: str,
                 opening_balance: float, branch_location: str, business_type: str,
                 tax_id: str):
        super().__init__(account_id, account_holder, currency, opening_balance,
                        "business", branch_location)
        self.business_type = business_type
        self.tax_id = tax_id
        self.authorized_signers = []
        self.monthly_transaction_volume = 0

    def add_authorized_signer(self, signer_name: str) -> None:
        self.authorized_signers.append(signer_name)

    def remove_authorized_signer(self, signer_name: str) -> None:
        if signer_name in self.authorized_signers:
            self.authorized_signers.remove(signer_name)

    def update_monthly_transaction_volume(self, volume: int) -> None:
        self.monthly_transaction_volume = volume

    def get_authorized_signers_count(self) -> int:
        return len(self.authorized_signers)