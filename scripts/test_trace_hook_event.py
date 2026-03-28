"""Tests for Zeus hook attendance ledger/report generation."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path


_SCRIPT_DIR = Path(__file__).resolve().parent
_MODULE_PATH = _SCRIPT_DIR / "trace_hook_event.py"

_SPEC = importlib.util.spec_from_file_location("trace_hook_event", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_trace = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_trace)  # type: ignore[union-attr]


def test_record_hook_event_writes_jsonl_and_markdown(tmp_path: Path) -> None:
    payload = {
        "hookEventName": "SubagentStart",
        "traceId": "zeus-demo-1",
        "parentAgent": "Zeus",
        "subagentName": "Prometheus",
        "status": "started",
    }

    event = _trace.record_hook_event(payload, repo_root=tmp_path)

    ledger_path = _trace.trace_ledger_path("zeus-demo-1", repo_root=tmp_path)
    report_path = _trace.trace_report_path("zeus-demo-1", repo_root=tmp_path)

    assert event["trace_id"] == "zeus-demo-1"
    assert ledger_path.exists()
    assert report_path.exists()

    lines = ledger_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    stored = json.loads(lines[0])
    assert stored["hook_event"] == "SubagentStart"
    assert stored["edge"] == "Zeus -> Prometheus"

    report = report_path.read_text(encoding="utf-8")
    assert "ATTENDANCE_COUNT: 1" in report
    assert "`Zeus -> Prometheus`" in report


def test_build_event_record_reads_nested_payload_keys() -> None:
    payload = {
        "metadata": {
            "hookEvent": "SubagentStop",
            "conversationId": "nested-trace",
        },
        "details": {
            "callerAgent": "Zeus",
            "agentName": "Argus - QA Testing Subagent",
            "result": "passed",
        },
    }

    event = _trace.build_event_record(payload)

    assert event["trace_id"] == "nested-trace"
    assert event["hook_event"] == "SubagentStop"
    assert event["parent_agent"] == "Zeus"
    assert event["subagent_name"] == "Argus - QA Testing Subagent"
    assert event["status"] == "passed"


def test_render_trace_markdown_aggregates_multiple_events(tmp_path: Path) -> None:
    trace_id = "attendance-rollcall"
    _trace.record_hook_event(
        {
            "hookEventName": "SubagentStart",
            "traceId": trace_id,
            "parentAgent": "Zeus",
            "subagentName": "Prometheus",
            "status": "started",
        },
        repo_root=tmp_path,
    )
    _trace.record_hook_event(
        {
            "hookEventName": "SubagentStop",
            "traceId": trace_id,
            "parentAgent": "Zeus",
            "subagentName": "Prometheus",
            "status": "completed",
        },
        repo_root=tmp_path,
    )
    _trace.record_hook_event(
        {
            "hookEventName": "SubagentStart",
            "traceId": trace_id,
            "parentAgent": "Zeus",
            "subagentName": "Sisyphus-subagent",
            "status": "started",
        },
        repo_root=tmp_path,
    )

    markdown = _trace.render_trace_markdown(trace_id, repo_root=tmp_path)

    assert "ATTENDANCE_COUNT: 2" in markdown
    assert "OBSERVED_EDGES: 2" in markdown
    assert "`completed`: 1" in markdown
    assert "`started`: 2" in markdown
    assert "`Prometheus`" in markdown
    assert "`Sisyphus-subagent`" in markdown


# ---------------------------------------------------------------------------
# _read_payload_from_stdin edge cases
# ---------------------------------------------------------------------------

def test_read_payload_from_stdin_empty_returns_empty_dict(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    assert _trace._read_payload_from_stdin() == {}


def test_read_payload_from_stdin_whitespace_only_returns_empty_dict(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO("   \n  "))
    assert _trace._read_payload_from_stdin() == {}


def test_read_payload_from_stdin_valid_dict_passthrough(monkeypatch) -> None:
    payload = {"hookEventName": "SubagentStart", "traceId": "t1"}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    assert _trace._read_payload_from_stdin() == payload


def test_read_payload_from_stdin_non_dict_json_wraps_into_payload_key(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(["a", "b"])))
    result = _trace._read_payload_from_stdin()
    assert result == {"payload": ["a", "b"]}


def test_read_payload_from_stdin_invalid_json_returns_empty_dict(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO("{not valid json"))
    assert _trace._read_payload_from_stdin() == {}


# ---------------------------------------------------------------------------
# _sanitize_trace_id edge cases
# ---------------------------------------------------------------------------

def test_sanitize_trace_id_cleans_special_characters() -> None:
    result = _trace._sanitize_trace_id("zeus trace/2026 test!")
    assert "/" not in result
    assert " " not in result
    assert "!" not in result


def test_sanitize_trace_id_preserves_allowed_characters() -> None:
    assert _trace._sanitize_trace_id("zeus-trace.1_ok") == "zeus-trace.1_ok"


def test_sanitize_trace_id_none_produces_timestamp_fallback() -> None:
    result = _trace._sanitize_trace_id(None)
    assert result.startswith("zeus-trace-")


def test_sanitize_trace_id_empty_string_produces_timestamp_fallback() -> None:
    result = _trace._sanitize_trace_id("")
    assert result.startswith("zeus-trace-")


def test_build_event_record_without_trace_id_generates_fallback() -> None:
    payload = {"hookEventName": "SubagentStart", "subagentName": "Prometheus"}
    event = _trace.build_event_record(payload)
    assert event["trace_id"].startswith("zeus-trace-")


# ---------------------------------------------------------------------------
# main() CLI integration
# ---------------------------------------------------------------------------


def test_main_reads_stdin_writes_ledger_report_prints_summary_and_returns_0(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    import functools

    payload = {
        "hookEventName": "SubagentStart",
        "traceId": "main-cli-test",
        "parentAgent": "Zeus",
        "subagentName": "Prometheus",
        "status": "running",
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    monkeypatch.setattr(
        _trace,
        "record_hook_event",
        functools.partial(_trace.record_hook_event, repo_root=tmp_path),
    )
    monkeypatch.setattr(
        _trace,
        "trace_ledger_path",
        functools.partial(_trace.trace_ledger_path, repo_root=tmp_path),
    )
    monkeypatch.setattr(
        _trace,
        "trace_report_path",
        functools.partial(_trace.trace_report_path, repo_root=tmp_path),
    )

    result = _trace.main()

    captured = capsys.readouterr()
    summary = json.loads(captured.out)

    assert result == 0
    assert summary["trace_id"] == "main-cli-test"
    assert summary["hook_event"] == "SubagentStart"
    assert summary["subagent_name"] == "Prometheus"
    assert (tmp_path / ".specify" / "traces" / "main-cli-test.jsonl").exists()
    assert (tmp_path / ".specify" / "traces" / "main-cli-test.md").exists()


def test_main_accepts_cli_arguments_without_stdin(tmp_path: Path, capsys) -> None:
    result = _trace.main(
        [
            "--repo-root",
            str(tmp_path),
            "--hook-event",
            "before_specify",
            "--trace-id",
            "stage-hook-1",
            "--parent-agent",
            "Prometheus",
            "--subagent-name",
            "SpecifySpec",
            "--status",
            "started",
            "--feature-id",
            "demo-feature",
            "--phase",
            "SP-2",
        ]
    )

    captured = capsys.readouterr()
    summary = json.loads(captured.out)

    assert result == 0
    assert summary["trace_id"] == "stage-hook-1"
    assert summary["hook_event"] == "before_specify"
    assert summary["subagent_name"] == "SpecifySpec"
    ledger = tmp_path / ".specify" / "traces" / "stage-hook-1.jsonl"
    stored = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
    assert stored["payload"]["featureId"] == "demo-feature"
    assert stored["payload"]["phase"] == "SP-2"


# ---------------------------------------------------------------------------
# render_trace_markdown empty-trace path
# ---------------------------------------------------------------------------


def test_render_trace_markdown_fresh_trace_id_shows_zeros_and_placeholders(
    tmp_path: Path,
) -> None:
    markdown = _trace.render_trace_markdown("never-seen-trace", repo_root=tmp_path)

    assert "ATTENDANCE_COUNT: 0" in markdown
    assert "OBSERVED_EDGES: 0" in markdown
    assert "EVENT_COUNT: 0" in markdown
    assert "_(none observed yet)_" in markdown
    assert "_(no parent" in markdown
    assert "_(no statuses reported yet)_" in markdown
    assert "_(no events recorded yet)_" in markdown