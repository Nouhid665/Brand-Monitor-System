# 📡 Brand Monitor System

A real-time brand sentiment analysis dashboard that monitors what people are saying about any brand across HackerNews and NewsAPI — powered by local/cloud AI using Groq + Mistral.

---

## 🚀 Features

- 🔍 **Multi-source monitoring** — fetches mentions from HackerNews and NewsAPI simultaneously
- 🤖 **AI-powered sentiment analysis** — uses Groq (Mistral) to analyze each mention
- 📊 **Interactive dashboard** — dark-themed UI with sentiment breakdown, score bars, and filters
- 🗄️ **Persistent storage** — saves all results to a local SQLite database
- 🔎 **Filter by sentiment & source** — quickly drill down into positive, negative, or neutral mentions
- ⚡ **Real-time progress** — shows live analysis progress while fetching

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| AI Analysis | Groq API (Mistral LLM) |
| Data Sources | HackerNews Algolia API + NewsAPI |
| Database | SQLite |
| Language | Python 3.x |

---

## 📁 Project Structure

```
brand_monitor/
├── main.py          ← Streamlit UI (dashboard)
├── database.py      ← SQLite setup, insert & fetch functions
├── fetcher.py       ← HackerNews + NewsAPI data fetching
├── analyzer.py      ← Groq AI sentiment analysis
├── pipeline.py      ← Connects fetcher + analyzer + database
├── requirements.txt ← Python dependencies
└── .env             ← API keys (not committed to GitHub)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/brand-monitor-system.git
cd brand-monitor-system
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys

Create a `.env` file in the root folder:
```
NEWS_API_KEY=your_newsapi_key_here
GROQ_API_KEY=your_groq_key_here
```

Get your free API keys from:
- NewsAPI → [newsapi.org](https://newsapi.org/register)
- Groq → [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run main.py
```

---

## 🖥️ How to Use

1. Enter a brand name in the sidebar (e.g. `Tesla`, `Apple`, `OpenAI`)
2. Click **Fetch & Analyze**
3. Watch the live progress as mentions are fetched and analyzed
4. View the sentiment dashboard with scores, breakdown, and all mentions
5. Use filters to drill into positive, negative, or neutral mentions

---

## 🌐 Deployment

This app is deployed on **Streamlit Community Cloud**.

👉 Link: https://brand-monitor-system-vwrfnl3b7yeccd2lzxnvwp.streamlit.app/
---

## 📸 Screenshots

> Add screenshots of your dashboard here after deployment.
<img width="1919" height="794" alt="image" src="https://github.com/user-attachments/assets/f1266064-9e53-49be-b7af-f64f2f9a0d5a" />
<img width="1861" height="813" alt="image" src="https://github.com/user-attachments/assets/9cf7cb3b-b018-4fa9-b5f5-1a9294b83042" />

---

## 🙋‍♂️ Author

**Nouhid Siddiqui**
- Computer Science Engineering Student
- Built as a Capstone Project

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
