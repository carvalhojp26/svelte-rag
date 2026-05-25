import os
import json
import time
import asyncio
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

MCP_MODEL = "llama-3.1-8b-instant"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

FALLBACK_SECTIONS = ["svelte/overview", "svelte/what-are-runes"]

def pick_sections(question: str, sections_text: str, logs: list[dict]) -> list[str]:
    # Extrair só title e path de cada secção
    compact_lines = []
    for line in sections_text.splitlines():
        if not line.startswith("- title:"):
            continue
        # Exemplo da linha:
        # - title: $state, use_cases: always, any svelte..., path: svelte/$state
        try:
            title = line.split("title:")[1].split(", use_cases:")[0].strip()
            path = line.split("path:")[1].strip()
            compact_lines.append(f"{title} -> {path}")
        except IndexError:
            continue

    compact_sections = "\n".join(compact_lines)
    print(f"[MCP] Sections list: {len(compact_sections)} chars (was {len(sections_text)})")

    t = time.time()
    resp = client.chat.completions.create(
        model=MCP_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Svelte documentation assistant. "
                    "Given a list of documentation sections and a question, "
                    "return ONLY a valid JSON object with a single key 'sections' "
                    "containing an array of the 1 most relevant section path. "
                    "Example: {\"sections\": [\"svelte/$state\", \"svelte/what-are-runes\"]}"
                )
            },
            {
                "role": "user",
                "content": f"Sections:\n{compact_sections}\n\nQuestion: {question}"
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    raw = resp.choices[0].message.content
    try:
        parsed = json.loads(raw)
        sections = parsed.get("sections", FALLBACK_SECTIONS)
        if not isinstance(sections, list) or len(sections) == 0:
            raise ValueError("Empty or invalid sections")
    except Exception as e:
        print(f"[MCP] Failed to parse sections, using fallback: {e}")
        sections = FALLBACK_SECTIONS

    logs.append({
        "step": "pick_sections",
        "sections": sections,
        "used_fallback": sections == FALLBACK_SECTIONS,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "latency_s": round(time.time() - t, 2)
    })

    return sections


async def fetch_svelte_docs(question: str) -> tuple[str, list[dict]]:
    logs = []
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@sveltejs/mcp"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Step 1: Initialize
            t = time.time()
            await session.initialize()
            logs.append({
                "step": "mcp_initialize",
                "latency_s": round(time.time() - t, 2)
            })

            # Step 2: List sections
            t = time.time()
            sections_result = await session.call_tool("list-sections", {})
            sections_text = sections_result.content[0].text
            logs.append({
                "step": "mcp_tool_call",
                "tool": "list-sections",
                "output_chars": len(sections_text),
                "is_error": sections_result.isError,
                "latency_s": round(time.time() - t, 2)
            })

            # Step 3: LLM picks relevant sections
            sections = pick_sections(question, sections_text, logs)
            print(f"[MCP] Sections selected: {sections}")

            # Step 4: Get documentation
            t = time.time()
            docs = await session.call_tool("get-documentation", {"section": sections})
            result_text = docs.content[0].text
            logs.append({
                "step": "mcp_tool_call",
                "tool": "get-documentation",
                "input": {"section": sections},
                "output_response": result_text,
                "output_chars": len(result_text),
                "is_error": docs.isError,
                "latency_s": round(time.time() - t, 2)
            })

            print(f"[MCP] Docs received: {len(result_text)} chars")
            print(f"[MCP] Preview: {result_text[:300]}")
            return result_text, logs


def ask_mcp(question: str) -> tuple[str, list[dict]]:
    logs = []

    # Step 1: Fetch docs via MCP
    t = time.time()
    context, fetch_logs = asyncio.run(fetch_svelte_docs(question))
    logs.extend(fetch_logs)
    logs.append({
        "step": "mcp_fetch_total",
        "latency_s": round(time.time() - t, 2)
    })

    # Step 2: Generate answer
    t = time.time()
    resp = client.chat.completions.create(
        model=MCP_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a Svelte documentation assistant. Answer questions using ONLY the documentation provided by the user."
            },
            {
                "role": "user",
                "content": f"Documentation:\n{context}\n\nQuestion: {question}\n\nGive a thorough answer:"
            }
        ],
        temperature=0.2,
    )
    answer = resp.choices[0].message.content
    logs.append({
        "step": "generate",
        "model": MCP_MODEL,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "answer_chars": len(answer),
        "latency_s": round(time.time() - t, 2)
    })

    print(f"[MCP] Response received ({len(answer)} chars)")
    return answer, logs