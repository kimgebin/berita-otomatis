import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # Pastikan sudah diset di GitHub Secrets

def rewrite_article(original_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah asisten yang bisa menulis ulang artikel berita agar lebih ringkas dan netral."
                },
                {
                    "role": "user",
                    "content": f"""Tulis ulang berita berikut agar lebih ringkas, natural, dan netral:
                    {text}"""

{original_text}"
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return original_text  # fallback
