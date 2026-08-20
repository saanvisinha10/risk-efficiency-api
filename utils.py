import numpy as np

def calculate_shot_ev(deliveries: int, runs: int, dismissals: int, dots: int, cost: float):
    dismissal_prob = dismissals / deliveries
    scoring_deliveries = max(0, deliveries - dots - dismissals)
    scoring_prob = scoring_deliveries / deliveries

    non_dismissal_balls = deliveries - dismissals
    avg_reward = (runs / non_dismissal_balls) if non_dismissal_balls > 0 else 0.0

    ev = (scoring_prob * avg_reward) - (dismissal_prob * cost)
    efficiency_index = float(100 / (1 + np.exp(-2.0 * ev)))

    return scoring_prob, dismissal_prob, avg_reward, ev, efficiency_index
