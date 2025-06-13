import os
import json
import feedparser
from datetime import datetime
from typing import List, Dict
from ai_rewriter import rewrite_article  # Pastikan file ini ada di folder yang sama

# Konfigurasi
RSS_FEED_URL = "https://example-news-site.com/rss"  # Ganti dengan RSS/API nyata
JSON_FILE = "berita.json"

def load_articles(file_path: str = JSON_FILE) -> List[Dict]:
    """Load artikel dari JSON atau buat file baru jika tidak ada."""
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Gagal memuat artikel: {e}")
        return []

def save_articles(articles: List[Dict], file_path: str = JSON_FILE) -> bool:
    """Simpan artikel ke JSON."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan artikel: {e}")
        return False

def fetch_new_articles() -> List[Dict]:
    """Fetch berita terbaru dari RSS Feed (ganti URL dengan sumber nyata)."""
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        return [
            {
                "id": entry.get("id", entry.link),
                "title": entry.title,
                "content": entry.description,
                "source": entry.link,
                "published": entry.get("published", ""),
                "raw_date": datetime.now().isoformat()
            }
            for entry in feed.entries
        ]
    except Exception as e:
        print(f"[ERROR] Gagal fetch berita: {e}")
        return []

def is_article_exist(article: Dict, existing_articles: List[Dict]) -> bool:
    """Cek duplikat berdasarkan source + published date."""
    return any(
        a["source"] == article["source"] and 
        a["published"] == article["published"]
        for a in existing_articles
    )

def process_articles():
    """Proses utama: fetch, rewrite, dan simpan artikel."""
    existing_articles = load_articles()
    new_articles = fetch_new_articles()

    for article in new_articles:
        if is_article_exist(article, existing_articles):
            print(f"[SKIP] Artikel sudah ada: {article['title']}")
            continue
        
        rewritten = rewrite_article(article["content"])
        if rewritten:
            article["rewritten_content"] = rewritten
            existing_articles.append(article)
            print(f"[ADDED] Berhasil menambah: {article['title']}")

    if save_articles(existing_articles):
        print(f"[SUCCESS] Total artikel: {len(existing_articles)}")
        return True
    return False

if __name__ == "__main__":
    print("=== MEMULAI PROSES ===")
    if process_articles():
        print("Proses selesai sukses!")
    else:
        print("Proses gagal!", file=sys.stderr)
        sys.exit(1)
