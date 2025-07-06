from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL =os.getenv("SUPABASE_URL")
SUPABSE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL,SUPABSE_KEY)