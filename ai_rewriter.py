import os
import requests

def rewrite_article(original_text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("Missing OPENAI_API_KEY environment variable")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"Tulis ulang berita berikut agar lebih ringkas, natural, dan netral:

{original_text}"
            }
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
