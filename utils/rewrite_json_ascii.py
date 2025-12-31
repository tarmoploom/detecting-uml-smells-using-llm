import json
from pathlib import Path

# ==========================================
# CONFIG: changes non utf-8 text parts only
# ==========================================

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = (SCRIPT_DIR / ".." / "Results").resolve()  # git_main_folder/Results


def load_text(path: Path) -> str:
    # Most JSON files are UTF-8; this also handles UTF-8 with BOM.
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")

def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"Folder not found: {ROOT}")

    rewritten = 0
    skipped = 0

    for p in ROOT.rglob("*.json"):
        try:
            raw = load_text(p)
            data = json.loads(raw)  # decodes \u00xx escapes properly

            pretty = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
            p.write_text(pretty, encoding="utf-8")

            rewritten += 1
        except Exception as e:
            skipped += 1
            print(f"SKIP  {p}  ({type(e).__name__}: {e})")

    print(f"Done. Rewritten: {rewritten}, skipped: {skipped}")

if __name__ == "__main__":
    main()
