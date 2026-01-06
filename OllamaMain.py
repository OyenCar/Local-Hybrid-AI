import requests
import json
import sys
import config

# --- Inisialisasi Modul Suara (TTS) ---
try:
    from TTS import bicara  # Pastikan ada file TTS.py yang berisi fungsi bicara()
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  Info: Modul suara (TTS) tidak aktif/ditemukan.")
except Exception as e:
    TTS_AVAILABLE = False
    print(f"⚠️  Error TTS: {e}")
    
if not config.TTS:
    TTS_AVAILABLE = False

def tanya_ollama(model=config.MODEL_NAME):
    url = config.API_URL
    
    # Cek mode stream dari config
    mode_str = "Streaming" if config.STREAM else "Full Response"
    print(f"--- Chat dengan {model.capitalize()} (Mode: {mode_str}) ---")
    
    while True:
        try:
            prompt = input("\nKamu: ")
            
            # Fitur keluar
            if prompt.lower() in ["/bye", "keluar", "exit"]:
                print("Sampai jumpa!")
                break
            
            # Abaikan input kosong
            if not prompt.strip():
                continue

            # Siapkan data
            payload = {
                    "model": model,
                    "prompt": prompt,
                    "system": config.SYSTEM_INSTRUCTION,
                    "stream": config.STREAM,
                    "options": {
                        "temperature": 0.7,       # Kreativitas (standar)
                        "repeat_penalty": 1.1,    # <--- TAMBAHKAN INI (Hukuman untuk kata berulang)
                        "top_k": 40,              # Membatasi pilihan kata agar tetap nyambung
                        "num_ctx": 4096           # Memperbesar memori konteks (agar tidak lupa soal awal)
                    }
                }

            # --- LOGIKA STREAMING (Teks muncul per kata) ---
            if config.STREAM:
                print("Bot: ", end="", flush=True)
                buffer_kalimat = "" # Reset buffer per prompt baru
                
                with requests.post(url, json=payload, stream=True) as response:
                    if response.status_code == 200:
                        for line in response.iter_lines():
                            if line:
                                try:
                                    chunk = json.loads(line.decode('utf-8'))
                                    content = chunk.get("response", "")
                                    done = chunk.get("done", False)
                                    
                                    # 1. Tampilkan teks langsung
                                    print(content, end="", flush=True)
                                    
                                    # 2. Jika TTS aktif, tampung kata
                                    if TTS_AVAILABLE:
                                        buffer_kalimat += content
                                        
                                        # Cek tanda baca pemisah kalimat
                                        tanda_baca = ['.', '?', '!', '\n', ':']
                                        if any(t in content for t in tanda_baca) and len(buffer_kalimat.strip()) > 3:
                                            bicara(buffer_kalimat.strip())
                                            buffer_kalimat = "" # Reset buffer setelah bicara

                                    # 3. Cek sisa buffer saat selesai
                                    if done and TTS_AVAILABLE and buffer_kalimat.strip():
                                        bicara(buffer_kalimat.strip())
                                        
                                except json.JSONDecodeError:
                                    continue
                        print("") # Enter baris baru setelah selesai
                    else:
                        print(f"Error API: {response.status_code}")

            # --- LOGIKA NON-STREAMING (Tunggu jawaban selesai baru muncul) ---
            else:
                print("Bot: (Sedang berpikir...)", end="\r") # Loading indicator
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    jawaban_full = data.get("response", "")
                    
                    # Hapus loading text, ganti dengan jawaban
                    # " " * 20 digunakan untuk membersihkan sisa teks loading
                    print(f"Bot: {jawaban_full}      ") 
                    
                    if TTS_AVAILABLE:
                        bicara(jawaban_full)
                else:
                    print(f"\nError API: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n❌ Gagal terhubung! Pastikan 'ollama serve' berjalan di WSL.")
        except KeyboardInterrupt:
            print("\nProgram dihentikan user.")
            break
        except Exception as e:
            print(f"\n❌ Error tidak terduga: {e}")

if __name__ == "__main__":
    # HAPUS os.system pip install agar program cepat terbuka
    # Jalankan pip install manual di terminal jika perlu
    tanya_ollama()