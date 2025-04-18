import os
import requests

def fetch_rival_news(company_name):
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        raise ValueError("SERPAPI_KEY not found in environment.")

    url = "https://serpapi.com/search.json"
    params = {
        "q": f"{company_name} latest news",
        "api_key": serpapi_key,
        "engine": "google_news",
        "hl": "en",
        "gl": "us",
        "num": 5
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"⚠️ Failed to fetch news for {company_name}"

    results = response.json().get("news_results", [])

    if not results:
        return "No news found."

    # Just return titles, no links
    headlines = []
    for item in results[:5]:
        title = item.get("title", "No title")
        headlines.append(f"- {title}")

    return "\n".join(headlines)
