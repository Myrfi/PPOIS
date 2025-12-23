class Department:
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        self.department_id = department_id
        self.name = name
        self.location = location
        self.manager_id = manager_id
        self.budget = budget
        self.employee_capacity = employee_capacity
        self.employees = []
        self.projects = []
        self.is_active = True

    def add_employee(self, employee_id: str) -> bool:
        if len(self.employees) < self.employee_capacity:
            self.employees.append(employee_id)
            return True
        return False

    def remove_employee(self, employee_id: str) -> bool:
        if employee_id in self.employees:
            self.employees.remove(employee_id)
            return True
        return False

    def add_project(self, project_id: str) -> None:
        self.projects.append(project_id)

    def allocate_budget(self, amount: float) -> bool:
        if self.budget >= amount:
            self.budget -= amount
            return True
        return False

    def get_employee_count(self) -> int:
        return len(self.employees)

    def get_utilization_rate(self) -> float:
        return (len(self.employees) / self.employee_capacity) * 100

