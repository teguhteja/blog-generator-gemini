# Automatic Blog Post Generator from YouTube Videos

This project automates the creation of blog articles, complete with SEO analysis and supporting images, directly from YouTube video subtitles. It uses the Google Gemini API to generate high-quality content and streamlines the workflow from video to blog post.

## Key Features

- **YouTube Subtitle Downloader**: Fetches and cleans subtitles from any YouTube video.
- **Modular & Structured**: Code is organized into logical modules within the `lib` directory for easy maintenance and extension.
- **Step-by-Step Workflow**: The content generation process is divided into 7 distinct steps:
    1.  **Draft Creation**: Creates an initial article draft from the video transcript.
    2.  **SEO Analysis**: Generates a list of relevant SEO keywords.
    3.  **Final Blog Post Generation**: Rewrites the draft into a complete, SEO-optimized blog article.
    4.  **SEO Metadata Update**: Adds meta descriptions and tags.
    5.  **Image Generation**: Creates a relevant featured image for the article.
    6.  **HTML Conversion**: Converts the final Markdown blog post into a clean HTML file.
    7.  **SEO JSON Generation**: Creates `seo.json` file for WordPress integration.
- **Smart Prompt Auto-Selection**: Automatically selects appropriate prompts based on content (Odoo vs general content).
- **Customizable Prompts**: Easily tailor the style and content by editing the Markdown files in the `prompt/` directory.
- **Flexible Model Configuration**: Choose different Gemini models for different tasks (e.g., 'flash' for drafts, 'pro' for final content) via the `model/model.json` file.
- **Image Optimization**: Automatically resizes and optimizes generated images for the web (requires ImageMagick).
- **Cost Tracking**: Logs the estimated cost of each API call to `usage_log.csv`.
- **WordPress Integration Ready**: Generated files work seamlessly with the included WordPress uploader.
- **Full Automation Script**: New `subs-blog-wordpress.py` handles the entire workflow in one command.

## Project Structure

```
/
├── lib/                     # Core Python modules for each step
├── model/                   # Gemini model configurations (JSON)
├── prompt/                  # Markdown files with prompts for the AI
├── video/                   # Default output directory for generated content
├── chat/                    # Chat logs and session history
├── get_subs_youtube.py      # Script to download YouTube subtitles
├── main.py                  # Main script to run the blog generation workflow
├── subs-blog-wordpress.py   # All-in-one automation script (NEW!)
├── wordpress-uploader.py    # WordPress upload script with Rank Math integration
├── README.md                # This file
├── subs-blog-wordpress.README.md  # Automation script documentation
├── README.wordpress-uploader.md  # WordPress uploader documentation
└── usage_log.csv            # API usage cost tracking
```

## Modules in `lib/`

- `download_subs.py`: Handles downloading and cleaning of YouTube video subtitles.
- `gemini_api.py`: Manages all interactions with the Google Gemini API.
- `my_generate_blog.py`: Contains the main logic for generating the blog post from a draft.
- `workflow_steps.py`: Defines the individual steps of the content generation process.
- `image_processing.py`: Handles image generation and optimization.
- `utils.py`: Provides helper functions used across the project.

## Prerequisites

1.  **Python 3.8+**
2.  **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).
3.  **ImageMagick** (Optional, for image optimization): Download from its [official website](https://imagemagick.org/).

## Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows: .\venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your API Key**
    Create a `.env` file in the root directory and add your API key:
    ```
    GANAI_API_KEY="your_api_key_here"
    ```

## How to Run

### Option 1: Full Automation (Recommended)

Use the all-in-one automation script that handles the entire workflow:

```bash
# Full automation: Download subtitles → Generate blog → Upload to WordPress
python subs-blog-wordpress.py "Video Title [video_id]" --status publish

# Or with draft status (default)
python subs-blog-wordpress.py "Tutorial Video Name"
```

This script will:
1. **Extract identifier** from your input (YouTube code from `[code]` or first 3 words)
2. **Find existing subtitles** or download them if needed
3. **Generate blog post** with all SEO optimization
4. **Upload to WordPress** with featured image and Rank Math SEO

See [`subs-blog-wordpress.README.md`](subs-blog-wordpress.README.md) for detailed automation documentation.

### Option 2: Manual Step-by-Step Process

For more control over individual steps:

#### Step 1: Download Subtitles

First, download the subtitles from a YouTube video. This will create a `.txt` file in the project directory.

```bash
python get_subs_youtube.py [YOUTUBE_VIDEO_URL]
```
This will generate a file like `Video Title [video_id].txt`.

#### Step 2: Generate Blog Post

Next, use the generated text file as input for the main script.

#### Basic Syntax
```bash
python main.py -i "path/to/your_input_file.txt" [options]
```

#### Arguments
- `-i, --input`: **(Required)** Path to the input `.txt` file.
- `-p, --prompt`: (Optional) The name of a prompt file from the `prompt/` directory. Auto-selected based on content if not specified.
- `-m, --model-config`: (Optional) The name of a model configuration file from the `model/` directory. Default: `model.json`.
- `--step`: (Optional) The specific steps to run (e.g., `1 2 6`). If not specified, all steps (1-7) will be executed.
- `-sk, --seo-keyphrase`: (Optional) Choose SEO keyphrase: 1-5 for direct selection, 0 for manual selection. Default: auto-select highest score.

#### Example Usage

1.  **Run all steps on the downloaded transcript:**
    ```bash
    python main.py -i "Video Title [video_id].txt"
    ```

2.  **Only create a draft (step 1) and SEO analysis (step 2):**
    ```bash
    python main.py -i "Video Title [video_id].txt" --step 1 2
    ```

3.  **Generate the final blog and convert it to HTML (steps 3 and 6):**
    ```bash
    python main.py -i "Video Title [video_id].txt" --step 3 6
    ```

4.  **Run all steps with specific SEO keyphrase selection:**
    ```bash
    python main.py -i "Video Title [video_id].txt" -sk 1
    ```

5.  **Generate only SEO JSON for WordPress integration (step 7):**
    ```bash
    python main.py -i "Video Title [video_id].txt" --step 7
    ```

## Output Structure

For an input file named `My Video [12345].txt`, the script will create the following structure in the `video/` directory:

```
video/My Video [12345]/
├── My Video [12345].md         # Initial draft
├── My Video [12345].seo.md     # SEO analysis & metadata
├── My Video [12345].blog.md    # Final blog article
├── My Video [12345].html       # HTML version of the blog
├── seo.json                    # SEO metadata for WordPress (step 7)
└── main_keyphrase.jpg          # Generated image
```

## WordPress Integration

After generating your blog content, use the included WordPress uploader to publish:

```bash
# Upload generated content to WordPress
python wordpress-uploader.py -f "video/My Video [12345]" -s publish
```

The uploader will:
- Create WordPress post from the HTML file
- Upload the generated image as featured image
- Apply SEO metadata from `seo.json` using Rank Math API
- Set optimized slug and meta descriptions

See [`README.wordpress-uploader.md`](README.wordpress-uploader.md) for detailed WordPress integration instructions.
