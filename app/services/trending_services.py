from supabase import create_client, Client
import os

# Initialize Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Example trending keywords
trending_keywords = [
    "cargo pants", "denim jackets", "kurti", "lawn", "summer outfit"
]

def find_matching_clothing_items(trending_keywords):
    matching_items = []

    for keyword in trending_keywords:
        response = supabase.table("clothing_items").select("*").or_(
            f"name.ilike.%{keyword}%,description.ilike.%{keyword}%,style_tag.ilike.%{keyword}%,category.ilike.%{keyword}%"
        ).execute()

        if response.data:
            for item in response.data:
                item['matched_keyword'] = keyword  # tag with which keyword matched
                matching_items.append(item)

    return matching_items

if __name__ == "__main__":
    matched_items = find_matching_clothing_items(trending_keywords)
    for item in matched_items:
        print(f"[{item['matched_keyword']}] {item['name']}")

def insert_trending_items(matching_items):
    inserted_count = 0

    for item in matching_items:
        clothing_id = item["id"]
        keyword = item["matched_keyword"]

        # Avoid duplicate insertions
        existing = supabase.table("trending_items") \
            .select("id") \
            .eq("clothing_item_id", clothing_id) \
            .eq("trend_keyword", keyword) \
            .execute()

        if not existing.data:
            supabase.table("trending_items").insert({
                "clothing_item_id": clothing_id,
                "trend_keyword": keyword
            }).execute()
            inserted_count += 1

    print(f"✅ Inserted {inserted_count} new trending items.")

if __name__ == "__main__":
    matched_items = find_matching_clothing_items(trending_keywords)
    insert_trending_items(matched_items)
