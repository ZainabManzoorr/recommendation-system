from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def recommend_root():
    return {"message": "Recommend API placeholder"}
