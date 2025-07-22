# RSS Job Feed 📡

[![Last Commit](https://img.shields.io/github/last-commit/cmaurice25/rss-job-feed)](https://github.com/cmaurice25/rss-job-feed)
[![License](https://img.shields.io/github/license/cmaurice25/rss-job-feed)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/cmaurice25/rss-job-feed)](https://github.com/cmaurice25/rss-job-feed)
# RSS Job Feed Summarizer

This project fetches the latest job listings from [We Work Remotely](https://weworkremotely.com/), summarizes them using Groq's LLaMA 3 model, and writes the summaries to a timestamped Google Doc inside a Drive folder.

## 🔧 Features
- Pulls top 5 remote jobs from WWR's RSS feed
- Summarizes each job using Groq's LLaMA 3.3-70B model
- Creates a new Google Doc with timestamped title
- Automatically stores the doc in a designated Drive folder

## 📁 Output Example
A Google Doc titled like:
WWR Job Feed - 2025-07-21 14:35

Each entry includes:
- Title
- Link
- Summary in bullet points

## 🚀 Tech Stack
- Python
- Google Docs & Drive API
- Groq API (LLaMA 3)
- Feedparser
- dotenv

## 📦 Local Setup
1. Clone this repo  
2. Create a `.env` file with your Groq API key: GROQ_API_KEY=your_api_key_herefa
3. Add your Google API `credentials.json`  
4. Run the script:python main.py
## 🛑 .gitignore Notes
Sensitive files excluded:
- `.env`
- `credentials.json`
- `token.json`
- `__pycache__/`
- `.venv/`
