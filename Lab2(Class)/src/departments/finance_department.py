from .department import Department

class FinanceDepartment(Department):
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        super().__init__(department_id, name, location, manager_id, budget, employee_capacity)
        self.financial_reports = []
        self.audits_completed = 0

    def generate_financial_report(self, report_type: str) -> dict:
        report = {"type": report_type, "date": "2024-01-01"}
        self.financial_reports.append(report)
        return report

    def complete_audit(self) -> None:
        self.audits_completed += 1

    def get_reports_count(self) -> int:
        return len(self.financial_reports)

