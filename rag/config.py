import os

DB_URL      = os.getenv("DATABASE_URL", "postgresql://svelte:svelte@localhost:5432/svelte-rag")
OLLAMA_URL  = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.1:8b"
TOP_K       = 150
RERANK_TOP_K = 5
RERANK_MODEL = "ms-marco-MiniLM-L-12-v2"