from openai import OpenAI
import os

# Ambil API Key dari variabel lingkungan
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_article(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah penulis berita profesional. Rewrite artikel di bawah agar lebih ringkas, padat, dan mudah dipahami."},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error rewrite: {e}")
        return None
