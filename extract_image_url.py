import requests
from bs4 import BeautifulSoup

def extract_image_url(article_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(article_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]

        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]

        return None
    except Exception as e:
        return None

# Contoh:
# print(extract_image_url("https://www.detik.com/xyz"))