from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
import numpy as np
import joblib
from supabase import client, create_client
from dotenv import load_dotenv
import os
import logging 

model = joblib.load("body_type_classifier.joblib")

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase : client = create_client(SUPABASE_URL,SUPABASE_KEY)

logger = logging.getLogger(__name__)

class MeasurementRequest(BaseModel):
    user_id: str
    height: float = Field(..., gt=50, lt=300, description="Height in centimeters")
    weight: float = Field(..., gt=20, lt=300, description="Weight in kilograms")
    chest: float = Field(..., gt=30, lt=200, description="Chest circumference in inches")
    waist: float = Field(..., gt=30, lt=200, description="Waist circumference in inches")
    shoulder: float = Field(..., gt=30, lt=200, description="Shoulder width in inches")
    hips: float = Field(..., gt=30, lt=200, description="Hip circumference in inches")
    sleeve: float = Field(..., gt=30, lt=100, description="Sleeve length in inches")

# ------------------ Router ------------------
router = APIRouter()

@router.post("/predict-body-type")
def predict_body_type(req: MeasurementRequest):
    try:
        # Ensure feature order matches the model's training data
        feature_order = ['height', 'weight', 'chest', 'waist', 'shoulder', 'hips', 'sleeve']
        features = np.array([[getattr(req, f) for f in feature_order]])

        # Predict body type
        predicted_body_type = model.predict(features)[0]

        # Update Supabase user record
        response = supabase.table('users').update({
            'body_type': predicted_body_type
        }).eq("id", req.user_id).execute()

        # Check if user update was successful
        if len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found or update failed")

        return {
            "predicted_body_type": predicted_body_type,
            "status": "success"
        }

    except Exception as e:
        logger.exception("Prediction or Supabase update failed")
        raise HTTPException(status_code=500, detail="Internal server error")