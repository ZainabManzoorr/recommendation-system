import os
from dotenv import load_dotenv
from supabase import create_client, client
import pandas as pd

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase : client = create_client(SUPABASE_URL,SUPABASE_KEY)

def fetch_measurements():
  response = supabase.table('user_measurements').select("*").execute()
  data = response.data
  df = pd.DataFrame(data)
  print(f"Feteched {len(df)} rows from Supabase")
  return df

if __name__ == "__main__":
  df = fetch_measurements()
  print(df.head())