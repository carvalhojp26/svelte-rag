import os

DB_URL     = os.getenv("DATABASE_URL", "postgresql://svelte:svelte@localhost:5432/svelte-rag")
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "gemma3"
TOP_K       = 10
RERANK_TOP_K = 3
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"