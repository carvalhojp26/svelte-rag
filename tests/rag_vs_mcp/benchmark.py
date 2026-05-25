import json
import time
from datetime import datetime
from rag.generator import ask
from svelte_mcp.query import ask_mcp

QUESTIONS = [
    "How do I create a reactive variable in Svelte?",
]

RAG_MODEL = "llama-3.1-8b-instant"
MCP_MODEL = "llama-3.1-8b-instant"


def run_benchmark():
    run_start = datetime.now()
    results = []
    log_entries = []

    for q in QUESTIONS:
        print(f"\nRunning: {q}")
        entry = {"question": q}
        log = {"question": q}

        # RAG
        start = time.time()
        try:
            entry["rag_answer"], rag_logs = ask(q)
            entry["rag_latency_s"] = round(time.time() - start, 2)
            log["rag"] = {"status": "ok", "latency_s": entry["rag_latency_s"], "steps": rag_logs}
        except Exception as e:
            entry["rag_answer"] = None
            entry["rag_latency_s"] = round(time.time() - start, 2)
            log["rag"] = {"status": "error", "error": str(e), "latency_s": entry["rag_latency_s"]}
        print(f"  RAG done ({entry['rag_latency_s']}s)")

        # MCP
        start = time.time()
        try:
            entry["mcp_answer"], mcp_logs = ask_mcp(q)
            entry["mcp_latency_s"] = round(time.time() - start, 2)
            log["mcp"] = {"status": "ok", "latency_s": entry["mcp_latency_s"], "steps": mcp_logs}
        except Exception as e:
            entry["mcp_answer"] = None
            entry["mcp_latency_s"] = round(time.time() - start, 2)
            log["mcp"] = {"status": "error", "error": str(e), "latency_s": entry["mcp_latency_s"]}
        print(f"  MCP done ({entry['mcp_latency_s']}s)")

        results.append(entry)
        log_entries.append(log)

    # Results file
    output = {
        "date": run_start.isoformat(),
        "rag_model": RAG_MODEL,
        "mcp_model": MCP_MODEL,
        "results": results
    }

    # Logs file
    total_rag = sum(e["rag"]["latency_s"] for e in log_entries)
    total_mcp = sum(e["mcp"]["latency_s"] for e in log_entries)
    logs = {
        "date": run_start.isoformat(),
        "duration_s": round((datetime.now() - run_start).total_seconds(), 2),
        "questions_count": len(QUESTIONS),
        "models": {"rag": RAG_MODEL, "mcp": MCP_MODEL},
        "summary": {
            "rag_total_latency_s": round(total_rag, 2),
            "mcp_total_latency_s": round(total_mcp, 2),
            "rag_avg_latency_s": round(total_rag / len(log_entries), 2),
            "mcp_avg_latency_s": round(total_mcp / len(log_entries), 2),
        },
        "questions": log_entries
    }

    timestamp = run_start.strftime('%Y%m%d_%H%M%S')
    results_file = f"tests/rag_vs_mcp/results/results_{timestamp}.json"
    logs_file = f"tests/rag_vs_mcp/results/logs_{timestamp}.json"

    with open(results_file, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    with open(logs_file, "w") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to:  {results_file}")
    print(f"Logs saved to:     {logs_file}")
    print(f"\nRAG avg: {logs['summary']['rag_avg_latency_s']}s | MCP avg: {logs['summary']['mcp_avg_latency_s']}s")


if __name__ == "__main__":
    run_benchmark()