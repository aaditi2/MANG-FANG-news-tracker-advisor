from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv(dotenv_path="../.env")  # adjust path if needed

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
LLM_MODEL = "meta-llama/Llama-3-8b-chat-hf"

# MANG + FANG competitors
MANG_FANG_COMPETITORS = [
    "Meta", "Apple", "Netflix", "Google", "Microsoft", "Amazon", "Nvidia"
]

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # change if deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_news/{company}")
def get_news(company: str):
    # Remove selected company from query
    competitors = [c for c in MANG_FANG_COMPETITORS if c.lower() != company.lower()]
    query = " OR ".join(competitors) + " news"

    # Fetch news from SerpAPI
    params = {
        "q": query,
        "tbm": "nws",
        "api_key": SERPAPI_KEY
    }

    serp_response = requests.get("https://serpapi.com/search", params=params)
    articles = serp_response.json().get("news_results", [])

    if not articles:
        return {"news": "No news found.", "suggestions": "N/A"}

    # Extract top 5 headlines
    headlines = "\n".join([f"- {a['title']}" for a in articles[:5]])

    # Construct LLM prompt
    prompt = f"""
You are a strategic advisor for the company **{company}**.
Below are recent competitor headlines from major tech companies (Meta, Apple, Netflix, Google, Microsoft, Amazon, Nvidia).
Based on this, suggest 3 actionable strategies {company} can adopt to stay competitive.

Headlines:
{headlines}

Be concise, insightful, and business-relevant.
"""

    # Call LLaMA-3 model
    llama_response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7,
        }
    )

    if llama_response.status_code != 200:
        return {"news": headlines, "suggestions": "⚠️ Failed to fetch suggestions."}

    suggestions = llama_response.json()["choices"][0]["message"]["content"]

    return {"news": headlines, "suggestions": suggestions}
