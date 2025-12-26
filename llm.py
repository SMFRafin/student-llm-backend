import os, requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY missing")

def call_llm(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are an academic advisor for university students."},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.4
    }

    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
