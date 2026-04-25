# youtube-digest

A Python CLI tool that fetches a YouTube video transcript and produces a structured, academic-style summary using OpenAI. Handles long videos by chunking the transcript and stitching the section summaries into one cohesive result.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env` and paste your OpenAI API key.

## Usage

```
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The output is a markdown summary printed to your terminal, including:
- A clear title
- The topic and area of coverage
- A structured summary with key insights, frameworks, and actionable advice

## How it works

1. Fetches the video title and transcript via `youtube-transcript-api`
2. Counts tokens with `tiktoken` and chunks the transcript if it exceeds the model context window
3. Summarizes each chunk with `gpt-4.1-mini`
4. Stitches the chunk summaries into one final summary

## License

MIT
