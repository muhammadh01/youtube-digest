import os
import hashlib
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "604800"))

try:
    _client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    _client.ping()
    _enabled = True
except Exception:
    _client = None
    _enabled = False


def _key(url):
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return f"summary:{digest}"


def get(url):
    if not _enabled:
        return None
    try:
        return _client.get(_key(url))
    except Exception:
        return None


def set(url, summary):
    if not _enabled:
        return
    try:
        _client.setex(_key(url), CACHE_TTL_SECONDS, summary)
    except Exception:
        pass


def is_enabled():
    return _enabled
