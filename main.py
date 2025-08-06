#!/usr/bin/env python3
import argparse
import os
import sys
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Impor modul dari direktori lib
from lib import workflow_steps, utils

def run_workflow(input_path, blog_prompt_path, model_config_path, steps_to_run):
    """
    Mengorkestrasi alur kerja pembuatan blog dengan memanggil fungsi dari modul.
    """
    print(f"🚀 Memulai alur kerja untuk '{input_path}' dengan langkah: {steps_to_run}")

    # Langkah 0: Konfigurasi awal dan validasi path
    load_dotenv()

    try:
        with open(model_config_path, 'r') as f:
            model_config = json.load(f)
        print(f"✅ Konfigurasi model berhasil dimuat dari {model_config_path}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error memuat atau mem-parsing file konfigurasi model: {e}")
        sys.exit(1)

    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        sys.exit(1)
    genai.configure(api_key=api_key)

    base_name = os.path.basename(input_path)
    youtube_code_match = re.search(r'\[([a-zA-Z0-9_-]+)\]', base_name)
    youtube_link = f"https://www.youtube.com/watch?v={youtube_code_match.group(1)}" if youtube_code_match else None
    if youtube_link:
        print(f"🔗 Tautan YouTube terdeteksi: {youtube_link}")

    # Siapkan nama direktori dan path file
    dir_name, _ = os.path.splitext(base_name)
    if not dir_name:
        print(f"❌ Error: Nama file tidak valid untuk membuat direktori dari '{input_path}'")
        sys.exit(1)

    output_md_path = os.path.join(dir_name, f"{dir_name}.md")
    output_seo_path = os.path.join(dir_name, f"{dir_name}.seo.md")
    output_blog_path = os.path.join(dir_name, f"{dir_name}.blog.md")

    os.makedirs(dir_name, exist_ok=True)
    print(f"✅ Direktori '{dir_name}' berhasil disiapkan.")

    # --- Eksekusi Alur Kerja Berdasarkan Langkah ---
    if 1 in steps_to_run:
        if not workflow_steps.generate_draft_tutorial(input_path, blog_prompt_path, base_name, output_md_path, model_config):
            sys.exit(1)

    if 2 in steps_to_run:
        if not workflow_steps.get_seo_keyphrases(output_md_path, output_seo_path, youtube_link, model_config):
            sys.exit(1)

    # Persiapan untuk langkah-langkah yang memerlukan keyphrase (3, 4, 5)
    selected_keyphrase = None
    if any(step in steps_to_run for step in [3, 4, 5]):
        if os.path.exists(output_seo_path):
            with open(output_seo_path, 'r', encoding='utf-8') as f:
                seo_content_for_selection = f.read()
            selected_keyphrase = utils.parse_and_select_keyphrase(seo_content_for_selection)
        else:
            print(f"ℹ️  File SEO '{output_seo_path}' tidak ditemukan. Keyphrase perlu diinput manual jika diperlukan.")

    if 3 in steps_to_run:
        if not selected_keyphrase:
            print("❌ Error: Langkah 3 memerlukan keyphrase. Jalankan langkah 2 terlebih dahulu.")
            sys.exit(1)
        if not workflow_steps.create_final_blog(selected_keyphrase, input_path, output_md_path, output_blog_path, base_name, youtube_link, model_config):
            sys.exit(1)

    if 4 in steps_to_run:
        if not workflow_steps.update_seo_with_metadata(output_blog_path, output_seo_path, model_config):
            print("⚠️ Peringatan: Gagal memperbarui metadata SEO, melanjutkan proses...")

    if 5 in steps_to_run:
        if not workflow_steps.generate_blog_image(selected_keyphrase, dir_name, model_config, api_key):
            print("⚠️ Peringatan: Gagal membuat gambar, melanjutkan proses...")

    if 6 in steps_to_run:
        blog_md_file = os.path.join(dir_name, f"{dir_name}.blog.md")
        if not workflow_steps.convert_md_to_html(
            blog_md_path=blog_md_file, output_dir=dir_name,
            prompt_path="prompt/prompt_convert_md_to_html.md",
            model_name=model_config.get("model_html", "gemini-1.5-flash"), # Ambil dari config model
            api_key=os.getenv("GANAI_API_KEY")):
            print("⚠️ Peringatan: Gagal membuat html, melanjutkan proses...")

    print("\n🎉 Alur kerja selesai.")

def main():
    """Fungsi utama untuk parsing argumen dan menjalankan skrip."""
    PROMPT_DIR = "prompt"
    MODEL_DIR = "model"
    DEFAULT_PROMPT = "prompt_tutorial_odoo18.md"

    # Validasi direktori
    for dir_path, dir_name in [(PROMPT_DIR, "prompt"), (MODEL_DIR, "model")]:
        if not os.path.isdir(dir_path):
            print(f"❌ Error: Direktori '{dir_name}' ('{dir_path}/') tidak ditemukan.")
            sys.exit(1)

    # Dapatkan pilihan dari direktori
    prompt_choices = [f for f in os.listdir(PROMPT_DIR) if f.endswith('.md')]
    model_choices = [f for f in os.listdir(MODEL_DIR) if f.endswith('.json')]

    if not prompt_choices:
        print(f"❌ Error: Tidak ada file prompt (.md) yang ditemukan di direktori '{PROMPT_DIR}/'.")
        sys.exit(1)
    if not model_choices:
        print(f"❌ Error: Tidak ada file model (.json) yang ditemukan di direktori '{MODEL_DIR}/'.")
        sys.exit(1)

    default_prompt_choice = DEFAULT_PROMPT if DEFAULT_PROMPT in prompt_choices else prompt_choices[0]
    default_model_choice = "model.json" if "model.json" in model_choices else model_choices[0]

    parser = argparse.ArgumentParser(
        description="Membuat artikel blog dan analisis SEO dari file input menggunakan Gemini.",
        epilog=f"Contoh: python {sys.argv[0]} nama_file.txt -m {default_model_choice} --step 1 2"
    )

    parser.add_argument("input", help="Path ke file input (.txt).", metavar="FILE_INPUT")
    parser.add_argument("-p", "--prompt", choices=prompt_choices, help=f"Pilih file prompt dari '{PROMPT_DIR}/'. (Default: auto-select berdasarkan konten)")
    parser.add_argument("-m", "--model-config", default=default_model_choice, choices=model_choices, help=f"Pilih file konfigurasi model dari '{MODEL_DIR}/'. (Default: %(default)s)")
    parser.add_argument("--step", nargs='+', type=int, default=list(range(1, 7)), choices=range(1, 7), metavar='N', help="Langkah yang akan dijalankan: 1.Draft, 2.Keyphrases, 3.Blog, 4.Update SEO, 5.Image. 6.HTML (Default: semua)")
    args = parser.parse_args()

    if not args.input.lower().endswith('.txt'):
        parser.error("File input harus berupa file .txt untuk menghemat kuota API.")

    if not os.path.exists(args.input):
        parser.error(f"File input tidak ditemukan: {args.input}")

    # Auto-select prompt based on input file content if not specified
    if args.prompt is None:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                file_content = f.read().lower()
            
            if 'odoo' in file_content:
                selected_prompt = "prompt_tutorial_odoo18.md"
                print(f"🎯 Auto-selected prompt: {selected_prompt} (detected 'odoo' in input file)")
            else:
                selected_prompt = "prompt_tutorial_subs.md"
                print(f"🎯 Auto-selected prompt: {selected_prompt} (default for non-odoo content)")
                
            # Validate that the selected prompt exists
            if selected_prompt not in prompt_choices:
                print(f"❌ Error: Auto-selected prompt '{selected_prompt}' tidak ditemukan di direktori '{PROMPT_DIR}/'.")
                sys.exit(1)
                
            args.prompt = selected_prompt
        except Exception as e:
            print(f"❌ Error membaca file input untuk auto-select prompt: {e}")
            sys.exit(1)

    full_prompt_path = os.path.join(PROMPT_DIR, args.prompt)
    full_model_config_path = os.path.join(MODEL_DIR, args.model_config)

    run_workflow(args.input, full_prompt_path, full_model_config_path, sorted(list(set(args.step))))

if __name__ == "__main__":
    main()
