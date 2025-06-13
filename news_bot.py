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

def generate_article(data):
    template_path = "templates/artikel_template.md"
    with open(template_path, "r") as f:
        template = Template(f.read())

    today = datetime.now().strftime("%Y-%m-%d")
    slug = data['title'].lower().replace(" ", "-")[:50]
    filename = f"berita/{today}-{slug}.md"

    output = template.render(
        title=data["title"],
        date=today,
        source_name=data["source"],
        url=data["url"],
        image_url="https://via.placeholder.com/1200x675?text=Berita+Otomatis",
        image_alt="Gambar Berita",
        summary=f"Berikut adalah ringkasan berita dari {data['source'].capitalize()}."
    )

    with open(filename, "w") as f:
        f.write(output)
    print(f"✅ Artikel dibuat: {filename}")

if __name__ == "__main__":
    os.makedirs("berita", exist_ok=True)
    for name, url in SOURCES.items():
        result = fetch_headline(name, url)
        if result:
            generate_article(result)