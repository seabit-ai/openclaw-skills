#!/bin/bash
# Tavily Search Script for OpenClaw

QUERY="$1"
MAX_RESULTS="${2:-5}"

if [ -z "$TAVILY_API_KEY" ]; then
  echo "Error: TAVILY_API_KEY environment variable is not set."
  exit 1
fi

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"basic\",
    \"max_results\": $MAX_RESULTS
  }"
