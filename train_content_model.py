import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch clothing items
response = supabase.table("clothing_items").select("*").execute()
items = response.data

if not items:
    raise Exception("No clothing items found in Supabase.")

# Convert to DataFrame
df = pd.DataFrame(items)

# Optional: drop items without essential fields
df = df.dropna(subset=["tags", "type", "color", "fabric", "suitable_gender"])

# Combine attributes for vectorization
df["combined"] = (
    df["tags"] + " " +
    df["type"] + " " +
    df["color"] + " " +
    df["fabric"] + " " +
    df["suitable_gender"]
)

# Train vectorizer
vectorizer = TfidfVectorizer()
item_vectors = vectorizer.fit_transform(df["combined"])

# Save both vectorizer and the DataFrame
joblib.dump((vectorizer, df), "content_model.pkl")

print("✅ Saved: content_model.pkl")
