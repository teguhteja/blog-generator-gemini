__TASK__
Create a JSON file named "seo.json" based on the provided content.

__CONTEXT__
The context from file *.seo.md that include detail about seo for this blog.

__INPUT_SOURCE__
The content for the JSON object will be provided in a markdown file with the following format:
- Meta Title: [Your SEO Title]
- Meta Description: [Your Meta Description]
- Focus Keyword: [Your Focus Keyword]
- Slug: [Your URL Slug]

__OUTPUT_FORMAT__
Generate a single JSON object with the following structure, using the data from the input source.
```json
{
  "meta": {
    "rank_math_title": "[Meta Title]",
    "rank_math_description": "[Meta Description]",
    "rank_math_focus_keyword": "[Focus Keyword]"
  },
  "slug": "[Slug]"
}
```

