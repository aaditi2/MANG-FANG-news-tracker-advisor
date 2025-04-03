from dotenv import load_dotenv
import os
from tasks import generate_news_summary_and_strategy
from agents import fetch_rival_news

def main():
    load_dotenv()
    companies = ["Meta", "Apple", "Netflix", "Google", "Amazon", "Microsoft"]

    # Step 1: Collect news for all companies
    all_news = {}
    for company in companies:
        news_items = fetch_rival_news(company)
        all_news[company] = news_items

    # Step 2: Print all news
    print("📰 **Competitor News**\n")
    for company in sorted(all_news):
        print(f"🔹 {company}:")
        print(all_news[company])
        print()

    # Step 3: Print strategy suggestions
    print("💡 **Strategic Suggestions**\n")
    for company in companies:
        print(f"📊 {company} Strategy Brief\n")
        strategy = generate_news_summary_and_strategy(company, all_news)
        print(strategy)
        print("\n" + "="*100 + "\n")

if __name__ == "__main__":
    main()
