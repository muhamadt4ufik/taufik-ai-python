import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent

def load_key_from_config_js() -> str:
    config_js_path = PARENT_DIR / "config.js"
    if config_js_path.exists():
        try:
            content = config_js_path.read_text(encoding="utf-8")
            match = re.search(r"API_KEY\s*:\s*['""]([^'""]+)['""]", content)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
    return ""

def get_secret_api_key() -> str:
    """Membaca API key dengan aman tanpa pernah menampilkannya ke UI publik."""
    # 1. Cek Streamlit Cloud secrets
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            return str(st.secrets["GROQ_API_KEY"]).strip()
    except Exception:
        pass

    # 2. Cek Environment Variable
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        return env_key.strip()

    # 3. Fallback lokal
    return load_key_from_config_js() or "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"

DEFAULT_API_KEY = get_secret_api_key()

# Daftar kandidat model Groq dengan fallback otomatis
AVAILABLE_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

DEFAULT_MODEL = AVAILABLE_MODELS[0]

# System Prompt Taufik AI
SYSTEM_PROMPT = (
    "Anda adalah Taufik AI, asisten AI pribadi yang ramah, cerdas, dan membantu. "
    "Diciptakan oleh Taufik. Selalu jawab dengan bahasa Indonesia yang sopan, jelas, "
    "terstruktur, dan natural."
)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_TOKENS = 2048
TEMPERATURE = 0.7
