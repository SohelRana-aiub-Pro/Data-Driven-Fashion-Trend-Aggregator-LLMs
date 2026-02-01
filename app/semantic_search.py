# app/semantic_search.py
from sentence_transformers import SentenceTransformer
import numpy as np

# ✅ Initialize the embedder once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Currency conversion rates (example values)
CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.9,
    "GBP": 0.8,
    "BDT": 100.0
}

# ✅ Example product catalog
PRODUCTS = [
    {"name": "Casual Shirt", "desc": "Light cotton shirt", "price": 40, "occasion": "casual", "gender": "male"},
    {"name": "Evening Dress", "desc": "Elegant evening gown", "price": 120, "occasion": "party", "gender": "female"},
    {"name": "Sneakers", "desc": "Comfortable running shoes", "price": 60, "occasion": "casual", "gender": "unisex"},
    {"name": "Blazer", "desc": "Formal office blazer", "price": 90, "occasion": "formal", "gender": "male"},
    {"name": "Saree", "desc": "Traditional silk saree", "price": 150, "occasion": "wedding", "gender": "female"},
    {"name": "T-Shirt", "desc": "Casual cotton t-shirt", "price": 25, "occasion": "casual", "gender": "unisex"},
]

def semantic_search(query, gender=None, budget=None, currency="USD", occasion=None):
    # Encode the query
    query_emb = embedder.encode([query])[0]

    results = []
    for item in PRODUCTS:
        # Filter by gender (allow unisex always)
        if gender and item["gender"] not in [gender, "unisex"]:
            continue

        # Convert budget to USD for comparison
        if budget and currency in CURRENCY_RATES:
            budget_usd = budget / CURRENCY_RATES[currency]
            if item["price"] > budget_usd:
                continue

        # Flexible occasion matching (case-insensitive, substring)
        if occasion and occasion.lower() not in item["occasion"].lower():
            continue

        # Compute similarity
        item_emb = embedder.encode([item["desc"]])[0]
        sim = np.dot(query_emb, item_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(item_emb))

        # Lower threshold to catch more matches
        if sim > 0.1:
            results.append(item)

    # ✅ Fallback: if still empty, return all items under budget
    if not results and budget:
        budget_usd = budget / CURRENCY_RATES.get(currency, 1.0)
        results = [item for item in PRODUCTS if item["price"] <= budget_usd]

    # ✅ Final fallback: if still empty, return all products
    if not results:
        results = PRODUCTS

    return results
#