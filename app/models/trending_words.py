from pytrends.request import TrendReq
import pandas as pd

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=300)

# Seed keywords related to fashion
seed_keywords = ["fashion", "clothing", "dresses", "jeans", "outfits", "summer wear"]

def get_fashion_trends(seeds=seed_keywords, top_n=10):
    fashion_trends = set()

    for kw in seeds:
        try:
            pytrends.build_payload([kw], cat=0, timeframe='now 7-d', geo='PK', gprop='')
            related = pytrends.related_topics()[kw]['top']

            if related is not None:
                top_keywords = related.sort_values(by='value', ascending=False)['topic_title'].head(top_n)
                fashion_trends.update(top_keywords.tolist())

        except Exception as e:
            print(f"Error with keyword '{kw}': {e}")
            continue

    return list(fashion_trends)

if __name__ == "__main__":
    fashion_keywords = get_fashion_trends()
    print("Fashion-related trending keywords in Pakistan:")
    for kw in fashion_keywords:
        print("-", kw)
