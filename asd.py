# -------------------------------------------------
#  diagnostic_groq.py
# -------------------------------------------------
import os
import sys
import json
import requests
from dotenv import load_dotenv

# ---------- 1️⃣ Load and clean the API key ----------
load_dotenv()
key = os.getenv("GROQ_API_KEY")
if not key:
    sys.stderr.write("❌ GROQ_API_KEY not set in .env\n")
    sys.exit(1)

# Remove *any* surrounding whitespace or new‑lines
key = key.strip()
if "\n" in key or "\r" in key:
    sys.stderr.write("❌ Your key contains hidden newline characters!\n")
    sys.exit(1)

# ---------- 2️⃣ Build the request ----------
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Accept": "application/json",          # optional but harmless
}
payload = {
    "model": "llama-3.1-8b-instant",            # <-- make sure this exact string appears in your Groq dashboard
    "messages": [
        {"role": "system", "content": "You are an academic advisor for university students."},
        {"role": "user",   "content": "Hello, how are you?"}
    ],
    "temperature": 0.4
}

# ---------- 3️⃣ Send the request ----------
try:
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()                     # raises on 4xx/5xx
except requests.exceptions.HTTPError:
    # ----------- 4️⃣ Print the *exact* error payload ----------
    print("\n⚠️  Groq responded with a 4xx/5xx status code.")
    try:
        err_json = resp.json()
        print("Response JSON:")
        print(json.dumps(err_json, indent=2))
    except Exception:
        # If Groq didn’t return JSON, show the raw text (truncated)
        print("Response text (first 500 chars):")
        print(resp.text[:500])
    # re‑raise so you still see the traceback if you want
    raise

# ---------- 5️⃣ Success – print the answer ----------
data = resp.json()
answer = data["choices"][0]["message"]["content"]
print("\n✅ Assistant reply:")
print(answer)