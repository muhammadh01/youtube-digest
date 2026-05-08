# youtube-digest

[![Deploy](https://github.com/muhammadh01/youtube-digest/actions/workflows/deploy.yml/badge.svg)](https://github.com/muhammadh01/youtube-digest/actions/workflows/deploy.yml)
[![Release](https://github.com/muhammadh01/youtube-digest/actions/workflows/release.yml/badge.svg)](https://github.com/muhammadh01/youtube-digest/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-grade YouTube video summarization service. Paste a URL, get a structured summary in seconds — backed by either OpenAI or a self-hosted LLM.

- **Live demo:** https://durak.dev
- **API docs:** https://api.durak.dev/docs

## Features

- **REST API** — FastAPI with auto-generated OpenAPI docs
- **Web UI** — Streamlit frontend at `durak.dev`
- **Pluggable LLM** — runtime switch between OpenAI (`gpt-4.1-mini`) and self-hosted Llama 3.2 (Ollama) via `LLM_PROVIDER` env var
- **Caching** — Redis layer reduces repeat-request latency from ~15s to <50ms
- **HTTPS** — auto-renewing Let's Encrypt certs across 4 subdomains
- **Observability** — Prometheus metrics + Grafana dashboards (request rate, p95 latency, status codes)
- **CI/CD** — GitHub Actions: test, build, SSH deploy, and tag-triggered semantic releases publishing to GHCR

## Stack

Python 3.11, FastAPI, Pydantic, OpenAI SDK, Ollama, Redis, Streamlit, nginx, certbot, Prometheus, Grafana, Docker Compose, GitHub Actions, Hetzner Cloud (ARM).

## Development (local)

    git clone https://github.com/muhammadh01/youtube-digest.git
    cd youtube-digest
    cp .env.example .env
    docker compose up -d --build

- API: http://localhost:8000/docs
- Web: http://localhost:8501
- Grafana: http://localhost:3000

## CLI usage

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID"

## Endpoints

- `GET /` — service info
- `GET /health` — health check
- `GET /metrics` — Prometheus metrics
- `POST /summarize` — body: `{"url": "..."}` returns `{"url": "...", "summary": "...", "cached": bool}`

## How it works

1. Fetches the video title and transcript via `youtube-transcript-api`
2. Counts tokens with `tiktoken` and chunks the transcript if it exceeds the model context window
3. Summarizes each chunk with the configured LLM (OpenAI or local Ollama)
4. Stitches the chunk summaries into one final cohesive summary
5. Caches the result in Redis (7-day TTL) keyed by SHA-256 of the URL

## Roadmap

- [x] CLI tool
- [x] FastAPI service
- [x] Dockerize
- [x] Deploy to cloud (Hetzner)
- [x] Redis caching
- [x] HTTPS via nginx + Let's Encrypt
- [x] Streamlit frontend
- [x] CI/CD with GitHub Actions + GHCR releases
- [x] Self-hosted LLM (Ollama)
- [x] Prometheus + Grafana
- [ ] Auth + rate limiting

## License

MIT