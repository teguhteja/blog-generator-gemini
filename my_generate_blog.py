#!/usr/bin/env python3
import argparse
import os
import sys
import re
import io
import json
import subprocess
from datetime import datetime
from google import genai as genai_image
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from google.genai import types
from io import BytesIO

# Data harga berdasarkan dokumentasi resmi Google AI.
# Ini digunakan untuk membuat estimasi biaya dan mencatatnya.
MODEL_PRICING = {
    "gemini-1.5-pro": {
        "input_per_1k_chars": 0.0035, "output_per_1k_chars": 0.0105, "image_cost": 0.0180
    },
    "gemini-1.5-flash": {
        "input_per_1k_chars": 0.00035, "output_per_1k_chars": 0.00105, "image_cost": 0.0
    },
    "gemini-1.0-pro": {
        "input_per_1k_chars": 0.0005, "output_per_1k_chars": 0.0015, "image_cost": 0.0
    },
    # Model default jika tidak ditemukan
    "default": {
        "input_per_1k_chars": 0.0035, "output_per_1k_chars": 0.0105, "image_cost": 0.0180
    }
}

def get_pricing(model_name):
    """Mencari data harga untuk model tertentu, atau mengembalikan harga default."""
    for key, value in MODEL_PRICING.items():
        if key in model_name:
            return value
    return MODEL_PRICING["default"]


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
        
        # Catat penggunaan setelah panggilan berhasil
        input_chars = len(prompt_text)
        output_chars = len(response.text)
        log_usage_and_cost(model_name, input_chars=input_chars, output_chars=output_chars)

        return response.text
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menghubungi Gemini API: {e}")
        return None

def log_usage_and_cost(model_name, input_chars=0, output_chars=0, images_generated=0):
    """Mencatat penggunaan API dan estimasi biaya ke file CSV."""
    log_file = 'usage_log.csv'
    
    pricing = get_pricing(model_name)
    input_cost = (input_chars / 1000) * pricing['input_per_1k_chars']
    output_cost = (output_chars / 1000) * pricing['output_per_1k_chars']
    image_cost = images_generated * pricing.get('image_cost', 0.0)
    total_cost = input_cost + output_cost + image_cost

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{model_name},{input_chars},{output_chars},{images_generated},{total_cost:.6f}\n"

    # Buat header jika file belum ada
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Timestamp,Model,Input Chars,Output Chars,Images Generated,Estimated Cost ($)\n")

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(f"📝 Penggunaan dicatat. Estimasi biaya untuk panggilan ini: ${total_cost:.6f}")

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
    Mengubah teks menjadi nama file yang valid tanpa menggunakan '-'.
    CATATAN: Versi ini mempertahankan spasi, yang tidak direkomendasikan untuk web.
    """
    # Hapus karakter non-alfanumerik (kecuali spasi) dan ubah ke huruf kecil.
    sanitized = re.sub(r'[^\w\s]', '', text.lower()).strip()
    # Ganti beberapa spasi yang berurutan dengan satu spasi tunggal.
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return f"{sanitized}.{extension}"

def resize_image(image_path, target_kb=100):
    """
    Mengubah ukuran dan mengoptimalkan gambar untuk web menggunakan ImageMagick,
    dengan menargetkan ukuran file di bawah `target_kb`.
    """
    try:
        # Dapatkan ekstensi file untuk menentukan format
        _, extension = os.path.splitext(image_path)
        is_jpeg = extension.lower() in ['.jpg', '.jpeg']

        print(f"🖼️  Mengoptimalkan gambar: {image_path} (Target: < {target_kb} KB)")

        # Perintah dasar untuk mengubah ukuran dan menghapus metadata
        # -resize '1024x720>' : hanya resize jika gambar lebih besar dari dimensi ini
        # -strip : hapus semua data meta (EXIF, dll) untuk mengurangi ukuran
        # -interlace Plane : membuat gambar progressive (baik untuk web)
        command = [
            'convert', str(image_path),
            '-resize', '1024x720>',
            '-strip',
            '-interlace', 'Plane',
        ]

        # Opsi terbaik untuk JPEG: targetkan ukuran file secara langsung.
        # ImageMagick akan mencoba mencapai target ini dengan menyesuaikan kualitas.
        if is_jpeg:
            command.extend(['-define', f'jpeg:extent={target_kb}kb'])
        else: # Fallback untuk format lain seperti PNG
            command.extend(['-quality', '85']) # Kualitas 85 adalah kompromi yang baik

        command.append(str(image_path)) # Timpa file asli
        subprocess.run(command, check=True, capture_output=True, text=True)

        final_size_kb = os.path.getsize(image_path) / 1024
        print(f"✅ Gambar berhasil dioptimalkan. Ukuran akhir: {final_size_kb:.2f} KB.")
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

    # --- Persiapan untuk langkah-langkah yang memerlukan keyphrase (3 & 5) ---
    selected_keyphrase = None
    if any(step in steps_to_run for step in [3, 5]):
        if os.path.exists(output_seo_path):
            with open(output_seo_path, 'r', encoding='utf-8') as f:
                seo_content_for_selection = f.read()
            selected_keyphrase = parse_and_select_keyphrase(seo_content_for_selection)
        else:
            print(f"ℹ️  File SEO '{output_seo_path}' tidak ditemukan. Keyphrase perlu diinput manual jika diperlukan.")

    # --- LANGKAH 3: Create Final Blog ---
    if 3 in steps_to_run:
        print("\n--- LANGKAH 3: Membuat Blog Final ---")
        if not selected_keyphrase:
            print("❌ Error: Langkah 3 memerlukan keyphrase. Jalankan langkah 2 terlebih dahulu atau pastikan ada pilihan di file .seo.md.")
            sys.exit(1)

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
        keyphrase_for_image = selected_keyphrase
        if not keyphrase_for_image:
            print("⚠️ Keyphrase belum dipilih atau ditentukan.")
            try:
                keyphrase_for_image = input("   Masukkan keyphrase untuk gambar: ").strip()
                if not keyphrase_for_image:
                    print("❌ Input kosong, melewatkan pembuatan gambar.")
                    keyphrase_for_image = None
            except KeyboardInterrupt:
                print("\n❌ Input dibatalkan, melewatkan pembuatan gambar.")
                keyphrase_for_image = None

        if keyphrase_for_image:
            image_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_picture.md')
            if not os.path.exists(image_prompt_path):
                print(f"⚠️ Peringatan: File prompt '{image_prompt_path}' tidak ditemukan. Melewatkan pembuatan gambar.")
            else:
                with open(image_prompt_path, 'r', encoding='utf-8') as f:
                    image_prompt_content = f.read()

                final_image_prompt = image_prompt_content.format(keyphrase_for_image)
                image_model = model_config.get('model_image', 'gemini-1.5-pro-latest')
                print(f"ℹ️  Menggunakan keyphrase '{keyphrase_for_image}' dan model '{image_model}' untuk pembuatan gambar.")
                generated_image = generate_image(final_image_prompt, model_name=image_model, api_key=api_key)

                # Catat penggunaan setelah panggilan berhasil
                if generated_image:
                    log_usage_and_cost(image_model, input_chars=len(final_image_prompt), images_generated=1)

                if generated_image:
                    image_filename = sanitize_filename(keyphrase_for_image, 'jpg')
                    image_path = os.path.join(dir_name, image_filename)

                    if generated_image.mode == 'RGBA':
                        print("ℹ️  Mengonversi gambar dari RGBA ke RGB untuk penyimpanan JPEG.")
                        generated_image = generated_image.convert('RGB')

                    generated_image.save(image_path, 'JPEG', quality=95)
                    print(f"✅ Gambar berhasil dibuat dan disimpan di: {image_path}")
                    resize_image(image_path, target_kb=100)
        else:
            print("   Tidak ada keyphrase yang valid, pembuatan gambar dilewati.")
    
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
        "-i", "--input", required=True, help="Path ke file input (.txt). File selain .txt tidak diizinkan untuk menghemat kuota API.", metavar="FILE_INPUT"
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
    allowed_extensions = ['.txt']
    _, file_extension = os.path.splitext(args.input)
    if file_extension.lower() not in allowed_extensions:
        parser.error(f"File input harus berupa file .txt. Tipe file lain tidak diizinkan untuk menghemat kuota API.")

    if not os.path.exists(args.input):
        parser.error(f"File input tidak ditemukan: {args.input}")

    full_prompt_path = os.path.join(PROMPT_DIR, args.prompt)
    full_model_config_path = os.path.join(MODEL_DIR, args.model_config)
    run_generation_workflow(args.input, full_prompt_path, full_model_config_path, sorted(args.step))


if __name__ == "__main__":
    main()
