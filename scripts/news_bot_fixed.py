import json
import os
from datetime import datetime
from markdown2 import markdown
from ai_rewriter import rewrite_article

def process_articles():
    """Main processing pipeline"""
    articles = load_articles()
    
    for article in articles:
        article['content'] = rewrite_article(article['content'])
        save_article(article)

def save_article(article):
    """Save in standardized HTML format"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>{article['title']}</title>
      <meta property="og:title" content="{article['title']}">
      <meta property="og:image" content="{article.get('image', '')}">
      <meta property="og:description" content="{article['content'][:100]}...">
    </head>
    <body>
      <article>
        <header>
          <h1>{article['title']}</h1>
          <div class="meta">
            <span class="source">{article['source']}</span>
            <time datetime="{article['date']}">{article['date']}</time>
          </div>
        </header>
        {f'<img src="{article["image"]}" alt="" class="article-image">' if article.get('image') else ''}
        <div class="content">
          {markdown(article['content'])}
        </div>
      </article>
    </body>
    </html>
    """
    
    date_dir = datetime.strptime(article['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    os.makedirs(f"berita/{date_dir}", exist_ok=True)
    
    with open(f"berita/{date_dir}/{generate_slug(article['title'])}.html", 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()



def render_html(berita_list):
    from markdown2 import markdown
    html_articles = ""
    for berita in berita_list:
        title = berita.get("judul", "Tanpa Judul")
        content = markdown(berita.get("isi", ""))
        published = berita.get("published", "")
        html_articles += f"<article><h2>{title}</h2><time>{published}</time>{content}</article>\n"

    html_template = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Berita Otomatis</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
        article {{ margin-bottom: 40px; }}
        h2 {{ color: #333; }}
        time {{ color: gray; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>Berita Otomatis</h1>
    {{articles}}
</body>
</html>"""
    html_output = html_template.replace("{{articles}}", html_articles)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)
