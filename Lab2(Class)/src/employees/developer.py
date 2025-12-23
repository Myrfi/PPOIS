from .employee import Employee

class Developer(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, programming_languages: list,
                 experience_years: int, specialization: str):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.programming_languages = programming_languages
        self.experience_years = experience_years
        self.specialization = specialization
        self.projects_completed = 0
        self.code_quality_score = 0.0

    def add_programming_language(self, language: str) -> None:
        self.programming_languages.append(language)

    def add_certification(self, certification: str) -> None:
        pass

    def update_code_quality_score(self, score: float) -> None:
        self.code_quality_score = score

    def increment_projects_completed(self) -> None:
        self.projects_completed += 1

    def get_experience_level(self) -> str:
        return "mid"

