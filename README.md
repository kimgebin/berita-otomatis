
# 📰 Auto News Crawler

Sistem otomatis untuk mengambil berita terbaru dari RSS portal, rewrite menggunakan AI (DeepSeek / OpenAI), menyimpannya ke `berita.json`, dan menampilkan hasilnya di halaman web melalui GitHub Pages.

---

## 🔧 Fitur

- ✅ Ambil berita dari RSS Feed (contoh: BBC Indonesia)
- ✅ Rewrite otomatis menggunakan:
  - 🔹 DeepSeek AI (prioritas utama)
  - 🔹 OpenAI GPT (fallback jika DeepSeek gagal)
  - 🔹 Dummy rewrite (jika keduanya tidak aktif)
- ✅ Simpan hasil ke:
  - `berita.json` (semua artikel)
  - `berita_rewrite.log` (log hasil rewrite)
  - `preview_rewrite.html` (tampilan HTML hasil)
- ✅ Auto-generate halaman `index.html` untuk GitHub Pages
- ✅ Workflow GitHub Actions otomatis setiap jam

---

## 🚀 Cara Pakai

### 1. **Clone Repo**
```bash
git clone https://github.com/username/repo.git
```

### 2. **Isi Secrets GitHub**
Masukkan ke:
`Settings → Secrets → Actions`

- `DEEPSEEK_API_KEY` = `sk-...` (dari deepseek.com)
- `OPENAI_API_KEY` = `sk-...` (opsional, dari OpenAI)

### 3. **Deploy GitHub Pages**
- Aktifkan Pages di `Settings → Pages`
- Source = `main` branch → root
- Hasil akan muncul di `https://username.github.io/repo/`

---

## 📁 Struktur Output

| File | Deskripsi |
|------|-----------|
| `berita.json` | Semua artikel yang sudah diambil & di-rewrite |
| `preview_rewrite.html` | Tampilan HTML hasil rewrite |
| `index.html` | Template tampilan utama |
| `berita_rewrite.log` | Log setiap hasil rewrite |

---

## 📅 Cron Schedule

```yaml
schedule:
  - cron: '0 * * * *'  # Setiap jam (bisa ubah ke */15 untuk tiap 15 menit)
```

---

## 🧠 Teknologi

- Python 3.11
- feedparser
- requests
- openai
- GitHub Actions
