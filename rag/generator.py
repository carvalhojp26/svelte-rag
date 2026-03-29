import requests
from rag.config import OLLAMA_URL, CHAT_MODEL
from rag.retrieval import retrieve, rerank

def ask(question: str) -> str:
    chunks = retrieve(question)
    chunks = rerank(question, chunks)
    context = "\n\n---\n\n".join(
        f"Source: {c['page']} > {c['section']}\n{c['content']}"
        for c in chunks
    )
    prompt = f"""You are a Svelte documentation assistant. Answer the question using ONLY the excerpts below. Include code examples when available. If the question is not covered in the excerpts, say so clearly.

Documentation excerpts:
{context}

Question: {question}

Give a thorough answer that covers all relevant aspects found in the excerpts above:"""
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": CHAT_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 8192
        }
    })
    resp.raise_for_status()
    return resp.json()["response"]