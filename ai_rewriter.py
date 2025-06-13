import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Pastikan variabel ini sudah diset di GitHub Actions

def rewrite_article(original_text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4",  # Bisa diganti ke gpt-3.5-turbo kalau ingin lebih cepat
        "messages": [
            {
                "role": "user",
                "content": f"Tulis ulang berita berikut agar lebih ringkas, natural, dan netral:\n\n{original_text}"
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()
