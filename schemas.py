from pydantic import BaseModel, Field
from typing import List, Optional

class ShotPerformanceInput(BaseModel):
    shot_name: str = Field(..., description="Name of the shot (e.g., Cover Drive, Sweep)")
    deliveries_played: int = Field(..., ge=5, description="Number of deliveries played (min 5)")
    runs_scored: int = Field(..., ge=0, description="Total runs scored off this shot")
    dismissals: int = Field(..., ge=0, description="Number of times dismissed playing this shot")
    dot_balls: int = Field(..., ge=0, description="Number of dot balls resulting from this shot")

class ShotEfficiencyRequest(BaseModel):
    player_id: str
    player_name: str
    dismissal_cost: Optional[float] = Field(default=10.0, ge=1.0, description="Wicket loss penalty in runs")
    shots: List[ShotPerformanceInput] = Field(..., min_items=1, description="List of shot profiles")

class DerivedShotMetrics(BaseModel):
    scoring_probability: float
    dismissal_probability: float
    average_reward: float
    expected_value: float

class ShotEfficiencyItem(BaseModel):
    shot_name: str
    deliveries_played: int
    derived_metrics: DerivedShotMetrics
    efficiency_index: float
    risk_category: str
    assessment: str

class ShotEfficiencyResponse(BaseModel):
    player_id: str
    player_name: str
    total_shots_evaluated: int
    overall_best_shot: str
    shot_evaluations: List[ShotEfficiencyItem]
