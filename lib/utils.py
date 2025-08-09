import os
import re
from datetime import datetime

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

def parse_and_select_keyphrase(seo_content, choice=None):
    """
    Mem-parsing konten SEO dan memilih keyphrase berdasarkan pilihan.

    Args:
        seo_content (str): Teks mentah yang berisi daftar keyphrase bernomor.
        choice (int, optional): 1-5 untuk memilih keyphrase berdasarkan nomor,
                               0 untuk pemilihan manual, None untuk auto-select skor tertinggi.
    
    Returns:
        str: Keyphrase yang dipilih (tanpa skor), atau None jika tidak ada yang dipilih.
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

    # Parse keyphrase dan skor
    parsed_keyphrases = []
    for phrase in keyphrases:
        # Cari pola skor dalam format (skor: X.X) atau (score: X.X) di akhir
        score_match = re.search(r'\((?:skor|score):\s*(\d+(?:\.\d+)?)\)', phrase.strip(), re.IGNORECASE)
        if score_match:
            score = float(score_match.group(1))
            # Hapus skor dari keyphrase
            clean_phrase = re.sub(r'\s*\((?:skor|score):\s*\d+(?:\.\d+)?\)', '', phrase.strip(), flags=re.IGNORECASE)
        else:
            score = 0.0
            clean_phrase = phrase.strip()
        
        parsed_keyphrases.append((clean_phrase, score))

    if not parsed_keyphrases:
        print("\n⚠️ Tidak dapat mem-parsing keyphrase dari hasil SEO.")
        return None

    # Logika pemilihan berdasarkan parameter choice
    if choice is None:
        # Auto-select keyphrase dengan skor tertinggi
        selected_phrase, highest_score = max(parsed_keyphrases, key=lambda x: x[1])
        print(f"\n🎯 Keyphrase dengan skor tertinggi dipilih secara otomatis: \"{selected_phrase}\" (skor: {highest_score})")
        return selected_phrase
    
    elif choice == 0:
        # Pemilihan manual
        print("\n💡 Silakan pilih Keyphrase SEO utama Anda dari daftar berikut:")
        for i, (phrase, score) in enumerate(parsed_keyphrases):
            print(f"  [{i+1}] {phrase} (skor: {score})")

        while True:
            try:
                manual_choice = int(input(f"\nMasukkan pilihan Anda (1-{len(parsed_keyphrases)}): "))
                if 1 <= manual_choice <= len(parsed_keyphrases):
                    selected_phrase, score = parsed_keyphrases[manual_choice - 1]
                    print(f"\n✅ Anda memilih: \"{selected_phrase}\"")
                    return selected_phrase
                else:
                    print(f"❌ Pilihan tidak valid. Harap masukkan angka antara 1 dan {len(parsed_keyphrases)}.")
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Pemilihan dibatalkan.")
                return None
    
    else:
        # Pilih langsung berdasarkan nomor (1-5)
        if 1 <= choice <= len(parsed_keyphrases):
            selected_phrase, score = parsed_keyphrases[choice - 1]
            print(f"\n✅ Keyphrase #{choice} dipilih: \"{selected_phrase}\" (skor: {score})")
            return selected_phrase
        else:
            print(f"\n❌ Pilihan #{choice} tidak valid. Hanya ada {len(parsed_keyphrases)} keyphrase tersedia.")
            return None
