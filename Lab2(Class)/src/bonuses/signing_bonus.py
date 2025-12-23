from .bonus import Bonus

class SigningBonus(Bonus):
    def __init__(self, bonus_id: str, employee_id: str, base_amount: float,
                 description: str, granted_by: str, contract_term_years: int,
                 payment_schedule: str):
        super().__init__(bonus_id, employee_id, "signing", base_amount, description, granted_by)
        self.contract_term_years = contract_term_years
        self.payment_schedule = payment_schedule

    def calculate_signing_bonus_value(self) -> float:
        return self.base_amount / self.contract_term_years

    def get_contract_term_years(self) -> int:
        return self.contract_term_years

