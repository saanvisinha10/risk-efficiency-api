from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ShotEfficiencyRequest, ShotEfficiencyResponse
from services import evaluate_shot_efficiency

app = FastAPI(
    title="Shot Risk Efficiency API",
    description="Evaluates shot selection efficiency using Expected Value decision theory.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"status": "live", "service": "Shot Risk Efficiency API"}

@app.post("/analytics/shot-efficiency", response_model=ShotEfficiencyResponse, tags=["Analytics"])
def get_shot_efficiency(request: ShotEfficiencyRequest):
    try:
        return evaluate_shot_efficiency(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
