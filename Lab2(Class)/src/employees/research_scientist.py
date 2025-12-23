from .employee import Employee

class ResearchScientist(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, research_field: str,
                 phd_year: int, publications_count: int):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.research_field = research_field
        self.phd_year = phd_year
        self.publications_count = publications_count
        self.patents_filed = 0
        self.research_grants_secured = 0

    def increment_publications(self) -> None:
        self.publications_count += 1

    def increment_patents_filed(self) -> None:
        self.patents_filed += 1

    def increment_research_grants_secured(self) -> None:
        self.research_grants_secured += 1