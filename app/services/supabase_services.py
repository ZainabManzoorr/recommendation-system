import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_user_measurements():
  response = supabase.table('user_measurements').select('*').execute()
  return response.data

def update_predicted_body_type(user_id: str, prediction: str):
    try:
        response = (
            supabase.table("users")
            .update({"body_type": prediction})
            .eq("id", user_id) 
            .execute()
        )
        print(" Updated prediction in users:", response)
        return response
    except Exception as e:
        print("Error updating prediction in users:", str(e))
        return None

def upload_avatar(user_id: str, file: bytes, filename: str) -> str:
    path = f"{user_id}/{filename}"

    res = supabase.storage.from_("avatars").upload(path, file, {"content-type": "image/jpeg"})
    if res.get("error"):
        raise Exception(res["error"]["message"])
    
    public_url = supabase.storage.from_("avatars").get_public_url(path)
    return public_url

def update_user_avatar_url(user_id: str, avatar_url: str):
    res = supabase.table("users").update({"avatar_url": avatar_url}).eq("id", user_id).execute()
    if res.get("error"):
        raise Exception(res["error"]["message"])

