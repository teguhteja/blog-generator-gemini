import os
import requests
import json
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

# Ganti dengan URL API Gemini yang sesuai
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
GANAI_API_KEY = os.getenv("GANAI_API_KEY")

if not GANAI_API_KEY:
    raise ValueError("GANAI_API_KEY not found in .env file.")

def get_directory_size(start_path='.'):
    """
    Menghitung total ukuran direktori dalam byte, mengabaikan folder .git.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        # Mencegah os.walk masuk ke dalam direktori .git
        if '.git' in dirnames:
            dirnames.remove('.git')
            
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def get_git_diff():
    """Mendapatkan perbedaan (diff) dari perubahan yang sudah di-staged."""
    try:
        diff_output = os.popen("git diff --cached").read()
        if not diff_output:
            print("Tidak ada perubahan yang di-staged. Silakan `git add` file yang ingin Anda commit.")
            return None
        return diff_output
    except Exception as e:
        print(f"Error saat mendapatkan diff Git: {e}")
        return None

def generate_commit_message(diff_content):
    """Mengirimkan diff ke Gemini API untuk membuat pesan commit."""
    headers = {
        "Content-Type": "application/json"
    }
    
    # Prompt untuk Gemini
    prompt = f"""
    Anda adalah seorang asisten yang membantu membuat pesan commit Git. Berdasarkan perubahan kode berikut, buatlah satu baris pesan commit yang ringkas namun deskriptif. Fokus pada tujuan utama dari perubahan ini.

    Diff:
    {diff_content}

    Pesan commit:
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    try:
        response = requests.post(f"{GEMINI_API_URL}?key={GANAI_API_KEY}", headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Akan memunculkan error jika respons tidak 200 OK
        
        response_data = response.json()
        commit_message = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Hapus prefix atau konten tidak relevan lainnya dari respons Gemini
        if commit_message.startswith("Pesan commit:"):
            commit_message = commit_message.replace("Pesan commit:", "").strip()
            
        return commit_message
        
    except requests.exceptions.RequestException as e:
        print(f"Error saat menghubungi Gemini API: {e}")
        return None
    except KeyError:
        print("Struktur respons Gemini tidak seperti yang diharapkan.")
        print(response.text)
        return None

def main():
    # --- PENGECEKAN UKURAN FOLDER ---
    max_size_kb = 100
    total_size_bytes = get_directory_size()
    total_size_kb = total_size_bytes / 1024

    print(f"ℹ️  Ukuran total folder proyek (tanpa .git): {total_size_kb:.2f} KB.")

    if total_size_kb >= max_size_kb:
        print(f"Ukuran folder melebihi {max_size_kb} KB. Script ini dihentikan.")
        print("   (Ini dirancang untuk proyek dengan aset besar seperti video/subs yang dipindahkan).")
        return
    
    print("-" * 30)
    # --- AKHIR PENGECEKAN ---

    diff = get_git_diff()
    if not diff:
        return

    print("Menganalisis perubahan dan membuat pesan commit...")
    commit_message = generate_commit_message(diff)

    if commit_message:
        print(f"\nPesan commit yang disarankan:\n'{commit_message}'")
        
        # Konfirmasi sebelum commit
        confirm = input("Apakah Anda ingin menggunakan pesan ini? (y/n): ")
        if confirm.lower() == 'y':
            try:
                os.system(f"git commit -m '{commit_message}'")
                print("\nCommit berhasil dibuat!")
            except Exception as e:
                print(f"Error saat membuat commit: {e}")
        else:
            print("Operasi dibatalkan.")
    else:
        print("Gagal membuat pesan commit otomatis.")

if __name__ == "__main__":
    main()