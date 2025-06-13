import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def rewrite_article(original_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"""Tulis ulang berita berikut agar lebih ringkas, natural, dan netral:

{original_text}"""
            }
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()