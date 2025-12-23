from .employee import Employee

class LogisticsCoordinator(Employee):
    def __init__(self, employee_id: str, first_name: str, last_name: str, email: str,
                 hire_date: str, salary: float, department_id: str, transportation_modes: list,
                 international_shipping_experience: int, hazardous_materials_certified: bool):
        super().__init__(employee_id, first_name, last_name, email, hire_date, salary, department_id)
        self.transportation_modes = transportation_modes
        self.international_shipping_experience = international_shipping_experience
        self.hazardous_materials_certified = hazardous_materials_certified
        self.shipments_coordinated = 0
        self.on_time_delivery_rate = 0.0

    def add_transportation_mode(self, mode: str) -> None:
        self.transportation_modes.append(mode)

    def increment_shipments_coordinated(self) -> None:
        self.shipments_coordinated += 1

    def update_on_time_delivery_rate(self, rate: float) -> None:
        self.on_time_delivery_rate = rate

    def can_handle_international_logistics(self) -> bool:
        return self.international_shipping_experience > 3

    def can_handle_hazardous_materials(self) -> bool:
        return self.hazardous_materials_certified

