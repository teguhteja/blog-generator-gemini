#!/usr/bin/env python3
"""
WordPress Auto Upload Script
Membaca file HTML dan JPG dari folder, kemudian upload ke WordPress
"""

import os
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv
import json
import mimetypes
from bs4 import BeautifulSoup
import argparse

class WordPressUploader:
    def __init__(self, env_file='.env'):
        """Initialize dengan kredensial dari file .env"""
        # Jika env_file adalah path relatif, gunakan direktori script
        if not os.path.isabs(env_file):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            env_file = os.path.join(script_dir, env_file)
        load_dotenv(env_file)
        
        self.wp_url = os.getenv('WP_URL')  # https://yoursite.com
        self.wp_username = os.getenv('WP_USERNAME')
        self.wp_password = os.getenv('WP_PASSWORD')
        
        if not all([self.wp_url, self.wp_username, self.wp_password]):
            raise ValueError("Missing WordPress credentials in .env file")
        
        # API endpoints
        self.api_base = f"{self.wp_url.rstrip('/')}/wp-json/wp/v2"
        self.media_endpoint = f"{self.api_base}/media"
        self.posts_endpoint = f"{self.api_base}/posts"
        
        # Rank Math API endpoint
        self.rankmath_endpoint = f"{self.wp_url.rstrip('/')}/wp-json/rank-math-api/v1/update-meta"
        
        # Auth header
        credentials = f"{self.wp_username}:{self.wp_password}"
        token = base64.b64encode(credentials.encode())
        self.headers = {
            'Authorization': f'Basic {token.decode("utf-8")}',
            'Content-Type': 'application/json'
        }
    
    def get_small_images(self, folder_path, max_size_kb=100):
        """Dapatkan list gambar yang ukurannya kurang dari max_size_kb"""
        folder_path = Path(folder_path)
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
        small_images = []
        
        for ext in image_extensions:
            for image_file in folder_path.glob(ext):
                # Cek ukuran file dalam KB
                file_size_kb = image_file.stat().st_size / 1024
                if file_size_kb < max_size_kb:
                    small_images.append(image_file)
                    print(f"📏 {image_file.name}: {file_size_kb:.1f} KB (akan diupload)")
                else:
                    print(f"⚠️ {image_file.name}: {file_size_kb:.1f} KB (terlalu besar, dilewati)")
        
        return small_images

    def upload_image(self, image_path):
        """Upload gambar ke WordPress Media Library dengan alt text"""
        if not os.path.exists(image_path):
            print(f"❌ File gambar tidak ditemukan: {image_path}")
            return None
        
        print(f"📤 Uploading gambar: {image_path}")
        
        # Prepare file untuk upload
        filename = os.path.basename(image_path)
        alt_text = Path(image_path).stem  # Nama file tanpa ekstensi
        mime_type = mimetypes.guess_type(image_path)[0] or 'image/jpeg'
        
        with open(image_path, 'rb') as img_file:
            files = {
                'file': (filename, img_file, mime_type)
            }
            
            data = {
                'alt_text': alt_text,
                'title': alt_text
            }
            
            headers_upload = {
                'Authorization': self.headers['Authorization']
            }
            
            response = requests.post(
                self.media_endpoint,
                headers=headers_upload,
                files=files,
                data=data
            )
        
        if response.status_code == 201:
            media_data = response.json()
            print(f"✅ Gambar berhasil diupload - ID: {media_data['id']}, Alt: '{alt_text}'")
            return media_data
        else:
            print(f"❌ Gagal upload gambar: {response.status_code} - {response.text}")
            return None
    
    def read_seo_json(self, folder_path):
        """Baca file seo.json dari folder"""
        seo_file_path = os.path.join(folder_path, 'seo.json')
        if os.path.exists(seo_file_path):
            try:
                with open(seo_file_path, 'r', encoding='utf-8') as f:
                    seo_data = json.load(f)
                print(f"📊 SEO data dimuat dari {seo_file_path}")
                return seo_data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ Error membaca seo.json: {e}")
                return None
        return None

    def update_rankmath_seo(self, post_id, seo_data):
        """Update Rank Math SEO metadata menggunakan API"""
        if not seo_data or 'meta' not in seo_data:
            print("⚠️ Tidak ada SEO data untuk update Rank Math")
            return False
        
        meta = seo_data['meta']
        
        # Prepare data untuk Rank Math API
        rankmath_data = {
            'post_id': post_id
        }
        
        # Map SEO fields ke Rank Math API
        if 'rank_math_title' in meta:
            rankmath_data['rank_math_title'] = meta['rank_math_title']
        
        if 'rank_math_description' in meta:
            rankmath_data['rank_math_description'] = meta['rank_math_description']
        
        if 'rank_math_focus_keyword' in meta:
            rankmath_data['rank_math_focus_keyword'] = meta['rank_math_focus_keyword']
        
        if 'rank_math_canonical_url' in meta:
            rankmath_data['rank_math_canonical_url'] = meta['rank_math_canonical_url']
        
        # Jika tidak ada field yang akan diupdate
        if len(rankmath_data) == 1:  # Hanya post_id
            print("⚠️ Tidak ada field Rank Math untuk diupdate")
            return False
        
        print(f"🎯 Updating Rank Math SEO untuk post ID: {post_id}")
        
        # Headers untuk form-urlencoded
        headers_rankmath = {
            'Authorization': self.headers['Authorization'],
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Kirim request ke Rank Math API
        response = requests.post(
            self.rankmath_endpoint,
            headers=headers_rankmath,
            data=rankmath_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Rank Math SEO berhasil diupdate")
            
            # Log field yang berhasil diupdate
            for field, status in result.items():
                if status == 'updated':
                    print(f"   ✓ {field}: updated")
            
            return True
        else:
            print(f"❌ Gagal update Rank Math SEO: {response.status_code} - {response.text}")
            return False

    def create_post(self, html_file_path, featured_image_id=None, status='draft', seo_data=None):
        """Buat post WordPress dari file HTML dengan SEO metadata"""
        if not os.path.exists(html_file_path):
            print(f"❌ File HTML tidak ditemukan: {html_file_path}")
            return None
        
        # Baca konten HTML
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Extract title dari H1 tag (prioritas utama)
        h1_tag = soup.find('h1')
        if h1_tag:
            post_title = h1_tag.get_text().strip()
            # 2. Hapus H1 tag dari konten
            h1_tag.decompose()
            print(f"📰 Title dari H1: {post_title}")
        else:
            # Fallback ke title tag atau nama file
            title_tag = soup.find('title')
            post_title = title_tag.get_text() if title_tag else os.path.splitext(os.path.basename(html_file_path))[0]
            print(f"📰 Title fallback: {post_title}")
        
        # Ambil konten dari <body> atau gunakan semua HTML
        body_tag = soup.find('body')
        post_content = str(body_tag) if body_tag else str(soup)
        
        print(f"📝 Membuat post: {post_title}")
        
        # Data post dasar
        post_data = {
            'title': post_title,
            'content': post_content,
            'status': status  # 'draft', 'publish', 'private'
        }
        
        # Set featured image jika ada
        if featured_image_id:
            post_data['featured_media'] = featured_image_id
        
        # Set slug dari SEO data jika ada
        if seo_data and 'slug' in seo_data:
            post_data['slug'] = seo_data['slug']
            print(f"🔗 Slug: {seo_data['slug']}")
        
        # Kirim ke WordPress
        response = requests.post(
            self.posts_endpoint,
            headers=self.headers,
            json=post_data
        )
        
        if response.status_code == 201:
            post_info = response.json()
            post_id = post_info['id']
            print(f"✅ Post berhasil dibuat - ID: {post_id}")
            print(f"🔗 URL: {post_info['link']}")
            
            # Update Rank Math SEO menggunakan API terpisah
            if seo_data:
                print("🔄 Mengupdate Rank Math SEO metadata...")
                self.update_rankmath_seo(post_id, seo_data)
            
            return post_info
        else:
            print(f"❌ Gagal membuat post: {response.status_code} - {response.text}")
            return None
    
    def process_folder(self, folder_path, post_status='draft'):
        """Proses semua file HTML dan upload gambar kecil dalam folder"""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print(f"❌ Folder tidak ditemukan: {folder_path}")
            return
        
        print(f"📁 Memproses folder: {folder_path}")
        
        # Baca SEO data dari seo.json jika ada
        seo_data = self.read_seo_json(str(folder_path))
        
        # Cari file HTML dan gambar kecil
        html_files = list(folder_path.glob('*.html'))
        small_images = self.get_small_images(folder_path, max_size_kb=100)
        
        print(f"\nDitemukan {len(html_files)} file HTML dan {len(small_images)} gambar kecil (<100KB)")
        
        # Upload semua gambar kecil terlebih dahulu
        uploaded_images = {}  # {filename_stem: media_data}
        if small_images:
            print(f"\n🖼️ Mengupload {len(small_images)} gambar kecil...")
            for image_file in small_images:
                media_data = self.upload_image(str(image_file))
                if media_data:
                    uploaded_images[image_file.stem] = media_data
        
        # Proses setiap file HTML
        for html_file in html_files:
            print(f"\n--- Memproses {html_file.name} ---")
            
            # Cari gambar dengan nama yang sama (tanpa ekstensi)
            html_name = html_file.stem
            featured_image_id = None
            
            if html_name in uploaded_images:
                featured_image_id = uploaded_images[html_name]['id']
                print(f"🖼️ Menggunakan featured image: {html_name} (ID: {featured_image_id})")
            else:
                print("⚠️ Tidak ada gambar yang cocok ditemukan untuk featured image")
            
            # Buat post dengan SEO data
            self.create_post(str(html_file), featured_image_id, post_status, seo_data)


def main():
    """Fungsi utama"""
    parser = argparse.ArgumentParser(
        description='WordPress Auto Upload Script - Upload HTML dan JPG files ke WordPress',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python wordpress-uploader.py                           # Interactive mode
  python wordpress-uploader.py -f ./content             # Upload dari folder content
  python wordpress-uploader.py -f ./content -s publish  # Upload sebagai published post
  python wordpress-uploader.py -f ./content -s draft    # Upload sebagai draft (default)

Catatan:
  - File .env harus berisi WP_URL, WP_USERNAME, dan WP_PASSWORD
  - Script akan mencari file HTML dan JPG dengan nama yang sama
  - Jika ada gambar JPG dengan nama sama, akan dijadikan featured image
        """
    )
    
    parser.add_argument(
        '-f', '--folder',
        type=str,
        help='Path folder yang berisi file HTML dan JPG (default: interactive input)'
    )
    
    parser.add_argument(
        '-s', '--status',
        choices=['draft', 'publish', 'private'],
        default='draft',
        help='Status post WordPress (default: draft)'
    )
    
    args = parser.parse_args()
    
    try:
        # Inisialisasi uploader
        uploader = WordPressUploader()
        
        # Tentukan folder
        if args.folder:
            content_folder = args.folder
            post_status = args.status
            print(f"📁 Menggunakan folder: {content_folder}")
            print(f"📝 Status post: {post_status}")
        else:
            # Mode interaktif
            content_folder = input("Masukkan path folder konten (enter untuk folder saat ini): ").strip()
            if not content_folder:
                content_folder = "."
            
            # Status post
            print("\nPilih status post:")
            print("1. Draft (default)")
            print("2. Published")
            print("3. Private")
            
            status_choice = input("Pilihan (1-3): ").strip()
            status_map = {'1': 'draft', '2': 'publish', '3': 'private'}
            post_status = status_map.get(status_choice, 'draft')
        
        print(f"\n🚀 Memulai upload dengan status: {post_status}")
        
        # Proses folder
        uploader.process_folder(content_folder, post_status)
        
        print("\n✅ Selesai!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()