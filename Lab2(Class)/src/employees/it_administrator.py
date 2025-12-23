from .employee import Employee

class ITAdministrator(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, technical_certifications: list,
                 systems_administered: list, security_clearance_level: str):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.technical_certifications = technical_certifications
        self.systems_administered = systems_administered
        self.security_clearance_level = security_clearance_level
        self.incidents_resolved = 0
        self.uptime_maintained = 0.0

    def add_technical_certification(self, certification: str) -> None:
        self.technical_certifications.append(certification)

    def add_system_administered(self, system: str) -> None:
        self.systems_administered.append(system)

    def increment_incidents_resolved(self) -> None:
        self.incidents_resolved += 1

    def update_uptime_maintained(self, uptime: float) -> None:
        self.uptime_maintained = uptime

    def can_access_critical_systems(self) -> bool:
        return True

