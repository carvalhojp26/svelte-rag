import os
from fastapi import FastAPI
from pydantic import BaseModel
from rag.generator import ask
from svelte_mcp.query import ask_mcp

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    mode: str = "RAG"

@app.post("/query")
def query(req: QueryRequest):
    if req.mode == "MCP":
        answer, logs = ask_mcp(req.question)
    elif req.mode == "RAG + MCP":
        rag_answer, rag_logs = ask(req.question)
        mcp_answer, mcp_logs = ask_mcp(req.question)
        answer = f"**RAG:**\n{rag_answer}\n\n**MCP:**\n{mcp_answer}"
        logs = rag_logs + mcp_logs
    else:
        answer, logs = ask(req.question)
    return {"answer": answer, "logs": logs}