from .employee import Employee

class Analyst(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, analysis_tools: list,
                 domain_expertise: str, security_clearance: str):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.analysis_tools = analysis_tools
        self.domain_expertise = domain_expertise
        self.security_clearance = security_clearance
        self.reports_generated = 0
        self.accuracy_rating = 0.0

    def add_analysis_tool(self, tool: str) -> None:
        self.analysis_tools.append(tool)

    def add_special_project(self, project: str) -> None:
        pass

    def update_accuracy_rating(self, rating: float) -> None:
        self.accuracy_rating = rating

    def increment_reports_generated(self) -> None:
        self.reports_generated += 1

    def can_access_confidential_data(self) -> bool:
        return True

