import os
import time
from groq import Groq
from dotenv import load_dotenv
from rag.retrieval import retrieve, rerank

load_dotenv()

RAG_MODEL = "llama-3.1-8b-instant"
client = Groq(api_key=os.environ["GROQ_API_KEY"])


def ask(question: str) -> tuple[str, list[dict]]:
    logs = []

    # Step 1: Retrieve
    t = time.time()
    chunks = retrieve(question)
    logs.append({
        "step": "retrieve",
        "chunks_found": len(chunks),
        "latency_s": round(time.time() - t, 2)
    })

    # Step 2: Rerank
    t = time.time()
    chunks = rerank(question, chunks)
    logs.append({
        "step": "rerank",
        "chunks_kept": len(chunks),
        "top_sources": [f"{c['page']} > {c['section']}" for c in chunks[:3]],
        "latency_s": round(time.time() - t, 2)
    })

    # Step 3: Build context
    context = "\n\n---\n\n".join(
        f"Source: {c['page']} > {c['section']}\n{c['content']}"
        for c in chunks
    )
    logs.append({
        "step": "build_context",
        "context_chars": len(context),
    })

    # Step 4: Generate
    t = time.time()
    resp = client.chat.completions.create(
        model=RAG_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a Svelte documentation assistant. Answer questions using ONLY the documentation excerpts provided. Include code examples when available. If the question is not covered in the excerpts, say so clearly."
            },
            {
                "role": "user",
                "content": f"Documentation excerpts:\n{context}\n\nQuestion: {question}\n\nGive a thorough answer that covers all relevant aspects found in the excerpts above:"
            }
        ],
        temperature=0.2,
    )
    answer = resp.choices[0].message.content
    logs.append({
        "step": "generate",
        "model": RAG_MODEL,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "answer_chars": len(answer),
        "latency_s": round(time.time() - t, 2)
    })

    return answer, logs