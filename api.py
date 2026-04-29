from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from summarizer import summarize
import cache

app = FastAPI(
    title="youtube-digest",
    description="Summarize YouTube videos using OpenAI.",
    version="0.2.0",
)


class SummarizeRequest(BaseModel):
    url: str


class SummarizeResponse(BaseModel):
    url: str
    summary: str
    cached: bool


@app.get("/")
def root():
    return {
        "service": "youtube-digest",
        "status": "ok",
        "cache_enabled": cache.is_enabled(),
    }


@app.get("/health")
def health():
    return {"status": "healthy", "cache_enabled": cache.is_enabled()}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(payload: SummarizeRequest):
    try:
        was_cached = cache.get(payload.url) is not None
        summary = summarize(payload.url)
        return SummarizeResponse(url=payload.url, summary=summary, cached=was_cached)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
