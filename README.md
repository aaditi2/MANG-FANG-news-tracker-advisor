# Company news tracker and advisor

![GitHub stars](https://img.shields.io/github/stars/aaditi2/news-strategizer?style=social)
![Made with](https://img.shields.io/badge/Made%20with-Python%20%26%20LLMs-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This News Strategizer is an AI-powered assistant that helps generate strategic suggestions for any company based on real-time competitor news. It automatically fetches the latest headlines and uses a language model to provide insightful, actionable strategies.

---

## 🚀 Features

- **Live Competitor News:-** Fetches real-time news using online APIs.
- **Company-Aware Suggestions:-** Uses custom prompt engineering to tailor recommendations
- **LLM Powered:-** Leverages LLaMA 3 via open source API for high-quality insights
- **Industry-Agnostic:-** Works across any industry; not limited to tech
- **Command-Line Tool:-** Simple to run with customizable company input

---

## 🧰 Tech Stack

- **Python** – Project scripting and API handling
- **SerpAPI** – For live news headlines
- **Together API (LLaMA-3)** – Strategy generation
- **dotenv** – Secure environment variable management
- **Prompt Engineering** – Custom strategy prompt format

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/aaditi2/news-strategizer.git
cd news-strategizer
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
