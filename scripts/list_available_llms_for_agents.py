import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Iterable


def _read_item(db_path: Path, key: str) -> str | None:
    if not db_path.exists():
        return None
    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()
        row = cur.execute("SELECT value FROM ItemTable WHERE key = ?", (key,)).fetchone()
        if not row:
            return None
        value = row[0]
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value
    finally:
        con.close()


def _iter_models_from_cached_language_models(payload: Any) -> Iterable[dict[str, Any]]:
    if not isinstance(payload, list):
        return
    for item in payload:
        if isinstance(item, dict) and "metadata" in item:
            yield item


def _qualified_name(name: str, vendor: str) -> str:
    # VS Code qualified model name format is "Model Name (vendor)".
    # For vendor==copilot, VS Code also matches bare model name.
    return f"{name} ({vendor})"


def main() -> int:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("APPDATA env var not set")
        return 2

    global_db = Path(appdata) / "Code" / "User" / "globalStorage" / "state.vscdb"

    keys = [
        "chat.cachedLanguageModels.v2",
        "chat.modelsControl",
        "chat.currentLanguageModel.panel",
    ]

    print(f"global_db: {global_db}")
    for key in keys:
        raw = _read_item(global_db, key)
        print(f"\n[{key}] present={raw is not None}")
        if raw is None:
            continue
        if key == "chat.currentLanguageModel.panel":
            print(raw)
            continue

        try:
            payload = json.loads(raw)
        except Exception as e:
            print(f"(failed to parse JSON: {e})")
            continue

        if key == "chat.modelsControl":
            # This structure changes; print only labels/ids if present.
            free = payload.get("free") if isinstance(payload, dict) else None
            if isinstance(free, dict):
                print("modelsControl.free:")
                for model_id, meta in free.items():
                    label = meta.get("label") if isinstance(meta, dict) else None
                    print(f"- {model_id}: {label}")
            else:
                print("(unexpected modelsControl shape)")

        if key == "chat.cachedLanguageModels.v2":
            models = list(_iter_models_from_cached_language_models(payload))
            print(f"cachedLanguageModels.count={len(models)}")
            # Print a compact table of likely-usable qualified names.
            for item in models:
                md = item.get("metadata") or {}
                name = md.get("name")
                vendor = md.get("vendor")
                identifier = item.get("identifier")
                if not isinstance(name, str) or not isinstance(vendor, str):
                    continue
                q = _qualified_name(name, vendor)
                print(f"- {q}  (identifier={identifier})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
