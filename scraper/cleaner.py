# cleaner.py
import json
import re
from pathlib import Path

INPUT  = Path(__file__).resolve().parent / "output/docs.json"
OUTPUT = Path(__file__).resolve().parent / "output/chunks.json"

def clean_code(code: str) -> str:
    # Remove the mangled type annotation noise from the scraper
    # e.g. "importdefineAddondefineAddon" -> keep only actual code lines
    lines = code.splitlines()
    clean = []
    for line in lines:
        # Skip lines that are pure type-hover artifacts (no spaces, camelCase run-ons)
        if re.match(r'^[a-z]+[A-Z][a-zA-Z]+[a-z]+[A-Z]', line.strip()):
            continue
        clean.append(line)
    return "\n".join(clean).strip()

def make_chunks(docs: list[dict]) -> list[dict]:
    chunks = []

    for doc in docs:
        url   = doc["url"]
        title = doc["title"]

        for section in doc["sections"]:
            # Skip empty sections (navigation artifacts)
            if not section["paragraphs"] and not section["code_blocks"]:
                continue

            parts = []

            # Add section heading as context at the top of the chunk
            if section["title"]:
                parts.append(f"# {section['title']}")

            parts.extend(section["paragraphs"])

            for code in section["code_blocks"]:
                cleaned = clean_code(code)
                if cleaned:
                    parts.append(f"```\n{cleaned}\n```")

            content = "\n\n".join(parts).strip()
            if not content:
                continue

            chunks.append({
                "id":      f"{url}#{section['id']}" if section["id"] else url,
                "url":     url,
                "page":    title,
                "section": section["title"],
                "level":   section["level"],
                "content": content,
            })

    return chunks

def main():
    with open(INPUT, encoding="utf-8") as f:
        docs = json.load(f)

    chunks = make_chunks(docs)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(chunks)} chunks from {len(docs)} pages -> {OUTPUT}")

    # Quick sanity check
    print("\nSample chunk:")
    print(json.dumps(chunks[0], indent=2))

if __name__ == "__main__":
    main()