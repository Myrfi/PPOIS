import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.bonuses.referral_bonus import ReferralBonus

def test_referral_bonus_initialization():
    ref_bonus = ReferralBonus("BON003", "EMP001", 2000.0, "Employee referral bonus", "HR001", "EMP002", "2023-06-01")
    assert ref_bonus.bonus_id == "BON003"
    assert ref_bonus.referred_employee_id == "EMP002"
    assert ref_bonus.referral_date == "2023-06-01"

def test_calculate_referral_bonus():
    ref_bonus = ReferralBonus("BON003", "EMP001", 2000.0, "Employee referral bonus", "HR001", "EMP002", "2023-06-01")
    amount = ref_bonus.calculate_referral_bonus()
    assert amount == 2200.0

def test_get_referred_employee_id():
    ref_bonus = ReferralBonus("BON003", "EMP001", 2000.0, "Employee referral bonus", "HR001", "EMP002", "2023-06-01")
    assert ref_bonus.get_referred_employee_id() == "EMP002"