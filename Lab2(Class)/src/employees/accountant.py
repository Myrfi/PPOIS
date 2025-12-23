from .employee import Employee

class Accountant(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, accounting_standards: list,
                 cpa_certified: bool, audit_experience: int):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.accounting_standards = accounting_standards
        self.cpa_certified = cpa_certified
        self.audit_experience = audit_experience
        self.financial_statements_prepared = 0
        self.audits_conducted = 0

    def add_accounting_standard(self, standard: str) -> None:
        self.accounting_standards.append(standard)

    def conduct_audit(self, audit_type: str) -> None:
        self.audits_conducted += 1

    def prepare_financial_statement(self, statement_type: str) -> None:
        self.financial_statements_prepared += 1

    def is_cpa_certified(self) -> bool:
        return self.cpa_certified

