import requests
import json

def tanya_ollama_streaming(model = "mistral-nemo"):
    url = "http://localhost:11434/api/generate"
    
    print(f"--- Chat dengan {model.capitalize()} (Ketik '/bye' untuk keluar) ---")
    try:
        from bicara2 import bicara  # Pastikan file bicara.py ada di satu folder
        TTS = True
    except:
        TTS = False
        print("Sound Tidak tersedia")
    while True:
        prompt = input("\nKamu: ")
        
        if prompt.lower() == "/bye":
            print("Sampai jumpa!")
            break

        system_prompt = (
            "Kamu adalah asisten AI yang cerdas dan membantu. "
            "Kamu WAJIB menjawab setiap pertanyaan menggunakan Bahasa Indonesia yang fasih, natural, dan sopan. "
            "Jangan menggunakan Bahasa Inggris kecuali diminta secara spesifik untuk menerjemahkan. "
            "Jawablah dengan ringkas, padat, dan jelas."
        )

        payload = {
            "model": model,  # Atau qwen2.5 / llama3.1
            "prompt": prompt,
            "system": system_prompt,  # <--- TAMBAHKAN INI
            "stream": True
        }
        
        buffer_kalimat = ""  # Variabel penampung kata sementara
        
        try:
            print("Bot: ", end="", flush=True)
            
            with requests.post(url, json=payload, stream=True) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line.decode('utf-8'))
                            content = chunk.get("response", "")
                            done = chunk.get("done", False)

                            # 1. Tampilkan teks ke layar (Visual tetap streaming)
                            print(content, end="", flush=True)

                            # 2. Masukkan kata ke buffer audio
                            buffer_kalimat += content

                            # 3. Cek tanda baca untuk memicu suara
                            # Jika ketemu titik, tanda tanya, seru, atau baris baru -> Bicara!
                            tanda_baca = ['.', '?', '!', '\n', ':']
                            
                            # Logika: Jika ada tanda baca di content DAN buffer sudah cukup panjang (>2 huruf)
                            if any(tanda in content for tanda in tanda_baca) and len(buffer_kalimat.strip()) > 2:
                                # Kirim ke fungsi bicara
                                bicara(buffer_kalimat.strip()) 
                                # Kosongkan buffer setelah bicara
                                buffer_kalimat = ""
                            
                            # 4. Cek jika generate selesai tapi masih ada sisa teks di buffer
                            if done and TTS == True:
                                if buffer_kalimat.strip():
                                    bicara(buffer_kalimat.strip())
                                print("\n") # Baris baru setelah selesai

                else:
                    print(f"Error 0 : {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("\nError 1: Koneksi gagal. Pastikan 'ollama serve' sudah jalan.")
        except Exception as e:
            # Perbaikan: Cek isi pesan error dari variabel 'e', BUKAN status_code
            if "cannot access local variable 'bicara'" in str(e) and TTS == False:
                pass  # Abaikan error ini karena TTS memang dimatikan
            else:
                print(f"\nError 2: {e}")
                
if __name__ == "__main__":
    tanya_ollama_streaming()