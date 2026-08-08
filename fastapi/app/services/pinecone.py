# fastapi/app/services/pinecone.py
import os

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "valola-vectors")

_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def embed_text(text: str) -> list[float]:
    if not _client:
        raise RuntimeError("OPENAI_API_KEY no configurada")
    resp = _client.embeddings.create(model="text-embedding-3-small", input=[text])
    return resp.data[0].embedding


def upsert_vectors(vectors: list[dict]):
    """vectors: [{"id": str, "vector": [...], "metadata": {...}}]"""
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key=PINECONE_API_KEY)
    idx = pc.Index(PINECONE_INDEX_NAME)
    prepared = [
        {
            "id": v["id"],
            "values": v["vector"],
            "metadata": v.get("metadata", {}),
        }
        for v in vectors
    ]
    idx.upsert(vectors=prepared)
    return len(prepared)


def query_vectors(vector: list[float], top_k: int = 5, namespace: str = ""):
    from pinecone import Pinecone

    pc = Pinecone(api_key=PINECONE_API_KEY)
    idx = pc.Index(PINECONE_INDEX_NAME)
    resp = idx.query(vector=vector, top_k=top_k, namespace=namespace, include_metadata=True)
    return resp.matches