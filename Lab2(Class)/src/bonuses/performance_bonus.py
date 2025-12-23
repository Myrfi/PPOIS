from .bonus import Bonus

class PerformanceBonus(Bonus):
    def __init__(self, bonus_id: str, employee_id: str, base_amount: float,
                 description: str, granted_by: str, performance_period: str,
                 kpi_achievements: dict):
        super().__init__(bonus_id, employee_id, "performance", base_amount, description, granted_by)
        self.performance_period = performance_period
        self.kpi_achievements = kpi_achievements

    def calculate_performance_rating(self) -> float:
        return sum(self.kpi_achievements.values()) / len(self.kpi_achievements)

    def determine_bonus_tier(self) -> str:
        rating = self.calculate_performance_rating()
        if rating >= 4.5:
            return "excellent"
        return "good"

