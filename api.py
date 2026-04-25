from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from summarizer import summarize

app = FastAPI(
    title="youtube-digest",
    description="Summarize YouTube videos using OpenAI.",
    version="0.1.0",
)


class SummarizeRequest(BaseModel):
    url: str


class SummarizeResponse(BaseModel):
    url: str
    summary: str


@app.get("/")
def root():
    return {"service": "youtube-digest", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(payload: SummarizeRequest):
    try:
        summary = summarize(payload.url)
        return SummarizeResponse(url=payload.url, summary=summary)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
