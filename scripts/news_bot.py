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