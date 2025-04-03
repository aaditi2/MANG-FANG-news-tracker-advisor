from dotenv import load_dotenv
import os

from tasks import generate_news_summary_and_strategy

def main():
    load_dotenv()

    companies = ["Meta", "Apple", "Netflix", "Google", "Amazon", "Microsoft"]

    for company in companies:
        print(f"\n📊 {company} Strategy Brief\n")
        output = generate_news_summary_and_strategy(company)
        print(output)
        print("\n" + "="*100 + "\n")  # Optional divider between companies

if __name__ == "__main__":
    main()
