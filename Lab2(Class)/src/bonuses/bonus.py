class Bonus:
    def __init__(self, bonus_id: str, employee_id: str, bonus_type: str,
                 base_amount: float, description: str, granted_by: str):
        self.bonus_id = bonus_id
        self.employee_id = employee_id
        self.bonus_type = bonus_type
        self.base_amount = base_amount
        self.description = description
        self.granted_by = granted_by
        self.status = "pending"
        self.net_amount = base_amount

    def approve_bonus(self) -> None:
        self.status = "approved"

    def pay_bonus(self, payment_date: str = None) -> None:
        self.status = "paid"

    def cancel_bonus(self) -> None:
        self.status = "cancelled"

    def apply_tax_withholding(self, tax_rate: float) -> None:
        self.net_amount = self.base_amount * (1 - tax_rate)

    def is_paid(self) -> bool:
        return self.status == "paid"

