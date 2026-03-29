import requests
from flashrank import Ranker, RerankRequest
from rag.config import OLLAMA_URL, EMBED_MODEL, TOP_K, RERANK_TOP_K, RERANK_MODEL
from rag.db import get_conn

reranker = Ranker(model_name=RERANK_MODEL)

def embed(text: str) -> list[float]:
    resp = requests.post(f"{OLLAMA_URL}/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text[:4000]
    })
    resp.raise_for_status()
    return resp.json()["embedding"]

def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    vec = embed(query)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT chunk_id, url, page, section, content,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (vec, vec, top_k))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "chunk_id":   row[0],
            "url":        row[1],
            "page":       row[2],
            "section":    row[3],
            "content":    row[4],
            "similarity": round(row[5], 3),
        }
        for row in rows
    ]

def rerank(query: str, chunks: list[dict], top_k: int = RERANK_TOP_K) -> list[dict]:
    passages = [{"id": i, "text": c["content"]} for i, c in enumerate(chunks)]
    request = RerankRequest(query=query, passages=passages)
    results = reranker.rerank(request)
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
    return [chunks[r["id"]] for r in ranked]