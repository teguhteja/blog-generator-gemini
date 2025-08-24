#!/usr/bin/env python3
"""
YouTube Subtitle Downloader
Download subtitles from YouTube videos in various formats (srt, vtt, txt)
"""

import argparse
import os
import sys
import re
import requests
from urllib.parse import urlparse, parse_qs
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api is required. Install with: pip install youtube-transcript-api")
    sys.exit(1)

def extract_video_id(url_or_code):
    """Extract YouTube video ID from URL or return if it's already a code"""
    if len(url_or_code) == 11 and re.match(r'^[0-9A-Za-z_-]{11}$', url_or_code):
        return url_or_code
    
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_code)
        if match:
            return match.group(1)
    
    return None

def extract_video_id_from_filename(filename):
    """Extract YouTube video ID from filename format: 'name [code].mp4'"""
    pattern = r'\[([0-9A-Za-z_-]{11})\]'
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    return None

def get_video_title(video_id):
    """Get YouTube video title from video ID"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url)
        response.raise_for_status()
        
        # Extract title from HTML
        title_match = re.search(r'<title>(.+?) - YouTube</title>', response.text)
        if title_match:
            title = title_match.group(1)
            # Clean title for filename
            return clean_filename(title)
        else:
            return video_id
    except:
        return video_id

def clean_filename(filename):
    """Clean filename by removing/replacing invalid characters"""
    # Replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'[\s]+', ' ', filename)  # Multiple spaces to single space
    filename = filename.strip()
    
    # Limit length to avoid filesystem issues
    if len(filename) > 100:
        filename = filename[:100].rsplit(' ', 1)[0]  # Cut at word boundary
    
    return filename if filename else "unknown_title"

def format_subtitle_content(transcript_data, format_type):
    """Format transcript content based on the specified format"""
    if format_type == 'srt':
        content = ""
        for i, entry in enumerate(transcript_data, 1):
            start_time = format_time_srt(entry['start'])
            end_time = format_time_srt(entry['start'] + entry['duration'])
            content += f"{i}\n{start_time} --> {end_time}\n{entry['text']}\n\n"
        return content
    elif format_type == 'vtt':
        content = "WEBVTT\n\n"
        for entry in transcript_data:
            start_time = format_time_vtt(entry['start'])
            end_time = format_time_vtt(entry['start'] + entry['duration'])
            content += f"{start_time} --> {end_time}\n{entry['text']}\n\n"
        return content
    elif format_type == 'txt':
        return '\n'.join([entry['text'] for entry in transcript_data])
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def format_time_srt(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def format_time_vtt(seconds):
    """Convert seconds to VTT time format (HH:MM:SS.mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"

def download_subtitles(video_id, subtitle_formats=['txt'], language='en'):
    """Download subtitles for a YouTube video in one or more formats"""
    try:
        transcript_data_raw = None
        
        # Method 1: Use the correct modern API as per documentation
        ytt_api = YouTubeTranscriptApi()
        
        # Try to get the requested language first
        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=[language])
            transcript_data_raw = fetched_transcript.to_raw_data()
        except:
            # Try English as fallback
            try:
                fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
                transcript_data_raw = fetched_transcript.to_raw_data()
                print(f"Warning: {language} subtitles not found, using English instead")
                language = 'en'
            except Exception as inner_e:
                # Method 2: Try with transcript list approach
                try:
                    transcript_list = ytt_api.list(video_id)
                    # Use any available transcript
                    available_transcripts = list(transcript_list)
                    if available_transcripts:
                        transcript = available_transcripts[0]
                        fetched_transcript = transcript.fetch()
                        transcript_data_raw = fetched_transcript.to_raw_data()
                        language = transcript.language_code
                        print(f"Warning: Using available language: {language}")
                    else:
                        raise Exception(f"No transcripts available for this video: {str(inner_e)}")
                except Exception as final_e:
                    raise Exception(f"No transcripts available for this video: {str(final_e)}")
        
        if not transcript_data_raw:
            raise Exception("Failed to fetch transcript data")
        title = get_video_title(video_id)
        downloaded_files = []

        for subtitle_format in set(subtitle_formats):
            formatted_content = format_subtitle_content(transcript_data_raw, subtitle_format)
            filename = f"{title} [{video_id}].{language}.{subtitle_format}"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            print(f"Subtitles downloaded successfully: {filename}")
            downloaded_files.append(filename)
            
        return downloaded_files
        
    except Exception as e:
        print(f"Error downloading subtitles: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube subtitles in various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python get_subs_youtube.py https://youtu.be/dQw4w9WgXcQ
  python get_subs_youtube.py dQw4w9WgXcQ -sf srt
  python get_subs_youtube.py dQw4w9WgXcQ -sf srt vtt txt
  python get_subs_youtube.py https://youtube.com/watch?v=dQw4w9WgXcQ -sl id -sf vtt
  python get_subs_youtube.py -f "Never Gonna Give You Up [dQw4w9WgXcQ].mp4"
  python get_subs_youtube.py -f "Tutorial Video [abc123defgh].mp4" -sf srt

Supported formats: srt, vtt, txt
Common language codes: en, id, es, fr, de, ja, ko, zh
        """)
    parser.add_argument('input', nargs='?', help='YouTube URL or 11-character video code')
    parser.add_argument('-f', '--filename', help='Extract video ID from filename format: "name [code].mp4"')
    parser.add_argument('-sl', '--sub-language', default='en', 
                       help='Subtitle language code (default: en)')
    parser.add_argument('-sf', '--subtitle-format', choices=['srt', 'vtt', 'txt'], 
                       nargs='+', default=['txt'], help='One or more subtitle formats (e.g., srt vtt txt). Default: txt')
    
    args = parser.parse_args()
    
    # Determine video ID source
    video_id = None
    if args.filename:
        video_id = extract_video_id_from_filename(args.filename)
        if not video_id:
            print("Error: Could not extract video ID from filename. Expected format: 'name [code].mp4'")
            sys.exit(1)
    elif args.input:
        video_id = extract_video_id(args.input)
        if not video_id:
            print("Error: Invalid YouTube URL or video ID")
            sys.exit(1)
    else:
        print("Error: Must provide either input URL/ID or filename (-f)")
        sys.exit(1)
    
    print(f"Downloading subtitles for video ID: {video_id}")
    print(f"Formats: {', '.join(args.subtitle_format)}")
    print(f"Language: {args.sub_language}")
    
    results = download_subtitles(video_id, args.subtitle_format, args.sub_language)
    
    if results:
        print(f"\nDownload completed for:")
        for result in results:
            print(f"- {result}")
    else:
        print("\nDownload failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
