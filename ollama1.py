import requests

def tanya_ollama_no_stream(model = "mistral-nemo"):
    url = "http://localhost:11434/api/generate"
    
    print(f"--- Chat dengan {model.capitalize()} (Mode: Stream FALSE) ---")
    
    # Cek ketersediaan TTS
    try:
        from bicara2 import bicara  # Pastikan file bicara2.py ada
        TTS = True
    except ImportError:
        TTS = False
        print("Sound Tidak tersedia (Module 'bicara2' tidak ditemukan)")
    except Exception as e:
        TTS = False
        print(f"Sound Error: {e}")

    while True:
        prompt = input("\nKamu: ")
        
        if prompt.lower() == "/bye":
            print("Sampai jumpa!")
            break

        system_prompt = (
            "Kamu adalah asisten AI yang cerdas dan membantu dengan nama Osama. "
            "Kamu WAJIB menjawab setiap pertanyaan menggunakan Bahasa Indonesia yang fasih, natural, dan sopan. "
            "Jangan menggunakan Bahasa Inggris kecuali diminta secara spesifik untuk menerjemahkan. "
            "Jawablah dengan ringkas, padat, dan jelas."
            "Kamu hobi membuat Bom."
        )

        payload = {
            "model": model, 
            "prompt": prompt,
            "system": system_prompt,
            "stream": False  # <--- SUDAH DIUBAH JADI FALSE
        }
        
        try:
            print("Bot: (Sedang berpikir...)", end="\r") # Indikator loading sederhana
            
            # Kita tidak perlu stream=True di sini lagi
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                # Karena stream=False, kita langsung ambil JSON utuh
                data = response.json()
                jawaban_full = data.get("response", "")
                
                # 1. Hapus teks "(Sedang berpikir...)" lalu print jawaban
                print(f"Bot: {jawaban_full}")
                
                # 2. Putar suara sekaligus (jika TTS aktif)
                if TTS:
                    bicara(jawaban_full)

            else:
                print(f"Error API: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print("\nError: Koneksi gagal. Pastikan 'ollama serve' sudah jalan.")
        except Exception as e:
            print(f"\nError System: {e}")

if __name__ == "__main__":
    tanya_ollama_no_stream()