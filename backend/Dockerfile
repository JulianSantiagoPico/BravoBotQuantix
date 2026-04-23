# ─────────────────────────────────────────────────────────────────
# Backend Dockerfile — Python 3.11 + FastAPI + uvicorn
# ─────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# Evitar archivos .pyc y buffering de stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Hugging Face Spaces requiere un usuario no-root (uid 1000)
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Cambiar permisos del directorio de trabajo
RUN chown -R user:user /app

# Instalar dependencias del sistema necesarias para sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python primero (aprovecha cache de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente del backend (con permisos)
COPY --chown=user:user . .

# Cambiar al usuario no-root
USER user

# Puerto de la API para Hugging Face Spaces
EXPOSE 7860

# Iniciar uvicorn apuntando al app FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
