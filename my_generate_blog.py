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

def run_generation_workflow(input_path, blog_prompt_path, model_config_path, steps_to_run):
    """
    Menjalankan alur kerja lengkap: membuat direktori, konten blog, dan analisis SEO.
    """
    # Langkah 0: Konfigurasi awal dan validasi path
    print(f"🚀 Memulai alur kerja untuk '{input_path}' dengan langkah: {steps_to_run}")
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

    PROMPT_DIR = "prompt"
    # Definisikan semua path prompt yang dibutuhkan
    keyphrase_prompt_path = os.path.join(PROMPT_DIR, "prompt_add_seo.md") # Prompt untuk mendapatkan keyphrase
    # Validasi file prompt (blog_prompt_path sudah divalidasi di main)
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
    if 1 in steps_to_run:
        print("\n--- LANGKAH 1: Membuat Draf Tutorial ---")
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(blog_prompt_path, 'r', encoding='utf-8') as f:
            blog_prompt_content = f.read()

        final_blog_prompt = f"{blog_prompt_content}\n\n---\n\nKonteks dari file `{base_name}`:\n\n{input_content}"
        blog_content = call_gemini(final_blog_prompt, model_config.get('model_tutorial', 'gemini-1.5-flash-latest'))

        if blog_content:
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(blog_content)
            print(f"✅ Draf berhasil dibuat dan disimpan di: {output_md_path}")
        else:
            print("❌ Gagal membuat draf, proses dihentikan.")
            sys.exit(1)

    # --- LANGKAH 2: Get SEO Keyphrases ---
    if 2 in steps_to_run:
        print("\n--- LANGKAH 2: Mendapatkan Keyphrase SEO ---")
        if not os.path.exists(output_md_path):
            print(f"❌ Error: File draf '{output_md_path}' tidak ditemukan. Jalankan langkah 1 terlebih dahulu.")
            sys.exit(1)

        with open(output_md_path, 'r', encoding='utf-8') as f:
            blog_content = f.read()
        with open(keyphrase_prompt_path, 'r', encoding='utf-8') as f:
            keyphrase_prompt_content = f.read()

        final_seo_prompt = f"{keyphrase_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_md_path)}`:\n\n{blog_content}"
        seo_content = call_gemini(final_seo_prompt, model_config.get('model_seo', 'gemini-1.5-flash-latest'))

        if seo_content:
            content_to_write = seo_content
            if youtube_link:
                content_to_write = f"**Sumber Video:** {youtube_link}\n\n---\n\n{seo_content}"
            with open(output_seo_path, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            print(f"✅ Analisis Keyphrase SEO berhasil dibuat dan disimpan di: {output_seo_path}")
        else:
            print("❌ Gagal mendapatkan keyphrase SEO, proses dihentikan.")
            sys.exit(1)

    # --- Persiapan untuk langkah 3, 4, 5: Memilih Keyphrase ---
    selected_keyphrase = None
    if any(step in steps_to_run for step in [3, 4, 5]):
        if not os.path.exists(output_seo_path):
            print(f"❌ Error: File SEO '{output_seo_path}' tidak ditemukan. Jalankan langkah 2 terlebih dahulu.")
            sys.exit(1)
        with open(output_seo_path, 'r', encoding='utf-8') as f:
            seo_content_for_selection = f.read()
        selected_keyphrase = parse_and_select_keyphrase(seo_content_for_selection)
        if not selected_keyphrase:
            print("⚠️ Tidak ada keyphrase yang dipilih. Melewatkan langkah-langkah berikutnya.")
            sys.exit(0)

    # --- LANGKAH 3: Create Final Blog ---
    if 3 in steps_to_run:
        print("\n--- LANGKAH 3: Membuat Blog Final ---")
        if not os.path.exists(output_md_path) or not os.path.exists(input_path):
            print(f"❌ Error: File draf '{output_md_path}' atau file input '{input_path}' tidak ditemukan. Jalankan langkah 1 terlebih dahulu.")
            sys.exit(1)

        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(output_md_path, 'r', encoding='utf-8') as f:
            blog_content = f.read()
        
        create_blog_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_blog.md')
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

        if final_blog_post_content:
            content_to_write = final_blog_post_content
            if youtube_link:
                lines = content_to_write.split('\n', 1)
                title = lines[0]
                body = lines[1] if len(lines) > 1 else ''
                link_markdown = f"\n_Tonton video tutorial asli di YouTube_\n"
                content_to_write = f"{title}\n{link_markdown}\n{body}"
            with open(output_blog_path, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            print(f"✅ Blog post final berhasil dibuat dan disimpan di: {output_blog_path}")
        else:
            print("❌ Gagal membuat blog post final.")
            sys.exit(1)

    # --- LANGKAH 4: Update SEO with Metadata ---
    if 4 in steps_to_run:
        print("\n--- LANGKAH 4: Memperbarui SEO dengan Metadata ---")
        if not os.path.exists(output_blog_path):
            print(f"❌ Error: File blog final '{output_blog_path}' tidak ditemukan. Jalankan langkah 3 terlebih dahulu.")
            sys.exit(1)

        with open(output_blog_path, 'r', encoding='utf-8') as f:
            final_blog_post_content = f.read()
        
        seo_meta_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_seo.md')
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
    if 5 in steps_to_run:
        print("\n--- LANGKAH 5: Membuat Gambar ---")
        image_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_picture.md')
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
    PROMPT_DIR = "prompt"
    MODEL_DIR = "model"
    DEFAULT_PROMPT = "prompt_tutorial_odoo18.md"

    if not os.path.isdir(PROMPT_DIR):
        print(f"❌ Error: Direktori prompt '{PROMPT_DIR}/' tidak ditemukan.")
        sys.exit(1)

    prompt_choices = [f for f in os.listdir(PROMPT_DIR) if f.endswith('.md')]
    if not prompt_choices:
        print(f"❌ Error: Tidak ada file prompt (.md) yang ditemukan di direktori '{PROMPT_DIR}/'.")
        sys.exit(1)

    default_prompt_choice = DEFAULT_PROMPT if DEFAULT_PROMPT in prompt_choices else prompt_choices[0]

    if not os.path.isdir(MODEL_DIR):
        print(f"❌ Error: Direktori model '{MODEL_DIR}/' tidak ditemukan.")
        sys.exit(1)

    model_choices = [f for f in os.listdir(MODEL_DIR) if f.endswith('.json')]
    if not model_choices:
        print(f"❌ Error: Tidak ada file model (.json) yang ditemukan di direktori '{MODEL_DIR}/'.")
        sys.exit(1)

    default_model_choice = "model.json" if "model.json" in model_choices else model_choices[0]

    parser = argparse.ArgumentParser(
        description="Membuat artikel blog dan analisis SEO dari file input menggunakan Gemini.",
        epilog=f"Contoh: python my_generate_blog.py -i nama_file.txt -m {default_model_choice} --step 1 2"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path ke file input teks (misal: .txt).", metavar="FILE_INPUT"
    )
    parser.add_argument(
        "-p", "--prompt",
        default=default_prompt_choice,
        choices=prompt_choices,
        help=f"Pilih file prompt dari direktori '{PROMPT_DIR}/'. (Default: %(default)s)"
    )
    parser.add_argument(
        "-m", "--model-config",
        default=default_model_choice,
        choices=model_choices,
        help=f"Pilih file konfigurasi model dari direktori '{MODEL_DIR}/'. (Default: %(default)s)"
    )
    parser.add_argument(
        "--step",
        nargs='+',
        type=int,
        default=[1, 2, 3, 4, 5],
        choices=range(1, 6),
        metavar='N',
        help="Langkah yang akan dijalankan: 1.Generate Draft, 2.Get Keyphrases, 3.Create Blog, 4.Update SEO, 5.Generate Image. (Default: semua langkah)"
    )
    args = parser.parse_args()

    # Validasi tipe file input
    allowed_extensions = ['.txt', '.vtt', '.srt', '.md']
    _, file_extension = os.path.splitext(args.input)
    if file_extension.lower() not in allowed_extensions:
        parser.error(f"File input harus berupa file teks dengan ekstensi: {', '.join(allowed_extensions)}")

    if not os.path.exists(args.input):
        parser.error(f"File input tidak ditemukan: {args.input}")

    full_prompt_path = os.path.join(PROMPT_DIR, args.prompt)
    full_model_config_path = os.path.join(MODEL_DIR, args.model_config)
    run_generation_workflow(args.input, full_prompt_path, full_model_config_path, sorted(args.step))


if __name__ == "__main__":
    main()
