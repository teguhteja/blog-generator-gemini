# YouTube to WordPress Blog Automation

The `subs-blog-wordpress.py` script provides a complete automation solution for converting YouTube videos into published WordPress blog posts with a single command.

## Overview

This all-in-one script streamlines the entire workflow:
1. **Download YouTube subtitles** (if needed)
2. **Generate SEO-optimized blog content** with images
3. **Upload to WordPress** with Rank Math SEO integration

## Features

- ✅ **Smart File Detection**: Automatically finds existing subtitle files or downloads new ones
- ✅ **Direct .txt File Support**: Skip download step when input is already a .txt file
- ✅ **Intelligent Identifier Extraction**: Uses YouTube video codes `[abc123]` or keywords from filename
- ✅ **Flexible Input Handling**: Works with various file naming conventions
- ✅ **WordPress Integration**: Uploads with featured images and SEO metadata
- ✅ **Error Recovery**: Robust error handling with clear status messages
- ✅ **Status Control**: Publish as draft, published, or private posts

## Installation

The script is included with the main project. No additional installation required.

## Prerequisites

1. **Environment Setup**: All prerequisites from main README.md
2. **WordPress Credentials**: Configure `.env` file with WordPress credentials:
   ```
   WP_URL=https://yoursite.com
   WP_USERNAME=your_username
   WP_PASSWORD=your_app_password
   GANAI_API_KEY=your_gemini_api_key
   ```

## Usage

### Basic Syntax

```bash
python subs-blog-wordpress.py <input_name> [--status STATUS]
```

### Parameters

- **`input_name`** (required): Input identifier - can be:
  - YouTube video filename: `"Tutorial Video [dQw4w9WgXcQ]"`
  - Simple name: `"odoo tutorial basic"`
  - Just the video code: `"dQw4w9WgXcQ"`
  - Direct .txt file: `"subtitle_file.txt"` (skips download step)

- **`--status`** (optional): WordPress post status
  - `draft` (default) - Save as draft
  - `publish` - Publish immediately  
  - `private` - Save as private post

### Examples

#### 1. Process YouTube Video (with code)
```bash
# Draft post (default)
python subs-blog-wordpress.py "Complete RankMath SEO Tutorial [iNyPGLYBc_E]"

# Published post
python subs-blog-wordpress.py "Complete RankMath SEO Tutorial [iNyPGLYBc_E]" --status publish
```

#### 2. Process with Keywords Only
```bash
# Uses first 3 words as identifier: "odoo-tutorial-basic"
python subs-blog-wordpress.py "Odoo Tutorial Basic Configuration" --status draft
```

#### 3. Process Just Video Code
```bash
python subs-blog-wordpress.py "iNyPGLYBc_E" --status publish
```

#### 4. Process Existing .txt File (Skip Download)
```bash
# Direct processing of existing subtitle file
python subs-blog-wordpress.py "Tutorial SEO Complete [xyz789].txt" --status publish

# Or any .txt file
python subs-blog-wordpress.py "my_content.txt" --status draft
```

## How It Works

### Step 1: Input Type Detection
The script first determines the type of input:

**Direct .txt File:**
- Input: `"Tutorial [abc123].txt"`
- Action: Skip download, use file directly
- Identifier extracted from filename

**Non-.txt Input:**
- Input: `"Tutorial Video [abc123defgh]"`
- Action: Search for existing files or download

### Step 2: Identifier Extraction
For non-.txt inputs, extracts identifier:

**Pattern `[code]` Found:**
- Input: `"Tutorial Video [abc123defgh]"`
- Identifier: `abc123defgh`

**No Pattern Found:**
- Input: `"WordPress SEO Complete Guide"`
- Identifier: `wordpress-seo-complete`

### Step 3: File Discovery (Non-.txt inputs only)
Searches for existing subtitle files using patterns:
- `*identifier*.txt`
- `*identifier*.srt`
- `*identifier*.vtt`

If no files found, downloads subtitles using `get_subs_youtube.py`.

### Step 4: Blog Generation
Runs `main.py` with the discovered subtitle file to generate:
- Draft article
- SEO analysis
- Final blog post
- HTML version
- Featured image
- SEO JSON metadata

### Step 5: Folder Discovery
Finds the output folder created by `main.py`:
- Searches for folders containing the identifier
- Example: folder `Complete RankMath SEO Tutorial [iNyPGLYBc_E]/`

### Step 6: WordPress Upload
Uploads to WordPress using `wordpress_uploader.py`:
- Creates post from HTML file
- Sets featured image
- Applies Rank Math SEO metadata
- Sets specified post status

## Output Structure

For input `"Tutorial [abc123]"`, the process creates:

```
Tutorial [abc123]/
├── Tutorial [abc123].html          # WordPress post content
├── seo.json                        # Rank Math SEO metadata
├── main_keyphrase.jpg              # Featured image
└── ... (other generated files)
```

## Example Workflow

### Example 1: Process with Download
```bash
$ python subs-blog-wordpress.py "WordPress SEO Guide [xyz789]" --status publish

🚀 Memulai otomasi untuk: WordPress SEO Guide [xyz789]
📝 Status WordPress: publish
📂 Script directory: /path/to/project
==================================================

🔍 Kode ditemukan: xyz789

📥 LANGKAH 1: Cari atau download subtitle
⚠️ File subtitle tidak ditemukan untuk: xyz789
📥 File subtitle tidak ditemukan, mencoba download...
🔄 Download YouTube subtitles
📝 Menjalankan: python /path/get_subs_youtube.py -f WordPress SEO Guide [xyz789]
✅ Download YouTube subtitles berhasil
✅ File subtitle ditemukan: WordPress SEO Guide [xyz789].en.txt

📝 LANGKAH 2: Generate blog post
🔄 Generate blog post
📝 Menjalankan: python /path/main.py WordPress SEO Guide [xyz789].en.txt
✅ Generate blog post berhasil

🔍 LANGKAH 3: Cari folder output
✅ Folder output ditemukan: WordPress SEO Guide [xyz789]

📤 LANGKAH 4: Upload ke WordPress
🔄 Upload ke WordPress
📝 Menjalankan: python /path/wordpress_uploader.py -f WordPress SEO Guide [xyz789] -s publish
✅ Upload ke WordPress berhasil

==================================================
🎉 Proses otomasi selesai!
✅ Identifier: xyz789
✅ Subtitle file: WordPress SEO Guide [xyz789].en.txt
✅ Blog folder: WordPress SEO Guide [xyz789]
✅ WordPress uploaded dengan status: publish
```

### Example 2: Process .txt File (Skip Download)
```bash
$ python subs-blog-wordpress.py "Tutorial Content [abc123].txt" --status draft

🚀 Memulai otomasi untuk: Tutorial Content [abc123].txt
📝 Status WordPress: draft
📂 Script directory: /path/to/project
==================================================

📄 Input adalah file .txt: Tutorial Content [abc123].txt
🔍 Kode ditemukan: abc123

⏭️ LANGKAH 1: Skip download subtitle (file .txt sudah tersedia)

📝 LANGKAH 2: Generate blog post
🔄 Generate blog post
📝 Menjalankan: python /path/main.py Tutorial Content [abc123].txt
✅ Generate blog post berhasil

🔍 LANGKAH 3: Cari folder output
✅ Folder output ditemukan: Tutorial Content [abc123]

📤 LANGKAH 4: Upload ke WordPress
🔄 Upload ke WordPress
📝 Menjalankan: python /path/wordpress_uploader.py -f Tutorial Content [abc123] -s draft
✅ Upload ke WordPress berhasil

==================================================
🎉 Proses otomasi selesai!
✅ Identifier: abc123
✅ Subtitle file: Tutorial Content [abc123].txt
✅ Blog folder: Tutorial Content [abc123]
✅ WordPress uploaded dengan status: draft
```

## Error Handling

The script includes comprehensive error handling:

- **Subtitle not found**: Attempts download, fails gracefully if unsuccessful
- **Blog generation fails**: Stops process with clear error message
- **Folder not found**: Reports missing output folder
- **WordPress upload fails**: Shows detailed error information

## Tips for Success

1. **Use YouTube video codes**: Include `[video_id]` in filenames for best results
2. **Check credentials**: Ensure `.env` file has correct WordPress credentials
3. **Test with drafts**: Use default draft status for testing
4. **Monitor output**: Watch for error messages and status updates
5. **File organization**: Keep subtitle files and generated content organized

## Troubleshooting

### Common Issues

**"File subtitle tidak ditemukan"**
- Ensure YouTube video exists and has subtitles
- Check video ID format (11 characters)
- Verify internet connection

**"Folder output tidak ditemukan"**
- Check if `main.py` completed successfully
- Look for error messages in blog generation step
- Verify Gemini API key is working

**"WordPress upload gagal"**
- Check WordPress credentials in `.env`
- Verify WordPress site is accessible
- Ensure user has proper permissions

### Debug Mode

For debugging, run individual scripts manually:
```bash
# Step by step debugging
python get_subs_youtube.py -f "video_name"
python main.py "subtitle_file.txt"
python wordpress_uploader.py -f "output_folder/" -s draft
```

## Integration with Other Scripts

This automation script works seamlessly with:
- `get_subs_youtube.py` - YouTube subtitle downloader
- `main.py` - Blog content generator
- `wordpress_uploader.py` - WordPress publisher

All scripts use the same configuration files and follow the same conventions.