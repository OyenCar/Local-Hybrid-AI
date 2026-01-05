# config.py

# --- KONFIGURASI KONEKSI ---
# URL localhost WSL (Default Ollama)
API_URL = "http://localhost:11434/api/generate"

# Model yang digunakan (Pastikan sudah di-pull di WSL, misal: llama3, mistral, gemma:2b)
MODEL_NAME = "mistral-nemo"

# --- KONFIGURASI SUARA (EDGE-TTS) ---
# Daftar suara umum:
# - id-ID-GadisNeural (Bahasa Indonesia - Cewek)
# - id-ID-ArdiNeural (Bahasa Indonesia - Cowok)
# - en-US-AnaNeural (Inggris - Cewek)
VOICE_NAME = "id-ID-GadisNeural"
VOICE_RATE = "+0%"   # Kecepatan bicara (+10% lebih cepat, -10% lebih lambat)
VOICE_PITCH = "+0Hz" # Nada suara

# --- IDENTITAS AI ---
USER_NAME = "Bos"
AI_NAME = ""

# System Prompt: Instruksi dasar agar AI tahu perannya
SYSTEM_INSTRUCTION = f"""
Kamu adalah {AI_NAME}, asisten pribadi yang cerdas, ramah, dan sedikit humoris.
Kamu berbicara dengan {USER_NAME}.
Jawablah dengan singkat, padat, dan natural seperti percakapan sehari-hari.
Jangan memberikan jawaban yang terlalu panjang kecuali diminta.
Gunakan Bahasa Indonesia yang gaul tapi sopan.
"""
STREAM = True