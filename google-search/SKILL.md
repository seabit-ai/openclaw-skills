---
name: google-search
description: High-performance Google Search via Serper.dev. Returns raw organic search results, snippets, and knowledge graph data. Use when you need the broadest index of the web, or for highly specific technical/local information.
---

# Google Search (via Serper)

This skill provides access to Google Search results via the Serper.dev API.

## Usage

Run the search script via `exec`:

```bash
skills/google-search/scripts/search.sh "your search query" [max_results]
```

### Examples

1. Basic Google search:
   `exec(command="skills/google-search/scripts/search.sh 'rust async-std vs tokio benchmark'")`

2. News search (if implemented in script):
   (Current script defaults to organic search)

## Output Format

The script returns a JSON object containing `organic` results, `knowledgeGraph`, and `relatedSearches`.

## Environment Requirements

- `SERPER_API_KEY`: Must be set in the OpenClaw environment.
