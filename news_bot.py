import json
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from ai_rewriter import rewrite_article

def load_articles(file_path="berita.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_slug(title):
    return (
        title.lower()
        .replace(" ", "-")
        .replace(".", "")
        .replace(",", "")
        .replace(":", "")
        .replace("?", "")
        .replace("!", "")
    )

def save_as_html(article):
    today = datetime.today().strftime("%Y-%m-%d")
    slug = generate_slug(article["title"])
    rewritten = rewrite_article(article["content"])

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{article["title"]}">
  <meta name="keywords" content="berita terkini, update, indonesia">
  <meta name="author" content="AutoNewsBot">
  <title>{article["title"]}</title>
</head>
<body>
  <h1>{article["title"]}</h1>
  <p><em>{article["date"]} - {article["source"]}</em></p>
  <img src="{article["image"]}" alt="thumbnail" width="100%">
  <div>{rewritten}</div>
</body>
</html>
"""

    folder_path = f"berita/{today}"
    os.makedirs(folder_path, exist_ok=True)

    with open(f"{folder_path}/{today}-{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    articles = load_articles()
    for article in articles:
        save_as_html(article)

if __name__ == "__main__":
    main()