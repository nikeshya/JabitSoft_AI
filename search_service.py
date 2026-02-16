import requests
from difflib import SequenceMatcher
from functools import lru_cache

PRODUCTS_URL = "https://koala-productsearch.s3.ap-southeast-2.amazonaws.com/products_search.json"
products = requests.get(PRODUCTS_URL).json()

PRODUCT_INDEX = [
    {
        "legacy_id": str(p["legacy_id"]),
        "name": p["name"],
        "name_lower": p["name"].lower(),
        "name_words": p["name"].lower().split(),
        "slug": p["slug"].lower(),
        "image": p["default_image"]
    }
    for p in products
]

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

@lru_cache(maxsize=500)
def search(query, limit=8):    # limit can be managed based on website search box size
    if not query or len(query) < 2:
        return []

    query = query.strip().lower()
    query_tokens = query.split()
    results = []

    enable_fuzzy = len(query) <= 20

    for product in PRODUCT_INDEX:
        score = 0

        # 1 Exact matching very high score
        if query == product["legacy_id"]:
            score += 200

        if query == product["slug"]:
            score += 180

        if query == product["name_lower"]:
            score += 150

        # 2 Prefix match per word
        matched_tokens = 0
        for q in query_tokens:
            for word in product["name_words"]:
                if word.startswith(q):
                    score += 20
                    matched_tokens += 1
                    break

        # Reward full intent match
        if matched_tokens == len(query_tokens):
            score += 40

        # 3 Fuzzy token matches 
        if enable_fuzzy:
            for q in query_tokens:
                for word in product["name_words"]:
                    if similarity(q, word) >= 0.8:  # 0.8 is used for mistaked spells
                        score += 6
                        break

        # 4 Partial slug match
        if query in product["slug"]:
            score += 10

        if score > 0:
            results.append({
                "score": score,
                "legacy_id": product["legacy_id"],
                "name": product["name"],
                "slug": product["slug"],
                "image": product["image"]
            })

        if len(results) > limit * 5:
            break

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]
