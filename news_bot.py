import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from extract_image_url import extract_image_url
from ai_rewriter import rewrite_article

# Dummy example data (replace with real scraping logic)
def get_articles():
    return [
        {
            "title": "Contoh Judul Berita",
            "link": "https://example.com/artikel-asli",
            "content": "Ini isi ringkasan atau artikel lengkap.",
            "slug": "contoh-judul-berita"
        }
    ]

def save_as_html(article):
    tanggal = datetime.today().strftime("%Y-%m-%d")
    folder = "berita"
    os.makedirs(folder, exist_ok=True)
    filename = f"{tanggal}-{article['slug']}.html"
    path = os.path.join(folder, filename)

    # Rewrite isi artikel
    rewritten = rewrite_article(article["content"])

    # Ambil gambar dari artikel asli
    image_url = extract_image_url(article["link"])

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>{article['title']}</title>
        <meta name="description" content="{rewritten[:150]}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {'<meta property="og:image" content="' + image_url + '">' if image_url else ''}
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 720px;
                margin: 40px auto;
                padding: 20px;
                background: #fff;
                color: #222;
                line-height: 1.6;
            }}
            img {{
                max-width: 100%;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>{article['title']}</h1>
        {'<img src="' + image_url + '">' if image_url else ''}
        <p>{rewritten}</p>
        <hr>
        <small>Source: <a href="{article['link']}" target="_blank">{article['link']}</a></small>
    </body>
    </html>
    """

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    articles = get_articles()
    for article in articles:
        save_as_html(article)

if __name__ == "__main__":
    main()