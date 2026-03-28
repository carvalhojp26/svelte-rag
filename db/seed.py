import json
import os
import psycopg2
from pgvector.psycopg2 import register_vector
from pathlib import Path

DB_URL = os.getenv("DATABASE_URL", "postgresql://svelte:svelte@localhost:5432/svelte-rag")
CHUNKS = Path(__file__).resolve().parent.parent / "scraper/output/chunks.json"

def get_conn():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn

def seed():
    with open(CHUNKS, encoding="utf-8") as f:
        chunks = json.load(f)

    conn = get_conn()
    cur = conn.cursor()

    print(f"Seeding {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        cur.execute("""
            INSERT INTO documents (chunk_id, url, page, section, level, content)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id) DO NOTHING
        """, (
            chunk["id"],
            chunk["url"],
            chunk["page"],
            chunk["section"],
            chunk["level"],
            chunk["content"],
        ))
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(chunks)}")

    conn.commit()
    cur.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    seed()