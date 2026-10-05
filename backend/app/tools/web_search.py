from ddgs import DDGS
from langchain_core.tools import tool
import json


@tool
def web_search(query: str) -> str:
    """
    Search the web for current travel information.
    """

    print("\n==============================")
    print("WEB SEARCH TOOL")
    print("==============================")

    print(f"Search query: {query}")

    results = []

    try:
        with DDGS(timeout=15) as ddgs:

            search_results = ddgs.text(
                query,
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

        return json.dumps({
            "status": "error",
            "message": f"Web search failed for query: {query}"
        })

    if not results:
        return json.dumps({
            "status": "no_results",
            "message": f"No search results found for: {query}"
        })

    print(f"Results found: {len(results)}")

    return json.dumps({
        "status": "success",
        "results": results
    }, indent=2, ensure_ascii=False)