# Settings for the EETT extractor

# Export settings
__all__ = [
    'DEFAULT_MODEL',
    'DEFAULT_PROMPT_PATH',
    'DEFAULT_FILE_PATH',
    'DENSE_EMBEDDINGS_MODEL',
    'DENSE_EMBEDDINGS_DIMENSION',
    'SPARSE_EMBEDDINGS_MODEL',
    'QDRANT_COLLECTION_URL',
    'QDRANT_API_KEY'
]


# Model settings
DEFAULT_MODEL = "gpt-4o-mini"
DENSE_EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DENSE_EMBEDDINGS_DIMENSION = 768
SPARSE_EMBEDDINGS_MODEL = "Qdrant/bm25"

# File paths
DEFAULT_PROMPT_PATH = "src/prompts/extraction_prompt copy.md"
DEFAULT_FILE_PATH = "EETT Infranormativo JI Los Palomos_rev02_normativo-print.pdf"

# Qdrant settings
QDRANT_COLLECTION_URL = "https://2abb314c-18b3-48ed-8bb3-4594a30c6ca1.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "K8337dWIuSN6dOr1t8HYQH0MU0mctqqJSzcF306eSuJzHLUvsSxZew"
