# fastapi/app/services/agents.py
import os

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def run_agent(persona: str, query: str, history: list | None = None) -> str:
    """Ejecuta un agente con OpenAI. Devuelve la respuesta del modelo."""
    if not _client:
        return "OPENAI_API_KEY no configurada en el servidor."

    messages = [
        {"role": "system", "content": persona},
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": query})

    resp = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()