def calc_penalty_score(car_state):
  speed = int(car_state['speed'])
  penalty = 0
  if 60 < speed < 81:
    penalty += (speed - 60)
  elif 80 < speed < 101:
    penalty += (20 + (speed - 80)*2)
  elif speed > 100:
    penalty += (20 + 40 + (speed - 100)*5)
  return penalty
