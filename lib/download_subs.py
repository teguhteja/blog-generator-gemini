import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

try:
    from youtube_utils import get_youtube_transcript
except ImportError:
    print("Error: Gagal mengimpor 'youtube_utils'.")
    print("Pastikan Anda menjalankan skrip ini dari direktori root proyek,")
    print("dan file 'lib/youtube_utils.py' ada.")
    sys.exit(1)

def convert_code_to_url(code):
    """Mengkonversi kode menjadi URL YouTube."""
    return f"https://youtube.com/watch?v={code}"

def main():
    """Fungsi utama untuk menjalankan skrip dari command line."""
    parser = argparse.ArgumentParser(
        description="Mengunduh transkrip dari video YouTube sebagai file .txt.\n"
                    "Menyimpan file dengan format 'Judul Video [ID Video].txt'.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Membuat grup argumen yang saling eksklusif
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l", "--link",
        help="URL lengkap video YouTube"
    )
    group.add_argument(
        "-lc", "--link-code",
        help="Kode video YouTube (11 karakter)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Direktori tujuan untuk menyimpan file transkrip (default: direktori saat ini)."
    )
    
    args = parser.parse_args()

    # Menentukan URL berdasarkan argumen yang diberikan
    if args.link:
        url = args.link
    else:
        url = convert_code_to_url(args.link_code)

    # Memanggil fungsi untuk mengunduh transkrip dan mendapatkan path file
    filepath = get_youtube_transcript(url, output_dir=args.output)

    if not filepath:
        sys.exit(1)  # Pesan error sudah dicetak di dalam get_youtube_transcript

if __name__ == "__main__":
    main()
