# youtube-digest

A YouTube video summarizer with two interfaces: a simple CLI for quick use, and a FastAPI service ready for production. Fetches a video transcript, chunks it if needed, and returns a structured academic-style summary using OpenAI.

## Features

- CLI tool for one-off summaries from the terminal
- REST API with auto-generated Swagger docs
- Automatic transcript chunking and stitching for long videos
- Structured markdown output (title, topic, key insights)

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env` and paste your OpenAI API key.

## Usage

### CLI mode

```
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### API mode

Start the server:

```
python -m uvicorn api:app --reload
```

Then open the interactive docs at **http://127.0.0.1:8000/docs**, or call it directly:

```
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=VIDEO_ID"}'
```

## Endpoints

- `GET /` — service info
- `GET /health` — health check
- `POST /summarize` — body: `{"url": "..."}` → returns `{"url": "...", "summary": "..."}`

## How it works

1. Fetches the video title and transcript via `youtube-transcript-api`
2. Counts tokens with `tiktoken` and chunks the transcript if it exceeds the model context window
3. Summarizes each chunk with `gpt-4.1-mini`
4. Stitches the chunk summaries into one final cohesive summary

## Roadmap

- [x] CLI tool
- [x] FastAPI service
- [ ] Dockerize
- [ ] Redis caching
- [ ] Self-hosted model (Ollama / vLLM)
- [ ] Prometheus + Grafana metrics
- [ ] GitHub Actions CI/CD
- [ ] Cloud deployment

## License

MIT
