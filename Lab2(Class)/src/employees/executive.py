from .employee import Employee

class Executive(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, executive_title: str,
                 board_member: bool, stock_options: int):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.executive_title = executive_title
        self.board_member = board_member
        self.stock_options = stock_options
        self.strategic_decisions = 0

    def make_strategic_decision(self, decision: str) -> None:
        self.strategic_decisions += 1

    def can_make_strategic_decisions(self) -> bool:
        return True

    def is_board_member(self) -> bool:
        return self.board_member

