import os
import subprocess

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
