# Automatic Blog Post Generator from YouTube Videos

This project automates the creation of blog articles, complete with SEO analysis and supporting images, directly from YouTube video subtitles. It uses the Google Gemini API to generate high-quality content and streamlines the workflow from video to blog post.

## Key Features

- **YouTube Subtitle Downloader**: Fetches and cleans subtitles from any YouTube video.
- **Modular & Structured**: Code is organized into logical modules within the `lib` directory for easy maintenance and extension.
- **Step-by-Step Workflow**: The content generation process is divided into distinct steps:
    1.  **Draft Creation**: Creates an initial article draft from the video transcript.
    2.  **SEO Analysis**: Generates a list of relevant SEO keywords.
    3.  **Final Blog Post Generation**: Rewrites the draft into a complete, SEO-optimized blog article.
    4.  **SEO Metadata Update**: Adds meta descriptions and tags.
    5.  **Image Generation**: Creates a relevant featured image for the article.
    6.  **HTML Conversion**: Converts the final Markdown blog post into a clean HTML file.
- **Customizable Prompts**: Easily tailor the style and content by editing the Markdown files in the `prompt/` directory.
- **Flexible Model Configuration**: Choose different Gemini models for different tasks (e.g., 'flash' for drafts, 'pro' for final content) via the `model/model.json` file.
- **Image Optimization**: Automatically resizes and optimizes generated images for the web (requires ImageMagick).
- **Cost Tracking**: Logs the estimated cost of each API call to `usage_log.csv`.

## Project Structure

```
/
├── lib/                # Core Python modules for each step
├── model/              # Gemini model configurations (JSON)
├── prompt/             # Markdown files with prompts for the AI
├── video/              # Default output directory for generated content
├── get_subs_youtube.py # Script to download YouTube subtitles
├── main.py             # Main script to run the blog generation workflow
└── README.md           # This file
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

The workflow is a two-step process:

### Step 1: Download Subtitles

First, download the subtitles from a YouTube video. This will create a `.txt` file in the project directory.

```bash
python get_subs_youtube.py [YOUTUBE_VIDEO_URL]
```
This will generate a file like `Video Title [video_id].txt`.

### Step 2: Generate Blog Post

Next, use the generated text file as input for the main script.

#### Basic Syntax
```bash
python main.py -i "path/to/your_input_file.txt" [options]
```

#### Arguments
- `-i, --input`: **(Required)** Path to the input `.txt` file.
- `-p, --prompt`: (Optional) The name of a prompt file from the `prompt/` directory. Default: `prompt`.
- `-m, --model-config`: (Optional) The name of a model configuration file from the `model/` directory.
- `--step`: (Optional) The specific steps to run (e.g., `1 2 6`). If not specified, all steps (1-6) will be executed.

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

## Output Structure

For an input file named `My Video [12345].txt`, the script will create the following structure in the `video/` directory:

```
video/My Video [12345]/
├── My Video [12345].md         # Initial draft
├── My Video [12345].seo.md     # SEO analysis & metadata
├── My Video [12345].blog.md    # Final blog article
├── My Video [12345].html       # HTML version of the blog
└── main_keyphrase.jpg          # Generated image
```
