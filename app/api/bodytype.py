from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import numpy as np
import joblib
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load ML model
MODEL_PATH = "app/models/bodytype_model.pkl"
model = joblib.load(MODEL_PATH)

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI router
router = APIRouter()

# Pydantic schema
class UserMeasurement(BaseModel):
    user_id: str
    height: float
    weight: float
    chest: float
    waist: float
    hips: float
    shoulder: float
    sleeve: float
    gender: Literal["male", "female"]


@router.post("/predict-body-type")
async def predict_body_type(user_data: UserMeasurement):
    try:
        # Encode gender: male=0, female=1
        gender_type_encoded = 0 if user_data.gender == "male" else 1

        input_data = [[
            user_data.height,
            user_data.weight,
            user_data.chest,
            user_data.waist,
            user_data.hips,
            user_data.shoulder,
            user_data.sleeve,
            gender_type_encoded
        ]]

        # Predict body type
        prediction = model.predict(input_data)[0]
        logger.info(f"Predicted body type: {prediction}")

        # Update Supabase users table
        update_response = supabase.table("users").update({
            "body_type": prediction
        }).eq("id", user_data.user_id).execute()

        logger.info(f"Supabase update response: {update_response}")

        # Check update success by verifying if data is returned (updated rows)
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update user record in Supabase")

        return {
            "user_id": user_data.user_id,
            "predicted_body_type": prediction
        }

    except Exception as e:
        logger.exception("Error during body type prediction or database update")
        raise HTTPException(status_code=500, detail=str(e))
