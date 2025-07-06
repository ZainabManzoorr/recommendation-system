import os
from dotenv import load_dotenv
from supabase import create_client, Client
from recommendation.data.generate_synthetic_data import generate_measurements

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_measurements_to_supabase():
    data = generate_measurements()

    for row in data:
        try:
            print("📤 Inserting row:", row)
            response = supabase.table("user_measurements").insert(row).execute()
            print("Success:", response)
        except Exception as e:
            print("Failed to insert row:", row)
            print("🔍 Error:", e)

if __name__ == "__main__":
    insert_measurements_to_supabase()
