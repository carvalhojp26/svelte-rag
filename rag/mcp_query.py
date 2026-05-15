import re
import asyncio
import requests
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rag.config import OLLAMA_URL

MCP_MODEL = "llama3.1:8b"

async def fetch_svelte_docs(topic: str) -> str:
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@upstash/context7-mcp"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            resolve = await session.call_tool("resolve-library-id", {
                "query": topic,
                "libraryName": "Svelte"
            })

            match = re.search(r'Context7-compatible library ID: (/\S+)', resolve.content[0].text)
            library_id = match.group(1) if match else "/sveltejs/svelte"
            print("LIBRARY ID:", library_id)

            docs = await session.call_tool("query-docs", {
                "libraryId": library_id,
                "query": topic
            })
            print("DOCS PREVIEW:", docs.content[0].text[:300])
            return docs.content[0].text

def ask_mcp(question: str) -> str:
    context = asyncio.run(fetch_svelte_docs(question))

    prompt = f"""You are a Svelte documentation assistant. Answer the question using ONLY the documentation below.

Documentation:
{context}

Question: {question}

Give a thorough answer:"""

    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": MCP_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 8192
        }
    })
    resp.raise_for_status()
    return resp.json()["response"]