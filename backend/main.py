from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os
import re

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

def detect_company(headline: str) -> str:
    headline = headline.lower()
    for name in MANG_FANG_COMPETITORS:
        if name.lower() in headline:
            return name
    return "Unknown"

@app.get("/get_news/{company}")
def get_news(company: str):
    competitors = [c for c in MANG_FANG_COMPETITORS if c.lower() != company.lower()]
    query = " OR ".join(competitors) + " news"

    params = {
        "q": query,
        "tbm": "nws",
        "api_key": SERPAPI_KEY
    }

    serp_response = requests.get("https://serpapi.com/search", params=params)
    articles = serp_response.json().get("news_results", [])

    if not articles:
        return {"news": [], "suggestions": "[]"}

    # Prepare structured news
    headlines_data = [
        {
            "company": detect_company(a.get('title', '')),
            "title": a.get('title', '').strip(),
            "link": a.get('link', '#')
        }
        for a in articles[:5]
        if isinstance(a, dict) and 'title' in a and 'link' in a
    ]

    # Flatten news into plain text for LLM
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
