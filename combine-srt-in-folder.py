#!/usr/bin/env python3
"""
SRT Combiner Script
Combine all SRT files in a folder into a single text file
- Reads all .srt files in specified folder
- Removes timestamps and sequence numbers
- Combines all text content into single .txt file
- Output filename matches folder name
"""

import os
import sys
import glob
import re
import argparse
from pathlib import Path


def clean_srt_line(line):
    """
    Clean SRT line by removing timestamps and formatting
    """
    line = line.strip()
    
    # Skip empty lines
    if not line:
        return ""
    
    # Skip sequence numbers (lines with only digits)
    if line.isdigit():
        return ""
    
    # Skip timestamp lines (format: 00:00:00,000 --> 00:00:00,000)
    timestamp_pattern = r'^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}'
    if re.match(timestamp_pattern, line):
        return ""
    
    # Remove HTML tags if any
    line = re.sub(r'<[^>]+>', '', line)
    
    # Remove SRT formatting tags
    line = re.sub(r'<b>', '', line)
    line = re.sub(r'</b>', '', line)
    line = re.sub(r'<i>', '', line)
    line = re.sub(r'</i>', '', line)
    line = re.sub(r'<u>', '', line)
    line = re.sub(r'</u>', '', line)
    line = re.sub(r'<font[^>]*>', '', line)
    line = re.sub(r'</font>', '', line)
    
    # Clean up common HTML entities
    line = re.sub(r'&nbsp;', ' ', line)
    line = re.sub(r'&amp;', '&', line)
    line = re.sub(r'&lt;', '<', line)
    line = re.sub(r'&gt;', '>', line)
    line = re.sub(r'&quot;', '"', line)
    line = re.sub(r'&#39;', "'", line)
    
    # Remove speaker indicators (like "Speaker 1:" or "[Speaker]:")
    line = re.sub(r'^\[?[A-Za-z\s]+\d*\]?\s*:\s*', '', line)
    
    # Remove action descriptions in brackets [like this]
    line = re.sub(r'\[.*?\]', '', line)
    
    # Remove music/sound descriptions in parentheses (like this)
    line = re.sub(r'\([^)]*music[^)]*\)', '', line, flags=re.IGNORECASE)
    line = re.sub(r'\([^)]*sound[^)]*\)', '', line, flags=re.IGNORECASE)
    
    # Clean up multiple spaces
    line = re.sub(r'\s+', ' ', line)
    
    return line.strip()


def process_srt_file(srt_file_path):
    """
    Process single SRT file and extract text content
    Returns list of text lines
    """
    text_lines = []
    
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                cleaned_line = clean_srt_line(line)
                if cleaned_line:  # Only add non-empty lines
                    text_lines.append(cleaned_line)
        
        print(f"✅ Processed: {os.path.basename(srt_file_path)} ({len(text_lines)} text lines)")
        return text_lines
        
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(srt_file_path, 'r', encoding='latin1') as f:
                for line in f:
                    cleaned_line = clean_srt_line(line)
                    if cleaned_line:
                        text_lines.append(cleaned_line)
            
            print(f"✅ Processed: {os.path.basename(srt_file_path)} ({len(text_lines)} text lines) [latin1 encoding]")
            return text_lines
            
        except Exception as e:
            print(f"❌ Error processing {srt_file_path}: {e}")
            return []
    
    except Exception as e:
        print(f"❌ Error processing {srt_file_path}: {e}")
        return []


def combine_srt_files_in_folder(folder_path):
    """
    Combine all SRT files in folder into single text content
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"❌ Folder tidak ditemukan: {folder_path}")
        return None, []
    
    if not folder_path.is_dir():
        print(f"❌ Path bukan folder: {folder_path}")
        return None, []
    
    # Find all SRT files in folder
    srt_files = list(folder_path.glob('*.srt'))
    
    if not srt_files:
        print(f"❌ Tidak ada file .srt ditemukan dalam folder: {folder_path}")
        return None, []
    
    print(f"📁 Folder: {folder_path}")
    print(f"🔍 Ditemukan {len(srt_files)} file SRT:")
    for srt_file in sorted(srt_files):
        print(f"   - {srt_file.name}")
    
    # Process all SRT files
    all_text_lines = []
    processed_count = 0
    
    for srt_file in sorted(srt_files):  # Sort for consistent order
        text_lines = process_srt_file(srt_file)
        if text_lines:
            all_text_lines.extend(text_lines)
            processed_count += 1
        
        # Add separator between files (optional)
        if text_lines and srt_file != sorted(srt_files)[-1]:  # Not last file
            all_text_lines.append("")  # Empty line as separator
    
    print(f"\n📊 Summary:")
    print(f"   • Total SRT files: {len(srt_files)}")
    print(f"   • Successfully processed: {processed_count}")
    print(f"   • Total text lines: {len(all_text_lines)}")
    
    return folder_path.name, all_text_lines


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Combine SRT files in folder into single text file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine-srt-in-folder.py /path/to/folder
  python combine-srt-in-folder.py ./video_subtitles/
  python combine-srt-in-folder.py "My Video Folder" --output custom_name.txt

The script will:
1. Find all .srt files in the specified folder
2. Remove sequence numbers, timestamps and SRT formatting
3. Combine all text content
4. Save as folder_name.txt (or custom output name)
        """
    )
    
    parser.add_argument(
        'folder_path',
        type=str,
        help='Path to folder containing SRT files'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Custom output filename (default: folder_name.txt)'
    )
    
    parser.add_argument(
        '--no-separators',
        action='store_true',
        help='Do not add empty lines between SRT files'
    )
    
    args = parser.parse_args()
    
    print("🚀 SRT Combiner - Menggabungkan file SRT dalam folder")
    print("=" * 60)
    
    # Process folder
    folder_name, text_lines = combine_srt_files_in_folder(args.folder_path)
    
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