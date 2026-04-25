import os
import re
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from youtube import YouTubeVideo

load_dotenv(override=True)

MODEL = "gpt-4.1-mini"
MAX_CHUNK_TOKENS = 4000

SYSTEM_PROMPT = """
You are an expert YouTube video summarizer. Your job is to take the transcript of a video
and generate a structured, precise, and academically grounded summary.

Your output must include:

1. Title — reuse the video's title if clear, or write a sharper one.
2. Topic & Area of Coverage — domain (Finance, Health, Tech, etc.) and sub-area.
3. Summary — structured, concise, focused on key insights, frameworks, and actionable advice.

Rules:
- Be specific. Avoid vague generalizations.
- Use bullet points or numbered lists where it helps.
- Skip ads, jokes, tangents, and filler.
- Reference any studies or sources mentioned.
- Respond in markdown. Do not wrap the markdown in a code block.
"""

STITCH_PROMPT = """You are combining multiple section-summaries of one video into a single
cohesive summary. Eliminate redundancy, keep all important information, maintain the
academic tone, and follow the same structure (Title, Topic, Summary)."""


def count_tokens(text):
    try:
        encoding = tiktoken.encoding_for_model(MODEL)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def chunk_text(text, max_tokens=MAX_CHUNK_TOKENS):
    if count_tokens(text) <= max_tokens:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""

    for sentence in sentences:
        candidate = (current + " " + sentence).strip() if current else sentence
        if count_tokens(candidate) <= max_tokens:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks


def _client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found. Copy .env.example to .env and add your key.")
    return OpenAI(api_key=api_key)


def _ask(client, system, user):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system.strip()},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def summarize(url):
    video = YouTubeVideo(url)
    client = _client()

    chunks = chunk_text(video.transcript)
    print(f"Title: {video.title}")
    print(f"Transcript split into {len(chunks)} chunk(s).\n")

    if len(chunks) == 1:
        user_prompt = f"Video Title: {video.title}\n\nTranscript:\n{chunks[0]}"
        return _ask(client, SYSTEM_PROMPT, user_prompt)

    chunk_summaries = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        user_prompt = f"Video Title: {video.title}\n\nTranscript section:\n{chunk}"
        chunk_summaries.append(_ask(client, SYSTEM_PROMPT, user_prompt))

    print("Stitching final summary...\n")
    joined = "\n\n".join([f"Section {i+1}:\n{s}" for i, s in enumerate(chunk_summaries)])
    stitch_user = f"Video Title: {video.title}\n\nSection summaries:\n{joined}"
    return _ask(client, STITCH_PROMPT, stitch_user)
