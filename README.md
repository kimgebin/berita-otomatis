# 📰 Berita Otomatis

Sistem ini secara otomatis mengambil berita dari berbagai sumber (Detik, Kompas, dsb), merangkum/menulis ulang kontennya, dan mempublikasikan artikel ke repository ini secara berkala menggunakan GitHub Actions.

## 📌 Fitur Utama

- Crawl berita terbaru
- Auto-summary atau rewrite konten
- Generate file Markdown/HTML
- Auto commit ke repo GitHub
- Bisa dihubungkan ke GitHub Pages

## 🔧 Teknologi

- Python 3.x
- GitHub Actions
- BeautifulSoup / Newspaper3k
- Optional: OpenAI API (untuk rewrite)
- Optional: DeepSeek API (untuk rewrite)

## 📁 Struktur Direktori

## 🚀 Cara Kerja

1. Script Python mengambil artikel terbaru
2. Artikel diubah menjadi format `.md` atau `.html`
3. File otomatis di-commit ke GitHub
4. Bisa tampil di GitHub Pages (static site)

## 📄 Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detailnya.
