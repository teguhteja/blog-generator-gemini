# Automatic Blog Article Generator with Gemini AI

A Python script to automate the creation of blog articles, SEO analysis, and supporting images from raw text files (like video transcripts) using the Google Gemini API.

This project is designed to be modular and easily configurable, allowing you to generate high-quality content with an efficient workflow.

## Key Features

  - **Modular & Structured**: The code is broken down into logical modules within the `lib` directory for easy maintenance and development.
  - **Step-by-Step Workflow**: The process is divided into 5 steps that can be run separately:
    1.  **Draft Creation**: Creates an initial article draft from the input text.
    2.  **SEO Analysis**: Generates a list of relevant SEO keyphrases.
    3.  **Final Blog Post Generation**: Rewrites the draft into a complete, SEO-optimized blog article based on a chosen keyphrase.
    4.  **SEO Metadata Update**: Adds additional SEO metadata (like meta description, tags) to the analysis file.
    5.  **Image Generation**: Creates a relevant featured image for the article.
    6.  **HTML Conversion**: Converts the final Markdown blog post into a clean HTML file.
  - **Customizable Prompts**: Easily change the style and content instructions by editing the markdown files in the `prompt/` directory.
  - **Flexible Model Configuration**: Choose different Gemini models for different tasks (e.g., the cheaper 'flash' model for drafts, the more powerful 'pro' model for the final content) via the `model/model.json` file.
  - **Image Optimization**: Automatically resizes and optimizes generated images for the web (requires ImageMagick).
  - **Cost Tracking**: Logs the estimated cost of each API call to `usage_log.csv` for budget monitoring.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.8+**
2.  **Google Gemini API Key**: Get one from Google AI Studio.
3.  **ImageMagick** (Optional, but highly recommended): Required for the image optimization functionality. Download from its official website.

## Installation & Setup

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/teguhteja/repo-name.git
    cd repo-name
    ```

2.  **Create and Activate a Virtual Environment** (Highly Recommended)

    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    Install all required Python libraries using the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Your API Key**

    Create a new file named `.env` in the project's root directory and add your API Key.

    **File: `.env`**

    ```
    GANAI_API_KEY="AIzaSy...YOUR_API_KEY_HERE"
    ```

## How to Run

The script is run from the terminal using `main.py`. All output files will be created in a new directory named after the input file.

### Basic Syntax

```bash
python main.py -i "path/to/your_input_file.txt" [options]
```

### Arguments

  - `-i, --input`: **(Required)** Path to the input `.txt` file.
  - `-p, --prompt`: (Optional) The name of a prompt file from the `prompt/` directory. Default: `prompt`.
  - `-m, --model-config`: (Optional) The name of a model configuration file from the `model/` directory.
  - `--step`: (Optional) The specific steps you want to run (e.g., `1 2 6`). If not specified, all steps (1-6) will be executed.

### Example Usage

1.  **Run all steps (default) from a local file:**

    ```bash
    python main.py -i "my transcript [video_id].txt"
    ```

2.  **Only create a draft (step 1) and SEO analysis (step 2):**

    ```bash
    python main.py -i "my transcript.txt" --step 1 2
    ```

3.  **Only create an image (step 5):**
    *(If step 2 has not been run, the script will prompt you to manually enter a keyphrase)*

    ```bash
    python main.py -i "my transcript.txt" --step 5
    ```

4.  **Generate the final blog and convert it to HTML (steps 3 and 6):**

    ```bash
    python main.py -i "my transcript.txt" --step 3 6
    ```

## Output Structure

For each input file, for example `cool-article.txt`, the script will create the following structure:

```
cool-article/
├── cool-article.md         # Initial draft
├── cool-article.seo.md     # SEO analysis & metadata
├── cool-article.blog.md    # Final blog article
├── cool-article.html       # HTML version of the blog
└── main keyphrase.jpg      # Generated image
```