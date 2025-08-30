#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

def configure_api():
    """
    Load GANAI_API_KEY from .env or environment and configure the client.
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("GANAI_API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable GANAI_API_KEY belum diset")
    genai.configure(api_key=api_key)

def build_prompt(language: str, fmt: str) -> str:
    """
    Create a prompt for Gemini based on desired language and output format.
    """
    lang_desc = language.capitalize()
    if fmt == "srt":
        return (
            f"Transcribe the following audio into {lang_desc} and output "
            "as a subtitle file in SRT format (include timestamps)."
        )
    elif fmt == "vtt":
        return (
            f"Transcribe the following audio into {lang_desc} and output "
            "as a WebVTT file (include timestamps)."
        )
    else:  # txt
        return (
            f"Transcribe the following audio into {lang_desc} and output "
            "as plain text (no timestamps)."
        )

def process_audio(audio_path: str, language: str, fmt: str) -> str:
    """
    Send one prompt + audio to Gemini and return the generated text.
    """
    with open(audio_path, "rb") as fa:
        audio_bytes = fa.read()

    contents = [
        {"text": build_prompt(language, fmt)},
        {
            "inline_data": {
                "mime_type": "audio/mp3",
                "data": audio_bytes
            }
        }
    ]

    response = genai.GenerativeModel("gemini-1.5-flash-latest") \
                  .generate_content(contents)
    return response.text

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe MP3 to SRT/VTT/TXT using Gemini 1.5 Flash"
    )
    parser.add_argument(
        "-a", "--audio",
        required=True,
        help="Path to the MP3 audio file"
    )
    parser.add_argument(
        "-l", "--language",
        default="english",
        help="Language for transcription (default: english)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["srt", "vtt", "txt"],
        default="srt",
        help="Output format: srt, vtt, or txt (default: srt)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="Optional directory to save the result file"
    )

    args = parser.parse_args()

    if not os.path.isfile(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    configure_api()

    print(f"Processing '{args.audio}' → language={args.language}, format={args.format} ...")
    result = process_audio(args.audio, args.language, args.format)

    base_name = os.path.splitext(os.path.basename(args.audio))[0]
    out_filename = f"{base_name}.{args.format}"
    out_path = (args.output_dir or ".") + os.sep + out_filename

    with open(out_path, "w", encoding="utf-8") as of:
        of.write(result)

    print(f"Done. Result saved to: {out_path}")

if __name__ == "__main__":
    main()