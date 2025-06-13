import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from jinja2 import Template

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'
}

SOURCES = {
    "detik": "https://www.detik.com/",
    "kompas": "https://www.kompas.com/",
    "cnn": "https://www.cnnindonesia.com/",
    "liputan6": "https://www.liputan6.com/"
}

def fetch_headline(site_name, url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        if site_name == "detik":
            headline = soup.find("h1") or soup.find("h2")
        elif site_name == "kompas":
            headline = soup.find("h2", class_="most__title") or soup.find("h1")
        elif site_name == "cnn":
            headline = soup.find("h2") or soup.find("h1")
        elif site_name == "liputan6":
            headline = soup.find("h4") or soup.find("h1")
        else:
            return None

        link = headline.find_parent("a")["href"] if headline and headline.find_parent("a") else url
        title = headline.get_text(strip=True) if headline else "Judul Tidak Ditemukan"
        return {"title": title, "url": link, "source": site_name}
    except Exception as e:
        print(f"Gagal fetch dari {site_name}: {e}")
        return None

def generate_markdown(data, slug, today):
    md_template_path = "templates/artikel_template.md"
    with open(md_template_path, "r") as f:
        template = Template(f.read())

    output = template.render(
        title=data["title"],
        date=today,
        source_name=data["source"],
        url=data["url"],
        image_url="https://via.placeholder.com/1200x675?text=Berita+Otomatis",
        image_alt="Gambar Berita",
        summary=f"Berikut adalah ringkasan berita dari {data['source'].capitalize()}."
    )

    md_path = f"berita/{today}-{slug}.md"
    with open(md_path, "w") as f:
        f.write(output)
    print(f"✅ Artikel markdown dibuat: {md_path}")

def generate_html(data, slug, today):
    html_template = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>{data['title']}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>{data['title']}</h1>
  <p><em>{today} · {data['source'].capitalize()}</em></p>
  <img src="https://via.placeholder.com/1200x675?text=Berita+Otomatis" alt="Gambar Berita" style="width:100%">
  <p>Berikut adalah ringkasan berita dari {data['source'].capitalize()}.</p>
  <p><a href="{data['url']}" target="_blank">➡️ Baca selengkapnya</a></p>
</body>
</html>"""

    html_path = f"berita/{today}-{slug}.html"
    with open(html_path, "w") as f:
        f.write(html_template.strip())
    print(f"✅ Artikel HTML dibuat: {html_path}")

if __name__ == "__main__":
    os.makedirs("berita", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    for name, url in SOURCES.items():
        result = fetch_headline(name, url)
        if result:
            slug = result['title'].lower().replace(" ", "-")[:50]
            generate_markdown(result, slug, today)
            generate_html(result, slug, today)