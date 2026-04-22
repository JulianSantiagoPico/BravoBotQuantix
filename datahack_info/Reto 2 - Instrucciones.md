## **Reto 2: BravoBot, Asistente Inteligente Universitario**

## **Contexto**

Cada semestre, cientos de aspirantes buscan información detallada sobre la oferta académica, procesos de admisión, requisitos, costos y beneficios de estudiar en la **Institución Universitaria Pascual Bravo**. Navegar por un sitio web institucional para encontrar un dato muy específico puede tomar tiempo. ¿Qué pasaría si los aspirantes tuvieran a su disposición un asistente inteligente, disponible 24/7, capaz de responder cualquier duda en segundos basándose **exclusivamente** en la información oficial?

### **Objetivo Principal**

Desarrollar un agente conversacional (chatbot) utilizando la arquitectura **RAG (Retrieval-Augmented Generation)**. El sistema debe alimentarse de los datos extraídos mediante *web scraping* del sitio web oficial de la I.U. Pascual Bravo y servir como un guía preciso para los futuros estudiantes.

### **Requisitos Técnicos y Fases del Reto**

El proyecto debe contemplar las siguientes fases:

1. **Ingesta de Datos (Web Scraping):**  
   * Diseñar un pipeline automatizado para raspar (scrape) la información pública del sitio web oficial (pascualbravo.edu.co).  
   * **Foco de los datos:** Oferta académica (pregrados, posgrados, tecnologías), fechas de inscripción, costos, perfiles ocupacionales y requisitos de admisión.  
2. **Procesamiento y Almacenamiento (Bases de Datos Vectoriales):**  
   * Limpiar y estructurar el texto extraído.  
   * Aplicar técnicas de *chunking* (división de texto) y generar los *embeddings* correspondientes.  
   * Almacenar los vectores en una base de datos vectorial (ChromaDB, Pinecone, FAISS, Qdrant).  
3. **Generación de Respuestas (Integración LLM):**  
   * Conectar la base de datos vectorial con un Modelo de Lenguaje Grande (LLM) a elección (OpenAI, Gemini, Llama 3, Claude, etc.).  
   * Diseñar un *System Prompt* robusto para que el agente tenga un tono amable, institucional y, lo más importante, no alucine. Si la información no está en el sitio web, el bot debe indicarlo claramente.  
4. **Interfaz de Usuario (UX/UI):**  
   * Crear una interfaz sencilla y funcional donde los usuarios puedan chatear con el agente. Pueden usar frameworks rápidos como Streamlit, Gradio, o desarrollar un frontend personalizado.

### **Entregables Esperados**

Al finalizar el hackathon, los equipos deberán entregar:

1. **Repositorio de Código Público:** (GitHub/GitLab) con instrucciones claras en el README.md sobre cómo ejecutar el proyecto localmente.  
2. **Demo Funcional:** Un enlace al chatbot desplegado y funcionando en la nube (Hugging Face Spaces, Render, Vercel).  
3. **Pitch de 3 minutos:** Una presentación rápida demostrando cómo un usuario interactúa con el bot realizando preguntas complejas.