__TASK__
- Create 5 potential SEO-focused keyphrases in English for a blog post.
- The keyphrases should be based on the provided context from the file.
- The keyphrases should have a maximum of 4 content words.

__OUTPUT_FORMAT__
- For each keyphrase, provide an SEO evaluation matrix with the following metrics and their scores (High=3, Medium=2, Low=1):
  - Search Volume (Volume Pencarian)
  - Keyword Difficulty (Tingkat Kesulitan)
  - Search Intent (Niat Pencarian)
- Calculate the total score for each keyphrase by summing the scores of the three metrics.
- Rank the keyphrases in descending order of their total score (from highest to lowest).
- **Ranking Rules (Tie-breaking Rule):**
  - If two or more keyphrases have the same total score, prioritize the keyphrase with a higher "Search Intent" score.
  - If all metrics have the same score, prioritize the keyphrase that is most relevant to the main topic discussed in the file.

__CONTEXT__
- Extract the file I uploaded and use it as context.
- Include the file name.