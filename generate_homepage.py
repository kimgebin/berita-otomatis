
import os
from datetime import datetime

BERITA_DIR = "berita"
OUTPUT_FILE = "index.html"

def extract_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if "<title>" in line:
                    return line.replace("<title>", "").replace("</title>", "").strip()
                if "<h1>" in line:
                    return line.replace("<h1>", "").replace("</h1>", "").strip()
    except:
        return "Berita"
    return "Berita"

def extract_date_from_filename(filename):
    try:
        return datetime.strptime(filename[:10], "%Y-%m-%d").strftime("%d %B %Y")
    except:
        return "Tidak diketahui"

def generate_homepage():
    articles = []
    for fname in sorted(os.listdir(BERITA_DIR), reverse=True):
        if fname.endswith(".html"):
            filepath = os.path.join(BERITA_DIR, fname)
            title = extract_title(filepath)
            date = extract_date_from_filename(fname)
            url = os.path.join(BERITA_DIR, fname)
            articles.append(f'''
            <div class="card">
              <a href="{url}">
                <div class="card-content">
                  <div class="card-title">{title}</div>
                  <div class="card-meta">{date}</div>
                </div>
              </a>
            </div>
            ''')

    page_start = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Berita Otomatis</title>
  <style>
    body {
      font-family: 'Helvetica Neue', sans-serif;
      margin: 0;
      background: #f7f7f7;
      color: #222;
    }
    header {
      background: #fff;
      padding: 1rem 1.5rem;
      font-size: 1.5rem;
      font-weight: bold;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .container {
      max-width: 800px;
      margin: auto;
      padding: 1.5rem;
    }
    .card {
      background: white;
      border-radius: 10px;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 10px rgba(0,0,0,0.05);
      transition: 0.3s;
    }
    .card:hover {
      box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    .card-content {
      padding: 1rem;
    }
    .card-title {
      font-size: 1.1rem;
      margin: 0 0 0.5rem;
      font-weight: 600;
    }
    .card-meta {
      font-size: 0.85rem;
      color: #888;
      margin-bottom: 0.5rem;
    }
    .card a {
      text-decoration: none;
      color: inherit;
    }
  </style>
</head>
<body>
  <header>📰 Berita Otomatis</header>
  <div class="container">
"""

    page_end = """
  </div>
</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(page_start + ''.join(articles) + page_end)

if __name__ == "__main__":
    generate_homepage()
