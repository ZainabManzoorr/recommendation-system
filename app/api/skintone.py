from fastapi import APIRouter, HTTPException
from app.services.skintone_services import fetch_and_classify_skin_tone


router = APIRouter()

@router.post("/detect-skin-tone/{user_id}")
def detect_skin_tone(user_id: str):
    try:
        result = fetch_and_classify_skin_tone(user_id)
        return {"skin_tone": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

