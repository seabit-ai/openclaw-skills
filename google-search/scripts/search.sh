#!/bin/bash
# Serper Google Search Script for OpenClaw

QUERY="$1"
MAX_RESULTS="${2:-5}"

if [ -z "$SERPER_API_KEY" ]; then
  echo "Error: SERPER_API_KEY environment variable is not set."
  exit 1
fi

curl -s -X POST https://google.serper.dev/search \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"q\": \"$QUERY\",
    \"num\": $MAX_RESULTS
  }"
