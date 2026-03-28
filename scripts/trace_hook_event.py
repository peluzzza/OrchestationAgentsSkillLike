"""Append Zeus subagent hook events into a trace ledger and render attendance reports.

The hook payload schema can vary across VS Code / Copilot builds, so this
script prefers resilient key discovery over rigid field assumptions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SPECIFY_DIRNAME = ".specify"
TRACE_ROOT = REPO_ROOT / SPECIFY_DIRNAME / "traces"

_TRACE_KEY_CANDIDATES = (
    "trace_id",
    "traceId",
    "conversationId",
    "conversation_id",
    "sessionId",
    "session_id",
    "invocationId",
    "invocation_id",
)
_EVENT_KEY_CANDIDATES = ("hookEventName", "hook_event_name", "hookEvent", "event")
_SUBAGENT_KEY_CANDIDATES = (
    "subagentName",
    "subagent_name",
    "agentName",
    "agent_name",
    "agent",
)
_PARENT_KEY_CANDIDATES = (
    "parentAgent",
    "parent_agent",
    "callerAgent",
    "caller_agent",
    "sourceAgent",
    "source_agent",
)
_STATUS_KEY_CANDIDATES = ("status", "result", "outcome")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _is_present(value: Any) -> bool:
    return value not in (None, "", [], {})


def _iter_nested_values(payload: Any):
    if isinstance(payload, dict):
        for value in payload.values():
            yield value
        return
    if isinstance(payload, list):
        for item in payload:
            yield item


def _first_nested_value(payload: Any, candidates: tuple[str, ...]) -> Any:
    if isinstance(payload, dict):
        for key in candidates:
            value = payload.get(key)
            if _is_present(value):
                return value
    for nested_value in _iter_nested_values(payload):
        found = _first_nested_value(nested_value, candidates)
        if _is_present(found):
            return found
    return None


def _as_text(value: Any) -> str | None:
    if value in (None, "", [], {}):
        return None
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, (int, float, bool)):
        return str(value)
    return None


def _sanitize_trace_id(value: str | None) -> str:
    if value:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
        if cleaned:
            return cleaned[:120]
    return f"zeus-trace-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"


def _trace_root(repo_root: Path) -> Path:
    return repo_root / SPECIFY_DIRNAME / "traces"


def trace_ledger_path(trace_id: str, repo_root: Path = REPO_ROOT) -> Path:
    return _trace_root(repo_root) / f"{trace_id}.jsonl"


def trace_report_path(trace_id: str, repo_root: Path = REPO_ROOT) -> Path:
    return _trace_root(repo_root) / f"{trace_id}.md"


def _unique_trace_values(events: list[dict[str, Any]], field: str) -> list[str]:
    return sorted({event[field] for event in events if event.get(field)})


def _build_section(title: str, items: list[str], empty_line: str) -> list[str]:
    lines = ["", title, ""]
    if items:
        lines.extend(items)
    else:
        lines.append(empty_line)
    return lines


def _timeline_lines(events: list[dict[str, Any]]) -> list[str]:
    if not events:
        return ["- _(no events recorded yet)_"]
    lines: list[str] = []
    for event in events:
        parts = [f"- {event['timestamp']}", f"`{event['hook_event']}`"]
        if event.get("subagent_name"):
            parts.append(f"subagent=`{event['subagent_name']}`")
        if event.get("parent_agent"):
            parts.append(f"parent=`{event['parent_agent']}`")
        if event.get("status"):
            parts.append(f"status=`{event['status']}`")
        lines.append(" | ".join(parts))
    return lines


def build_event_record(payload: dict[str, Any]) -> dict[str, Any]:
    event_name = _as_text(_first_nested_value(payload, _EVENT_KEY_CANDIDATES)) or "unknown"
    subagent_name = _as_text(_first_nested_value(payload, _SUBAGENT_KEY_CANDIDATES))
    parent_agent = _as_text(_first_nested_value(payload, _PARENT_KEY_CANDIDATES))
    status = _as_text(_first_nested_value(payload, _STATUS_KEY_CANDIDATES))
    raw_trace_id = _as_text(_first_nested_value(payload, _TRACE_KEY_CANDIDATES))
    trace_id = _sanitize_trace_id(raw_trace_id)

    return {
        "timestamp": _utc_now(),
        "trace_id": trace_id,
        "hook_event": event_name,
        "subagent_name": subagent_name,
        "parent_agent": parent_agent,
        "edge": f"{parent_agent} -> {subagent_name}" if parent_agent and subagent_name else None,
        "status": status,
        "payload": payload,
    }


def load_trace_events(trace_id: str, repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    ledger_path = trace_ledger_path(trace_id, repo_root=repo_root)
    if not ledger_path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def render_trace_markdown(trace_id: str, repo_root: Path = REPO_ROOT) -> str:
    events = load_trace_events(trace_id, repo_root=repo_root)
    unique_subagents = _unique_trace_values(events, "subagent_name")
    unique_edges = _unique_trace_values(events, "edge")
    status_counts = Counter(event["status"] for event in events if event.get("status"))
    report_path = trace_report_path(trace_id, repo_root=repo_root)

    lines = [
        f"## Zeus Attendance Trace: {trace_id}",
        "",
        f"- TRACE_ID: `{trace_id}`",
        f"- ATTENDANCE_COUNT: {len(unique_subagents)}",
        f"- OBSERVED_EDGES: {len(unique_edges)}",
        f"- REPORT_PATH: `{report_path.relative_to(repo_root)}`",
        f"- EVENT_COUNT: {len(events)}",
    ]
    lines.extend(
        _build_section(
            "### Subagents",
            [f"- `{name}`" for name in unique_subagents],
            "- _(none observed yet)_",
        )
    )
    lines.extend(
        _build_section(
            "### Edges",
            [f"- `{edge}`" for edge in unique_edges],
            "- _(no parent → subagent edges observed yet)_",
        )
    )
    lines.extend(
        _build_section(
            "### Status counts",
            [f"- `{status}`: {count}" for status, count in sorted(status_counts.items())],
            "- _(no statuses reported yet)_",
        )
    )
    lines.extend(_build_section("### Timeline", _timeline_lines(events), "- _(no events recorded yet)_"))

    markdown = "\n".join(lines) + "\n"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(markdown, encoding="utf-8")
    return markdown


def record_hook_event(payload: dict[str, Any], repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    event = build_event_record(payload)
    ledger_path = trace_ledger_path(event["trace_id"], repo_root=repo_root)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    render_trace_markdown(event["trace_id"], repo_root=repo_root)
    return event


def _read_payload_from_stdin() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if isinstance(loaded, dict):
        return loaded
    return {"payload": loaded}


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record Zeus hook attendance events")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--hook-event")
    parser.add_argument("--trace-id")
    parser.add_argument("--parent-agent")
    parser.add_argument("--subagent-name")
    parser.add_argument("--status")
    parser.add_argument("--feature-id")
    parser.add_argument("--phase")
    return parser.parse_args(argv)


def _payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    payload = {
        "hookEventName": args.hook_event,
        "traceId": args.trace_id,
        "parentAgent": args.parent_agent,
        "subagentName": args.subagent_name,
        "status": args.status,
        "featureId": args.feature_id,
        "phase": args.phase,
    }
    return {key: value for key, value in payload.items() if _is_present(value)}


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    payload = _payload_from_args(args)
    if not payload:
        payload = _read_payload_from_stdin()
    event = record_hook_event(payload, repo_root=args.repo_root)
    summary = {
        "trace_id": event["trace_id"],
        "ledger_path": str(trace_ledger_path(event["trace_id"], repo_root=args.repo_root)),
        "report_path": str(trace_report_path(event["trace_id"], repo_root=args.repo_root)),
        "hook_event": event["hook_event"],
        "subagent_name": event["subagent_name"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())