import json
import requests
from typing import List, Dict, Generator, Tuple, Optional
from config import (
    DEFAULT_API_KEY,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    SYSTEM_PROMPT,
    GROQ_API_URL,
    MAX_TOKENS,
    TEMPERATURE,
)

class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or DEFAULT_API_KEY
        self.current_model = DEFAULT_MODEL

    def _prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Pastikan ada system prompt di awal riwayat pesan."""
        if not messages or messages[0].get("role") != "system":
            return [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        return messages

    def send_chat_non_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE,
    ) -> Tuple[str, str]:
        """
        Mengirim chat completion secara synchronous (non-streaming).
        Mengembalikan tuple: (jawaban_teks, model_yang_digunakan).
        Mendukung auto-fallback ke model lain jika terjadi error.
        """
        if not self.api_key:
            raise ValueError("API Key Groq tidak ditemukan! Pastikan GROQ_API_KEY sudah diisi.")

        full_messages = self._prepare_messages(messages)
        candidate_models = [model] if model else AVAILABLE_MODELS
        last_error = "Tidak ada model yang berhasil."

        headers = {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json",
        }

        for candidate in candidate_models:
            payload = {
                "model": candidate,
                "messages": full_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }

            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices:
                        self.current_model = candidate
                        content = choices[0].get("message", {}).get("content", "").strip()
                        return content, candidate

                error_data = {}
                try:
                    error_data = response.json()
                except Exception:
                    pass

                err_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}: {response.text}")
                last_error = f"Model {candidate} gagal: {err_msg}"

                # Jika API key salah (401), tidak perlu coba model lain
                if response.status_code == 401:
                    raise ValueError(f"API Key Groq tidak valid (HTTP 401): {err_msg}")

            except requests.exceptions.RequestException as e:
                last_error = f"Gagal menghubungi server Groq: {e}"

        raise RuntimeError(last_error)

    def send_chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE,
    ) -> Generator[str, None, None]:
        """
        Mengirim chat completion dengan HTTP streaming (efek mengetik kata demi kata).
        Yields teks potongan (token/chunk).
        """
        if not self.api_key:
            raise ValueError("API Key Groq tidak ditemukan! Pastikan GROQ_API_KEY sudah diisi.")

        full_messages = self._prepare_messages(messages)
        candidate_models = [model] if model else AVAILABLE_MODELS
        headers = {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json",
        }

        success = False
        last_error = ""

        for candidate in candidate_models:
            payload = {
                "model": candidate,
                "messages": full_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True,
            }

            try:
                response = requests.post(
                    GROQ_API_URL,
                    headers=headers,
                    json=payload,
                    stream=True,
                    timeout=30,
                )

                if response.status_code != 200:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except Exception:
                        pass
                    err_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                    last_error = f"Model {candidate} gagal: {err_msg}"
                    if response.status_code == 401:
                        raise ValueError(f"API Key Groq tidak valid: {err_msg}")
                    continue

                self.current_model = candidate
                success = True

                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    line = line.strip()
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk_json = json.loads(data_str)
                            choices = chunk_json.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                break

            except requests.exceptions.RequestException as e:
                last_error = f"Gagal streaming: {e}"

        if not success:
            raise RuntimeError(last_error or "Gagal memuat respons dari Groq AI.")
