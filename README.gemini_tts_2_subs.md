# Gemini Audio to Subtitles Converter

The `gemini-tts-2-subs.py` script uses Google's Gemini 1.5 Flash model to transcribe MP3 audio files into subtitle formats (SRT, VTT) or plain text.

## Overview

This script leverages Google Gemini's multimodal capabilities to:
1. **Upload audio files** directly to Gemini API
2. **Transcribe speech** into text with high accuracy
3. **Generate subtitles** with proper timestamps (SRT/VTT)
4. **Support multiple languages** for transcription

## Features

- ✅ **Multiple Output Formats**: SRT, VTT, and plain TXT
- ✅ **Multi-language Support**: Transcribe in various languages
- ✅ **High Accuracy**: Uses Gemini 1.5 Flash for quality transcription
- ✅ **Timestamp Generation**: Automatic timing for subtitle formats
- ✅ **Flexible Output**: Save to custom directories
- ✅ **Simple CLI**: Easy-to-use command line interface

## Prerequisites

1. **Python 3.8+**
2. **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/)
3. **Required Python packages**:
   ```bash
   pip install google-generativeai python-dotenv
   ```

## Installation

The script is included with the main project. Ensure you have the required dependencies:

```bash
pip install google-generativeai python-dotenv
```

## Setup

Create or update your `.env` file with your Gemini API key:
```
GANAI_API_KEY=your_gemini_api_key_here
```

## Usage

### Basic Syntax

```bash
python gemini-tts-2-subs.py -a <audio_file> [options]
```

### Parameters

- **`-a, --audio`** (required): Path to the MP3 audio file to transcribe
- **`-l, --language`** (optional): Language for transcription (default: `english`)
- **`-f, --format`** (optional): Output format - choices: `srt`, `vtt`, `txt` (default: `srt`)
- **`-o, --output-dir`** (optional): Directory to save the result file (default: current directory)

### Examples

#### 1. Basic Transcription to SRT
```bash
# Transcribe MP3 to SRT format in English
python gemini-tts-2-subs.py -a "podcast_episode.mp3"
# Output: podcast_episode.srt
```

#### 2. Different Languages and Formats
```bash
# Transcribe to Indonesian VTT format
python gemini-tts-2-subs.py -a "tutorial.mp3" -l "indonesian" -f "vtt"

# Transcribe to plain text in Spanish
python gemini-tts-2-subs.py -a "interview.mp3" -l "spanish" -f "txt"
```

#### 3. Custom Output Directory
```bash
# Save results to specific directory
python gemini-tts-2-subs.py -a "video_audio.mp3" -o "subtitles/" -f "srt"
# Output: subtitles/video_audio.srt
```

#### 4. Multiple Files Processing
```bash
# Process multiple files (using shell loop)
for file in *.mp3; do
    python gemini-tts-2-subs.py -a "$file" -f "srt"
done
```

## Supported Formats

### SRT (SubRip Text)
- **Extension**: `.srt`
- **Features**: Numbered entries with timestamps
- **Use case**: Most widely supported subtitle format
- **Example output**:
  ```
  1
  00:00:01,000 --> 00:00:05,000
  Hello and welcome to this tutorial

  2
  00:00:05,500 --> 00:00:10,000
  Today we'll learn about WordPress SEO
  ```

### VTT (WebVTT)
- **Extension**: `.vtt`
- **Features**: Web-native subtitle format
- **Use case**: HTML5 video players, web streaming
- **Example output**:
  ```
  WEBVTT

  00:01.000 --> 00:05.000
  Hello and welcome to this tutorial

  00:05.500 --> 00:10.000
  Today we'll learn about WordPress SEO
  ```

### TXT (Plain Text)
- **Extension**: `.txt`
- **Features**: Clean text without timestamps
- **Use case**: Content analysis, blog writing, transcripts
- **Example output**:
  ```
  Hello and welcome to this tutorial. Today we'll learn about WordPress SEO optimization techniques and best practices.
  ```

## Supported Languages

The script supports multiple languages. Common examples:
- `english` (default)
- `indonesian`
- `spanish`
- `french`
- `german`
- `chinese`
- `japanese`
- `korean`
- `portuguese`
- `italian`

## Example Workflow

```bash
$ python gemini-tts-2-subs.py -a "tutorial_video.mp3" -l "english" -f "srt" -o "output/"

Processing 'tutorial_video.mp3' → language=english, format=srt ...
Done. Result saved to: output/tutorial_video.srt
```

## Integration with Blog Workflow

This script integrates well with the blog generation workflow:

### 1. Extract Audio from Video
```bash
# Extract audio from video file (requires ffmpeg)
ffmpeg -i "video.mp4" -vn -acodec mp3 "audio.mp3"
```

### 2. Transcribe to Text
```bash
# Generate subtitle file
python gemini-tts-2-subs.py -a "audio.mp3" -f "txt"
```

### 3. Generate Blog Post
```bash
# Use transcribed text for blog generation
python subs-blog-wordpress.py "audio.txt" --status draft
```

## Error Handling

### Common Issues

**"Environment variable GANAI_API_KEY belum diset"**
- Ensure your `.env` file contains the API key
- Check that the .env file is in the correct directory
- Verify API key is valid and active

**"Audio file not found"**
- Check the file path is correct
- Ensure the file exists and is accessible
- Verify the file is in MP3 format

**API Errors**
- Check your Gemini API quota and limits
- Ensure stable internet connection
- Verify API key permissions

## Technical Details

### Audio Requirements
- **Format**: MP3 (other formats may work but not guaranteed)
- **Size limit**: Based on Gemini API limits (typically ~20MB)
- **Duration**: Optimal for files under 30 minutes
- **Quality**: Clear audio produces better transcription

### Model Information
- **Model**: `gemini-1.5-flash-latest`
- **Capabilities**: Multimodal (text + audio)
- **Strengths**: Fast processing, good accuracy, cost-effective

### Output Quality
- **Accuracy**: High for clear audio and common languages
- **Timestamps**: Generated automatically for SRT/VTT
- **Formatting**: Clean, properly structured output

## Tips for Best Results

1. **Audio Quality**: Use clear, high-quality audio files
2. **Language Specification**: Be specific with language parameter
3. **File Organization**: Use descriptive filenames for easy identification
4. **Batch Processing**: Process multiple files using shell scripts
5. **Format Selection**: Choose format based on intended use:
   - SRT: For video players, YouTube
   - VTT: For web players
   - TXT: For content analysis, blog writing

## Troubleshooting

### Poor Transcription Quality
- Check audio quality and clarity
- Ensure correct language is specified
- Try adjusting audio volume/noise reduction
- Split long files into smaller segments

### API Issues
- Verify API key is correct and active
- Check API quota and billing status
- Ensure stable internet connection
- Try reducing file size if upload fails

### File Issues
- Confirm MP3 format compatibility
- Check file permissions and accessibility
- Verify output directory exists and is writable

## Cost Considerations

- Gemini 1.5 Flash is cost-effective for audio processing
- Pricing based on input tokens (audio data)
- Monitor usage through Google AI Studio console
- Consider batch processing for efficiency