# fastapi/app/services/utils.py
import re
import hashlib
import secrets
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_phone(number: str) -> str:
    """Normaliza un número de WhatsApp a formato internacional E.164."""
    digits = re.sub(r"\D", "", number)
    if len(digits) == 10:
        digits = "52" + digits
    if not digits.startswith("+"):
        digits = "+" + digits
    return digits


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()