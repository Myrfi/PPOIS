from .bonus import Bonus

class ReferralBonus(Bonus):
    def __init__(self, bonus_id: str, employee_id: str, base_amount: float,
                 description: str, granted_by: str, referred_employee_id: str,
                 referral_date: str):
        super().__init__(bonus_id, employee_id, "referral", base_amount, description, granted_by)
        self.referred_employee_id = referred_employee_id
        self.referral_date = referral_date

    def calculate_referral_bonus(self) -> float:
        return self.base_amount * 1.1

    def get_referred_employee_id(self) -> str:
        return self.referred_employee_id

