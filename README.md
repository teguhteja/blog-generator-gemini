# Generator Artikel Blog Otomatis dengan Gemini AI

Skrip Python untuk mengotomatisasi pembuatan artikel blog, analisis SEO, dan gambar pendukung dari file teks mentah (seperti transkrip video) menggunakan Google Gemini API.

Proyek ini dirancang untuk menjadi modular dan mudah dikonfigurasi, memungkinkan Anda untuk menghasilkan konten berkualitas tinggi dengan alur kerja yang efisien.

## Fitur Utama

-   **Modular & Terstruktur**: Kode dipecah menjadi modul-modul logis di dalam direktori `lib` untuk kemudahan pemeliharaan dan pengembangan.
-   **Alur Kerja Bertahap**: Proses dibagi menjadi 5 langkah yang dapat dijalankan secara terpisah:
    1.  **Pembuatan Draf**: Membuat draf artikel awal dari teks input.
    2.  **Analisis SEO**: Menghasilkan daftar *keyphrase* SEO yang relevan.
    3.  **Pembuatan Blog Final**: Menulis ulang draf menjadi artikel blog yang lengkap dan dioptimalkan untuk SEO berdasarkan *keyphrase* yang dipilih.
    4.  **Pembaruan Metadata SEO**: Menambahkan metadata SEO tambahan (seperti meta deskripsi, tag) ke file analisis.
    5.  **Pembuatan Gambar**: Menghasilkan gambar *featured* yang relevan untuk artikel.
-   **Kustomisasi Prompt**: Mudah mengubah gaya dan instruksi konten dengan mengedit file markdown di direktori `prompt/`.
-   **Konfigurasi Model Fleksibel**: Pilih model Gemini yang berbeda untuk tugas yang berbeda (misalnya, model 'flash' yang lebih murah untuk draf, model 'pro' yang lebih kuat untuk konten final) melalui file `model/model.json`.
-   **Optimalisasi Gambar**: Secara otomatis mengubah ukuran dan mengoptimalkan gambar yang dihasilkan untuk web (memerlukan ImageMagick).
-   **Pelacakan Biaya**: Mencatat estimasi biaya setiap panggilan API ke `usage_log.csv` untuk pemantauan anggaran.

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

1.  **Python 3.8+**
2.  **Google Gemini API Key**: Dapatkan dari Google AI Studio.
3.  **ImageMagick** (Opsional, tetapi sangat disarankan): Diperlukan untuk fungsionalitas optimalisasi gambar. Unduh dari situs resminya.

## Instalasi & Konfigurasi

1.  **Clone Repositori**

    ```bash
    git clone https://github.com/username/repo-name.git
    cd repo-name
    ```

2.  **Buat dan Aktifkan Virtual Environment** (Sangat Disarankan)

    ```bash
    # Buat environment
    python -m venv venv

    # Aktifkan di Windows
    .\venv\Scripts\activate

    # Aktifkan di macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependensi**

    Install semua pustaka Python yang diperlukan menggunakan file `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Siapkan API Key**

    Buat file baru bernama `.env` di direktori utama proyek dan tambahkan API Key Anda.

    **File: `.env`**
    ```
    GANAI_API_KEY="AIzaSy...API_KEY_ANDA_DISINI"
    ```

## Cara Menjalankan

Skrip dijalankan dari terminal menggunakan `main.py`. Semua file output akan dibuat dalam direktori baru yang namanya diambil dari nama file input.

### Sintaks Dasar

```bash
python main.py -i "path/ke/file_input.txt" [opsi]
```

### Argumen

-   `-i, --input`: **(Wajib)** Path ke file input `.txt`.
-   `-p, --prompt`: (Opsional) Nama file prompt dari direktori `prompt/`.
-   `-m, --model-config`: (Opsional) Nama file konfigurasi model dari direktori `model/`.
-   `--step`: (Opsional) Langkah spesifik yang ingin dijalankan (misal: `1 2 5`). Jika tidak ditentukan, semua langkah (1-5) akan dijalankan.

### Contoh Penggunaan

1.  **Menjalankan semua langkah (default):**

    ```bash
    python main.py -i "transkrip saya [video_id].txt"
    ```

2.  **Hanya membuat draf (langkah 1) dan analisis SEO (langkah 2):**

    ```bash
    python main.py -i "transkrip saya.txt" --step 1 2
    ```

3.  **Hanya membuat gambar (langkah 5):**
    *(Jika langkah 2 belum dijalankan, skrip akan meminta Anda memasukkan keyphrase secara manual)*

    ```bash
    python main.py -i "transkrip saya.txt" --step 5
    ```

## Struktur Output

Untuk setiap file input, misalnya `artikel-keren.txt`, skrip akan membuat struktur berikut:

```
artikel-keren/
├── artikel-keren.md         # Draf awal
├── artikel-keren.seo.md     # Analisis & metadata SEO
├── artikel-keren.blog.md    # Artikel blog final
└── keyphrase utama.jpg      # Gambar yang dihasilkan
```
