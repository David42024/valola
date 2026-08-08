# fastapi/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from app.database import Base, engine
from app.routers import agents, users, whatsapp
from app.services import memory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando Valola API...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos lista.")
    except Exception as e:
        logger.warning(f"No se pudo conectar a la base: {e}")
    yield


app = FastAPI(
    title="Valola API",
    description="Sistema multi-agente para WhatsApp",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(whatsapp.router, prefix="/api/whatsapp", tags=["whatsapp"])


@app.get("/")
async def root():
    return {
        "message": "Valola API funcionando!",
        "status": "production",
        "environment": "cloud",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health():
    db_status = "connected"
    try:
        with engine.connect():
            pass
    except Exception:
        db_status = "unavailable"

    try:
        memory.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "unavailable"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_status,
            "redis": redis_status,
            "api": "active",
        },
    }


# Endpoint de prueba para validar n8n
@app.post("/api/test")
async def test_endpoint(data: dict):
    logger.info(f"Recibido: {data}")
    return {
        "status": "success",
        "received": data,
        "processed": True,
    }