import os
import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"
API_KEY = os.getenv("GROQ_API_KEY")


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
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(API_URL, headers=headers, json=body)
    print("🚨 GROQ RESPONSE STATUS:", response.status_code)
    print("🚨 GROQ RESPONSE BODY:", response.text)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()
