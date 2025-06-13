import os
from datetime import datetime
from bs4 import BeautifulSoup
import json

# Config
BERITA_DIR = "berita"
OUTPUT_FILE = "index.html"
CONFIG_FILE = "config.json"
DEFAULT_IMAGE = "assets/default-image.jpg"

def load_config():
    """Load UI configuration"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def extract_article_data(html_path):
    """Extract structured data from HTML articles"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
            return {
                'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else "Judul Berita",
                'date': soup.find('time')['datetime'] if soup.find('time') else "",
                'image': (soup.find('meta', property='og:image') or 
                         soup.find('img', src=True))['content' if soup.find('meta', property='og:image') else 'src'],
                'source': soup.find(class_='source').get_text(strip=True) if soup.find(class_='source') else "",
                'summary': (soup.find('meta', property='description') or 
                            soup.find('meta', property='og:description'))['content'],
                'url': os.path.relpath(html_path, start='.')
            }
    except Exception as e:
        print(f"Error processing {html_path}: {str(e)}")
        return None

def generate_homepage():
    """Generate the Google Discover-style homepage"""
    config = load_config()
    articles = []
    
    # Collect all articles
    for root, _, files in os.walk(BERITA_DIR):
        for file in sorted(files, reverse=True):
            if file.endswith('.html'):
                article = extract_article_data(os.path.join(root, file))
                if article:
                    articles.append(article)
    
    # Generate HTML cards
    cards = []
    for article in articles[:config['max_articles']]:
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
                    <p class="card-description">{article['summary'][:120]}...</p>
                </a>
            </div>
            <div class="card-footer">
                {generate_footer_actions()}
            </div>
        </div>
        """)
    
    # Render complete page
    with open('templates/base.html', 'r') as f:
        html_template = f.read()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template.replace('<!-- CONTENT_PLACEHOLDER -->', '\n'.join(cards)))

if __name__ == "__main__":
    generate_homepage()

    # Generate Sitemap
def generate_sitemap(articles):
    with open('sitemap.xml', 'w') as f:
        f.write('''<?xml ...>\n''')
        for article in articles:
            f.write(f'''<url>\n<loc>https://.../{article['url']}</loc>\n...''')