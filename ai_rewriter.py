import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def rewrite_article(original_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Kamu adalah penulis berita profesional."},
            {"role": "user", "content": f"Tulis ulang berita berikut agar lebih ringkas, natural, dan netral:

{original_text}"}
        ],
        temperature=0.7,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()