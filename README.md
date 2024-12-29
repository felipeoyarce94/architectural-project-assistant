# Asistente de Proyectos de Arquitectura

El asistente de proyectos de arquitectura es una herramienta que permite a los arquitectos optimizar el proceso
de estudio de antecedentes, formulación del proyecto y propuesta económica. Se encarga de ayudarte en el
papeleo y revisión de los documentos, para que tú puedas concentrarte en lo que realmente importa, la arquitectura.

## Setup

1. Clonar el repositorio
2. Instalar [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Crear `.venv` ejecutando `uv venv`
4. Activar entorno virtual ejecutando `source .venv/bin/activate`
5. Instalar dependencias ejecutando `uv sync`
6. Crear archivo `.streamlit/secrets.toml` con el siguiente contenido:

```
OPENAI_API_KEY = "sk-..."
```

7. Levantar el asistente en streamlit ejecutando `streamlit run chatbot_ui.py`
