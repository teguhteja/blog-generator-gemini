#!/usr/bin/env python3
"""
YouTube Subtitle to WordPress Blog Automation
Download YouTube subtitles, generate blog post, and upload to WordPress
"""

import subprocess
import sys
import os
import argparse
import glob
import re


def extract_code_or_keywords(nama_file):
    """
    Ekstrak kode dari [kode] atau ambil 3 kata pertama dari nama_file
    Returns: (identifier, is_code)
    """
    # Cari pattern [kode] dalam nama_file
    code_pattern = r'\[([a-zA-Z0-9_-]{8,})\]'
    match = re.search(code_pattern, nama_file)
    
    if match:
        code = match.group(1)
        print(f"🔍 Kode ditemukan: {code}")
        return code, True
    else:
        # Ambil 3 kata pertama, hilangkan karakter khusus
        words = re.findall(r'\w+', nama_file)
        if len(words) >= 3:
            keywords = '-'.join(words[:3]).lower()
        elif len(words) > 0:
            keywords = '-'.join(words).lower()
        else:
            keywords = nama_file.lower()
        
        print(f"🔍 Menggunakan keywords: {keywords}")
        return keywords, False

def find_subtitle_file(identifier):
    """
    Cari file subtitle .txt yang sudah ada berdasarkan identifier (kode atau keywords)
    Returns: path file subtitle atau None
    """
    # Hanya cari file .txt saja
    pattern = f"*{identifier}*.txt"
    
    files = glob.glob(pattern)
    if files:
        subtitle_file = files[0]  # Ambil file pertama
        print(f"✅ File subtitle .txt ditemukan: {subtitle_file}")
        return subtitle_file
    
    print(f"⚠️ File subtitle .txt tidak ditemukan untuk: {identifier}")
    return None

def find_output_folder(identifier, original_filename=None):
    """
    Cari folder output berdasarkan identifier atau nama file asli
    Returns: path folder atau None
    """
    # Pattern 1: Cari berdasarkan identifier yang dinormalisasi
    possible_folders = glob.glob(f"*{identifier}*")
    folders = [f for f in possible_folders if os.path.isdir(f)]
    
    if folders:
        output_folder = folders[0]
        print(f"✅ Folder output ditemukan (identifier): {output_folder}")
        return output_folder
    
    # Pattern 2: Jika ada original filename, cari berdasarkan nama asli
    if original_filename:
        # Hapus ekstensi dari nama file asli
        base_name = os.path.splitext(os.path.basename(original_filename))[0]
        possible_folders = glob.glob(f"*{base_name}*")
        folders = [f for f in possible_folders if os.path.isdir(f)]
        
        if folders:
            output_folder = folders[0]
            print(f"✅ Folder output ditemukan (nama asli): {output_folder}")
            return output_folder
    
    # Pattern 3: Cari folder yang mengandung kata-kata dari identifier
    if '-' in identifier:
        words = identifier.split('-')
        for word in words:
            if len(word) > 2:  # Skip kata pendek
                possible_folders = glob.glob(f"*{word}*")
                folders = [f for f in possible_folders if os.path.isdir(f)]
                if folders:
                    output_folder = folders[0]
                    print(f"✅ Folder output ditemukan (kata kunci '{word}'): {output_folder}")
                    return output_folder
    
    print(f"⚠️ Folder output tidak ditemukan untuk: {identifier}")
    return None

def check_folder_contents(folder_path):
    """
    Periksa apakah folder sudah berisi seo.json dan file .html
    Returns: (has_seo_json, has_html, html_file_path)
    """
    if not os.path.exists(folder_path):
        return False, False, None
    
    seo_json_path = os.path.join(folder_path, 'seo.json')
    has_seo_json = os.path.exists(seo_json_path)
    
    # Cari file .html dalam folder
    html_files = glob.glob(os.path.join(folder_path, '*.html'))
    has_html = len(html_files) > 0
    html_file_path = html_files[0] if html_files else None
    
    print(f"📋 Status folder {folder_path}:")
    print(f"   {'✅' if has_seo_json else '❌'} seo.json: {'Ada' if has_seo_json else 'Tidak ada'}")
    print(f"   {'✅' if has_html else '❌'} HTML file: {'Ada' if has_html else 'Tidak ada'} {f'({os.path.basename(html_file_path)})' if html_file_path else ''}")
    
    return has_seo_json, has_html, html_file_path

def run_command(command, description):
    """Jalankan command dan tampilkan hasilnya"""
    print(f"🔄 {description}")
    print(f"📝 Menjalankan: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} berhasil")
        if result.stdout:
            print(f"📤 Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} gagal")
        print(f"Error code: {e.returncode}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command tidak ditemukan: {command[0]}")
        return False


def main():
    """Fungsi utama"""
    parser = argparse.ArgumentParser(
        description='Otomasi YouTube subtitle ke WordPress blog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python subs-blog-wordpress.py my-video-file     # Proses dari my-video-file
  python subs-blog-wordpress.py video_id_123     # Proses dari video_id_123
  python subs-blog-wordpress.py subtitle.txt     # Skip download, langsung proses .txt file

Script akan menjalankan:
- Jika input .txt: main.py file.txt → wordpress_uploader.py folder/
- Jika bukan .txt: get_subs_youtube.py → main.py → wordpress_uploader.py

Catatan:
- File .env harus berisi kredensial WordPress
- Pastikan semua script dependencies tersedia
        """
    )
    
    parser.add_argument(
        'nama_file',
        type=str,
        help='Nama file untuk diproses (bisa .txt file atau nama tanpa ekstensi)'
    )
    
    parser.add_argument(
        '--status',
        choices=['draft', 'publish', 'private'],
        default='draft',
        help='Status post WordPress (default: draft)'
    )
    
    args = parser.parse_args()
    
    nama_file = args.nama_file
    post_status = args.status
    
    # Dapatkan direktori script ini
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path absolut untuk semua script
    get_subs_script = os.path.join(script_dir, 'get_subs_youtube.py')
    main_script = os.path.join(script_dir, 'main.py')
    wordpress_script = os.path.join(script_dir, 'wordpress_uploader.py')
    
    print(f"🚀 Memulai otomasi untuk: {nama_file}")
    print(f"📝 Status WordPress: {post_status}")
    print(f"📂 Script directory: {script_dir}")
    print("=" * 50)
    
    # Cek apakah input sudah file .txt
    if nama_file.lower().endswith('.txt'):
        print(f"📄 Input adalah file .txt: {nama_file}")
        if not os.path.exists(nama_file):
            print(f"❌ File tidak ditemukan: {nama_file}")
            sys.exit(1)
        subtitle_file = nama_file
        # Ekstrak identifier dari nama file untuk mencari folder output
        base_name = os.path.splitext(os.path.basename(nama_file))[0]
        identifier, is_code = extract_code_or_keywords(base_name)
        print("\n⏭️ LANGKAH 1: Skip download subtitle (file .txt sudah tersedia)")
    else:
        # Ekstrak kode atau keywords dari nama_file
        identifier, is_code = extract_code_or_keywords(nama_file)
        
        # Langkah 1: Cari atau download subtitle
        print("\n📥 LANGKAH 1: Cari atau download subtitle")
        subtitle_file = find_subtitle_file(identifier)
        
        if subtitle_file:
            print("✅ File subtitle sudah ada, skip download")
        else:
            print("📥 File subtitle tidak ditemukan, mencoba download...")
            if not run_command(['python', get_subs_script, '-f', nama_file], 
                              "Download YouTube subtitles"):
                print("❌ Gagal download subtitles, menghentikan proses")
                sys.exit(1)
            
            # Cari lagi setelah download
            subtitle_file = find_subtitle_file(identifier)
            if not subtitle_file:
                print(f"❌ File subtitle masih tidak ditemukan setelah download")
                sys.exit(1)
    
    # Cek apakah folder output sudah ada
    print("\n🔍 LANGKAH 2: Cek status folder output")
    output_folder = find_output_folder(identifier, subtitle_file)
    
    if output_folder:
        # Folder sudah ada, cek isinya
        has_seo_json, has_html, html_file_path = check_folder_contents(output_folder)
        
        if has_seo_json and has_html:
            print("✅ Folder sudah lengkap (seo.json + HTML), skip generate blog post")
            need_generate = False
        else:
            print("⚠️ Folder tidak lengkap, perlu generate ulang")
            need_generate = True
    else:
        print("⚠️ Folder belum ada, perlu generate blog post")
        need_generate = True
    
    # Langkah 3: Generate blog post (jika diperlukan)
    if need_generate:
        print("\n📝 LANGKAH 3: Generate blog post")
        if not run_command(['python', main_script, subtitle_file], 
                          "Generate blog post"):
            print("❌ Gagal generate blog post, menghentikan proses")
            sys.exit(1)
        
        # Cari folder output setelah generate dengan multiple strategies
        output_folder = find_output_folder(identifier, subtitle_file)
        if not output_folder:
            print(f"❌ Folder output tidak ditemukan setelah generate untuk identifier: {identifier}")
            print(f"💡 Mencoba dengan nama file asli: {subtitle_file}")
            sys.exit(1)
    else:
        print("\n⏭️ LANGKAH 3: Skip generate blog post (sudah ada)")
    
    # Langkah 4: Upload ke WordPress
    print("\n📤 LANGKAH 4: Upload ke WordPress")
    if not run_command(['python', wordpress_script, '-f', output_folder, '-s', post_status], 
                      "Upload ke WordPress"):
        print("❌ Gagal upload ke WordPress")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Proses otomasi selesai!")
    print(f"✅ Identifier: {identifier}")
    print(f"✅ Subtitle file: {subtitle_file}")
    print(f"✅ Blog folder: {output_folder}")
    print(f"✅ WordPress uploaded dengan status: {post_status}")


if __name__ == "__main__":
    main()