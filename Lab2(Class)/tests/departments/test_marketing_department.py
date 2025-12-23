import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.departments.marketing_department import MarketingDepartment

def test_marketing_department_initialization():
    marketing = MarketingDepartment("DEP005", "Marketing", "HQ", "MGR005", 250000.0, 18)
    assert marketing.department_id == "DEP005"
    assert marketing.name == "Marketing"

def test_launch_campaign():
    marketing = MarketingDepartment("DEP005", "Marketing", "HQ", "MGR005", 250000.0, 18)
    result = marketing.launch_campaign("Summer Sale")
    assert result == True
    assert "Summer Sale" in marketing.campaigns

def test_update_brand_awareness_score():
    marketing = MarketingDepartment("DEP005", "Marketing", "HQ", "MGR005", 250000.0, 18)
    marketing.update_brand_awareness_score(85.5)
    assert marketing.brand_awareness_score == 85.5

def test_get_campaigns_count():
    marketing = MarketingDepartment("DEP005", "Marketing", "HQ", "MGR005", 250000.0, 18)
    marketing.launch_campaign("Campaign 1")
    marketing.launch_campaign("Campaign 2")
    assert marketing.get_campaigns_count() == 2