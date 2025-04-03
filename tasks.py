import os
from agents import fetch_rival_news
from prompts import strategy_prompt
import requests

def generate_news_summary_and_strategy(company_name):
    companies = ["Meta", "Apple", "Netflix", "Google", "Amazon", "Microsoft"]
    rivals = [c for c in companies if c.lower() != company_name.lower()]

    # 1. Fetch & format news for all rivals
    formatted_rival_news = ""
    for rival in rivals:
        news_items = fetch_rival_news(rival)
        if news_items:
            formatted_rival_news += f"🔹 {rival}:\n{news_items}\n\n"

    # 2. Build prompt
    prompt = strategy_prompt(company_name, formatted_rival_news)

    # 3. Call Together AI API
    api_key = os.getenv("TOGETHER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": "You are a strategic advisor helping tech companies respond to their competitors."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return f"📊 {company_name} Strategy Brief\n\n{formatted_rival_news}\n{reply}"
    else:
        return f"⚠️ Error from Together API: {response.text}"
