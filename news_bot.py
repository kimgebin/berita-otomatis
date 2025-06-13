import os
import json
import feedparser
from datetime import datetime
from typing import List, Dict
from ai_rewriter import rewrite_article

# Konfigurasi (GANTI DENGAN SUMBER NYATA)
RSS_FEED_URL = "https://www.bbc.com/indonesia/index.xml"  # Contoh RSS BBC
JSON_FILE = "berita.json"

def log(message: str):
    """Helper untuk logging."""
    print(f"[{datetime.now().isoformat()}] {message}")

def load_articles(file_path: str = JSON_FILE) -> List[Dict]:
    """Load artikel dari JSON. Buat file baru jika tidak ada."""
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            log(f"File {file_path} dibuat baru.")
            return []
        
        with open(file_path, "r", encoding="utf-8") as f:
            articles = json.load(f)
            log(f"Memuat {len(articles)} artikel dari {file_path}.")
            return articles
            
    except Exception as e:
        log(f"Gagal memuat artikel: {str(e)}")
        return []

def save_articles(articles: List[Dict], file_path: str = JSON_FILE) -> bool:
    """Simpan artikel ke JSON."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        log(f"Berhasil menyimpan {len(articles)} artikel ke {file_path}.")
        return True
    except Exception as e:
        log(f"Gagal menyimpan artikel: {str(e)}")
        return False

def fetch_new_articles() -> List[Dict]:
    """Fetch berita terbaru dari RSS Feed."""
    try:
        log(f"Memulai fetch dari {RSS_FEED_URL}...")
        feed = feedparser.parse(RSS_FEED_URL)
        
        new_articles = []
        for entry in feed.entries[:5]:  # Ambil 5 artikel terbaru saja
            article = {
                "id": entry.get("id", entry.link),
                "title": entry.title,
                "content": entry.description or entry.title,
                "source": entry.link,
                "published": entry.get("published", datetime.now().isoformat()),
                "fetched_at": datetime.now().isoformat()
            }
            new_articles.append(article)
        
        log(f"Berhasil fetch {len(new_articles)} artikel baru.")
        return new_articles
        
    except Exception as e:
        log(f"Gagal fetch artikel: {str(e)}")
        return []

def is_duplicate(article: Dict, existing_articles: List[Dict]) -> bool:
    """Cek duplikat berdasarkan URL sumber."""
    return any(a["source"] == article["source"] for a in existing_articles)

def process_articles():
    """Proses utama: fetch, rewrite, simpan."""
    existing_articles = load_articles()
    new_articles = fetch_new_articles()
    
    added_count = 0
    for article in new_articles:
        if is_duplicate(article, existing_articles):
            log(f"Artikel sudah ada: {article['title']}")
            continue
        
        rewritten = rewrite_article(article["content"])
        if rewritten:
            article["rewritten_content"] = rewritten
            existing_articles.append(article)
            added_count += 1
            log(f"Artikel ditambahkan: {article['title']}")
    
    if added_count > 0:
        if save_articles(existing_articles):
            log(f"Total artikel sekarang: {len(existing_articles)}")
            return True
    else:
        log("Tidak ada artikel baru yang ditambahkan.")
    
    return False

if __name__ == "__main__":
    import sys
    log("=== MEMULAI PROSES ===")
    success = process_articles()
    log("=== PROSES SELESAI ===")
    sys.exit(0 if success else 1)
