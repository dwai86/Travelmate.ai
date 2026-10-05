from ddgs import DDGS
from langchain_core.tools import tool
import json


@tool
def place_search(location: str, query: str) -> str:
    """
    Search for specific places at a travel destination.

    Use this tool when looking for specific real-world places
    such as restaurants, attractions, temples, museums,
    markets, hotels, or other points of interest.
    """

    print("\n==============================")
    print("PLACE SEARCH TOOL")
    print("==============================")

    search_query = f"{query} in {location}"

    print(f"Search query: {search_query}")

    results = []

    try:

        with DDGS() as ddgs:

            search_results = ddgs.text(
                search_query,
                max_results=5,
                backend="auto"
            )

            for result in search_results:

                results.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "description":  (result.get("body") or "")[:500]
                })

    except Exception as e:

        print(f"Search failed: {e}")

        return (
            f"No search results were found for "
            f"'{query}' in {location}."
        )

    print(f"Results found: {len(results)}")

    if not results:

        return (
            f"No places found for "
            f"'{query}' in {location}."
        )

    return json.dumps(
        results,
        indent=2,
        ensure_ascii=False
    )