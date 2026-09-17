# 🤖 Taufik AI - Python Project (Versi Python dari index.html)

Aplikasi Chatbot Cerdas **Taufik AI** versi bahasa pemrograman Python. Proyek ini merupakan konversi dan pengembangan dari versi web `index.html`, mengintegrasikan antarmuka interaktif, akselerasi LPU Groq Cloud, streaming respon secara langsung (*real-time typing*), dan pembaca dokumen proyek.

---

## 📁 Struktur File di Folder `Phyton Project/`

* **`app.py`** : Aplikasi Web interaktif berbasis **Streamlit** (antarmuka grafis mirip `index.html`).
* **`main.py`** : Aplikasi Chatbot versi **Terminal / Console CLI** (bisa langsung dijalankan via CMD/PowerShell).
* **`groq_client.py`** : Modul komunikasi ke Groq API (mendukung *multi-model failover*, *streaming*, dan *error handling*).
* **`config.py`** : Modul konfigurasi API Key, daftar model Groq, dan System Prompt Taufik AI.
* **`Proposal_Project_Taufik_AI.docx`** : Proposal resmi proyek Taufik AI versi bahasa Python.
* **`Laporan_Akhir_Project_Taufik_AI.docx`** : Laporan akhir pelaksanaan sistem Taufik AI versi bahasa Python.
* **`Laporan_Perjalanan_Proyek_Taufik_AI (2).docx`** : Laporan perjalanan lengkap perancangan, library, dan langkah pembuatan chatbot Python.
* **`Profile.jpg`** : Foto avatar profil Taufik AI.
* **`requirements.txt`** : Daftar pustaka Python yang diperlukan (`streamlit`, `requests`, `python-dotenv`, `python-docx`).

---

## 🚀 Cara Menjalankan

Buka terminal atau PowerShell di dalam folder `Phyton Project` (atau arahkan ke folder ini).

### 1. Menjalankan Versi Web (Streamlit UI) 🌐
Gunakan perintah:
```bash
streamlit run app.py
```
> Peramban web (browser) akan terbuka secara otomatis di alamat `http://localhost:8501`.

**Fitur pada Versi Web:**
* Tampilan modern dengan tema gradien ungu/biru glassmorphism khas Taufik AI.
* Foto avatar `Profile.jpg` pada respon chatbot.
* Efek teks mengetik secara langsung (*real-time token streaming*).
* Pilihan pergantian model AI Groq secara instan dari bilah samping (*sidebar*).
* Menu unduh dan tinjau dokumen resmi (*Proposal*, *Laporan Akhir*, dan *Laporan Perjalanan*).
* Tombol untuk membersihkan riwayat chat (*Reset Chat*).

---

### 2. Menjalankan Versi Terminal (CLI Mode) 💻
Jika Anda ingin mengobrol langsung dari terminal/command prompt tanpa membuka browser:
```bash
python main.py
```

**Perintah khusus di terminal:**
* Ketik `keluar` atau `exit` untuk keluar dari aplikasi.
* Ketik `reset` atau `clear` untuk menghapus riwayat obrolan.
* Ketik `model` untuk memilih model Groq lain.

---

## ⚙️ Pengaturan API Key

Secara otomatis sistem membaca kunci API dari:
1. Variabel lingkungan sistem: `GROQ_API_KEY`
2. Atau file `config.js` di root folder
3. Atau melalui kotak input di Sidebar aplikasi Streamlit.

Model utama yang digunakan adalah `llama-3.3-70b-versatile` dengan auto-fallback ke model cadangan `llama-3.1-8b-instant` dan varian Llama lainnya.
