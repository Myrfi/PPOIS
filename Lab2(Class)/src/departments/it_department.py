from .department import Department

class ITDepartment(Department):
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        super().__init__(department_id, name, location, manager_id, budget, employee_capacity)
        self.systems_deployed = []
        self.security_incidents = 0

    def deploy_system(self, system_name: str) -> bool:
        self.systems_deployed.append(system_name)
        return True

    def report_security_incident(self) -> None:
        self.security_incidents += 1

    def get_systems_count(self) -> int:
        return len(self.systems_deployed)

