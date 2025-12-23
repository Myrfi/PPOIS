from .employee import Employee

class ProjectManager(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, pmp_certified: bool,
                 project_methodology: str, industry_experience: int):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.pmp_certified = pmp_certified
        self.project_methodology = project_methodology
        self.industry_experience = industry_experience
        self.projects_completed = 0
        self.on_time_delivery_rate = 0.0

    def increment_projects_completed(self) -> None:
        self.projects_completed += 1

    def update_on_time_delivery_rate(self, rate: float) -> None:
        self.on_time_delivery_rate = rate

