# fastapi/app/services/memory.py
import json
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_TOKEN = os.getenv("REDIS_TOKEN", "")

_client = None


def get_client():
    global _client
    if _client is None:
        opts = {"decode_responses": True}
        if REDIS_TOKEN:
            # Upstash usa el token como username/password vía TLS
            opts["username"] = "default"
            opts["password"] = REDIS_TOKEN
        _client = redis.Redis.from_url(REDIS_URL, **opts)
    return _client


def ping() -> bool:
    return bool(get_client().ping())


def set_memory(key: str, value: dict, ttl: int = 3600):
    get_client().setex(key, ttl, json.dumps(value))


def get_memory(key: str) -> dict | None:
    raw = get_client().get(key)
    return json.loads(raw) if raw else None


def delete_memory(key: str):
    get_client().delete(key)