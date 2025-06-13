
import os
import time
import requests
from openai import OpenAI

# --- KONFIGURASI ---
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY") or "sk-48e03e53410e46b8b48a5b15f1b29814"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_KEY)
client_openai = OpenAI(api_key=OPENAI_KEY) if USE_OPENAI else None

LOG_FILE = "berita_rewrite.log"
HTML_FILE = "preview_rewrite.html"

def log_result(status, title, source, model_used):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{status}] {model_used} | {title} | {source}\n")

def append_html(title, content, source):
    with open(HTML_FILE, "a", encoding="utf-8") as f:
        f.write(f"<h2>{title}</h2><p>{content}</p><a href='{source}' target='_blank'>Sumber</a><hr>\n")

def rewrite_with_deepseek(text: str, retries=3) -> str:
    for attempt in range(retries):
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "Kamu adalah penulis berita profesional. Tulis ulang artikel ini secara padat dan mudah dipahami."},
                        {"role": "user", "content": text}
                    ],
                    "temperature": 0.7
                }
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            elif response.status_code == 429:
                print("DeepSeek rate limited, retrying...")
                time.sleep(3)
            else:
                print(f"DeepSeek error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"DeepSeek exception: {e}")
            return None
    return None

def rewrite_with_openai(text: str, retries=3) -> str:
    for attempt in range(retries):
        try:
            if not client_openai:
                print("OpenAI client not initialized.")
                return None
            response = client_openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Kamu adalah penulis berita profesional. Tulis ulang artikel ini secara padat dan mudah dipahami."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "429" in str(e):
                print("OpenAI rate limited, retrying...")
                time.sleep(3)
            else:
                print(f"OpenAI exception: {e}")
                return None
    return None

def rewrite_article(text: str, title: str = "", source: str = "") -> str:
    rewritten = rewrite_with_deepseek(text)
    if rewritten:
        log_result("OK", title, source, "DeepSeek")
        append_html(title, rewritten, source)
        return rewritten

    print("Fallback to OpenAI...")
    if USE_OPENAI:
        rewritten = rewrite_with_openai(text)
        if rewritten:
            log_result("OK", title, source, "OpenAI")
            append_html(title, rewritten, source)
            return rewritten

    log_result("FAIL", title, source, "None")
    return None
