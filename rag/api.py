from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from rag.generator import ask
from rag.retrieval import retrieve
from svelte_mcp.query import ask_mcp

MAX_QUESTION_LENGTH = 500
MIN_RELEVANCE_SIMILARITY = 0.35

OFF_TOPIC_MESSAGE = (
    "Your question doesn't appear to be related to Svelte or SvelteKit. "
    "This assistant is limited to topics about the Svelte framework."
)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_LENGTH)
    mode: str = "RAG"


def is_on_topic(question: str) -> tuple[bool, list[dict]]:
    """Check whether the question is relevant to the Svelte documentation
    by inspecting the similarity score of the closest retrieved chunk."""
    chunks = retrieve(question, top_k=5)
    best_similarity = chunks[0]["similarity"] if chunks else 0
    passed = best_similarity >= MIN_RELEVANCE_SIMILARITY
    return passed, [{
        "step": "topic_check",
        "best_similarity": best_similarity,
        "passed": passed,
    }]


@app.post("/query")
@limiter.limit("10/minute")
def query(req: QueryRequest, request: Request):
    on_topic, topic_logs = is_on_topic(req.question)
    if not on_topic:
        return {"answer": OFF_TOPIC_MESSAGE, "logs": topic_logs}

    if req.mode == "MCP":
        answer, logs = ask_mcp(req.question)
    elif req.mode == "RAG + MCP":
        rag_answer, rag_logs = ask(req.question)
        mcp_answer, mcp_logs = ask_mcp(req.question)
        answer = f"**RAG:**\n{rag_answer}\n\n**MCP:**\n{mcp_answer}"
        logs = rag_logs + mcp_logs
    else:
        answer, logs = ask(req.question)

    return {"answer": answer, "logs": topic_logs + logs}