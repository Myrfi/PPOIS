import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.bonuses.retention_bonus import RetentionBonus

def test_retention_bonus_initialization():
    ret_bonus = RetentionBonus("BON004", "EMP001", 10000.0, "Retention bonus", "MGR001", 24, "quarterly")
    assert ret_bonus.bonus_id == "BON004"
    assert ret_bonus.retention_period_months == 24
    assert ret_bonus.vesting_schedule == "quarterly"

def test_calculate_vested_amount():
    ret_bonus = RetentionBonus("BON004", "EMP001", 10000.0, "Retention bonus", "MGR001", 24, "quarterly")
    amount = ret_bonus.calculate_vested_amount()
    assert abs(amount - 416.67) < 0.01

def test_get_retention_period_months():
    ret_bonus = RetentionBonus("BON004", "EMP001", 10000.0, "Retention bonus", "MGR001", 24, "quarterly")
    assert ret_bonus.get_retention_period_months() == 24