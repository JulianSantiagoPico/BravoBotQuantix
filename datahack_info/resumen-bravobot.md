# BravoBot — Resumen Técnico del Proyecto

El proyecto consiste en desarrollar un asistente conversacional inteligente orientado a aspirantes de la Institución Universitaria Pascual Bravo, cuyo objetivo es brindar respuestas rápidas, precisas y confiables sobre la oferta académica, procesos de admisión, costos, becas y demás información institucional relevante.

Para lograrlo, se implementa una arquitectura basada en **RAG (Retrieval-Augmented Generation)**, alimentada exclusivamente con información oficial obtenida mediante un proceso de web scraping controlado sobre un conjunto estratégico de páginas clave, garantizando así la veracidad de las respuestas.

---

## 1. Ingesta de Datos (Web Scraping)

Se implementa un pipeline mixto de scraping sobre aproximadamente 25 URLs priorizadas del sitio oficial, organizado en dos estrategias:

- **Scraper estático (requests + BeautifulSoup):** para páginas con contenido HTML directo como costos, calendario académico, preguntas frecuentes e información institucional.
- **Scraper dinámico (Playwright):** para páginas que renderizan contenido con JavaScript, especialmente programas académicos por facultad.

Las URLs se agrupan en categorías clave: **admisiones, programas, costos, bienestar/becas e institucional**, además de una categoría de **noticias**, utilizada para mantener información actualizada dentro del sistema.

---

## 2. Procesamiento y Almacenamiento
El contenido extraído es limpiado y segmentado mediante técnicas de *chunking* con tamaño y solapamiento controlado. Posteriormente, se generan embeddings que se almacenan en **ChromaDB** junto con metadata estructurada (categoría, fuente, URL).

Este enfoque                                         permite:
- Mejorar la precisión del retrieval
- Reducir ruido en las consultas
- Facilitar trazabilidad de la información

---

## 3. Generación de Respuestas (RAG Inteligente)
El sistema implementa un flujo optimizado en tres     etapas:

1. **Clasificación de la consulta (Query Routing):**
Se utiliza un prompt ligero con Gemini para identificar la categoría de la pregunta (admisiones, costos, programas, bienestar, etc.), retornando únicamente una etiqueta.

2. **Retrieval filtrado por metadata:**
Se realiza una búsqueda semántica en ChromaDB filtrada por la categoría detectada, lo que permite simular un enfoque multi-agente de forma eficiente y mejorar significativamente la relevancia de los resultados.

3. **Generación controlada de respuesta:**
Los fragmentos recuperados se envían como contexto al modelo, junto con un *system prompt* diseñado para:
- Evitar alucinaciones
- Restringir respuestas únicamente a la información disponible
- Comunicar explícitamente cuando no se encuentra información relevante

---

## 4. Interfaz de Usuario

Se desarrolla una interfaz tipo chatbot mediante **Streamlit**, simulando la integración del asistente dentro del sitio web institucional.

La interfaz                                                    incluye:
- Chat interactivo en tiempo real
- Visualización de fuentes utilizadas en cada respuesta
- Sección de noticias recientes obtenidas mediante scraping

---

## Diferenciadores Clave (Extras del Proyecto)

El sistema incorpora funcionalidades adicionales orientadas a mejorar la confiabilidad, experiencia de usuario y calidad de las respuestas:

### 1. Mecanismo Anti-Alucinación
El modelo está estrictamente condicionado a responder únicamente con base en el contexto recuperado. En caso de no encontrar información suficiente, el sistema responde de forma transparente, evitando respuestas incorrectas o inventadas.

### 2. Enfoque “Multi-Agente Simulado”
Aunque se implementa un único agente, el sistema utiliza clasificación de consultas y filtrado por metadata para emular múltiples expertos especializados (admisiones, costos, programas), mejorando la precisión sin aumentar la complejidad arquitectónica.

### 3. Trazabilidad de Respuestas
Cada respuesta incluye las fuentes utilizadas (URLs oficiales), permitiendo al usuario verificar la información y aumentando la confianza en el sistema.

### 4. Módulo de Actualización de Noticias
Se integra una sección de novedades que                       permite:
- Consultar información reciente del sitio institucional
- Evidenciar la vigencia del contenido
- Sentar bases para futuras notificaciones de cambios

---

## Cierre

Este enfoque prioriza la calidad de las respuestas, la confiabilidad del sistema y la experiencia del usuario, sobre la complejidad técnica innecesaria, lo cual resulta clave en el contexto de un hackathon. La combinación de un corpus curado, técnicas de retrieval optimizadas y mecanismos de control de generación permite construir un asistente robusto, escalable y alineado con necesidades reales de los aspirantes.