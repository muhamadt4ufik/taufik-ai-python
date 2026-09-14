import os
import streamlit as st
from pathlib import Path
from groq_client import GroqClient
from config import AVAILABLE_MODELS, DEFAULT_MODEL, get_secret_api_key, SYSTEM_PROMPT

# Set page configuration
st.set_page_config(
    page_title="Taufik AI - Asisten Cerdas",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
AVATAR_PATH = BASE_DIR / "Profile.jpg"
if not AVATAR_PATH.exists():
    AVATAR_PATH = PARENT_DIR / "Profile.jpg"

# Custom CSS matching index.html glassmorphism & gradients
st.markdown("""
<style>
    /* Header Gradient */
    .taufik-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 18px 24px;
        border-radius: 16px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.25);
    }
    .taufik-header h1 {
        color: white !important;
        margin: 0;
        font-size: 24px;
        font-weight: 700;
    }
    .taufik-header p {
        margin: 2px 0 0 0;
        font-size: 13px;
        opacity: 0.9;
        color: white !important;
    }
    .status-badge {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 10px;
        height: 10px;
        background-color: #4ade80;
        border-radius: 50%;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Halo! Saya **Taufik AI**. Ada yang bisa saya bantu hari ini? Silahkan Anda bertanya apapun!"
        }
    ]

# Ambil API key secara rahasia di backend tanpa menampilkannya di layar
api_key = get_secret_api_key()

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

# Sidebar
with st.sidebar:
    st.title("⚙️ Pengaturan & Menu")

    # Status Keamanan Sistem (Tanpa menampilkan isi kunci sama sekali)
    st.success("🔒 Sistem Aktif & Terlindungi")

    # Pemilihan Model
    st.markdown("### 🤖 Model AI Engine")
    st.session_state.selected_model = st.selectbox(
        "Pilih Model Groq:",
        options=AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(st.session_state.selected_model) if st.session_state.selected_model in AVAILABLE_MODELS else 0
    )

    st.caption(f"⚡ Akselerasi LPU via Groq Cloud ({st.session_state.selected_model})")

    st.divider()

    # Tombol Reset Chat
    if st.button("🧹 Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Halo! Riwayat percakapan telah dibersihkan. Silakan ajukan pertanyaan baru!"
            }
        ]
        st.rerun()

    st.divider()

    # Menu Dokumen Proyek
    st.markdown("### 📑 Dokumen Proyek Taufik AI")
    docs = [
        ("📋 Proposal Proyek", "Proposal_Project_Taufik_AI.docx"),
        ("📊 Laporan Akhir", "Laporan_Akhir_Project_Taufik_AI.docx"),
        ("🗺️ Laporan Perjalanan (2)", "Laporan_Perjalanan_Proyek_Taufik_AI (2).docx"),
    ]

    for label, filename in docs:
        file_path = BASE_DIR / filename
        if not file_path.exists():
            file_path = PARENT_DIR / filename

        if file_path.exists():
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ Unduh {label}",
                    data=f.read(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.info(f"{label} (Tersedia di server)")

# Main Layout
col_head, col_badge = st.columns([3, 1])

with col_head:
    st.markdown(f"""
    <div class="taufik-header">
        <div>
            <h1>🤖 Taufik AI</h1>
            <p>Powered by Groq • Model: <b>{st.session_state.selected_model}</b></p>
        </div>
        <div class="status-badge">
            <span class="status-dot"></span> Online & Siap
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tabs untuk Chatbot dan Penjelajah Dokumen
tab_chat, tab_docs = st.tabs(["💬 Jendela Chatbot", "📖 Ringkasan Dokumen Proyek"])

with tab_chat:
    bot_avatar = str(AVATAR_PATH) if AVATAR_PATH.exists() else "🤖"

    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = bot_avatar if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Tulis pesan untuk Taufik AI..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Client Groq menggunakan API key yang tersimpan aman di server
        client = GroqClient(api_key=api_key)

        with st.chat_message("assistant", avatar=bot_avatar):
            recent_context = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[-8:]
            ]

            message_placeholder = st.empty()
            full_response = ""

            try:
                for chunk in client.send_chat_stream(recent_context, model=st.session_state.selected_model):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                err_msg = f"❌ Terjadi kesalahan: {str(e)}"
                message_placeholder.markdown(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

with tab_docs:
    st.markdown("### 📚 Dokumen Resmi Proyek Taufik AI")
    st.info("Dokumen resmi proyek Taufik AI berbasis Python murni (Streamlit, Requests, & Groq Cloud).")

    doc_tab1, doc_tab2, doc_tab3 = st.tabs([
        "📋 Proposal Proyek",
        "📊 Laporan Akhir Pelaksanaan",
        "🗺️ Laporan Perjalanan Proyek"
    ])

    with doc_tab1:
        st.markdown("""
        #### 📋 PROPOSAL PROYEK: RANCANG BANGUN CHATBOT TAUFIK AI (PYTHON)
        * **Nama Proyek:** Taufik AI (Intelligent Virtual Assistant - Python Edition)
        * **Pengembang:** Muhamad Taufik
        * **Tujuan:** Membangun asisten AI berbasis LLM dengan latensi ultra-rendah memanfaatkan akselerasi hardware Groq LPU dalam ekosistem Python.
        * **Fitur Utama:**
          - Natural Language Processing (NLP) tingkat lanjut.
          - Kecepatan respons instan (>300 token/detik).
          - Multi-model failover otomatis untuk menjamin reliabilitas 24/7.
          - Real-Time Token Streaming (efek mengetik kata demi kata).
        """)

    with doc_tab2:
        st.markdown("""
        #### 📊 LAPORAN AKHIR PELAKSANAAN PROYEK
        * **Arsitektur Sistem:**
          - **Antarmuka Utama:** Python Streamlit Web Dashboard & Python CLI Console.
          - **Backend Engine:** Modul Requests dengan HTTP Server-Sent Events (SSE) Streaming.
          - **AI Inference Engine:** Groq Cloud LPU (Model utama: `openai/gpt-oss-120b`).
          - **Pustaka Utama:** `streamlit`, `requests`, `python-dotenv`, `python-docx`.
        * **Hasil Pengujian:**
          - Waktu tanggap rata-rata: **0.4 - 0.7 detik**.
          - Akurasi pemahaman bahasa: Menggunakan pemodelan BPE tokenization dan Multi-Head Attention.
        """)

    with doc_tab3:
        st.markdown("""
        #### 🗺️ LAPORAN PERJALANAN PROYEK (ROADMAP & TROUBLESHOOTING)
        * **Fase 1: Inisiasi Modul Python:** Perancangan modul modular `config.py` dan `groq_client.py`.
        * **Fase 2: Dual-Mode Interaksi:** Pengembangan visual Streamlit (`app.py`) dan terminal (`main.py`) dengan decoding UTF-8.
        * **Fase 3: Pengamanan & Publikasi:** Mengamankan API key di Streamlit Secrets dan integrasi embed iframe ke Blogspot 24/7.
        """)
