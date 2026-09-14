import sys
import os

# Pastikan UTF-8 encoding di Windows console agar tidak error saat print karakter/emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from groq_client import GroqClient
from config import AVAILABLE_MODELS, DEFAULT_MODEL, DEFAULT_API_KEY

def print_banner(client):
    print("=" * 60)
    print("        [+] TAUFIK AI - PYTHON CHATBOT ASSISTANT [+]        ")
    print("=" * 60)
    print(f"Status       : ONLINE [Aktif]")
    print(f"Model AI     : {client.current_model}")
    print(f"API Key      : {'Terpasang (OK)' if client.api_key else 'Belum diisi (X)'}")
    print("Perintah khusus:")
    print("   - 'keluar' atau 'exit' : Menutup aplikasi")
    print("   - 'reset' atau 'clear' : Menghapus riwayat percakapan")
    print("   - 'model'              : Mengganti model AI")
    print("-" * 60)
    print("Taufik AI: Halo! Saya Taufik AI. Ada yang bisa saya bantu hari ini?\n")

def select_model(client):
    print("\n--- Pilihan Model Groq Tersedia ---")
    for i, m in enumerate(AVAILABLE_MODELS, 1):
        indicator = " (Aktif)" if m == client.current_model else ""
        print(f"[{i}] {m}{indicator}")
    choice = input("\nPilih nomor model (atau tekan Enter untuk batal): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(AVAILABLE_MODELS):
        client.current_model = AVAILABLE_MODELS[int(choice) - 1]
        print(f"Model diubah menjadi: {client.current_model}\n")
    else:
        print("Model tidak diubah.\n")

def main():
    client = GroqClient()
    print_banner(client)

    chat_history = []

    while True:
        try:
            user_input = input("Anda > ").strip()
            if not user_input:
                continue

            lower = user_input.lower()
            if lower in ["keluar", "exit", "quit", "q"]:
                print("\nTerima kasih telah menggunakan Taufik AI. Sampai jumpa!\n")
                break

            if lower in ["reset", "clear"]:
                chat_history.clear()
                print("\n[i] Riwayat obrolan telah dibersihkan.\n")
                continue

            if lower == "model":
                select_model(client)
                continue

            # Tambahkan ke riwayat
            chat_history.append({"role": "user", "content": user_input})
            recent_history = chat_history[-10:]

            print("\nTaufik AI > ", end="", flush=True)

            # Streaming response
            bot_reply = ""
            try:
                for chunk in client.send_chat_stream(recent_history, model=client.current_model):
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    bot_reply += chunk
                print("\n")
                chat_history.append({"role": "assistant", "content": bot_reply})
            except Exception as err:
                print(f"\n[!] Error: {err}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nSesi dihentikan. Sampai jumpa!")
            break

if __name__ == "__main__":
    main()
