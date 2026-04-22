import logging

from .router import classify_query
from .retriever import retrieve
from .generator import generate_response

logger = logging.getLogger(__name__)


def ask(query: str) -> dict:
    logger.info(f"Query recibida: {query!r}")

    categoria = classify_query(query)
    logger.info(f"Categoría clasificada: {categoria}")

    chunks = retrieve(query, categoria)
    logger.info(f"Chunks recuperados: {len(chunks)}")

    result = generate_response(query, chunks)

    return {
        "respuesta": result["respuesta"],
        "fuentes": result["fuentes"],
        "categoria": categoria,
    }
