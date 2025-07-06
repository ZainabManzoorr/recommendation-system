### File: supabase/upload_to_supabase.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from recommendation.data.generate_synthetic_data import generate_measurements

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_measurements_to_supabase():
    data = generate_measurements()
    for row in data:
        supabase.table("user_measurements").insert(row).execute()
    print(f"✅ Uploaded {len(data)} rows to Supabase.")

if __name__ == "__main__":
    insert_measurements_to_supabase()
