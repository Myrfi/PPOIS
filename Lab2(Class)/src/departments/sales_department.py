from .department import Department

class SalesDepartment(Department):
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        super().__init__(department_id, name, location, manager_id, budget, employee_capacity)
        self.sales_targets = []
        self.revenue_generated = 0.0

    def set_sales_target(self, target_amount: float) -> bool:
        self.sales_targets.append(target_amount)
        return True

    def record_revenue(self, amount: float) -> None:
        self.revenue_generated += amount

    def get_targets_count(self) -> int:
        return len(self.sales_targets)