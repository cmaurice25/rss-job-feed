import feedparser
import os
from dotenv import load_dotenv
import requests
from utils.google_docs import create_doc_in_folder, append_to_doc

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
print("API KEY LOADED:", API_KEY[:8] + "...")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
RSS_URL = "https://weworkremotely.com/remote-jobs.rss"


def fetch_feed_entries(rss_url):
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]


def summarize_job(entry):
    prompt = f"""Summarize the following remote job posting in 3–4 bullet points with key details:
- Role and company
- Remote status and location if listed
- Required skills or tech stack
- Any standout info (salary, seniority, contract type, etc.)

Title: {entry.title}
Summary: {entry.summary}
Link: {entry.link}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes job listings.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.3,
    }

    response = requests.post(API_URL, headers=headers, json=body)

    # Debugging output
    print("🚨 GROQ RESPONSE STATUS:", response.status_code)
    print("🚨 GROQ RESPONSE BODY:", response.text)

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def main():
    print("🔍 Fetching remote job listings from We Work Remotely...")
    entries = fetch_feed_entries(RSS_URL)

    # Generate title like "WWR Job Feed - 2025-07-21 14:35"

    folder_name = "RSS WWR Job Feed"
    print(f"📄 Creating new Google Doc inside '{folder_name}' folder...")
    document_id = create_doc_in_folder(folder_name)

    for entry in entries:
        print("\n==============================")
        print(f"🔗 {entry.link}")
        print(f"📝 {entry.title}")
        summary = summarize_job(entry)
        print("📌 Summary:")
        print(summary)
        print("==============================")

        full_entry = f"🔗 {entry.link}\n📝 {entry.title}\n📌 {summary}\n\n"
        append_to_doc(document_id, full_entry)


if __name__ == "__main__":
    main()
