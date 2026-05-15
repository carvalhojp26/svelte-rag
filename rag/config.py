import os

DB_URL     = os.getenv("DATABASE_URL", "postgresql://svelte:svelte@localhost:5432/svelte-rag")
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.1:8b"
TOP_K       = 30
RERANK_TOP_K = 3
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"