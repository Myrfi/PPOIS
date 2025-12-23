from .bonus import Bonus

class RetentionBonus(Bonus):
    def __init__(self, bonus_id: str, employee_id: str, base_amount: float,
                 description: str, granted_by: str, retention_period_months: int,
                 vesting_schedule: str):
        super().__init__(bonus_id, employee_id, "retention", base_amount, description, granted_by)
        self.retention_period_months = retention_period_months
        self.vesting_schedule = vesting_schedule

    def calculate_vested_amount(self) -> float:
        return self.base_amount / self.retention_period_months

    def get_retention_period_months(self) -> int:
        return self.retention_period_months

