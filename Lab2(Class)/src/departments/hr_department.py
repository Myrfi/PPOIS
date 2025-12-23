from .department import Department

class HRDepartment(Department):
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        super().__init__(department_id, name, location, manager_id, budget, employee_capacity)
        self.recruitment_campaigns = []
        self.training_programs = []

    def recruit_employee(self, candidate_name: str) -> bool:
        self.recruitment_campaigns.append(candidate_name)
        return True

    def add_training_program(self, program_name: str) -> None:
        self.training_programs.append(program_name)

    def get_recruitment_count(self) -> int:
        return len(self.recruitment_campaigns)

