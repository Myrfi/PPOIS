from .department import Department

class MarketingDepartment(Department):
    def __init__(self, department_id: str, name: str, location: str, manager_id: str,
                 budget: float, employee_capacity: int):
        super().__init__(department_id, name, location, manager_id, budget, employee_capacity)
        self.campaigns = []
        self.brand_awareness_score = 0.0

    def launch_campaign(self, campaign_name: str) -> bool:
        self.campaigns.append(campaign_name)
        return True

    def update_brand_awareness_score(self, score: float) -> None:
        self.brand_awareness_score = score

    def get_campaigns_count(self) -> int:
        return len(self.campaigns)