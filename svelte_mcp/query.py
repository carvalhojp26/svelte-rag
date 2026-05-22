import os
import asyncio
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
load_dotenv()

MCP_MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# SECTION_MAP and FALLBACK_SECTIONS without changes
SECTION_MAP = [
    (["reactive", "state", "$state", "variable"],       ["svelte/$state", "svelte/what-are-runes"]),
    (["derived", "$derived", "computed", "calculated"], ["svelte/$derived", "svelte/$state"]),
    (["effect", "$effect", "side effect", "timer"],     ["svelte/$effect"]),
    (["props", "$props", "component", "passing data"],  ["svelte/$props", "svelte/basic-markup"]),
    (["lifecycle", "onmount", "ondestroy", "mount"],    ["svelte/lifecycle-hooks"]),
    (["store", "stores", "writable", "readable"],       ["svelte/svelte-store", "svelte/stores"]),
    (["bind", "binding", "two-way"],                    ["svelte/bind", "svelte/$bindable"]),
    (["form", "submit", "input", "validation"],         ["kit/form-actions", "svelte/bind"]),
    (["routing", "route", "navigation", "page"],        ["kit/routing", "kit/load"]),
    (["transition", "animation", "animate"],            ["svelte/transition", "svelte/svelte-transition"]),
    (["context", "setcontext", "getcontext"],           ["svelte/context"]),
    (["snippet", "slot", "render"],                     ["svelte/snippet", "svelte/@render"]),
    (["typescript", "types", "type safety"],            ["svelte/typescript", "kit/types"]),
    (["sveltekit", "kit", "load function", "ssr"],      ["kit/introduction", "kit/load"]),
]

FALLBACK_SECTIONS = ["svelte/overview", "svelte/what-are-runes"]


def pick_sections(topic: str) -> list[str]:
    topic_lower = topic.lower()
    matched = []
    for keywords, paths in SECTION_MAP:
        if any(kw in topic_lower for kw in keywords):
            matched.extend(paths)
    seen = set()
    result = []
    for p in matched:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result[:4] if result else FALLBACK_SECTIONS


async def fetch_svelte_docs(topic: str) -> str:
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@sveltejs/mcp"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            sections = pick_sections(topic)
            print(f"[MCP] Sections selected: {sections}")

            docs = await session.call_tool("get-documentation", {"section": sections})

            result_text = docs.content[0].text
            print(f"[MCP] Tokens received: {len(result_text)} chars")
            print(f"[MCP] Preview: {result_text[:300]}")
            return result_text


def ask_mcp(question: str) -> str:
    print(f"\n[MCP] Starting fetch for: '{question}'")
    context = asyncio.run(fetch_svelte_docs(question))

    print(f"[MCP] Sending prompt to model '{MCP_MODEL}'...")
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
    print(f"[MCP] Response received ({len(answer)} chars)")
    return answer