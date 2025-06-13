import os
import json
from datetime import datetime
from ai_rewriter import rewrite_article

def save_as_html(article):
    slug = article["slug"]
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"berita/{today}-{slug}.html"
    content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{article['title']}</title>
</head>
<body>
  <h1>{article['title']}</h1>
  <img src="{article['image']}" alt="image" width="100%" />
  <p>{article['summary']}</p>
  <hr/>
  <article>
    {article['content']}
  </article>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    with open("berita.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    for article in articles:
        rewritten = rewrite_article(article["content"])
        article["content"] = rewritten
        save_as_html(article)

if __name__ == "__main__":
    main()
