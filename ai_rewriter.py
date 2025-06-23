import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


import os
import requests
from openai import OpenAI

# --- KONFIGURASI ---
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-48e03e53410e46b8b48a5b15f1b29814"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # Pastikan ini tersedia di Secrets
USE_OPENAI = bool(OPENAI_KEY)
client_openai = OpenAI(api_key=OPENAI_KEY) if USE_OPENAI else None

def rewrite_with_deepseek(text: str) -> str:
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Kamu adalah penulis berita profesional. Tulis ulang artikel ini secara padat dan mudah dipahami."},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.7
            }
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"DeepSeek error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"DeepSeek exception: {e}")
        return None

def rewrite_with_openai(text: str) -> str:
    try:
        if not client_openai:
            print("OpenAI client not initialized.")
            return None
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah penulis berita profesional. Tulis ulang artikel ini secara padat dan mudah dipahami."},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI exception: {e}")
        return None

def rewrite_article(text: str) -> str:
    rewritten = rewrite_with_deepseek(text)
    if rewritten:
        return rewritten

    print("Fallback to OpenAI...")
    if USE_OPENAI:
        rewritten = rewrite_with_openai(text)
        if rewritten:
            return rewritten

    return None
