---
name: tavily-search
description: High-quality web search using Tavily API. Optimized for LLM agents. Returns clean, structured content from the web. Use when you need the most accurate and up-to-date information, or when Brave Search is rate-limited.
---

# Tavily Search

This skill provides access to the Tavily Search API, which is specifically designed for AI agents to retrieve high-quality, cleaned web content.

## Usage

Run the search script via `exec`:

```bash
scripts/search.sh "your search query" [max_results]
```

### Examples

1. Basic search:
   `exec(command="skills/tavily-search/scripts/search.sh 'current price of Nvidia stock'")`

2. Limited results:
   `exec(command="skills/tavily-search/scripts/search.sh 'best pizza in Seattle' 3")`

## Output Format

The script returns a JSON object with:
- `query`: Your search query
- `results`: An array of objects containing `url`, `title`, `content` (cleaned text), and `score`.

## Environment Requirements

- `TAVILY_API_KEY`: Must be set in the OpenClaw environment (already configured in `openclaw.json`).
