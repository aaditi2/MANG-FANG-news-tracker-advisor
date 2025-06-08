from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os
from collections import defaultdict
import time

# Load environment variables
load_dotenv(dotenv_path="../.env")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
LLM_MODEL = "meta-llama/Llama-3-8b-chat-hf"

MANG_FANG_COMPETITORS = ["Meta", "Apple", "Netflix", "Google", "Microsoft", "Amazon", "Nvidia"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect_company(article: dict) -> str:
    text = f"{article.get('title', '')} {article.get('snippet', '')} {article.get('link', '')}".lower()
    for name in MANG_FANG_COMPETITORS:
        if name.lower() in text:
            return name
    return "Unknown"

@app.get("/get_news/{company}")
def get_news(company: str, category: str = Query("Top"), timeframe: str = Query("Today")):
    category_keywords = {
        "Top": "",
        "Tech": "technology",
        "AI": "artificial intelligence",
        "Finance": "finance"
    }

    time_map = {
        "Today": "d",
        "Past Week": "w",
        "Past Month": "m"
    }

    keyword = category_keywords.get(category, "")
    time_filter = time_map.get(timeframe, "d")

    # Exclude selected company
    competitors = [c for c in MANG_FANG_COMPETITORS if c.lower() != company.lower()]

    headlines_data = []

    for comp in competitors:
        query = f"{comp} {keyword}".strip()
        params = {
            "q": query,
            "tbm": "nws",
            "api_key": SERPAPI_KEY,
            "tbs": f"qdr:{time_filter}"
        }

        try:
            resp = requests.get("https://serpapi.com/search", params=params)
            articles = resp.json().get("news_results", [])
        except Exception:
            continue

        count = 0
        for a in articles:
            if count >= 2:
                break
            if not isinstance(a, dict):
                continue
            title = a.get('title', '').strip()
            link = a.get('link', '#')
            snippet = a.get('snippet', '').strip()
            if not title or not link:
                continue
            detected = detect_company(a)
            headlines_data.append({
                "company": detected,
                "title": title,
                "link": link,
                "snippet": snippet
            })
            count += 1

        time.sleep(0.5)  # be nice to SerpAPI

    # Optional: sort for neatness
    headlines_data.sort(key=lambda x: x["company"])

    # Prompt for LLM
    headlines_text = "\n".join([f"- {item['company']}: {item['title']}" for item in headlines_data])

    prompt = f"""
You are a strategy advisor for the company **{company}**.

Below are recent competitor headlines from major tech companies (Meta, Apple, Netflix, Google, Microsoft, Amazon, Nvidia).

Based on this, suggest exactly 3 actionable strategies for {company}. Each strategy should include:

1. A short summary of the strategy
2. A clear objective
3. A list of 3 action steps

📦 Format the output in valid JSON using this structure:
[
  {{
    "strategy": "One-line summary",
    "objective": "Why it's useful for {company}",
    "actions": ["Step 1", "Step 2", "Step 3"]
  }},
  ...
]

📰 Headlines:
{headlines_text}

Return only the JSON array — no extra explanation.
"""

    llama_response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400,
            "temperature": 0.7,
        }
    )

    if llama_response.status_code != 200:
        return {"news": headlines_data, "suggestions": "[]"}

    suggestions = llama_response.json()["choices"][0]["message"]["content"]

    return {
        "news": headlines_data,
        "suggestions": suggestions
    }
