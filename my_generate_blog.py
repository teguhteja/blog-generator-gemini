#!/usr/bin/env python3
import argparse
import os
import sys
import re
import io
import json
import subprocess
from google import genai as genai_image
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from google.genai import types
from io import BytesIO
import base64

def call_gemini(prompt_text, model_name):
    """
    Memanggil Gemini API dengan prompt dan model tertentu.

    Args:
        prompt_text (str): Prompt lengkap untuk dikirim ke model.
        model_name (str): Nama model yang akan digunakan.

    Returns:
        str: Respon teks dari model, atau None jika terjadi error.
    """
    try:
        print(f"\n🤖 Menghubungi Gemini dengan model '{model_name}'... (ini mungkin butuh beberapa saat)")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menghubungi Gemini API: {e}")
        return None

def generate_image(prompt_text, model_name, api_key):
    """
    Memanggil Gemini API untuk membuat gambar.

    Args:
        prompt_text (str): Prompt teks yang mendeskripsikan gambar.
        model_name (str): Nama model yang akan digunakan (harus mampu membuat gambar).

    Returns:
        PIL.Image.Image: Objek gambar, atau None jika terjadi error.
    """
    try:
        print(f"\n🎨 Menghubungi Gemini dengan model '{model_name}' untuk membuat gambar...")
        client = genai_image.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                 response_modalities=['TEXT', 'IMAGE']
            )
        )

        # Iterasi melalui semua bagian respons untuk menemukan gambar
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                return image
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat membuat gambar: {e}")
        return None

def sanitize_filename(text, extension):
    """
    Mengubah teks menjadi nama file yang valid.
    """
    sanitized = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    return f"{sanitized}.{extension}"

def resize_image(image_path):
    """
    Mengubah ukuran gambar menggunakan ImageMagick.
    """
    try:
        print(f"🖼️  Mengubah ukuran gambar: {image_path}")
        command = ['convert', str(image_path), '-resize', '1024x720', '-quality', '100%', str(image_path)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ Gambar berhasil diubah ukurannya.")
    except FileNotFoundError:
        print("⚠️  Peringatan: Perintah 'convert' (ImageMagick) tidak ditemukan.")
        print("   Gambar tidak diubah ukurannya. Silakan install ImageMagick untuk fungsionalitas penuh.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Gagal mengubah ukuran gambar: {e.stderr}")


def parse_and_select_keyphrase(seo_content):
    """
    Mem-parsing konten SEO, menampilkan pilihan, dan meminta input pengguna.

    Args:
        seo_content (str): Teks mentah yang berisi daftar keyphrase bernomor.
    
    Returns:
        str: Keyphrase yang dipilih oleh pengguna, atau None jika tidak ada yang dipilih.
    """
    # Mencari baris yang diawali dengan angka, titik, dan spasi
    keyphrases = re.findall(r"^\s*\d+\.\s*(.*)", seo_content, re.MULTILINE)

    if not keyphrases:
        print("\n⚠️ Tidak dapat menemukan keyphrase bernomor pada hasil SEO.")
        print("Isi file .seo.md adalah:")
        print("--------------------")
        print(seo_content)
        print("--------------------")
        return None

    print("\n💡 Silakan pilih Keyphrase SEO utama Anda dari daftar berikut:")
    for i, phrase in enumerate(keyphrases):
        print(f"  [{i+1}] {phrase.strip()}")

    while True:
        try:
            choice = int(input(f"\nMasukkan pilihan Anda (1-{len(keyphrases)}): "))
            if 1 <= choice <= len(keyphrases):
                selected_phrase = keyphrases[choice - 1].strip()
                print(f"\n✅ Anda memilih: \"{selected_phrase}\"")
                return selected_phrase
            else:
                print(f"❌ Pilihan tidak valid. Harap masukkan angka antara 1 dan {len(keyphrases)}.")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Pemilihan dibatalkan.")
            return None

def run_generation_workflow(input_path, blog_prompt_path, model_config_path):
    """
    Menjalankan alur kerja lengkap: membuat direktori, konten blog, dan analisis SEO.
    """
    # Langkah 0: Konfigurasi awal dan validasi path
    print(f"🚀 Memulai alur kerja lengkap untuk '{input_path}'...")
    load_dotenv()

    if not os.path.exists(model_config_path):
        print(f"❌ Error: File konfigurasi model '{model_config_path}' tidak ditemukan.")
        sys.exit(1)
    try:
        with open(model_config_path, 'r') as f:
            model_config = json.load(f)
        print(f"✅ Konfigurasi model berhasil dimuat dari {model_config_path}")
    except json.JSONDecodeError:
        print(f"❌ Error: Gagal mem-parsing file JSON '{model_config_path}'. Pastikan formatnya benar.")
        sys.exit(1)

    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        sys.exit(1)
    genai.configure(api_key=api_key)

    base_name = os.path.basename(input_path)
    youtube_code_match = re.search(r'\[([a-zA-Z0-9_-]+)\]', base_name)
    youtube_link = None
    if youtube_code_match:
        youtube_code = youtube_code_match.group(1)
        youtube_link = f"https://www.youtube.com/watch?v={youtube_code}"
        print(f"🔗 Tautan YouTube terdeteksi: {youtube_link}")

    # Definisikan semua path prompt yang dibutuhkan
    keyphrase_prompt_path = "prompt_add_seo.md" # Prompt untuk mendapatkan keyphrase
    # Validasi file prompt (file input sudah divalidasi di main)
    for path in [blog_prompt_path, keyphrase_prompt_path]:
        if not os.path.exists(path):
            print(f"❌ Error: File '{path}' tidak ditemukan.")
            sys.exit(1)

    # Langkah 2: Siapkan nama direktori dan path file
    dir_name, _ = os.path.splitext(base_name)
    if not dir_name:
        print(f"❌ Error: Nama file tidak valid untuk membuat direktori dari '{input_path}'")
        sys.exit(1)

    output_md_path = os.path.join(dir_name, f"{dir_name}.md")
    output_seo_path = os.path.join(dir_name, f"{dir_name}.seo.md")
    output_blog_path = os.path.join(dir_name, f"{dir_name}.blog.md")

    # Buat direktori output jika belum ada
    os.makedirs(dir_name, exist_ok=True)
    print(f"✅ Direktori '{dir_name}' berhasil disiapkan.")

    # --- LANGKAH 1: Generate Draft ---
    print("\n--- LANGKAH 1: Membuat Draf Tutorial ---")
    with open(input_path, 'r', encoding='utf-8') as f:
        input_content = f.read()
    with open(blog_prompt_path, 'r', encoding='utf-8') as f:
        blog_prompt_content = f.read()

    final_blog_prompt = f"{blog_prompt_content}\n\n---\n\nKonteks dari file `{base_name}`:\n\n{input_content}"
    blog_content = call_gemini(final_blog_prompt, model_config.get('model_tutorial', 'gemini-1.5-flash-latest'))

    if not blog_content:
        print("❌ Gagal membuat draf, proses dihentikan.")
        sys.exit(1)
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(blog_content)
    print(f"✅ Draf berhasil dibuat dan disimpan di: {output_md_path}")

    # --- LANGKAH 2: Get SEO Keyphrases ---
    print("\n--- LANGKAH 2: Mendapatkan Keyphrase SEO ---")
    with open(keyphrase_prompt_path, 'r', encoding='utf-8') as f:
        keyphrase_prompt_content = f.read()

    final_seo_prompt = f"{keyphrase_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_md_path)}`:\n\n{blog_content}"
    seo_content = call_gemini(final_seo_prompt, model_config.get('model_seo', 'gemini-1.5-flash-latest'))

    if not seo_content:
        print("❌ Gagal mendapatkan keyphrase SEO, proses dihentikan.")
        sys.exit(1)
    
    content_to_write_seo = seo_content
    if youtube_link:
        content_to_write_seo = f"**Sumber Video:** {youtube_link}\n\n---\n\n{seo_content}"
    with open(output_seo_path, 'w', encoding='utf-8') as f:
        f.write(content_to_write_seo)
    print(f"✅ Analisis Keyphrase SEO berhasil dibuat dan disimpan di: {output_seo_path}")

    # --- Interaksi Pengguna: Memilih Keyphrase ---
    selected_keyphrase = parse_and_select_keyphrase(seo_content)
    if not selected_keyphrase:
        print("⚠️ Tidak ada keyphrase yang dipilih. Alur kerja berhenti.")
        sys.exit(0)

    # --- LANGKAH 3: Create Final Blog ---
    print("\n--- LANGKAH 3: Membuat Blog Final ---")
    create_blog_prompt_path = 'prompt_create_blog.md'
    with open(create_blog_prompt_path, 'r', encoding='utf-8') as f:
        create_blog_prompt_content = f.read()
    
    injected_create_blog_prompt = create_blog_prompt_content.format(selected_keyphrase)
    final_blog_post_prompt = (
        f"{injected_create_blog_prompt}\n\n---\n\n"
        f"CONTEXT FROM ORIGINAL TRANSCRIPT (`{base_name}`):\n\n{input_content}\n\n"
        f"---\n\n"
        f"CONTEXT FROM DRAFT POST (`{os.path.basename(output_md_path)}`):\n\n{blog_content}"
    )
    final_blog_post_content = call_gemini(final_blog_post_prompt, model_config.get('model_blog', 'gemini-1.5-pro-latest'))

    if not final_blog_post_content:
        print("❌ Gagal membuat blog post final.")
        sys.exit(1)

    content_to_write_blog = final_blog_post_content
    if youtube_link:
        lines = content_to_write_blog.split('\n', 1)
        title = lines[0]
        body = lines[1] if len(lines) > 1 else ''
        link_markdown = f"\n_Tonton video tutorial asli di YouTube_\n"
        content_to_write_blog = f"{title}\n{link_markdown}\n{body}"
    with open(output_blog_path, 'w', encoding='utf-8') as f:
        f.write(content_to_write_blog)
    print(f"✅ Blog post final berhasil dibuat dan disimpan di: {output_blog_path}")

    # --- LANGKAH 4: Update SEO with Metadata ---
    print("\n--- LANGKAH 4: Memperbarui SEO dengan Metadata ---")
    seo_meta_prompt_path = 'prompt_create_seo.md'
    with open(seo_meta_prompt_path, 'r', encoding='utf-8') as f:
        seo_meta_prompt_content = f.read()

    final_seo_meta_prompt = f"{seo_meta_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_blog_path)}`:\n\n{final_blog_post_content}"
    seo_meta_content = call_gemini(final_seo_meta_prompt, model_config.get('model_seo', 'gemini-1.5-pro-latest'))

    if seo_meta_content:
        with open(output_seo_path, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n\n## SEO Metadata Lanjutan\n\n")
            f.write(seo_meta_content)
        print(f"✅ Metadata SEO lanjutan berhasil ditambahkan ke: {output_seo_path}")
    else:
        print("❌ Gagal membuat metadata SEO lanjutan.")

    # --- LANGKAH 5: Generate Image ---
    print("\n--- LANGKAH 5: Membuat Gambar ---")
    image_prompt_path = 'prompt_create_picture.md'
    if not os.path.exists(image_prompt_path):
        print(f"⚠️ Peringatan: File prompt '{image_prompt_path}' tidak ditemukan. Melewatkan pembuatan gambar.")
    else:
        with open(image_prompt_path, 'r', encoding='utf-8') as f:
            image_prompt_content = f.read()

        final_image_prompt = image_prompt_content.format(selected_keyphrase)
        image_model = model_config.get('model_image', 'gemini-1.5-pro-latest')
        print(f"ℹ️  Menggunakan model '{image_model}' untuk pembuatan gambar (ini mungkin memerlukan waktu lebih lama).")
        generated_image = generate_image(final_image_prompt, model_name=image_model, api_key=api_key)

        if generated_image:
            image_filename = sanitize_filename(selected_keyphrase, 'png')
            image_path = os.path.join(dir_name, image_filename)
            generated_image.save(image_path)
            print(f"✅ Gambar berhasil dibuat dan disimpan di: {image_path}")
            resize_image(image_path)
    
    print("\n🎉 Alur kerja selesai.")

def main():
    """Fungsi utama untuk parsing argumen dan menjalankan skrip."""
    parser = argparse.ArgumentParser(
        description="Membuat artikel blog dan analisis SEO dari file input menggunakan Gemini.",
        epilog="Contoh: python my_generate_blog.py -i nama_file.vtt -m custom_models.json"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path ke file input teks (misal: .txt, .vtt, .srt).", metavar="FILE_INPUT"
    )
    parser.add_argument(
        "-p", "--prompt",
        default='prompt_tutorial_odoo18.md',
        choices=['prompt_tutorial_odoo18.md', 'prompt_tutorial_subs.md', 'prompt_create_blog.md'],
        help="Pilih file prompt untuk konten blog. (Default: %(default)s)"
    )
    parser.add_argument(
        "-m", "--model-config",
        default='model.json',
        help="Path ke file konfigurasi model JSON. (Default: %(default)s)",
        metavar="MODEL_JSON"
    )
    args = parser.parse_args()

    # Validasi tipe file input
    allowed_extensions = ['.txt', '.vtt', '.srt', '.md']
    _, file_extension = os.path.splitext(args.input)
    if file_extension.lower() not in allowed_extensions:
        parser.error(f"File input harus berupa file teks dengan ekstensi: {', '.join(allowed_extensions)}")

    if not os.path.exists(args.input):
        parser.error(f"File input tidak ditemukan: {args.input}")

    run_generation_workflow(args.input, args.prompt, args.model_config)


if __name__ == "__main__":
    main()
