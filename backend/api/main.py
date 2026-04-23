import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.pipeline import ask
from rag.retriever import get_index
from rag.router import VALID_CATEGORIES
from rag.sanitizer import sanitize_query, sanitize_session_id
import os
import httpx

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
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000", 
        "https://bravo-bot-quantix.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    try:
        get_index()
        logger.info("Pinecone cargado correctamente al iniciar.")
    except Exception as exc:
        logger.warning(
            f"No se pudo cargar Pinecone al iniciar: {exc}. "
        )


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Pregunta del aspirante (máx 500 caracteres)")
    session_id: str | None = Field(None, max_length=64, description="ID de sesión alfanumérico (máx 64 caracteres)")

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("La query no puede ser solo espacios en blanco.")
        return v

    @field_validator("session_id")
    @classmethod
    def session_id_format(cls, v: str | None) -> str | None:
        if v is None:
            return None
        import re
        if not re.match(r"^[a-zA-Z0-9_-]{1,64}$", v):
            raise ValueError("session_id inválido. Solo alfanuméricos, guiones y guiones bajos (máx 64 chars).")
        return v


class ChatResponse(BaseModel):
    respuesta: str
    fuentes: list[str]
    categoria: str
    categorias: list[str]
    session_id: str | None = None


# Almacenamiento en memoria para el historial de conversaciones
# Formato: { "session_id": [{"role": "user", "text": "..." }, {"role": "model", "text": "..."}] }
sessions: dict[str, list[dict]] = {}
MAX_HISTORY_LENGTH = 10   # Máximo de mensajes por sesión
MAX_SESSIONS = 1000       # Máximo de sesiones activas en memoria


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Sanitizar inputs (segunda capa de defensa tras la validación Pydantic)
    try:
        clean_query = sanitize_query(request.query)
        clean_session_id = sanitize_session_id(request.session_id)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))

    try:
        history = []

        if clean_session_id:
            # Protección contra memory flooding: limitar sesiones activas
            if clean_session_id not in sessions and len(sessions) >= MAX_SESSIONS:
                logger.warning(
                    f"[SECURITY] Límite de sesiones activas ({MAX_SESSIONS}) alcanzado. "
                    "Rechazando nueva sesión."
                )
                raise HTTPException(
                    status_code=429,
                    detail="Demasiadas sesiones activas. Inténtalo más tarde.",
                )
            if clean_session_id not in sessions:
                sessions[clean_session_id] = []
            history = sessions[clean_session_id]

        # Llamada al pipeline RAG con historial
        result = ask(clean_query, history=history)

        # Actualizar historial
        if clean_session_id:
            sessions[clean_session_id].append({"role": "user", "text": clean_query})
            sessions[clean_session_id].append({"role": "model", "text": result["respuesta"]})
            # Mantener solo los últimos N mensajes
            if len(sessions[clean_session_id]) > MAX_HISTORY_LENGTH:
                sessions[clean_session_id] = sessions[clean_session_id][-MAX_HISTORY_LENGTH:]

        return ChatResponse(
            respuesta=result["respuesta"],
            fuentes=result["fuentes"],
            categoria=result["categoria"],
            categorias=result.get("categorias", [result["categoria"]]),
            session_id=clean_session_id,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error en /chat: {exc}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")


@app.get("/categorias")
async def get_categorias():
    return {"categorias": list(VALID_CATEGORIES)}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "BravoBot API"}


# --- TELEGRAM WEBHOOK ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("CRÍTICO: TELEGRAM_BOT_TOKEN no encontrado en las variables de entorno.")
else:
    logger.info(f"TELEGRAM_BOT_TOKEN cargado (comienza por {TELEGRAM_BOT_TOKEN[:5]}...)")

@app.post("/webhook/telegram")
async def telegram_webhook(update: dict):
    """
    Recibe actualizaciones de Telegram vía Webhook.
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no está configurado.")
        return {"status": "error", "message": "Token not configured"}

    # Extraer el mensaje
    message = update.get("message")
    if not message:
        return {"status": "ok"}
    
    text = message.get("text")
    chat_id = message.get("chat", {}).get("id")
    
    if not text or not chat_id:
        return {"status": "ok"}

    chat_id_str = str(chat_id)

    # Manejar el comando /start
    if text.startswith("/start"):
        respuesta = (
            "¡Hola! 👋 Soy BravoBot, tu asistente inteligente para aspirantes de la "
            "I.U. Pascual Bravo. 🎓\n\n"
            "Puedes preguntarme sobre inscripciones, programas académicos, "
            "costos, o cualquier otra duda que tengas."
        )
    else:
        # Llamar a la API interna usando la misma lógica de chat
        try:
            # Reutilizamos el historial en memoria usando chat_id como session_id
            if chat_id_str not in sessions and len(sessions) < MAX_SESSIONS:
                sessions[chat_id_str] = []
            
            history = sessions.get(chat_id_str, [])
            
            # Sanitizar
            clean_query = sanitize_query(text)
            
            # Notificar que está escribiendo (con timeout para evitar bloqueos)
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction",
                        json={"chat_id": chat_id, "action": "typing"}
                    )
            except Exception:
                pass # Si falla el typing action no es crítico

            result = ask(clean_query, history=history)
            respuesta = result["respuesta"]
            
            # Actualizar historial
            if chat_id_str in sessions:
                sessions[chat_id_str].append({"role": "user", "text": clean_query})
                sessions[chat_id_str].append({"role": "model", "text": respuesta})
                if len(sessions[chat_id_str]) > MAX_HISTORY_LENGTH:
                    sessions[chat_id_str] = sessions[chat_id_str][-MAX_HISTORY_LENGTH:]

        except Exception:
            logger.exception("Error procesando mensaje de Telegram")
            respuesta = "Lo siento, estoy teniendo problemas técnicos temporales. 🛠️ Intenta de nuevo más tarde."

    # Enviar la respuesta a Telegram
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": respuesta
                }
            )
            resp.raise_for_status()
    except Exception:
        logger.exception("Error enviando respuesta a Telegram")

    return {"status": "ok"}
