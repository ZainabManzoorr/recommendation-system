import requests
import uuid
import os
from dotenv import load_dotenv
from app.models.detect_skintone import classify_skin_tone
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


TEMP_DIR = "temp_profiles"
os.makedirs(TEMP_DIR, exist_ok=True)

def fetch_and_classify_skin_tone(user_id: str):
    user = supabase.table("users").select("avatar_url").eq("id", user_id).single().execute()
    if not user.data or "avatar_url" not in user.data:
        return {"status": "error", "message": "User not found or no avatar_url"}

    image_url = user.data["avatar_url"]
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")

    try:
        with open(temp_path, "wb") as f:
            f.write(requests.get(image_url).content)

        skin_tone = classify_skin_tone(temp_path)

        supabase.table("users").update({"skin_tone": skin_tone}).eq("id", user_id).execute()
        return {"status": "success", "skin_tone": skin_tone}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
