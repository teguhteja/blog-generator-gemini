import re
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from pytube import YouTube
from pytube.exceptions import PytubeError

def get_video_id(url_or_id):
    """Mengekstrak ID video YouTube dari URL atau mengembalikan ID jika sudah berupa ID."""
    # Regex untuk menemukan ID video dari berbagai format URL YouTube
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url_or_id)
    if match:
        return match.group(1)
    # Jika tidak cocok, asumsikan itu sudah merupakan ID video yang valid
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    return None

def sanitize_filename(title):
    """Menghapus karakter yang tidak valid dari string untuk menjadikannya nama file yang valid."""
    return re.sub(r'[\\/*?:"<>|]', "", title)

def get_youtube_transcript(video_url_or_id, output_dir="."):
    """
    Mengunduh transkrip untuk video YouTube, menyimpannya ke file,
    dan mengembalikan path ke file tersebut. Dibuat lebih tangguh untuk
    menangani error dari pytube.
    """
    video_id = get_video_id(video_url_or_id)
    if not video_id:
        print(f"Error: URL atau ID Video YouTube tidak valid: {video_url_or_id}")
        return None

    # Langkah 1: Dapatkan transkrip (bagian paling penting)
    try:
        print(f"Mencoba mengambil transkrip untuk video ID: {video_id}...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['id', 'en'])  # Coba ID atau EN
        transcript_data = transcript.fetch()
        transcript_text = " ".join([item['text'] for item in transcript_data])
        print("Transkrip berhasil didapatkan.")
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"Error: Tidak dapat menemukan transkrip untuk video ID {video_id}.")
        print("Penyebab: Video mungkin tidak memiliki subtitle (CC) atau subtitle dinonaktifkan.")
        return None
    except Exception as e:
        print(f"Error: Terjadi kesalahan tak terduga saat mengambil transkrip untuk ID {video_id}: {e}")
        return None

    # Langkah 2: Dapatkan judul video (jika gagal, tetap lanjut)
    video_title = video_id  # Judul fallback jika pengambilan gagal
    try:
        print("Mencoba mengambil judul video...")
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}", use_oauth=False, allow_oauth_cache=False)
        video_title = sanitize_filename(yt.title)
        print(f"Judul video didapatkan: {video_title}")
    except PytubeError as e:
        print(f"\nPeringatan: Gagal mendapatkan judul video dari YouTube untuk ID {video_id}.")
        print("-> Transkrip akan tetap diunduh, namun nama file akan menggunakan ID video.")
        print(f"-> Detail error: {e}")
        print("-> SARAN: Error ini seringkali disebabkan oleh library 'pytube' yang usang. Coba perbarui dengan perintah:")
        print("   pip install --upgrade pytube\n")

    # Langkah 3: Simpan file
    try:
        filename = f"{video_title} [{video_id}].txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print(f"\nSukses! Transkrip berhasil disimpan ke: {filepath}")
        return filepath
    except IOError as e:
        print(f"Error: Gagal menyimpan file ke '{filepath}': {e}")
        return None