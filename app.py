from fastapi import FastAPI
from pydantic import BaseModel
import os
import pickle
from model import load_model, predict_proba_wrapper

app = FastAPI()

# Load model once at startup
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")
model = load_model(MODEL_PATH)

class PredictRequest(BaseModel):
    # simple numeric features, extend based on your classifier
    views: float
    purchases: float

class PredictResponse(BaseModel):
    success: bool
    score: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Create a single-row feature vector for the model
    features = [[req.views, req.purchases]]

    score = predict_proba_wrapper(model, features)

    return PredictResponse(
        success=True,
        score=float(score)
    )
