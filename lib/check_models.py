#!/usr/bin/env python3
import os
import google.generativeai as genai
from dotenv import load_dotenv

def list_available_models():
    """
    Mencetak daftar model Gemini yang tersedia yang mendukung 'generateContent'.
    """
    # Muat API Key dari file .env
    load_dotenv()
    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        return

    genai.configure(api_key=api_key)

    print("🤖 Mencari model Gemini yang tersedia...\n")
    for m in genai.list_models():
        # Filter hanya untuk model yang bisa digunakan untuk generate konten
        if 'generateContent' in m.supported_generation_methods:
            print(f"🔹 Nama Model: {m.name}")
            print(f"   Deskripsi: {m.description}\n")

if __name__ == "__main__":
    list_available_models()
