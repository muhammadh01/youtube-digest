# youtube-digest

A YouTube video summarizer with three ways to run it: a CLI, a FastAPI service, and a Docker container. Fetches a video transcript, chunks it if needed, and returns a structured academic-style summary using OpenAI.

## Features

- CLI tool for one-off summaries from the terminal
- REST API with auto-generated Swagger docs
- Containerized with Docker — runs identically anywhere
- Automatic transcript chunking and stitching for long videos
- Structured markdown output (title, topic, key insights)

## Setup (local)

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

### API mode (local)

```
python -m uvicorn api:app --reload
```

Then open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

### Docker mode

```
docker build -t utube-digest:0.1 .
docker run -d --name youtube-digest -p 8000:8000 --env-file .env youtube-digest:0.1
```

The API will be live at **http://127.0.0.1:8000/docs**.

## Endpoints

- `GET /` — service info
- `GET /health` — health check
- `POST /summarize` — body: `{"url": "..."}` → returns `{"url": "...", "summary": "..."}`

## Example

```
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=VIDEO_ID"}'
```

## How it works

1. Fetches the video title and transcript via `youtube-transcript-api`
2. Counts tokens with `tiktoken` and chunks the transcript if it exceeds the model context window
3. Summarizes each chunk with `gpt-4.1-mini`
4. Stitches the chunk summaries into one final cohesive summary

## Roadmap

- [x] CLI tool
- [x] FastAPI service
- [x] Dockerize
- [x] Deploy to cloud (Hetzner)
- [x] Redis caching (with docker-compose)
- [ ] Self-hosted model (Ollama / vLLM)
- [ ] Prometheus + Grafics
- [ ] GitHub Actions CI/CD

## License

MIT
