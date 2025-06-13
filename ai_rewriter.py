import os
import openai
from typing import Optional

# Konfigurasi API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def rewrite_article(original_text: str) -> Optional[str]:
    """
    Menulis ulang teks berita agar lebih ringkas, natural, dan netral menggunakan OpenAI GPT-3.5.
    
    Args:
        original_text (str): Teks berita asli yang akan ditulis ulang.
    
    Returns:
        str: Teks yang sudah ditulis ulang, atau None jika gagal.
    """
    try:
        # Validasi input
        if not original_text.strip():
            raise ValueError("Original text cannot be empty or whitespace.")
        
        # Call API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah penulis berita profesional yang ahli dalam merangkum dan menulis ulang konten."
                },
                {
                    "role": "user",
                    "content": f"""Tulis ulang berita berikut dengan ketentuan:
                    1. Ringkas (maksimal 3 paragraf)
                    2. Gunakan bahasa natural dan mudah dipahami
                    3. Bersikap netral tanpa opini pribadi
                    4. Pertahankan fakta inti

                    Teks asli:
                    {original_text}"""
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"[ERROR] Failed to rewrite article: {e}")
        return None

# Contoh penggunaan (untuk testing)
if __name__ == "__main__":
    test_text = "Contoh teks berita tentang teknologi terbaru..."
    rewritten = rewrite_article(test_text)
    if rewritten:
        print("Hasil rewrite:", rewritten)
    else:
        print("Gagal menulis ulang teks.")
