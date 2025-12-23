import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.bonuses.performance_bonus import PerformanceBonus

def test_performance_bonus_initialization():
    perf_bonus = PerformanceBonus("BON002", "EMP001", 5000.0, "Q4 Performance Bonus", "MGR001", "quarterly", {"productivity": 4.5, "quality": 4.2})
    assert perf_bonus.bonus_id == "BON002"
    assert perf_bonus.performance_period == "quarterly"
    assert perf_bonus.kpi_achievements == {"productivity": 4.5, "quality": 4.2}

def test_calculate_performance_rating():
    perf_bonus = PerformanceBonus("BON002", "EMP001", 5000.0, "Q4 Performance Bonus", "MGR001", "quarterly", {"productivity": 4.5, "quality": 4.2})
    rating = perf_bonus.calculate_performance_rating()
    assert rating == 4.35

def test_determine_bonus_tier():
    perf_bonus = PerformanceBonus("BON002", "EMP001", 5000.0, "Q4 Performance Bonus", "MGR001", "quarterly", {"productivity": 4.5, "quality": 4.2})
    tier = perf_bonus.determine_bonus_tier()
    assert tier == "good"