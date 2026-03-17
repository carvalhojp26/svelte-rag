import ollama
import re
from pathlib import Path

models = ["gemma3:latest", "deepseek-r1:1.5b", "codellama:latest"]
questions = [
    "Write a Svelte 5 counter: Increment button, count display, and decrement button.",
    "Write a Svelte 5 layout.",
    "Write a Svelte 5 component using Runes.",
]

OUTPUTS_DIR = Path(__file__).resolve().parent / "outputs"


def extract_svelte_code(text: str) -> str | None:
    """Extract .svelte code from markdown blocks or raw text."""
    if not text or not text.strip():
        return None
    match = re.search(r"```(?:svelte)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    stripped = text.strip()
    if stripped.startswith("<script") or stripped.startswith("<"):
        return stripped
    return None


def main() -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)

    for model in models:
        model_dir = OUTPUTS_DIR / model.replace(":", "_")
        model_dir.mkdir(exist_ok=True)

        for i, question in enumerate(questions, start=1):
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
            raw = response["message"]["content"]
            code = extract_svelte_code(raw)
            content = code if code else raw

            svelte_path = model_dir / f"q{i}.svelte"
            svelte_path.write_text(content, encoding="utf-8")
            print(f"Wrote {svelte_path.resolve()}")


if __name__ == "__main__":
    main()
