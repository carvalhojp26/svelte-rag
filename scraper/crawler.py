import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

USER_AGENT = "SvelteRAG-Scraper/1.0 (https://github.com/svelte-rag)"
DOCS_PATH = "/docs/"

def fetch(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    resp.raise_for_status()
    return resp.text


def discover_urls(base_url: str) -> set[str]:
    base = base_url.rstrip("/") + "/"
    html = fetch(base_url)
    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(base_url).netloc
    found: set[str] = set()

    nav = soup.find("nav", attrs={"aria-label": "Docs"})
    if not nav:
        return found

    sidebar = nav.find("ul", class_=lambda c: c and "sidebar" in c)
    if not sidebar:
        return found

    for a in sidebar.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith(("#", "mailto:", "javascript:")):
            continue

        full_url = urljoin(base, href)
        parsed = urlparse(full_url)

        if parsed.netloc != base_domain:
            continue
        if not parsed.path.startswith(DOCS_PATH):
            continue

        canonical = parsed._replace(fragment="").geturl()
        found.add(canonical)

    return found


if __name__ == "__main__":
    OUTPUT_DIR = Path(__file__).resolve().parent / "output"
    ROOTS = [
        "https://svelte.dev/docs/svelte",
        "https://svelte.dev/docs/kit",
        "https://svelte.dev/docs/cli",
    ]

    urls = set()
    for root in ROOTS:
        urls |= discover_urls(root)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "urls.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(sorted(urls), f, indent=2)

    print(f"Found {len(urls)} URLs -> {out_file}")
