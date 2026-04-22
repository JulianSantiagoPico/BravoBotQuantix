import logging
import os
import uuid

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from .cleaner import clean_text
from .chunker import chunk_text

load_dotenv()

logger = logging.getLogger(__name__)

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "bravobot")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Cargando modelo de embeddings: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection(reset: bool = False) -> chromadb.Collection:
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    if reset:
        try:
            chroma_client.delete_collection(COLLECTION_NAME)
            logger.info(f"Colección '{COLLECTION_NAME}' eliminada.")
        except Exception:
            pass
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def build_index(raw_pages: list[dict], reset: bool = False) -> None:
    if not raw_pages:
        logger.warning("No hay documentos para indexar.")
        return

    model = _get_model()
    collection = _get_collection(reset=reset)

    total_chunks = 0

    for doc in raw_pages:
        url = doc.get("url", "")
        categoria = doc.get("categoria", "general")
        texto_raw = doc.get("texto", "")
        tipo = doc.get("tipo", "web")

        if not texto_raw.strip():
            continue

        texto_limpio = clean_text(texto_raw)
        chunks = chunk_text(texto_limpio, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

        if not chunks:
            continue

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
            }
            for i in range(len(chunks))
        ]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        total_chunks += len(chunks)

    logger.info(f"\nIndexación completa. Total chunks en ChromaDB: {total_chunks}")
