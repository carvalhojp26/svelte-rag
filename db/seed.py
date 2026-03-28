import json
import os
import requests
import psycopg2
from pgvector.psycopg2 import register_vector
from pathlib import Path

DB_URL = os.getenv("DATABASE_URL", "postgresql://svelte:svelte@localhost:5432/svelte-rag")
CHUNKS = Path(__file__).resolve().parent.parent / "scraper/output/chunks.json"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

def get_conn():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn

MAX_CHARS = 4000  # nomic-embed-text has a ~512 token limit, ~4000 chars is safe

def embed(text: str) -> list[float]:
    truncated = text[:MAX_CHARS]
    resp = requests.post(OLLAMA_URL, json={
        "model": EMBED_MODEL,
        "prompt": truncated
    })
    if not resp.ok:
        print(f"  Warning: embedding failed, retrying with shorter text...")
        truncated = text[:2000]
        resp = requests.post(OLLAMA_URL, json={
            "model": EMBED_MODEL,
            "prompt": truncated
        })
    resp.raise_for_status()
    return resp.json()["embedding"]
    
def seed():
    with open(CHUNKS, encoding="utf-8") as f:
        chunks = json.load(f)

    conn = get_conn()
    cur = conn.cursor()

    # Find already-embedded chunks
    cur.execute("SELECT chunk_id FROM documents WHERE embedding IS NOT NULL")
    done = {row[0] for row in cur.fetchall()}
    remaining = [c for c in chunks if c["id"] not in done]
    print(f"Seeding {len(remaining)} chunks (skipping {len(done)} already done)...")

    for i, chunk in enumerate(remaining):
        embedding = embed(chunk["content"])
        cur.execute("""
            INSERT INTO documents (chunk_id, url, page, section, level, content, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id) DO UPDATE SET embedding = EXCLUDED.embedding
        """, (
            chunk["id"], chunk["url"], chunk["page"],
            chunk["section"], chunk["level"], chunk["content"], embedding,
        ))

        if (i + 1) % 50 == 0:
            conn.commit()
            print(f"  {i + 1}/{len(remaining)}")

    conn.commit()
    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    seed()