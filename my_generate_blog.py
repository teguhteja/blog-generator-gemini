#!/usr/bin/env python3
import argparse
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

def generate_folder(input_path,):
    """Membuat direktori dan artikel blog menggunakan Gemini berdasarkan file input dan prompt."""

    # 1. Ambil nama dasar file (misal: "nama_file.vtt" dari "path/to/nama_file.vtt")
    base_name = os.path.basename(input_path)

    # 2. Pisahkan nama file dari ekstensinya (misal: ("nama_file", ".vtt"))
    dir_name, _ = os.path.splitext(base_name)

    # Jika setelah dipisahkan namanya kosong (misal inputnya ".vtt"), jangan buat folder
    if not dir_name:
        print(f"Error: Nama file tidak valid untuk membuat direktori dari '{input_path}'")
        return

    # 3. Buat direktori. `exist_ok=True` agar tidak error jika direktori sudah ada.
    try:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Direktori '{dir_name}' berhasil dibuat atau sudah ada.")
    except OSError as e:
        print(f"❌ Gagal membuat direktori: {e}")

def generate_tutorial(input_path, prompt_path):
    """
    Membuat artikel tutorial menggunakan Gemini berdasarkan file input dan file prompt.

    Args:
        input_path (str): Path menuju file input (misal: .vtt).
        prompt_path (str): Path menuju file prompt (.md).
    """
    # Langkah 1: Muat API Key dari file .env
    load_dotenv()
    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        sys.exit(1)

    genai.configure(api_key=api_key)

    # Langkah 2: Pastikan file input dan prompt ada
    for path in [input_path, prompt_path]:
        if not os.path.exists(path):
            print(f"❌ Error: File '{path}' tidak ditemukan.")
            sys.exit(1)

    # Langkah 3: Siapkan nama direktori dan path file output
    base_name = os.path.basename(input_path)
    dir_name, _ = os.path.splitext(base_name)
    output_filename = f"{dir_name}.md"
    output_path = os.path.join(dir_name, output_filename)

    # Langkah 4: Buat direktori berdasarkan nama file input
    try:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Direktori '{dir_name}' berhasil disiapkan.")
    except OSError as e:
        print(f"❌ Gagal membuat direktori '{dir_name}': {e}")
        sys.exit(1)

    print(f"📖 Membaca file input: {input_path}")
    print(f"📄 Membaca file prompt: {prompt_path}")

    # Langkah 5: Baca konten dari kedua file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
    except Exception as e:
        print(f"❌ Error saat membaca file: {e}")
        sys.exit(1)

    # Langkah 6: Gabungkan prompt dan konten file input menjadi satu prompt utuh
    final_prompt = f"{prompt_content}\n\n---\n\nKonteks dari file `{base_name}`:\n\n{input_content}"

    # Langkah 7: Panggil Gemini API
    try:
        print("\n🤖 Menghubungi Gemini untuk membuat konten... (ini mungkin butuh beberapa saat)")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(final_prompt)

        # Langkah 8: Simpan hasilnya ke file .md di dalam direktori yang sudah dibuat
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"✅ Sukses! Konten berhasil dibuat dan disimpan di: {output_path}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menghubungi Gemini API: {e}")
        sys.exit(1)

def main():
    """Fungsi utama untuk parsing argumen dan menjalankan skrip."""
    parser = argparse.ArgumentParser(
        description="Membuat artikel blog dari file input (misal: .vtt) menggunakan Gemini.",
        epilog="Contoh: python my-generate-blog.py -i nama_file.vtt -p prompt_tutorial_subs.md"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path ke file input (misal: nama_file.vtt).", metavar="FILE_INPUT"
    )
    parser.add_argument(
        "-p", "--prompt",
        default='prompt_tutorial_odoo18.md',
        choices=['prompt_tutorial_odoo18.md', 'prompt_tutorial_subs.md'],
        help="Pilih file prompt. (Default: %(default)s)"
    )
    args = parser.parse_args()
    generate_folder(args.input,)
    generate_tutorial(args.input, args.prompt)

if __name__ == "__main__":
    main()
