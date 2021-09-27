import pytest

from services.penalty import calc_penalty_score

def test_calc_penalty_score_over_60():
  # 60..75   = 15     =  15
  # ------------------------
  # TOTAL                15

  state_1 = {'car_id': '3', 'driver_id': '6', 'speed': 75, 'coords': [-101.92228349480504, 62.08031098034954]}
  penalty_score = calc_penalty_score(state_1)
  assert penalty_score == 15

def test_calc_penalty_score_over_80():
  # 60..80   = 20     =  20
  # 80..98   = 18 * 2 =  36
  # ------------------------
  # TOTAL                56

  state_1 = {'car_id': '3', 'driver_id': '6', 'speed': 98, 'coords': [-101.92228349480504, 62.08031098034954]}
  penalty_score = calc_penalty_score(state_1)
  assert penalty_score == 56

def test_calc_penalty_score_over_100():
  # 60..80   = 20     =  20
  # 80..100  = 20 * 2 =  40
  # 100..179 = 79 * 5 = 395
  # ------------------------
  # TOTAL               455

  state_1 = {'car_id': '3', 'driver_id': '6', 'speed': 179, 'coords': [-101.92228349480504, 62.08031098034954]}
  penalty_score = calc_penalty_score(state_1)
  assert penalty_score == 455