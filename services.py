from schemas import ShotEfficiencyRequest, ShotEfficiencyResponse, ShotEfficiencyItem, DerivedShotMetrics
from utils import calculate_shot_ev

def evaluate_shot_efficiency(request: ShotEfficiencyRequest) -> ShotEfficiencyResponse:
    evaluations = []
    best_shot = ""
    max_index = -1.0

    for shot in request.shots:
        s_prob, d_prob, avg_rev, ev, index = calculate_shot_ev(
            shot.deliveries_played,
            shot.runs_scored,
            shot.dismissals,
            shot.dot_balls,
            request.dismissal_cost
        )

        if d_prob > 0.10:
            risk_cat = "High Risk / Poor Efficiency"
        elif d_prob > 0.04:
            risk_cat = "Calculated Risk"
        else:
            risk_cat = "Low Risk / High Safety"

        if ev > 0.5:
            assessment = f"High decision value. Yield outweighs dismissal risk for {request.player_name}."
        elif ev > 0.0:
            assessment = f"Positive expectation. Fair reward, but keep risk monitored under tight bowling."
        else:
            assessment = f"Negative expected value. Dismissal rate severely outweighs scoring output."

        if index > max_index:
            max_index = index
            best_shot = shot.shot_name

        evaluations.append(
            ShotEfficiencyItem(
                shot_name=shot.shot_name,
                deliveries_played=shot.deliveries_played,
                derived_metrics=DerivedShotMetrics(
                    scoring_probability=round(s_prob, 3),
                    dismissal_probability=round(d_prob, 3),
                    average_reward=round(avg_rev, 2),
                    expected_value=round(ev, 3)
                ),
                efficiency_index=round(index, 2),
                risk_category=risk_cat,
                assessment=assessment
            )
        )

    return ShotEfficiencyResponse(
        player_id=request.player_id,
        player_name=request.player_name,
        total_shots_evaluated=len(request.shots),
        overall_best_shot=best_shot,
        shot_evaluations=evaluations
    )
