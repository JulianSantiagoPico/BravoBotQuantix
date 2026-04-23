import logging
import os
import re
import uuid
from pathlib import Path
from urllib.parse import urlparse

from pinecone import Pinecone
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from .cleaner import clean_text
from .chunker import chunk_text

load_dotenv()

logger = logging.getLogger(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "bravobot")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

_model: SentenceTransformer | None = None

_POSGRADO_RE = re.compile(
    r"/programas/(?:especializacion|maestria|doctorado|posgrado)",
    re.IGNORECASE,
)


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Cargando modelo de embeddings: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_index(reset: bool = False):
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY no encontrada en .env")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Asumimos que el índice ya existe (o se crea manualmente desde la web de Pinecone)
    # Dimension del modelo paraphrase-multilingual-MiniLM-L12-v2 = 384
    index = pc.Index(PINECONE_INDEX_NAME)
    
    if reset:
        try:
            index.delete(delete_all=True)
            logger.info(f"Índice '{PINECONE_INDEX_NAME}' vaciado.")
        except Exception as e:
            logger.error(f"Error vaciando índice: {e}")
            
    return index


def _extract_titulo(texto_limpio: str) -> str:
    for line in texto_limpio.split("\n"):
        stripped = line.strip()
        if len(stripped) > 10:
            return stripped[:120]
    return ""


def _extract_program_name(url: str, texto_limpio: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1]
    if not slug:
        return ""
    name = slug.replace("-", " ").replace("_", " ").title()
    return name


def _extract_level(url: str, categoria: str) -> str:
    if categoria != "programas":
        return ""
    if _POSGRADO_RE.search(url):
        return "posgrado"
    return "pregrado"


def _extract_source_type(categoria: str, tipo: str) -> str:
    if tipo == "pdf":
        return "pdf"
    if categoria == "programas":
        return "web_program"
    return "web_general"


def _extract_program_slug(url: str, categoria: str) -> str:
    if categoria != "programas":
        return ""
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1]
    return slug.replace("-", " ").replace("_", " ").lower()


def build_index(raw_pages: list[dict], reset: bool = False) -> None:
    if not raw_pages:
        logger.warning("No hay documentos para indexar.")
        return

    model = _get_model()
    index = _get_index(reset=reset)

    total_chunks = 0

    for doc in raw_pages:
        url = doc.get("url", "")
        categoria = doc.get("categoria", "general")
        texto_raw = doc.get("texto", "")
        tipo = doc.get("tipo", "web")

        if not texto_raw.strip():
            continue

        texto_limpio = clean_text(texto_raw)
        chunks = chunk_text(texto_limpio, tipo=tipo)

        if not chunks:
            continue

        titulo = _extract_titulo(texto_limpio)
        program_name = _extract_program_name(url, texto_limpio) if categoria == "programas" else ""
        level = _extract_level(url, categoria)
        source_type = _extract_source_type(categoria, tipo)
        program_slug = _extract_program_slug(url, categoria)

        logger.info(f"Indexando {len(chunks)} chunks de: {url}")

        try:
            embeddings = model.encode(chunks, show_progress_bar=False, batch_size=32).tolist()
        except Exception as exc:
            logger.error(f"Error generando embeddings para {url}: {exc}")
            continue

        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [
            {
                "url": url,
                "categoria": categoria,
                "tipo": tipo,
                "chunk_index": i,
                "titulo": titulo,
                "program_name": program_name,
                "level": level,
                "source_type": source_type,
                "program_slug": program_slug,
            }
            for i in range(len(chunks))
        ]

        # Pinecone espera diccionarios para el metadato, pero text no puede ser documento plano, hay que meterlo en metadata
        vectors_to_upsert = []
        for i, (chunk_id, emb, texto_chunk, meta) in enumerate(zip(ids, embeddings, chunks, metadatas)):
            # Pinecone usa el campo 'text' dentro de metadata para guardar el contenido
            meta["texto"] = texto_chunk
            vectors_to_upsert.append({
                "id": chunk_id,
                "values": emb,
                "metadata": meta
            })

        # Upsert en lotes (batching) es recomendable en Pinecone
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            index.upsert(vectors=batch)
            
        total_chunks += len(chunks)

    logger.info(f"\nIndexación completa. Total chunks en Pinecone: {total_chunks}")
