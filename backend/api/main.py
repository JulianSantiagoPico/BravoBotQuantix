import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.pipeline import ask
from rag.retriever import get_collection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("bravobot.api")

app = FastAPI(
    title="BravoBot API",
    description="Asistente inteligente para aspirantes de la I.U. Pascual Bravo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    try:
        get_collection()
        logger.info("ChromaDB cargado correctamente al iniciar.")
    except Exception as exc:
        logger.warning(
            f"No se pudo cargar ChromaDB al iniciar: {exc}. "
            "Ejecuta run_ingestion.py primero."
        )


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    respuesta: str
    fuentes: list[str]
    categoria: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="La query no puede estar vacía.")
    try:
        result = ask(request.query)
        return ChatResponse(**result)
    except Exception as exc:
        logger.error(f"Error en /chat: {exc}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "BravoBot API"}
