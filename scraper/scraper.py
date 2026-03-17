import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
USER_AGENT = "SvelteRAG-Scraper/1.0 (https://github.com/svelte-rag)"


def fetch(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_sections(soup: BeautifulSoup) -> list[dict]:
    container = soup.find("main") or soup.find("article") or soup.body
    if not container:
        return []

    sections = []
    current = None
    current_paragraphs = []
    current_code_blocks = []

    def flush_section():
        nonlocal current, current_paragraphs, current_code_blocks
        if current is None:
            return
        sections.append({
            "id": current.get("id", ""),
            "title": current.get_text(strip=True),
            "level": int(current.name[1]),
            "paragraphs": current_paragraphs,
            "code_blocks": current_code_blocks,
        })
        current_paragraphs = []
        current_code_blocks = []

    for tag in container.find_all(["h2", "h3", "p", "pre"]):
        if tag.name in ("h2", "h3"):
            flush_section()
            current = tag
        elif current is not None:
            if tag.name == "p":
                text = tag.get_text(separator=" ", strip=True)
                if text:
                    current_paragraphs.append(text)
            elif tag.name == "pre":
                code = tag.find("code")
                if code:
                    current_code_blocks.append(code.get_text(strip=True))

    flush_section()
    return sections


def scrape_page(url: str) -> dict:
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)

    sections = extract_sections(soup)

    return {
        "url": url,
        "title": title,
        "sections": sections,
    }


def main() -> None:
    urls_file = OUTPUT_DIR / "urls.json"
    if not urls_file.exists():
        print("Run 'python crawler.py' first to generate urls.json")
        return

    with open(urls_file, encoding="utf-8") as f:
        urls = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    docs: list[dict] = []
    failed: list[str] = []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            data = scrape_page(url)
            docs.append(data)
        except Exception as e:
            print(f"  Failed: {e}")
            failed.append(url)
        time.sleep(1)

    out_file = OUTPUT_DIR / "docs.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f"Done. Scraped {len(docs)} pages -> {out_file}")
    if failed:
        print(f"Failed {len(failed)} URLs -> {OUTPUT_DIR / 'failed.json'}")
        with open(OUTPUT_DIR / "failed.json", "w", encoding="utf-8") as f:
            json.dump(failed, f, indent=2)


if __name__ == "__main__":
    main()
