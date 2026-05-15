import json
import re
from pathlib import Path

INPUT  = Path(__file__).resolve().parent / "output/docs.json"
OUTPUT = Path(__file__).resolve().parent / "output/chunks.json"

CHUNK_SIZE = 1500
OVERLAP    = 200


def is_noise_block(code: str) -> bool:
    """Detect TypeScript hover tooltip noise — no real whitespace, dense type signatures."""
    if len(code) < 50:
        return False
    # Real code has spaces and newlines; noise is one dense line
    lines = code.splitlines()
    if len(lines) <= 2:
        # Single/double line — check if it's dense type signature noise
        space_ratio = code.count(" ") / len(code)
        if space_ratio < 0.05:  # less than 5% spaces = noise
            return True
    return False

def clean_code(code: str) -> str:
    lines = code.splitlines()
    clean = []
    for line in lines:
        if re.match(r'^[a-z]+[A-Z][a-zA-Z]+[a-z]+[A-Z]', line.strip()):
            continue
        clean.append(line)
    return "\n".join(clean).strip()


def split_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Splits text into overlapping chunks.
    Tries to break on paragraph boundaries (\n\n) when possible,
    falling back to hard splits if needed.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            # Last chunk — take everything remaining
            chunks.append(text[start:].strip())
            break

        # Try to find a clean paragraph break near the end of the window
        split_pos = text.rfind("\n\n", start, end)

        if split_pos == -1 or split_pos <= start:
            # No paragraph break found — try a newline
            split_pos = text.rfind("\n", start, end)

        if split_pos == -1 or split_pos <= start:
            # No newline either — hard split at chunk_size
            split_pos = end

        chunks.append(text[start:split_pos].strip())

        # Next chunk starts overlap characters before the split point
        start = max(start + 1, split_pos - overlap)

    return [c for c in chunks if c]


def make_chunks(docs: list[dict]) -> list[dict]:
    chunks = []

    for doc in docs:
        url   = doc["url"]
        title = doc["title"]

        for section in doc["sections"]:
            if not section["paragraphs"] and not section["code_blocks"]:
                continue

            parts = []
            if section["title"]:
                parts.append(f"# {section['title']}")
            parts.extend(section["paragraphs"])

            for code in section["code_blocks"]:
                if is_noise_block(code):
                    continue
                cleaned = clean_code(code)
                if cleaned:
                    parts.append(f"```\n{cleaned}\n```")

            content = "\n\n".join(parts).strip()
            if not content:
                continue

            base_id = f"{url}#{section['id']}" if section["id"] else url

            # Split into overlapping chunks if the section is long
            sub_chunks = split_with_overlap(content, CHUNK_SIZE, OVERLAP)

            for i, sub_content in enumerate(sub_chunks):
                chunks.append({
                    # Append chunk index so each ID stays unique
                    "id":          f"{base_id}__chunk{i}" if len(sub_chunks) > 1 else base_id,
                    "url":         url,
                    "page":        title,
                    "section":     section["title"],
                    "level":       section["level"],
                    "chunk_index": i,
                    "chunk_total": len(sub_chunks),
                    "content":     sub_content,
                })

    return chunks


def main():
    with open(INPUT, encoding="utf-8") as f:
        docs = json.load(f)

    chunks = make_chunks(docs)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(chunks)} chunks from {len(docs)} pages -> {OUTPUT}")

    multi = [c for c in chunks if c["chunk_total"] > 1]
    print(f"Sections split into sub-chunks: {len(multi)}")
    print(f"Chunk size: {CHUNK_SIZE} chars | Overlap: {OVERLAP} chars")
    print("\nSample chunk:")
    print(json.dumps(chunks[0], indent=2))

if __name__ == "__main__":
    main()