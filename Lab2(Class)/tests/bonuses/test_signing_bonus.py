import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.bonuses.signing_bonus import SigningBonus

def test_signing_bonus_initialization():
    sign_bonus = SigningBonus("BON005", "EMP001", 15000.0, "Signing bonus", "HR001", 3, "lump_sum")
    assert sign_bonus.bonus_id == "BON005"
    assert sign_bonus.contract_term_years == 3
    assert sign_bonus.payment_schedule == "lump_sum"

def test_calculate_signing_bonus_value():
    sign_bonus = SigningBonus("BON005", "EMP001", 15000.0, "Signing bonus", "HR001", 3, "lump_sum")
    value = sign_bonus.calculate_signing_bonus_value()
    assert value == 5000.0

def test_get_contract_term_years():
    sign_bonus = SigningBonus("BON005", "EMP001", 15000.0, "Signing bonus", "HR001", 3, "lump_sum")
    assert sign_bonus.get_contract_term_years() == 3