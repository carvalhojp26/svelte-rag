import json
import time
from datetime import datetime
from rag.generator import ask
from rag.mcp_query import ask_mcp

QUESTIONS = [
    "How do I create a reactive variable in Svelte?",
    "What is the difference between $state and $derived in Svelte 5?",
    #"How do I handle form submissions in SvelteKit?",
    "How do lifecycle functions work in Svelte?",
    #"How do I use stores in Svelte?",
]

def run_benchmark():
    results = []

    for q in QUESTIONS:
        print(f"\nRunning: {q}")
        entry = {"question": q}

        start = time.time()
        entry["rag_answer"] = ask(q)
        entry["rag_latency_s"] = round(time.time() - start, 2)
        print(f"  RAG done ({entry['rag_latency_s']}s)")

        start = time.time()
        entry["mcp_answer"] = ask_mcp(q)
        entry["mcp_latency_s"] = round(time.time() - start, 2)
        print(f"  MCP done ({entry['mcp_latency_s']}s)")

        results.append(entry)

    output = {
        "date": datetime.now().isoformat(),
        "rag_model": "gemma3",
        "mcp_model": "llama3.1:8b",
        "results": results
    }

    filename = f"tests/rag-mcp/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nResultados guardados em: {filename}")

if __name__ == "__main__":
    run_benchmark()