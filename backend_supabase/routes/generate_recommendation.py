from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load Supabase config
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load AI model
vectorizer, item_df = joblib.load("content_model.pkl")

# Define FastAPI router
router = APIRouter()

class RecommendationRequest(BaseModel):
    user_id: str

@router.post("/generate-recommendation")
def generate_recommendation(req: RecommendationRequest):
    try:
        # Step 1: Fetch user
        user_resp = supabase.table("users").select("*").eq("id", req.user_id).limit(1).execute()
        if not user_resp.data:
            raise HTTPException(status_code=404, detail="User not found")

        user = user_resp.data[0]
        body_type = user.get("body_type")
        gender = user.get("gender")
        preferred_colors = user.get("preferred_colors", [])

        if not body_type or not gender:
            raise HTTPException(status_code=400, detail="User missing body_type or gender")

        # Step 2: Fetch clothing items
        clothing_resp = (
            supabase.table("clothing_items")
            .select("*")
            .ilike("tags", f"%{body_type}%")
            .eq("suitable_gender", gender)
            .execute()
        )

        items = clothing_resp.data
        if not items:
            return {"status": "no matches", "message": "No matching outfits found"}

        # Convert to DataFrame
        filtered_df = pd.DataFrame(items)
        if filtered_df.empty:
            return {"status": "no matches", "message": "No matching items after filtering"}

        # Step 3: Build item vectors
        filtered_df["text"] = (
            filtered_df["tags"] + " " +
            filtered_df["suitable_gender"] + " " +
            filtered_df["color"] + " " +
            filtered_df["type"]
        )
        item_vectors = vectorizer.transform(filtered_df["text"])

        # Step 4: User vector
        user_string = f"{body_type} {gender} {' '.join(preferred_colors)}"
        user_vector = vectorizer.transform([user_string])

        # Step 5: Similarity and Top Items
        similarities = cosine_similarity(user_vector, item_vectors)[0]
        top_indices = similarities.argsort()[::-1][:5]
        top_items = filtered_df.iloc[top_indices]

        # Step 6: Save recommendations
        count = 0
        for _, row in top_items.iterrows():
            exists = supabase.table("recommendations").select("id").eq("user_id", req.user_id).eq("item_id", row["id"]).execute()
            if exists.data:
                continue

            supabase.table("recommendations").insert({
                "user_id": req.user_id,
                "item_id": row["id"],
                "source": "hybrid_model",
                "reason": f"AI match for body type: {body_type}"
            }).execute()
            count += 1

        return {
            "status": "success",
            "recommended_count": count,
            "items": top_items["name"].tolist() if "name" in top_items else []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) or "Internal Server Error")
