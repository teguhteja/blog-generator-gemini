# WordPress Auto Upload Script

Python script to automatically upload HTML files and images to WordPress via REST API with full support for Rank Math SEO.

## Features

- ✅ Upload HTML files as WordPress posts
- ✅ Upload images (JPG, PNG, GIF, WebP) as featured images
- ✅ **Rank Math SEO Integration** - Automatic SEO metadata updates
- ✅ **seo.json Support** - Read SEO data from JSON files
- ✅ **Smart image filtering** - Only upload images <100KB
- ✅ Match HTML files with images based on filename
- ✅ Configuration via .env file
- ✅ Support multiple files in one folder
- ✅ Post status options (draft/published/private)
- ✅ **Command line interface** with arguments

## Setup for Claude Code

### 1. Environment Preparation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and edit .env file
cp .env.example .env
```

### 2. WordPress Configuration

1. **Create Application Password** in WordPress:
   - Login to WordPress Admin
   - Go to Users → Your Profile
   - Scroll down to "Application Passwords"
   - Create new password with name "Auto Upload Script"
   - Copy the generated password

2. **Edit .env file**:
```env
WP_URL=https://yoursite.com
WP_USERNAME=your_username  
WP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx  # Application Password
```

### 3. Folder Structure

Organize your files like this:
```
project-folder/
├── wordpress-uploader.py
├── requirements.txt
├── .env
└── content/
    ├── article1.html
    ├── article1.jpg
    ├── article2.html
    ├── article2.jpg
    ├── seo.json                 # SEO metadata file (optional)
    └── ...
```

### 4. SEO JSON File (Optional)

Create `seo.json` file in content folder for SEO metadata:
```json
{
  "meta": {
    "rank_math_title": "SEO Title Optimized",
    "rank_math_description": "Meta description for better search rankings",
    "rank_math_focus_keyword": "wordpress seo",
    "rank_math_canonical_url": "https://example.com/canonical-url"
  },
  "slug": "optimized-post-slug"
}
```

### 5. HTML File Format

HTML files can be:
- Complete HTML with `<html>`, `<head>`, `<body>`
- HTML fragments (content only)
- Will automatically extract title from `<h1>` tag (priority) or `<title>`

HTML Example:
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Article Title</title>
</head>
<body>
    <h1>Main Article Title</h1>
    <p>Article content goes here...</p>
</body>
</html>
```

## Usage

### Command Line Mode (Recommended)

```bash
# Upload from specific folder as draft
python wordpress-uploader.py -f ./content

# Upload as published post
python wordpress-uploader.py -f ./content -s publish

# Upload as private post
python wordpress-uploader.py -f ./content -s private
```

### Interactive Mode

```bash
python wordpress-uploader.py
```

The script will:
1. Ask for folder path (default: current folder)
2. Ask for post status choice (draft/published/private)
3. Automatically process all HTML files and small images (<100KB)

### Example Output

```
📁 Processing folder: ./content
📊 SEO data loaded from ./content/seo.json

📏 article1.jpg: 45.2 KB (will be uploaded)
⚠️ article2.jpg: 150.3 KB (too large, skipped)
Found 2 HTML files and 1 small image (<100KB)

🖼️ Uploading 1 small image...
📤 Uploading image: article1.jpg
✅ Image successfully uploaded - ID: 123, Alt: 'article1'

--- Processing article1.html ---
📰 Title from H1: Main Article Title
🔗 Slug: optimized-post-slug
🖼️ Using featured image: article1 (ID: 123)
📝 Creating post: Main Article Title
✅ Post successfully created - ID: 456
🔗 URL: https://yoursite.com/optimized-post-slug
🔄 Updating Rank Math SEO metadata...
🎯 Updating Rank Math SEO for post ID: 456
✅ Rank Math SEO successfully updated
   ✓ rank_math_title: updated
   ✓ rank_math_description: updated
   ✓ rank_math_focus_keyword: updated

--- Processing article2.html ---
⚠️ No matching image found for featured image
📰 Title from H1: Article Title 2
📝 Creating post: Article Title 2
✅ Post successfully created - ID: 457
🔗 URL: https://yoursite.com/article2
🔄 Updating Rank Math SEO metadata...
🎯 Updating Rank Math SEO for post ID: 457
✅ Rank Math SEO successfully updated
   ✓ rank_math_title: updated
   ✓ rank_math_description: updated

✅ Done!
```

## Rank Math Requirements

For SEO features to work properly, ensure:

1. **Rank Math plugin** is installed and active in WordPress
2. **Rank Math API Manager Plugin** is installed and active
3. User has `edit_posts` permission

## Arguments/Parameters

```bash
python wordpress-uploader.py [options]

Options:
  -f, --folder FOLDER    Path to folder containing HTML and image files
  -s, --status STATUS    Post status: draft, publish, private (default: draft)
  -h, --help            Show help message
```

## Customization with Claude Code

You can ask Claude Code to:

1. **Add taxonomy features**:
   ```
   "Add support for categories and tags from seo.json"
   ```

2. **Multiple SEO formats**:
   ```
   "Add support for Yoast SEO and All in One SEO"
   ```

3. **Batch processing**:
   ```
   "Create batch mode to process multiple folders at once"
   ```

4. **Advanced image handling**:
   ```
   "Add automatic image resize and compression features"
   ```

## Troubleshooting

### Error "Missing credentials"
- Ensure .env file exists and contains all required variables
- Check WP_URL format (must include https://)

### Error "401 Unauthorized" 
- Ensure you're using Application Password, not login password
- Check username and password in .env

### Error "Media upload failed"
- Ensure image files are not corrupted and size is <100KB (automatically filtered)
- Check upload permissions in WordPress
- Supported formats: JPG, PNG, GIF, WebP

### Error "Post creation failed"
- Check if user has permission to create posts
- Ensure HTML content is valid

### Error "Rank Math SEO update failed"
- Ensure Rank Math API Manager plugin is installed
- Check if endpoint `/wp-json/rank-math-api/v1/update-meta` is available
- Ensure seo.json file format is correct

## Security Notes

- ⚠️ Don't commit .env file to repository
- ✅ Use Application Password, not main password
- ✅ Store credentials securely
- ✅ Remove .env after use if necessary

## License

MIT License - Use freely for your projects.