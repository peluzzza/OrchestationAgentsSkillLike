import os
import sqlite3
from pathlib import Path
from urllib.parse import urlparse, unquote

def main() -> int:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("APPDATA env var not set")
        return 2

    workspace_dir = Path.cwd().resolve()
    print(f"Workspace: {workspace_dir}")

    def inspect(db: Path, label: str) -> None:
        print(f"\n=== Inspect: {label} ===")
        print(f"DB: {db}")
        if not db.exists():
            print("(missing)")
            return

        con = sqlite3.connect(db)
        cur = con.cursor()

        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print(f"tables: {tables}")

        kv_table = None
        for t in tables:
            cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})").fetchall()]
            low = [c.lower() for c in cols]
            if "key" in low and "value" in low:
                kv_table = t
                print(f"kv_table: {kv_table} cols={cols}")
                break

        if not kv_table:
            print("No key/value table found.")
            return

        def find(pattern: str):
            rows = cur.execute(
                f"SELECT key, value FROM {kv_table} WHERE key LIKE ? ORDER BY key LIMIT 200",
                (pattern,),
            ).fetchall()
            print(f"\n== keys like {pattern!r} ({len(rows)}) ==")
            for k, v in rows:
                vs = v
                if isinstance(vs, bytes):
                    vs = vs.decode("utf-8", errors="replace")
                if isinstance(vs, str) and len(vs) > 300:
                    vs = vs[:300] + "…"
                print(f"- {k}: {vs}")

        # Broad scan buckets
        find("%chat%")
        find("%agent%")
        find("%copilot%")
        find("%custom%")
        find("%mode%")
        find("%customModes%")
        find("%agentFiles%")
        find("%prompt%")
        find("%skills%")

        atlas_keys = cur.execute(
            f"SELECT key, value FROM {kv_table} WHERE key LIKE ? ORDER BY key LIMIT 200",
            ("%Atlas%",),
        ).fetchall()
        print(f"\n== keys like '%Atlas%' ({len(atlas_keys)}) ==")
        for k, v in atlas_keys:
            vs = v.decode("utf-8", errors="replace") if isinstance(v, bytes) else v
            if isinstance(vs, str) and len(vs) > 300:
                vs = vs[:300] + "…"
            print(f"- {k}: {vs}")

        con.close()

    # Inspect global state
    global_db = Path(appdata) / "Code" / "User" / "globalStorage" / "state.vscdb"
    inspect(global_db, "globalStorage/state.vscdb")

    # Locate and inspect workspace-scoped state
    ws_root = Path(appdata) / "Code" / "User" / "workspaceStorage"
    ws_db = None
    if ws_root.exists():
        for candidate in ws_root.iterdir():
            if not candidate.is_dir():
                continue
            ws_json = candidate / "workspace.json"
            if not ws_json.exists():
                continue
            try:
                folder_uri = ws_json.read_text(encoding="utf-8")
            except Exception:
                continue
            if "file:///" not in folder_uri:
                continue
            try:
                # quick parse: extract the URI string value without full JSON parse
                start = folder_uri.find("file:///")
                end = folder_uri.find('"', start)
                uri = folder_uri[start:end]
                parsed = urlparse(uri)
                fs_path = Path(unquote(parsed.path.lstrip("/"))).resolve()
            except Exception:
                continue
            if fs_path == workspace_dir:
                ws_db = candidate / "state.vscdb"
                break

    if ws_db:
        inspect(ws_db, "workspaceStorage/<hash>/state.vscdb")
    else:
        print("\n=== Inspect: workspaceStorage ===")
        print("No matching workspaceStorage state.vscdb found for this workspace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
