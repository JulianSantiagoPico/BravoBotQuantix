import logging
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ROUTER_MODEL = "gemini-2.5-flash"

VALID_CATEGORIES = {
    "admisiones",
    "programas",
    "costos",
    "bienestar",
    "becas",
    "institucional",
    "noticias",
    "general",
}

ROUTER_PROMPT = """Clasifica la siguiente pregunta de un aspirante universitario en UNA de estas categorías:
- admisiones: preguntas sobre inscripción, fechas, requisitos, proceso de admisión, calendario académico
- programas: preguntas sobre carreras, programas académicos, mallas curriculares, posgrados, maestrías
- costos: preguntas sobre matrículas, derechos pecuniarios, precios, pagos
- bienestar: preguntas sobre servicios, prácticas, inglés, bienestar universitario
- becas: preguntas sobre becas, financiamiento, apoyo socioeconómico
- institucional: preguntas sobre la institución, historia, filosofía, acreditación
- noticias: preguntas sobre novedades, eventos recientes
- general: cualquier otra pregunta

Responde ÚNICAMENTE con la etiqueta de la categoría, sin explicación adicional.

Pregunta: {query}"""


def classify_query(query: str) -> str:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=ROUTER_MODEL,
            contents=ROUTER_PROMPT.format(query=query),
        )
        categoria = response.text.strip().lower().replace(".", "").replace(":", "")
        if categoria not in VALID_CATEGORIES:
            logger.warning(f"Categoría desconocida '{categoria}', usando 'general'")
            return "general"
        return categoria
    except Exception as exc:
        logger.error(f"Error en router: {exc}")
        return "general"
