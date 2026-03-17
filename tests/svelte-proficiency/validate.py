#!/usr/bin/env python3

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "template"
OUTPUTS_DIR = SCRIPT_DIR / "outputs"
RESULTS_FILE = SCRIPT_DIR / "validation_results.json"


def extract_svelte_code(text: str) -> str | None:
    if not text or not text.strip():
        return None
    match = re.search(r"```(?:svelte)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    stripped = text.strip()
    if stripped.startswith("<script") or stripped.startswith("<"):
        return stripped
    return None


def build_svelte_app(cwd: Path) -> tuple[bool, str, str]:
    install = subprocess.run(
        ["npm", "install"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if install.returncode != 0:
        err = install.stderr or install.stdout
        return False, install.stdout or "", err

    build = subprocess.run(
        ["npm", "run", "build"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return (
        build.returncode == 0,
        build.stdout or "",
        build.stderr or "",
    )


def validate_answer(svelte_code: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp)
        shutil.copytree(TEMPLATE_DIR, dst, dirs_exist_ok=True)
        app_svelte = dst / "src" / "App.svelte"
        app_svelte.write_text(svelte_code, encoding="utf-8")
        ok, stdout, stderr = build_svelte_app(dst)
        return {
            "valid": ok,
            "stdout": stdout,
            "stderr": stderr,
        }


def main() -> None:
    if not OUTPUTS_DIR.exists():
        print(f"Run models.py first to generate {OUTPUTS_DIR}/{{model}}/q{{n}}.svelte")
        return

    if not TEMPLATE_DIR.exists():
        print(f"Template not found at {TEMPLATE_DIR}")
        return

    results: dict[str, dict[str, dict]] = {}

    for model_dir in sorted(OUTPUTS_DIR.iterdir()):
        if not model_dir.is_dir():
            continue
        model_name = model_dir.name
        results[model_name] = {}

        for svelte_file in sorted(model_dir.glob("q*.svelte")):
            q_name = svelte_file.stem
            content = svelte_file.read_text(encoding="utf-8")
            code = extract_svelte_code(content)
            if code:
                result = validate_answer(code)
                result["extracted"] = True
                results[model_name][q_name] = result
            else:
                results[model_name][q_name] = {
                    "valid": False,
                    "extracted": False,
                    "stdout": "",
                    "stderr": "Could not extract Svelte code from response",
                }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    total = sum(1 for qa in results.values() for r in qa.values() if r.get("valid"))
    count = sum(1 for qa in results.values() for _ in qa)
    print(f"Valid: {total}/{count}")
    print(f"Results written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
