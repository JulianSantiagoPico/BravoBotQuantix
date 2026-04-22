import logging
import os

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

logger = logging.getLogger(__name__)

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "bravobot")
TOP_K = int(os.getenv("TOP_K", "5"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

_model: SentenceTransformer | None = None
_collection: chromadb.Collection | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Cargando modelo de embeddings: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        _collection = chroma_client.get_collection(COLLECTION_NAME)
        logger.info(f"ChromaDB cargado: colección '{COLLECTION_NAME}'")
    return _collection


def retrieve(query: str, categoria: str, top_k: int = TOP_K) -> list[dict]:
    try:
        model = _get_model()
        query_embedding = model.encode([query], show_progress_bar=False)[0].tolist()
    except Exception as exc:
        logger.error(f"Error generando embedding de la query: {exc}")
        return []

    try:
        collection = get_collection()

        where_filter = None
        if categoria and categoria != "general":
            where_filter = {"categoria": {"$eq": categoria}}

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        chunks = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, dists):
            chunks.append(
                {
                    "texto": doc,
                    "url": meta.get("url", ""),
                    "categoria": meta.get("categoria", ""),
                    "score": round(1 - dist, 4),
                }
            )

        return chunks

    except Exception as exc:
        logger.error(f"Error en retrieval: {exc}")
        return []
