#!/usr/bin/env python3
"""
VTT Combiner Script
Combine all VTT files in a folder into a single text file
- Reads all .vtt files in specified folder
- Removes timestamps and formatting
- Combines all text content into single .txt file
- Output filename matches folder name
"""

import os
import sys
import glob
import re
import argparse
from pathlib import Path


def clean_vtt_line(line):
    """
    Clean VTT line by removing timestamps and formatting
    """
    line = line.strip()
    
    # Skip empty lines
    if not line:
        return ""
    
    # Skip WEBVTT header
    if line.startswith("WEBVTT"):
        return ""
    
    # Skip timestamp lines (format: 00:00:00.000 --> 00:00:00.000)
    timestamp_pattern = r'^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}'
    if re.match(timestamp_pattern, line):
        return ""
    
    # Skip cue settings (lines with position, align, etc.)
    cue_settings_pattern = r'^.*?(position:|align:|vertical:|size:|line:)'
    if re.match(cue_settings_pattern, line):
        return ""
    
    # Skip NOTE lines
    if line.startswith("NOTE"):
        return ""
    
    # Remove HTML tags if any
    line = re.sub(r'<[^>]+>', '', line)
    
    # Remove VTT styling (like <c.colorname>text</c>)
    line = re.sub(r'<c\.[^>]*>', '', line)
    line = re.sub(r'</c>', '', line)
    
    # Clean up common VTT artifacts
    line = re.sub(r'&nbsp;', ' ', line)
    line = re.sub(r'&amp;', '&', line)
    line = re.sub(r'&lt;', '<', line)
    line = re.sub(r'&gt;', '>', line)
    
    return line.strip()


def process_vtt_file(vtt_file_path):
    """
    Process single VTT file and extract text content
    Returns list of text lines
    """
    text_lines = []
    
    try:
        with open(vtt_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = clean_vtt_line(line)
                if cleaned_line:  # Only add non-empty lines
                    text_lines.append(cleaned_line)
        
        print(f"✅ Processed: {os.path.basename(vtt_file_path)} ({len(text_lines)} text lines)")
        return text_lines
        
    except Exception as e:
        print(f"❌ Error processing {vtt_file_path}: {e}")
        return []


def combine_vtt_files_in_folder(folder_path):
    """
    Combine all VTT files in folder into single text content
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"❌ Folder tidak ditemukan: {folder_path}")
        return None, []
    
    if not folder_path.is_dir():
        print(f"❌ Path bukan folder: {folder_path}")
        return None, []
    
    # Find all VTT files in folder
    vtt_files = list(folder_path.glob('*.vtt'))
    
    if not vtt_files:
        print(f"❌ Tidak ada file .vtt ditemukan dalam folder: {folder_path}")
        return None, []
    
    print(f"📁 Folder: {folder_path}")
    print(f"🔍 Ditemukan {len(vtt_files)} file VTT:")
    for vtt_file in sorted(vtt_files):
        print(f"   - {vtt_file.name}")
    
    # Process all VTT files
    all_text_lines = []
    processed_count = 0
    
    for vtt_file in sorted(vtt_files):  # Sort for consistent order
        text_lines = process_vtt_file(vtt_file)
        if text_lines:
            all_text_lines.extend(text_lines)
            processed_count += 1
        
        # Add separator between files (optional)
        if text_lines and vtt_file != sorted(vtt_files)[-1]:  # Not last file
            all_text_lines.append("")  # Empty line as separator
    
    print(f"\n📊 Summary:")
    print(f"   • Total VTT files: {len(vtt_files)}")
    print(f"   • Successfully processed: {processed_count}")
    print(f"   • Total text lines: {len(all_text_lines)}")
    
    return folder_path.name, all_text_lines


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Combine VTT files in folder into single text file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine-vtt-in-folder.py /path/to/folder
  python combine-vtt-in-folder.py ./video_subtitles/
  python combine-vtt-in-folder.py "My Video Folder" --output custom_name.txt

The script will:
1. Find all .vtt files in the specified folder
2. Remove timestamps and VTT formatting
3. Combine all text content
4. Save as folder_name.txt (or custom output name)
        """
    )
    
    parser.add_argument(
        'folder_path',
        type=str,
        help='Path to folder containing VTT files'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Custom output filename (default: folder_name.txt)'
    )
    
    parser.add_argument(
        '--no-separators',
        action='store_true',
        help='Do not add empty lines between VTT files'
    )
    
    args = parser.parse_args()
    
    print("🚀 VTT Combiner - Menggabungkan file VTT dalam folder")
    print("=" * 60)
    
    # Process folder
    folder_name, text_lines = combine_vtt_files_in_folder(args.folder_path)
    
    if not text_lines:
        print("❌ Tidak ada text yang berhasil diekstrak")
        sys.exit(1)
    
    # Determine output filename
    if args.output:
        output_filename = args.output
        if not output_filename.endswith('.txt'):
            output_filename += '.txt'
    else:
        output_filename = f"{folder_name}.txt"
    
    # Remove separators if requested
    if args.no_separators:
        text_lines = [line for line in text_lines if line.strip()]
    
    # Write combined text to file
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for line in text_lines:
                f.write(line + '\n')
        
        print(f"\n✅ File berhasil dibuat: {output_filename}")
        print(f"📄 Total baris: {len(text_lines)}")
        
        # Show file size
        file_size = os.path.getsize(output_filename)
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size/1024:.1f} KB"
        else:
            size_str = f"{file_size/(1024*1024):.1f} MB"
        
        print(f"📏 Ukuran file: {size_str}")
        
        # Show preview
        print(f"\n📖 Preview (5 baris pertama):")
        for i, line in enumerate(text_lines[:5]):
            if line.strip():  # Only show non-empty lines
                print(f"   {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
    
    except Exception as e:
        print(f"❌ Error menulis file output: {e}")
        sys.exit(1)
    
    print("\n🎉 Proses selesai!")


if __name__ == "__main__":
    main()