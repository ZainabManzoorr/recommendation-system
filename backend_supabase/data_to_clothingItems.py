import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Sample clothing items for different body types
Clothing_Items = [
    {
        "type": "Wrap Dress",
        "color": "Red",
        "fabric": "Cotton",
        "tags": ["hourglass", "formal"],
        "price": 49.99,
        "is_for_sale": True,
        "suitable_gender": "Female",
        "image_url": "https://i.imgur.com/3xTqRzE.jpg",
        "owner_id": None,
        "brand_id": None,
    },
    {
        "type": "A-Line Skirt",
        "color": "Blue",
        "fabric": "Linen",
        "tags": ["pear", "summer"],
        "price": 39.99,
        "is_for_sale": True,
        "suitable_gender": "Female",
        "image_url": "https://i.imgur.com/O4z1cRl.jpg",
        "owner_id": None,
        "brand_id": None,
    },
    {
        "type": "Empire Waist Dress",
        "color": "Green",
        "fabric": "Chiffon",
        "tags": ["apple", "wedding"],
        "price": 74.99,
        "is_for_sale": True,
        "suitable_gender": "Female",
        "image_url": "https://i.imgur.com/ozljdcS.jpg",
        "owner_id": None,
        "brand_id": None,
    },
    {
        "type": "Structured Blazer",
        "color": "Black",
        "fabric": "Polyester",
        "tags": ["inverted triangle", "business"],
        "price": 89.99,
        "is_for_sale": True,
        "suitable_gender": "Female",
        "image_url": "https://i.imgur.com/fz6LIFp.jpg",
        "owner_id": None,
        "brand_id": None,
    },
    {
        "type": "Peplum Top",
        "color": "White",
        "fabric": "Silk",
        "tags": ["rectangle", "party"],
        "price": 29.99,
        "is_for_sale": True,
        "suitable_gender": "Female",
        "image_url": "https://i.imgur.com/Gg0MPzD.jpg",
        "owner_id": None,
        "brand_id": None,
    }
]

# Insert each item
for item in Clothing_Items:
    try:
        print(f"Inserting: {item['type']} ({item['tags'][0]})")
        supabase.table("Clothing_Items").insert(item).execute()
    except Exception as e:
        print("❌ Error inserting:", e)
