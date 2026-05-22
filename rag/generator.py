import os
from groq import Groq
from dotenv import load_dotenv
from rag.retrieval import retrieve, rerank

load_dotenv()

RAG_MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def ask(question: str) -> str:
    chunks = retrieve(question)
    chunks = rerank(question, chunks)
    context = "\n\n---\n\n".join(
        f"Source: {c['page']} > {c['section']}\n{c['content']}"
        for c in chunks
    )

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

    return resp.choices[0].message.content