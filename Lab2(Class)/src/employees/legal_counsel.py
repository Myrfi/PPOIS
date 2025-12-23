from .employee import Employee

class LegalCounsel(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, jurisdictions: list,
                 bar_admission_year: int, practice_areas: list):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.jurisdictions = jurisdictions
        self.bar_admission_year = bar_admission_year
        self.practice_areas = practice_areas
        self.cases_handled = 0
        self.success_rate = 0.0

    def add_jurisdiction(self, jurisdiction: str) -> None:
        self.jurisdictions.append(jurisdiction)

    def add_practice_area(self, area: str) -> None:
        self.practice_areas.append(area)

    def increment_cases_handled(self) -> None:
        self.cases_handled += 1

    def update_success_rate(self, rate: float) -> None:
        self.success_rate = rate

    def get_years_of_practice(self) -> int:
        return 2024 - self.bar_admission_year

