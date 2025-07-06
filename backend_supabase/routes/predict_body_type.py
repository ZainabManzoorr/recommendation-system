from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
from supabase import client, create_client
from dotenv import load_dotenv
import os

model = joblib.load("body_type_classifier.joblib")

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase : client = create_client(SUPABASE_URL,SUPABASE_KEY)

class MeasurementRequest(BaseModel):
  user_id: str
  height: float
  weight:float
  chest:float
  waist:float
  shoulder:float
  hips:float
  sleeve:float

router = APIRouter() 

@router.post("/predict-body-type")
def predict_body_type(req: MeasurementRequest):
    try:
        features = np.array([[req.height, req.waist, req.weight, req.chest, req.hips, req.shoulder, req.sleeve]])
        predicted_body_type = model.predict(features)[0]

        supabase.table('users').update({
            'body_type': predicted_body_type
        }).eq("id", req.user_id).execute()

        return {
            'predicted_body_type': predicted_body_type,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
