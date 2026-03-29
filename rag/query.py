import sys
from rag.retrieval import retrieve, rerank
from rag.generator import ask

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if not question:
        print("Usage: python -m rag.query <your question>")
        sys.exit(1)

    print(f"\nQuestion: {question}")
    print("\nRetrieving relevant chunks...")
    chunks = retrieve(question)
    reranked = rerank(question, chunks)
    for i, c in enumerate(reranked, 1):
        print(f"  {i}. [{c['similarity']}] {c['page']} > {c['section']}")
    print("\nGenerating answer...\n")
    answer = ask(question)
    print(f"Answer:\n{answer}")