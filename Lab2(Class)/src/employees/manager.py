from .employee import Employee

class Manager(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, management_level: str):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.management_level = management_level
        self.subordinates = []
        self.budget_limit = 0.0
        self.decision_power = 0

    def add_subordinate(self, employee_id: str) -> None:
        self.subordinates.append(employee_id)

    def remove_subordinate(self, employee_id: str) -> None:
        if employee_id in self.subordinates:
            self.subordinates.remove(employee_id)

    def get_subordinates_count(self) -> int:
        return len(self.subordinates)

    def set_budget_limit(self, limit: float) -> None:
        self.budget_limit = limit

    def approve_expense(self, amount: float) -> bool:
        return amount <= self.budget_limit

