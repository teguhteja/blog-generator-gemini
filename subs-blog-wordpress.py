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

def find_output_folder(identifier):
    """
    Cari folder output berdasarkan identifier
    Returns: path folder atau None
    """
    # Cari folder yang mengandung identifier
    possible_folders = glob.glob(f"*{identifier}*")
    folders = [f for f in possible_folders if os.path.isdir(f)]
    
    if folders:
        output_folder = folders[0]
        print(f"✅ Folder output ditemukan: {output_folder}")
        return output_folder
    
    print(f"⚠️ Folder output tidak ditemukan untuk: {identifier}")
    return None

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
        
        if not subtitle_file:
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
    
    # Langkah 2: Generate blog post
    print("\n📝 LANGKAH 2: Generate blog post")
    if not run_command(['python', main_script, subtitle_file], 
                      "Generate blog post"):
        print("❌ Gagal generate blog post, menghentikan proses")
        sys.exit(1)
    
    # Langkah 3: Cari folder output
    print("\n🔍 LANGKAH 3: Cari folder output")
    output_folder = find_output_folder(identifier)
    
    if not output_folder:
        print(f"❌ Folder output tidak ditemukan untuk identifier: {identifier}")
        sys.exit(1)
    
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