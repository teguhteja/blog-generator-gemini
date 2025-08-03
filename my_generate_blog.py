#!/usr/bin/env python3
import argparse
import os
import sys
import re
import google.generativeai as genai
from dotenv import load_dotenv

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

def run_generation_workflow(input_path, blog_prompt_path, model_name):
    """
    Menjalankan alur kerja lengkap: membuat direktori, konten blog, dan analisis SEO.
    """
    # Langkah 1: Konfigurasi awal dan validasi path
    load_dotenv()
    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        print("❌ Error: Variabel GANAI_API_KEY tidak ditemukan di file .env Anda.")
        sys.exit(1)
    genai.configure(api_key=api_key)

    # Definisikan semua path prompt yang dibutuhkan
    seo_prompt_path = "prompt_add_seo.md"
    for path in [input_path, blog_prompt_path, seo_prompt_path]:
        if not os.path.exists(path):
            print(f"❌ Error: File '{path}' tidak ditemukan.")
            sys.exit(1)

    # Langkah 2: Siapkan nama direktori dan path file
    base_name = os.path.basename(input_path)
    dir_name, _ = os.path.splitext(base_name)
    if not dir_name:
        print(f"❌ Error: Nama file tidak valid untuk membuat direktori dari '{input_path}'")
        sys.exit(1)

    output_md_path = os.path.join(dir_name, f"{dir_name}.md")
    output_seo_path = os.path.join(dir_name, f"{dir_name}.seo.md")
    output_blog_path = os.path.join(dir_name, f"{dir_name}.blog.md")

    # Langkah 3: Buat direktori
    try:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Direktori '{dir_name}' berhasil disiapkan.")
    except OSError as e:
        print(f"❌ Gagal membuat direktori '{dir_name}': {e}")
        sys.exit(1)

    # Langkah 4: Buat konten blog
    print(f"📖 Membaca file input: {input_path}")
    print(f"📄 Membaca file prompt blog: {blog_prompt_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(blog_prompt_path, 'r', encoding='utf-8') as f:
            blog_prompt_content = f.read()
    except Exception as e:
        print(f"❌ Error saat membaca file: {e}")
        sys.exit(1)

    final_blog_prompt = f"{blog_prompt_content}\n\n---\n\nKonteks dari file `{base_name}`:\n\n{input_content}"
    blog_content = call_gemini(final_blog_prompt, model_name)

    if blog_content:
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(blog_content)
        print(f"✅ Konten blog berhasil dibuat dan disimpan di: {output_md_path}")
    else:
        print("❌ Gagal membuat konten blog, proses dihentikan.")
        sys.exit(1)

    # Langkah 5: Buat analisis SEO
    print(f"\n📄 Membaca file prompt SEO: {seo_prompt_path}")
    try:
        with open(seo_prompt_path, 'r', encoding='utf-8') as f:
            seo_prompt_content = f.read()
    except Exception as e:
        print(f"❌ Error saat membaca file SEO prompt: {e}")
        sys.exit(1)

    # Menggunakan konten blog yang baru dibuat sebagai konteks untuk SEO
    final_seo_prompt = f"{seo_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_md_path)}`:\n\n{blog_content}"
    seo_content = call_gemini(final_seo_prompt, model_name)

    if seo_content:
        with open(output_seo_path, 'w', encoding='utf-8') as f:
            f.write(seo_content)
        print(f"✅ Analisis SEO berhasil dibuat dan disimpan di: {output_seo_path}")
        
        # Langkah 6: Parsing dan pilih keyphrase
        selected_keyphrase = parse_and_select_keyphrase(seo_content)

        # Langkah 7: Buat blog post final berdasarkan keyphrase yang dipilih
        if selected_keyphrase:
            create_blog_prompt_path = 'prompt_create_blog.md'
            if not os.path.exists(create_blog_prompt_path):
                print(f"❌ Error: File prompt '{create_blog_prompt_path}' tidak ditemukan.")
                sys.exit(1)

            print(f"\n📄 Membaca file prompt final: {create_blog_prompt_path}")
            try:
                with open(create_blog_prompt_path, 'r', encoding='utf-8') as f:
                    create_blog_prompt_content = f.read()
            except Exception as e:
                print(f"❌ Error saat membaca file '{create_blog_prompt_path}': {e}")
                sys.exit(1)
            
            # Injeksi keyphrase ke dalam prompt
            injected_create_blog_prompt = create_blog_prompt_content.format(selected_keyphrase)

            # Gabungkan prompt, konteks dari .vtt, dan konteks dari .md
            final_blog_post_prompt = (
                f"{injected_create_blog_prompt}\n\n"
                f"---\n\n"
                f"CONTEXT FROM ORIGINAL TRANSCRIPT (`{base_name}`):\n\n{input_content}\n\n"
                f"---\n\n"
                f"CONTEXT FROM DRAFT POST (`{os.path.basename(output_md_path)}`):\n\n{blog_content}"
            )

            final_blog_post_content = call_gemini(final_blog_post_prompt, model_name)

            if final_blog_post_content:
                with open(output_blog_path, 'w', encoding='utf-8') as f:
                    f.write(final_blog_post_content)
                print(f"✅ Blog post final berhasil dibuat dan disimpan di: {output_blog_path}")
            else:
                print("❌ Gagal membuat blog post final.")
    else:
        print("❌ Gagal membuat analisis SEO.")
        sys.exit(1)

def main():
    """Fungsi utama untuk parsing argumen dan menjalankan skrip."""
    parser = argparse.ArgumentParser(
        description="Membuat artikel blog dan analisis SEO dari file input menggunakan Gemini.",
        epilog="Contoh: python my_generate_blog.py -i nama_file.vtt -p prompt_tutorial_subs.md -m gemini-1.5-pro-latest"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path ke file input (misal: nama_file.vtt).", metavar="FILE_INPUT"
    )
    parser.add_argument(
        "-p", "--prompt",
        default='prompt_tutorial_odoo18.md',
        choices=['prompt_tutorial_odoo18.md', 'prompt_tutorial_subs.md', 'prompt_create_blog.md'],
        help="Pilih file prompt untuk konten blog. (Default: %(default)s)"
    )
    parser.add_argument(
        "-m", "--model",
        default='gemini-1.5-flash-latest',
        help="Model Gemini yang akan digunakan. (Default: %(default)s)"
    )
    args = parser.parse_args()
    run_generation_workflow(args.input, args.prompt, args.model)

if __name__ == "__main__":
    main()
