"""Render Zeus attendance reports from JSONL trace ledgers."""

from __future__ import annotations

import sys
from pathlib import Path

from trace_hook_event import REPO_ROOT, TRACE_ROOT, render_trace_markdown


def _discover_trace_ids(trace_root: Path = TRACE_ROOT) -> list[str]:
    if not trace_root.exists():
        return []
    return sorted(path.stem for path in trace_root.glob("*.jsonl"))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    trace_ids = args or _discover_trace_ids()
    if not trace_ids:
        print("No trace ledgers found.", file=sys.stderr)
        return 1

    for trace_id in trace_ids:
        render_trace_markdown(trace_id, repo_root=REPO_ROOT)
        print(f"rendered {trace_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())