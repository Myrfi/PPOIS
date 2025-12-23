class Employee:
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hire_date = hire_date
        self.salary = salary
        self.department_id = department_id
        self.is_active = True
        self.manager_id = None
        self.location = "Headquarters"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def update_salary(self, new_salary: float) -> None:
        self.salary = new_salary

    def deactivate(self) -> None:
        self.is_active = False

    def assign_manager(self, manager_id: str) -> None:
        self.manager_id = manager_id

    def change_location(self, new_location: str) -> None:
        self.location = new_location

