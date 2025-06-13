import os
import json
from typing import List, Dict
from ai_rewriter import rewrite_article  # Pastikan file ai_rewriter.py ada di direktori yang sama

def load_articles(file_path: str = "berita.json") -> List[Dict]:
    """
    Memuat artikel dari file JSON. Jika file tidak ada, buat file baru kosong.
    
    Args:
        file_path (str): Path ke file JSON. Default: 'berita.json'.
    
    Returns:
        List[Dict]: Daftar artikel dalam bentuk list of dictionaries.
    """
    try:
        # Jika file tidak ada, buat file kosong
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        # Baca file
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    except json.JSONDecodeError:
        print(f"[ERROR] File {file_path} bukan format JSON valid. Mengembalikan list kosong.")
        return []
    except Exception as e:
        print(f"[ERROR] Gagal memuat file: {e}")
        return []

def save_articles(articles: List[Dict], file_path: str = "berita.json") -> bool:
    """
    Menyimpan artikel ke file JSON.
    
    Args:
        articles (List[Dict]): Daftar artikel yang akan disimpan.
        file_path (str): Path ke file JSON. Default: 'berita.json'.
    
    Returns:
        bool: True jika berhasil, False jika gagal.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file: {e}")
        return False

def fetch_new_articles() -> List[Dict]:
    """
    Fungsi simulasi untuk mengambil artikel baru dari sumber eksternal (contoh: RSS/API).
    Ganti dengan implementasi sesuai kebutuhan.
    
    Returns:
        List[Dict]: Daftar artikel baru.
    """
    # Contoh data dummy (ganti dengan logika sebenarnya)
    return [
        {
            "id": 1,
            "title": "Contoh Berita Terbaru",
            "content": "Ini adalah contoh konten berita yang akan ditulis ulang...",
            "source": "https://example.com"
        }
    ]

def process_articles() -> bool:
    """
    Proses utama: Memuat, memproses, dan menyimpan artikel.
    
    Returns:
        bool: True jika semua langkah berhasil.
    """
    try:
        # 1. Muat artikel yang ada
        existing_articles = load_articles()
        print(f"[INFO] Memuat {len(existing_articles)} artikel yang ada.")
        
        # 2. Ambil artikel baru
        new_articles = fetch_new_articles()
        print(f"[INFO] Menemukan {len(new_articles)} artikel baru.")
        
        # 3. Proses setiap artikel baru
        for article in new_articles:
            # Skip jika artikel sudah ada (berdasarkan ID/judul)
            if any(a.get("id") == article.get("id") for a in existing_articles):
                print(f"[SKIP] Artikel ID {article.get('id')} sudah ada.")
                continue
            
            # Tulis ulang konten menggunakan AI
            rewritten_content = rewrite_article(article["content"])
            if rewritten_content:
                article["rewritten_content"] = rewritten_content
                article["processed_at"] = datetime.now().isoformat()
                existing_articles.append(article)
                print(f"[PROCESSED] Berhasil memproses artikel ID {article.get('id')}")
        
        # 4. Simpan hasil
        if save_articles(existing_articles):
            print(f"[SUCCESS] Berhasil menyimpan {len(existing_articles)} artikel.")
            return True
    
    except Exception as e:
        print(f"[ERROR] Proses gagal: {e}")
    
    return False

if __name__ == "__main__":
    from datetime import datetime
    import sys
    
    print("=== Memulai Proses Berita ===")
    success = process_articles()
    
    if not success:
        print("Proses selesai dengan error.", file=sys.stderr)
        sys.exit(1)
    
    print("Proses selesai sukses!")
