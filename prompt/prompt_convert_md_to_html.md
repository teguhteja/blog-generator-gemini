__ASK__
- Convert the provided Markdown content into a clean, well-structured HTML file.

__CONSTRAINTS__
- The output must be only the raw HTML code.
- Remove `Tonton video tutorial asli di YouTube` 
- Add `<!-- wp:embed {"url":"youtube_link","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} --><figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper"> youtube_link </div></figure><!-- /wp:embed -->` after heading / title and replace `youtube_link` with youtube url
- Do not add any extra commentary, explanations, or markdown formatting like ```html.
- Preserve all original formatting from the Markdown, including:
    - Headings (h1, h2, h3, etc.)
    - Paragraphs
    - Bold and italic text
    - Unordered and ordered lists
    - Links (a href)
- Ensure the HTML is valid and ready to be used on a web page.

__CONTEXT__
- Use the content I uploaded as the Markdown source.