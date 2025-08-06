import os
import sys
from . import gemini_api, image_processing, utils
import google.generativeai as genai

PROMPT_DIR = "prompt"

def generate_draft_tutorial(input_path, blog_prompt_path, base_name, output_md_path, model_config):
    """Langkah 1: Membuat draf tutorial dari file input."""
    print("\n--- LANGKAH 1: Membuat Draf Tutorial ---")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_content = f.read()
        with open(blog_prompt_path, 'r', encoding='utf-8') as f:
            blog_prompt_content = f.read()

        final_blog_prompt = f"{blog_prompt_content}\n\n---\n\nKonteks dari file `{base_name}`:\n\n{input_content}"
        model_name = model_config.get('model_tutorial', 'gemini-1.5-flash-latest')
        
        blog_content, in_chars, out_chars = gemini_api.call_gemini(final_blog_prompt, model_name)

        if blog_content:
            utils.log_usage_and_cost(model_name, input_chars=in_chars, output_chars=out_chars)
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(blog_content)
            print(f"✅ Draf berhasil dibuat dan disimpan di: {output_md_path}")
            return True
        else:
            print("❌ Gagal membuat draf, proses dihentikan.")
            return False
    except FileNotFoundError as e:
        print(f"❌ Error file tidak ditemukan di Langkah 1: {e}")
        return False

def get_seo_keyphrases(output_md_path, output_seo_path, youtube_link, model_config):
    """Langkah 2: Mendapatkan keyphrase SEO dari draf."""
    print("\n--- LANGKAH 2: Mendapatkan Keyphrase SEO ---")
    if not os.path.exists(output_md_path):
        print(f"❌ Error: File draf '{output_md_path}' tidak ditemukan. Jalankan langkah 1 terlebih dahulu.")
        return False

    try:
        keyphrase_prompt_path = os.path.join(PROMPT_DIR, "prompt_add_seo.md")
        with open(output_md_path, 'r', encoding='utf-8') as f:
            blog_content = f.read()
        with open(keyphrase_prompt_path, 'r', encoding='utf-8') as f:
            keyphrase_prompt_content = f.read()

        final_seo_prompt = f"{keyphrase_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_md_path)}`:\n\n{blog_content}"
        model_name = model_config.get('model_seo', 'gemini-1.5-flash-latest')
        
        seo_content, in_chars, out_chars = gemini_api.call_gemini(final_seo_prompt, model_name)

        if seo_content:
            utils.log_usage_and_cost(model_name, input_chars=in_chars, output_chars=out_chars)
            content_to_write = seo_content
            if youtube_link:
                content_to_write = f"**Sumber Video:** {youtube_link}\n\n---\n\n{seo_content}"
            with open(output_seo_path, 'w', encoding='utf-8') as f:
                f.write(content_to_write)
            print(f"✅ Analisis Keyphrase SEO berhasil dibuat dan disimpan di: {output_seo_path}")
            return True
        else:
            print("❌ Gagal mendapatkan keyphrase SEO, proses dihentikan.")
            return False
    except FileNotFoundError as e:
        print(f"❌ Error file tidak ditemukan di Langkah 2: {e}")
        return False

def create_final_blog(selected_keyphrase, input_path, output_md_path, output_blog_path, base_name, youtube_link, model_config):
    """Langkah 3: Membuat konten blog final berdasarkan keyphrase."""
    print("\n--- LANGKAH 3: Membuat Blog Final ---")
    if not selected_keyphrase:
        print("❌ Error: Langkah 3 memerlukan keyphrase. Jalankan langkah 2 terlebih dahulu.")
        return False
    if not os.path.exists(output_md_path) or not os.path.exists(input_path):
        print(f"❌ Error: File draf '{output_md_path}' atau file input '{input_path}' tidak ditemukan.")
        return False

    try:
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
        model_name = model_config.get('model_blog', 'gemini-1.5-pro-latest')
        final_blog_post_content, in_chars, out_chars = gemini_api.call_gemini(final_blog_post_prompt, model_name)

        if final_blog_post_content:
            utils.log_usage_and_cost(model_name, input_chars=in_chars, output_chars=out_chars)
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
            return True
        else:
            print("❌ Gagal membuat blog post final.")
            return False
    except FileNotFoundError as e:
        print(f"❌ Error file tidak ditemukan di Langkah 3: {e}")
        return False

def update_seo_with_metadata(output_blog_path, output_seo_path, model_config):
    """Langkah 4: Memperbarui file SEO dengan metadata tambahan."""
    print("\n--- LANGKAH 4: Memperbarui SEO dengan Metadata ---")
    if not os.path.exists(output_blog_path):
        print(f"❌ Error: File blog final '{output_blog_path}' tidak ditemukan. Jalankan langkah 3 terlebih dahulu.")
        return False

    try:
        with open(output_blog_path, 'r', encoding='utf-8') as f:
            final_blog_post_content = f.read()
        
        seo_meta_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_seo.md')
        with open(seo_meta_prompt_path, 'r', encoding='utf-8') as f:
            seo_meta_prompt_content = f.read()

        final_seo_meta_prompt = f"{seo_meta_prompt_content}\n\n---\n\nKonteks dari file `{os.path.basename(output_blog_path)}`:\n\n{final_blog_post_content}"
        model_name = model_config.get('model_seo', 'gemini-1.5-pro-latest')
        seo_meta_content, in_chars, out_chars = gemini_api.call_gemini(final_seo_meta_prompt, model_name)

        if seo_meta_content:
            utils.log_usage_and_cost(model_name, input_chars=in_chars, output_chars=out_chars)
            with open(output_seo_path, 'a', encoding='utf-8') as f:
                f.write("\n\n---\n\n## SEO Metadata Lanjutan\n\n")
                f.write(seo_meta_content)
            print(f"✅ Metadata SEO lanjutan berhasil ditambahkan ke: {output_seo_path}")
            return True
        else:
            print("❌ Gagal membuat metadata SEO lanjutan.")
            return False
    except FileNotFoundError as e:
        print(f"❌ Error file tidak ditemukan di Langkah 4: {e}")
        return False

def generate_blog_image(selected_keyphrase, dir_name, model_config, api_key):
    """Langkah 5: Membuat gambar untuk blog."""
    print("\n--- LANGKAH 5: Membuat Gambar ---")
    if not selected_keyphrase:
        print("⚠️ Keyphrase belum dipilih atau ditentukan.")
        try:
            selected_keyphrase = input("   Masukkan keyphrase untuk gambar: ").strip()
            if not selected_keyphrase:
                print("❌ Input kosong, melewatkan pembuatan gambar.")
                return True # Bukan kegagalan, hanya dilewati
        except KeyboardInterrupt:
            print("\n❌ Input dibatalkan, melewatkan pembuatan gambar.")
            return True # Bukan kegagalan, hanya dilewati

    if not selected_keyphrase:
        print("   Tidak ada keyphrase yang valid, pembuatan gambar dilewati.")
        return True

    try:
        image_prompt_path = os.path.join(PROMPT_DIR, 'prompt_create_picture.md')
        with open(image_prompt_path, 'r', encoding='utf-8') as f:
            image_prompt_content = f.read()

        final_image_prompt = image_prompt_content.format(selected_keyphrase)
        image_model = model_config.get('model_image', 'gemini-1.5-pro-latest')
        print(f"ℹ️  Menggunakan keyphrase '{selected_keyphrase}' dan model '{image_model}' untuk pembuatan gambar.")
        
        generated_image = gemini_api.generate_image(final_image_prompt, model_name=image_model, api_key=api_key)

        if generated_image:
            utils.log_usage_and_cost(image_model, input_chars=len(final_image_prompt), images_generated=1)
            
            image_filename = utils.sanitize_filename(selected_keyphrase, 'jpg')
            image_path = os.path.join(dir_name, image_filename)

            if generated_image.mode == 'RGBA':
                print("ℹ️  Mengonversi gambar dari RGBA ke RGB untuk penyimpanan JPEG.")
                generated_image = generated_image.convert('RGB')

            generated_image.save(image_path, 'JPEG', quality=95)
            print(f"✅ Gambar berhasil dibuat dan disimpan di: {image_path}")
            image_processing.resize_image(image_path, target_kb=100)
            return True
        else:
            print("❌ Gagal membuat gambar.")
            return False
    except FileNotFoundError as e:
        print(f"❌ Error file tidak ditemukan di Langkah 5: {e}")
        return False

def convert_md_to_html(blog_md_path, output_dir, prompt_path, model_name, api_key):
    """
    Mengubah file Markdown blog menjadi file HTML menggunakan Gemini API.

    Args:
        blog_md_path (str): Path ke file .blog.md.
        output_dir (str): Direktori untuk menyimpan file .html.
        prompt_path (str): Path ke file prompt konversi.
        model_name (str): Nama model Gemini yang akan digunakan.
        api_key (str): Google API Key Anda.
    """
    if not os.path.exists(blog_md_path):
        print(f"❌ Error: File blog Markdown tidak ditemukan di {blog_md_path}")
        return

    print("🚀 Langkah 6: Mengubah Markdown menjadi HTML...")

    try:
        # Konfigurasi API
        genai.configure(api_key=api_key)

        # Baca konten markdown
        with open(blog_md_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Baca prompt
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()

        # Gabungkan prompt dan konten sebagai konteks
        full_prompt = f"{prompt_text}\n\n{markdown_content}"
        
        # Panggil Gemini API
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(full_prompt)
        html_content = response.text

        # Simpan file HTML
        base_name = os.path.splitext(os.path.basename(blog_md_path))[0].replace('.blog', '')
        html_file_path = os.path.join(output_dir, f"{base_name}.html")
        
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Berhasil membuat file HTML: {html_file_path}")
        # Anda bisa menambahkan tracking biaya di sini jika perlu
        return True
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat konversi HTML: {e}")
        return False