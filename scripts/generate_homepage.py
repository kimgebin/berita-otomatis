#!/usr/bin/env python3
import os
from datetime import datetime
from bs4 import BeautifulSoup
import json

# Configuration
BERITA_DIR = "berita"
OUTPUT_FILE = "index.html"
CONFIG_FILE = "config.json"
DEFAULT_IMAGE = "assets/default-image.jpg"

def load_config():
    """Load configuration from JSON file"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {
            "max_articles": 20,
            "ui_settings": {
                "card_style": "discover",
                "dark_mode": False
            }
        }

def extract_metadata(filepath):
    """Extract structured data from HTML articles"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
            return {
                'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else "Judul Berita",
                'date': soup.find('time')['datetime'] if soup.find('time') else "",
                'image': (soup.find('meta', property='og:image') or 
                         soup.find('img', src=True))['content' if soup.find('meta', property='og:image') else 'src'],
                'source': soup.find(class_='source').get_text(strip=True) if soup.find(class_='source') else "",
                'summary': (soup.find('meta', property='description') or 
                            soup.find('meta', property='og:description'))['content'],
                'url': os.path.relpath(filepath, start='.')
            }
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return None

def format_date(date_str):
    """Format date for display"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d %b %Y')
    except:
        return "Hari ini"

def generate_footer_actions():
    """Generate interactive footer buttons"""
    return """
    <div class="footer-action">
        <span class="material-icons footer-icon">bookmark_border</span>
        <span>Simpan</span>
    </div>
    <div class="footer-action">
        <span class="material-icons footer-icon">share</span>
        <span>Bagikan</span>
    </div>
    """

def load_template():
    """Load HTML template with fallback"""
    try:
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: Using fallback template")
        return """<!DOCTYPE html>
<html>
<head>
    <title>Berita Otomatis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .card { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <!-- CONTENT_PLACEHOLDER -->
</body>
</html>"""

def generate_sitemap(articles):
    """Generate dynamic sitemap.xml"""
    try:
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            f.write('  <url>\n    <loc>https://kimgebin.github.io/berita-otomatis/</loc>\n    <changefreq>hourly</changefreq>\n  </url>\n')
            
            for article in articles:
                if article and article.get('url'):
                    f.write(f'  <url>\n    <loc>https://kimgebin.github.io/berita-otomatis/{article["url"]}</loc>\n')
                    f.write(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n  </url>\n')
            
            f.write('</urlset>')
    except Exception as e:
        print(f"Error generating sitemap: {str(e)}")

def generate_homepage():
    """Generate the Google Discover-style homepage"""
    config = load_config()
    articles = []
    
    # Collect articles
    for root, _, files in os.walk(BERITA_DIR):
        for file in sorted(files, reverse=True):
            if file.endswith('.html'):
                article = extract_metadata(os.path.join(root, file))
                if article:
                    articles.append(article)
    
    # Generate HTML cards
    cards = []
    for article in articles[:config.get('max_articles', 20)]:
        cards.append(f"""
        <div class="card">
            <img src="{article['image'] or DEFAULT_IMAGE}" 
                 class="card-image" 
                 alt="{article['title']}">
            <div class="card-content">
                <div class="card-source">
                    <div class="source-icon" 
                         style="background-image: url('{article['image'] or DEFAULT_IMAGE}')"></div>
                    <span class="source-name">{article['source']}</span>
                    <span class="card-time">{format_date(article['date'])}</span>
                </div>
                <a href="{article['url']}" class="card-link">
                    <h3 class="card-title">{article['title']}</h3>
                    <p class="card-description">{article.get('summary', '')[:120]}...</p>
                </a>
            </div>
            <div class="card-footer">
                {generate_footer_actions()}
            </div>
        </div>
        """)
    
    # Render complete page
    template = load_template()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(template.replace('<!-- CONTENT_PLACEHOLDER -->', '\n'.join(cards)))
    
    # Generate sitemap
    generate_sitemap(articles)

if __name__ == "__main__":
    generate_homepage()