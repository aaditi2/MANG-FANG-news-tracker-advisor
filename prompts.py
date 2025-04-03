def strategy_prompt(company, formatted_rival_news):
    return f"""
You are a strategic advisor for {company}.

Below are **real competitor updates** from other major tech companies. Based on these updates, generate two **concrete, non-generic suggestions** that {company} could consider — only if the competitor moves are relevant.

---
{formatted_rival_news}
---

Respond with exactly two bullet points. Tie your suggestions clearly to the specific moves of competitors, and avoid generic ideas.
"""
