from .employee import Employee

class SalesRepresentative(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, sales_region: str,
                 commission_rate: float, total_sales: float):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.sales_region = sales_region
        self.commission_rate = commission_rate
        self.total_sales = total_sales
        self.target_achievement = 0.0

    def record_sale(self, amount: float) -> None:
        self.total_sales += amount

    def update_target_achievement(self, achievement: float) -> None:
        self.target_achievement = achievement

    def calculate_commission(self) -> float:
        return self.total_sales * self.commission_rate

