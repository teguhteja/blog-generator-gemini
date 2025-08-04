#!/usr/bin/env python3
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Data harga berdasarkan dokumentasi resmi Google AI per Juni 2024.
# Harga dapat berubah. Selalu periksa halaman harga resmi untuk data terbaru.
# Harga dikonversi ke per 1.000 karakter untuk kemudahan perbandingan.
MODEL_PRICING = {
    # Model Gemini 1.5
    "gemini-1.5-pro": {
        "input_per_1k_chars": 0.0035,
        "output_per_1k_chars": 0.0105,
        "notes": "Model Pro, kemampuan canggih."
    },
    "gemini-1.5-flash": {
        "input_per_1k_chars": 0.00035,
        "output_per_1k_chars": 0.00105,
        "notes": "Model Flash, sangat cepat dan hemat biaya."
    },
    # Model Gemini 1.0
    "gemini-1.0-pro": {
        "input_per_1k_chars": 0.0005,
        "output_per_1k_chars": 0.0015,
        "notes": "Model Pro generasi sebelumnya."
    },
    # Model untuk pembuatan gambar (harga per gambar)
    "gemini-1.5-pro-latest": { # Seringkali model latest menunjuk ke 1.5 Pro
        "input_per_1k_chars": 0.0035,
        "output_per_1k_chars": 0.0105,
        "image_generation_cost": 0.0180, # Estimasi biaya per gambar
        "notes": "Versi terbaru dari model Pro."
    },
}

def check_models_with_pricing():
    """
    Mencetak daftar model Gemini yang tersedia beserta informasi harganya.
    """
    load_dotenv()
    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        return

    genai.configure(api_key=api_key)

    print("🤖 Mencari model Gemini yang tersedia dan mencocokkannya dengan data harga...\n")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"🔹 Nama Model: {m.name}")
            
            # Cari harga untuk model ini
            # Kita periksa jika nama model ada di dalam kunci dictionary
            pricing_info = next((MODEL_PRICING[key] for key in MODEL_PRICING if key in m.name), None)

            if pricing_info:
                print(f"   - Harga Input:  ${pricing_info.get('input_per_1k_chars', 'N/A'):.5f} / 1k karakter")
                print(f"   - Harga Output: ${pricing_info.get('output_per_1k_chars', 'N/A'):.5f} / 1k karakter")
                if 'image_generation_cost' in pricing_info:
                    print(f"   - Harga Gambar: ${pricing_info.get('image_generation_cost', 'N/A'):.4f} / gambar")
                print(f"   - Catatan:      {pricing_info.get('notes', 'Tidak ada')}\n")
            else:
                print("   - Harga:        Tidak ada data harga di skrip ini.\n")

if __name__ == "__main__":
    check_models_with_pricing()
