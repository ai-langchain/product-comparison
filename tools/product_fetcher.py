"""
tools/product_fetcher.py
------------------------
Fetches real product data using Google Search via SerpAPI.
"""

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch

load_dotenv()


def search_google(query: str) -> str:
    """Run a Google search and return combined result snippets."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return "SerpAPI key not found."

    params = {
        "q": query,
        "api_key": api_key,
        "num": 5,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []

    # Shopping results (price, ratings)
    for item in results.get("shopping_results", [])[:3]:
        parts = [item.get("title", ""), item.get("price", ""), item.get("rating", ""), item.get("reviews", "")]
        snippets.append(" | ".join(str(p) for p in parts if p))

    # Organic results (specs, reviews)
    for item in results.get("organic_results", [])[:4]:
        snippet = item.get("snippet", "")
        if snippet:
            snippets.append(snippet)

    # Answer box if available
    answer = results.get("answer_box", {}).get("answer") or results.get("answer_box", {}).get("snippet")
    if answer:
        snippets.insert(0, answer)

    return "\n".join(snippets) if snippets else "No results found."


@tool
def fetch_product_data(product_name: str) -> str:
    """
    Searches Google for real, accurate product information
    including specs, price, and user ratings.
    """
    specs_data = search_google(f"{product_name} full specifications")
    price_data = search_google(f"{product_name} price India USD 2025")
    rating_data = search_google(f"{product_name} user rating review pros cons")

    return f"""=== SPECS ===
{specs_data}

=== PRICE ===
{price_data}

=== RATINGS & REVIEWS ===
{rating_data}
"""