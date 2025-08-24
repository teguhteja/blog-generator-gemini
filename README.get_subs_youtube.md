# YouTube Subtitle Downloader

A command-line Python script to download subtitles from YouTube videos in various formats (SRT, VTT, TXT). It can extract the video ID from a URL, a video code, or even a filename.

## Features

- **Flexible Input**: Accepts a full YouTube URL, an 11-character video ID, or a local filename containing the ID (e.g., `My Video [videoID].mp4`).
- **Multiple Formats**: Download subtitles as `.srt`, `.vtt`, or plain `.txt` files. You can download multiple formats at once.
- **Language Selection**: Specify the desired language for the subtitles (e.g., `en`, `id`, `es`).
- **Smart Language Fallback**: If the requested language is not available, it automatically tries to fetch English subtitles. If English is also unavailable, it grabs the first available transcript.
- **Clean Filenames**: Automatically fetches the video title and sanitizes it to create a valid and clean filename.
- **Easy to Use**: Simple and clear command-line arguments.

## Prerequisites

- Python 3.6+
- Required Python packages: `youtube-transcript-api`, `requests`

## Installation

1.  **Clone the repository or download the script `get_subs_youtube.py`**.

2.  **Install the necessary dependencies**:
    ```bash
    pip install youtube-transcript-api requests
    ```
    Or if you have a `requirements.txt` file that includes these:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script can be run from your terminal.

### Basic Syntax

```bash
python get_subs_youtube.py [INPUT] [OPTIONS]
```

### Arguments

- `input`: (Optional) The YouTube URL or the 11-character video ID.
- `-f, --filename`: (Optional) Extract the video ID from a filename with the format `"name [video_id].ext"`.
- `-sl, --sub-language`: (Optional) The language code for the subtitles. Defaults to `en`.
- `-sf, --subtitle-format`: (Optional) One or more output formats. Choices are `srt`, `vtt`, `txt`. Defaults to `txt`.

> **Note**: You must provide either an `input` (URL/ID) or a `--filename`.

### Examples

1.  **Download subtitles from a URL (default format: .txt)**:
    ```bash
    python get_subs_youtube.py https://www.youtube.com/watch?v=jExJ_XjrlNM
    ```

2.  **Download SRT subtitles using a video ID**:
    ```bash
    python get_subs_youtube.py jExJ_XjrlNM -sf srt
    ```

3.  **Download all supported formats for an Indonesian video**:
    ```bash
    python get_subs_youtube.py https://youtu.be/jExJ_XjrlNM -sl id -sf srt vtt txt
    ```

4.  **Extract video ID from a local filename and get VTT subtitles**:
    ```bash
    python get_subs_youtube.py -f "VPS Gratis Seumur Hidup [jExJ_XjrlNM].mp4" -sf vtt
    ```
