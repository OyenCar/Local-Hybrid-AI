import asyncio
import edge_tts
import pygame
import os
import time
import config

# Nama suara Indonesia Cowok yang natural: "id-ID-ArdiNeural"
# Nama suara Indonesia Cewek yang natural: "id-ID-GadisNeural"


def setup_suara():
    suara = input("Masukkan Suara (L/P): ")
    if suara.lower() == "l":
        return "id-ID-ArdiNeural"
    else:
        return "id-ID-GadisNeural"
    
VOICE = config.VOICE_NAME
OUTPUT_FILE = "temp.mp3"

def putar_audio(file_path):
    pygame.mixer.init()
    # Unload dulu biar gak error permission
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error play: {e}")

async def _generate_suara(teks):
    """Fungsi async untuk generate suara"""
    communicate = edge_tts.Communicate(teks, VOICE)
    await communicate.save(OUTPUT_FILE)

def bicara(teks):
    if not teks.strip():
        return
    
    try:
        # Hapus file lama jika ada
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
            
        # Jalankan fungsi async di environment synchronous
        asyncio.run(_generate_suara(teks))
        
        # Putar
        putar_audio(OUTPUT_FILE)
        
    except Exception as e:
        print(f"Error EdgeTTS: {e}")

if __name__ == "__main__":
    print("Mencoba suara Ardi (Edge TTS)...")
    bicara("Halo Kevin, ini adalah suara Ardi dari Microsoft Edge. Terdengar sangat natural kan?")
    #pip install edge-tts pygame