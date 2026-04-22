# BravoBot — Asistente Inteligente I.U. Pascual Bravo

Chatbot RAG (Retrieval-Augmented Generation) para aspirantes de la Institución Universitaria Pascual Bravo. Responde preguntas sobre programas académicos, admisiones, costos y bienestar usando exclusivamente información oficial del sitio web institucional.

## Stack

| Capa | Tecnología |
|------|-----------|
| Scraping | `requests` + `BeautifulSoup4` + `Playwright` |
| PDFs | `pdfplumber` |
| Embeddings | `google-genai` → `text-embedding-004` |
| Vector DB | `ChromaDB` (local) |
| LLM | `google-genai` → `gemini-2.5-flash` |
| Backend | `FastAPI` + `uvicorn` |
| Frontend | React + Vite + TailwindCSS |

---

## Requisitos Previos

- Python 3.11+
- Node.js 18+
- Cuenta de Google AI Studio con API key de Gemini

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd BravoBot
```

### 2. Backend — Python

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

### 4. Frontend — Node

```bash
cd ../frontend
npm install
```

---

## Uso

### Paso 1 — Ejecutar la ingesta de datos (scraping + indexado)

Desde la raíz del proyecto:

```bash
# Primera vez (o para regenerar todo desde cero):
python run_ingestion.py --reset

# Actualizar datos sin borrar el índice:
python run_ingestion.py

# Solo scraping (sin indexar):
python run_ingestion.py --scrape-only

# Solo indexar (si ya tienes raw_pages.json):
python run_ingestion.py --index-only
```

> **Nota:** El scraping completo puede tomar varios minutos por el uso de Playwright para páginas dinámicas.

### Paso 2 — Iniciar el backend API

```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

Documentación interactiva disponible en: http://localhost:8000/docs

### Paso 3 — Iniciar el frontend

```bash
cd frontend
npm run dev
```

Abrir en el navegador: http://localhost:5173

---

## Estructura del Proyecto

```
BravoBot/
├── backend/
│   ├── scraper/
│   │   ├── urls.py              # Lista de URLs con metadata
│   │   ├── static_scraper.py   # Scraper con requests + BS4
│   │   ├── dynamic_scraper.py  # Scraper con Playwright
│   │   └── pdf_extractor.py    # Extracción de texto de PDFs
│   ├── ingestion/
│   │   ├── cleaner.py          # Limpieza de texto
│   │   ├── chunker.py          # División en chunks
│   │   └── embedder.py         # Embeddings + carga a ChromaDB
│   ├── rag/
│   │   ├── router.py           # Clasificación de categoría
│   │   ├── retriever.py        # Búsqueda semántica en ChromaDB
│   │   ├── generator.py        # Generación de respuesta con Gemini
│   │   └── pipeline.py         # Orquestador RAG
│   ├── api/
│   │   └── main.py             # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── App.tsx
│       └── components/
│           ├── ChatWindow.tsx
│           ├── MessageBubble.tsx
│           ├── SourcesList.tsx
│           └── InputBar.tsx
└── run_ingestion.py            # Script principal de ingesta
```

---

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | API key de Google AI Studio | — |
| `CHROMA_PERSIST_DIR` | Directorio de persistencia ChromaDB | `./chroma_db` |
| `COLLECTION_NAME` | Nombre de la colección ChromaDB | `bravobot` |
| `CHUNK_SIZE` | Tamaño de chunks en caracteres | `500` |
| `CHUNK_OVERLAP` | Overlap entre chunks | `50` |
| `TOP_K` | Número de chunks a recuperar por query | `5` |
