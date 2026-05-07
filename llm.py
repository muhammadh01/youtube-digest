import os
import requests
from openai import OpenAI

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def _openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found.")
    return OpenAI(api_key=api_key)


def chat(system, user, temperature=0.3):
    if PROVIDER == "ollama":
        return _chat_ollama(system, user, temperature)
    return _chat_openai(system, user, temperature)


def _chat_openai(system, user, temperature):
    client = _openai_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system.strip()},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


def _chat_ollama(system, user, temperature):
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system.strip()},
                {"role": "user", "content": user},
            ],
            "options": {"temperature": temperature},
            "stream": False,
        },
        timeout=600,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def provider_info():
    if PROVIDER == "ollama":
        return {"provider": "ollama", "model": OLLAMA_MODEL}
    return {"provider": "openai", "model": OPENAI_MODEL}