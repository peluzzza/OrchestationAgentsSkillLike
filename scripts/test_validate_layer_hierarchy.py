"""Tests for scripts/validate_layer_hierarchy.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Load module under test
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_MODULE_PATH = _SCRIPT_DIR / "validate_layer_hierarchy.py"

_SPEC = importlib.util.spec_from_file_location("validate_layer_hierarchy", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_vlh = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_vlh)  # type: ignore[union-attr]

validate = _vlh.validate
AgentRecord = _vlh.AgentRecord
_parse_agent = _vlh._parse_agent
_extract_layer_from_body = _vlh._extract_layer_from_body
_extract_agents_list = _vlh._extract_agents_list
_parse_runtime_contract = _vlh._parse_runtime_contract
_check_runtime_contract = _vlh._check_runtime_contract
_STABLE_RUNTIME_AGENTS = _vlh._STABLE_RUNTIME_AGENTS
_collect_agent_files = _vlh._collect_agent_files
REPO_ROOT = _vlh.REPO_ROOT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_agent(
    tmp_path: Path,
    name: str,
    agent_name: str,
    layer_comment: str | None = None,
    agents: list[str] | None = None,
    extra_body: str = "",
    runtime_contract: str | None = None,
) -> Path:
    path = tmp_path / name
    frontmatter_lines = [f"name: {agent_name}"]
    if agents:
        frontmatter_lines.append("agents:")
        for a in agents:
            frontmatter_lines.append(f"  - {a}")
    frontmatter = "\n".join(frontmatter_lines)

    layer_line = f"{layer_comment}\n" if layer_comment else ""
    contract_line = f"{runtime_contract}\n" if runtime_contract else ""
    content = f"---\n{frontmatter}\n---\n{layer_line}{contract_line}{extra_body}"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Layer parsing
# ---------------------------------------------------------------------------


class TestLayerParsing:
    def test_layer_0_parsed(self, tmp_path: Path) -> None:
        """Agent with ``<!-- layer: 0 -->`` → parsed as layer 0."""
        p = _write_agent(tmp_path, "a.agent.md", "Atlas", "<!-- layer: 0 -->")
        rec = _parse_agent(p)
        assert rec.layer == 0

    def test_layer_1_with_domain(self, tmp_path: Path) -> None:
        """``<!-- layer: 1 | domain: Planning -->`` → parsed as layer 1."""
        p = _write_agent(tmp_path, "b.agent.md", "Prometheus", "<!-- layer: 1 | domain: Planning -->")
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_layer_2_with_parent(self, tmp_path: Path) -> None:
        """``<!-- layer: 2 | parent: X -->`` → parsed as layer 2."""
        p = _write_agent(tmp_path, "c.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        rec = _parse_agent(p)
        assert rec.layer == 2

    def test_layer_1_alias(self, tmp_path: Path) -> None:
        """``<!-- layer: 1 | type: alias | delegates-to: Y -->`` → parsed as layer 1."""
        p = _write_agent(tmp_path, "d.agent.md", "Sisyphus-subagent", "<!-- layer: 1 | type: alias | delegates-to: Sisyphus -->")
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_no_layer_comment_returns_none(self, tmp_path: Path) -> None:
        """No layer comment → layer is None."""
        p = _write_agent(tmp_path, "e.agent.md", "Unknown")
        rec = _parse_agent(p)
        assert rec.layer is None

    def test_layer_comment_on_second_line_still_detected(self, tmp_path: Path) -> None:
        """Layer comment on second line after ``---`` → still detected."""
        p = tmp_path / "f.agent.md"
        p.write_text(
            "---\nname: F\n---\n\n<!-- layer: 1 | domain: Test -->\nBody.\n",
            encoding="utf-8",
        )
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_layer_comment_on_third_line_detected(self, tmp_path: Path) -> None:
        """Layer comment on third line after ``---`` → still detected."""
        p = tmp_path / "g.agent.md"
        p.write_text(
            "---\nname: G\n---\n\n\n<!-- layer: 2 | parent: X -->\nBody.\n",
            encoding="utf-8",
        )
        rec = _parse_agent(p)
        assert rec.layer == 2


# ---------------------------------------------------------------------------
# Orphan detection
# ---------------------------------------------------------------------------


class TestOrphanDetection:
    def test_missing_layer_creates_orphan_violation(self, tmp_path: Path) -> None:
        """Agent with no layer comment → ORPHAN violation."""
        p = _write_agent(tmp_path, "orphan.agent.md", "Wanderer")
        _, violations = validate([p])
        assert any("ORPHAN" in v and str(p) in v for v in violations)

    def test_multiple_orphans_all_reported(self, tmp_path: Path) -> None:
        """Multiple orphans are all reported."""
        p1 = _write_agent(tmp_path, "o1.agent.md", "Ghost1")
        p2 = _write_agent(tmp_path, "o2.agent.md", "Ghost2")
        _, violations = validate([p1, p2])
        assert len([v for v in violations if "ORPHAN" in v]) == 2


# ---------------------------------------------------------------------------
# Atlas-specific rules
# ---------------------------------------------------------------------------


class TestAtlasRules:
    def test_atlas_layer_0_valid(self, tmp_path: Path) -> None:
        """Legacy Atlas alias at ``<!-- layer: 0 -->`` → valid, no root-layer violation."""
        p = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->")
        _, violations = validate([p])
        assert not any("ROOT LAYER ERROR" in v for v in violations)

    def test_atlas_layer_1_violation(self, tmp_path: Path) -> None:
        """Legacy Atlas alias at ``<!-- layer: 1 -->`` → root-layer violation."""
        p = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 1 -->")
        _, violations = validate([p])
        assert any("ROOT LAYER ERROR" in v for v in violations)

    def test_atlas_agents_list_l1_only_no_violation(self, tmp_path: Path) -> None:
        """Atlas ``agents:`` list with only L1 agents → no L0→L2 violation."""
        l1a = _write_agent(tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 | domain: Planning -->")
        l1b = _write_agent(tmp_path, "Sisyphus.agent.md", "Sisyphus", "<!-- layer: 1 | domain: Implementation -->")
        atlas = _write_agent(
            tmp_path,
            "Atlas.agent.md",
            "Atlas",
            "<!-- layer: 0 -->",
            agents=["Prometheus", "Sisyphus"],
        )
        _, violations = validate([atlas, l1a, l1b])
        assert not any("L0→L2" in v for v in violations)

    def test_atlas_agents_list_with_l2_agent_violation(self, tmp_path: Path) -> None:
        """Atlas ``agents:`` list containing a known L2 agent name → violation."""
        l2 = _write_agent(tmp_path, "Backend-Atlas.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        atlas = _write_agent(
            tmp_path,
            "Atlas.agent.md",
            "Atlas",
            "<!-- layer: 0 -->",
            agents=["Backend-Atlas"],
        )
        _, violations = validate([atlas, l2])
        assert any("L0→L2" in v and "Backend-Atlas" in v for v in violations)


# ---------------------------------------------------------------------------
# L1 rules
# ---------------------------------------------------------------------------


class TestL1Rules:
    def test_l1_referencing_l0_is_violation(self, tmp_path: Path) -> None:
        """L1 agent's ``agents:`` referencing an L0 agent → L1→L0 violation."""
        l0 = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->")
        l1 = _write_agent(
            tmp_path,
            "Prometheus.agent.md",
            "Prometheus",
            "<!-- layer: 1 | domain: Planning -->",
            agents=["Atlas"],
        )
        _, violations = validate([l0, l1])
        assert any("L1→L0" in v for v in violations)

    def test_non_atlas_l0_agent_normal(self, tmp_path: Path) -> None:
        """A non-Atlas L0 agent (rare) should not trigger the Atlas-name rule."""
        p = _write_agent(tmp_path, "Conductor.agent.md", "Conductor", "<!-- layer: 0 -->")
        _, violations = validate([p])
        assert not any("ROOT LAYER ERROR" in v for v in violations)

    def test_alias_with_correct_layer_valid(self, tmp_path: Path) -> None:
        """Alias agent at layer 1 with correct comment → no orphan."""
        p = _write_agent(
            tmp_path,
            "Sisyphus-subagent.agent.md",
            "Sisyphus-subagent",
            "<!-- layer: 1 | type: alias | delegates-to: Sisyphus -->",
        )
        _, violations = validate([p])
        assert not any("ORPHAN" in v for v in violations)

    def test_l1_referencing_l2_no_violation(self, tmp_path: Path) -> None:
        """L1 agent referencing L2 is allowed (normal delegation path)."""
        l2 = _write_agent(tmp_path, "Backend-Atlas.agent.md", "Backend-Atlas", "<!-- layer: 2 | parent: Sisyphus -->")
        l1 = _write_agent(
            tmp_path,
            "Sisyphus.agent.md",
            "Sisyphus",
            "<!-- layer: 1 | domain: Implementation -->",
            agents=["Backend-Atlas"],
        )
        _, violations = validate([l1, l2])
        assert not any("L1→L0" in v or "L0→L2" in v for v in violations)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_file_no_crash(self, tmp_path: Path) -> None:
        """Empty file → no crash, treated as ORPHAN."""
        p = tmp_path / "empty.agent.md"
        p.write_text("", encoding="utf-8")
        _, violations = validate([p])
        assert isinstance(violations, list)
        assert any("ORPHAN" in v for v in violations)

    def test_only_opening_fence_no_crash(self, tmp_path: Path) -> None:
        """File with only opening ``---`` (no closing) → no crash."""
        p = tmp_path / "partial.agent.md"
        p.write_text("---\nname: Ghost\n", encoding="utf-8")
        _, violations = validate([p])
        assert isinstance(violations, list)

    def test_layer_3_unknown_treated_as_valid_layer(self, tmp_path: Path) -> None:
        """Layer 3 is unusual but should not crash — only orphan check matters."""
        p = _write_agent(tmp_path, "deep.agent.md", "Deep", "<!-- layer: 3 | parent: X -->")
        _, violations = validate([p])
        # Should not be flagged as ORPHAN since it has a layer comment.
        assert not any("ORPHAN" in v for v in violations)

    def test_records_returned_for_each_file(self, tmp_path: Path) -> None:
        """``validate`` returns one record per input file."""
        p1 = _write_agent(tmp_path, "a.agent.md", "A", "<!-- layer: 1 -->")
        p2 = _write_agent(tmp_path, "b.agent.md", "B", "<!-- layer: 2 -->")
        records, _ = validate([p1, p2])
        assert len(records) == 2

    def test_validate_empty_list(self) -> None:
        """``validate([])`` returns empty records and violations."""
        records, violations = validate([])
        assert records == []
        assert violations == []

    def test_bom_crlf_file_parsed(self, tmp_path: Path) -> None:
        """BOM + CRLF line endings handled without crash."""
        p = tmp_path / "bom.agent.md"
        p.write_bytes(
            "\ufeff---\r\nname: BOM\r\n---\r\n<!-- layer: 1 -->\r\nBody.\r\n".encode("utf-8")
        )
        rec = _parse_agent(p)
        assert rec.layer == 1

    def test_name_extracted_correctly(self, tmp_path: Path) -> None:
        """Agent name is extracted from frontmatter."""
        p = _write_agent(tmp_path, "x.agent.md", "MyAgent", "<!-- layer: 1 -->")
        rec = _parse_agent(p)
        assert rec.name == "MyAgent"


# ---------------------------------------------------------------------------
# Runtime-contract parsing
# ---------------------------------------------------------------------------

# Full valid contracts mirroring Phase-1 output — used across multiple test classes.
_ATLAS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=conductor | layer=0 | "
    "accepts=user | returns=user | approval=explicit-only | session=required | trace=required | "
    "request=goal,constraints,success_criteria | "
    "response=status,phase,last_action_changes,delegations,decision,pending_approvals,next -->"
)
_PROMETHEUS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=planner | layer=1 | "
    "accepts=Atlas | returns=Atlas | "
    "request=goal,tech_stack,feature_id,plan_dir | "
    "response=feature_id,feature_dir,spec_path,plan_path,analysis_report,specify_pipeline_status,open_questions,atlas_notes -->"
)
_SISYPHUS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=implementer | layer=1 | "
    "accepts=Atlas | returns=Atlas | "
    "request=feature_id,phase,acceptance_criteria,constraints | "
    "response=status,scope_completed,feature_id,files_changed,tests_added,tasks_completed,next_phase,validation_run,risks_found -->"
)
_AFRODITA_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=ui_implementer | layer=1 | "
    "accepts=Atlas | returns=Atlas | "
    "request=ui_scope,component_patterns,design_tokens,acceptance_criteria | "
    "response=status,scope_completed,files_changed,ui_states_covered,accessibility_notes,responsive_notes,validation_run,tests_added,risks_found -->"
)
_THEMIS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=reviewer | layer=1 | "
    "accepts=Atlas | returns=Atlas | "
    "request=phase_objective,acceptance_criteria,files_changed | "
    "response=status,summary,strengths,issues_found,recommendations,residual_risks,next_steps -->"
)
_ARGUS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=qa_specialist | layer=1 | "
    "accepts=Atlas | returns=Atlas | "
    "request=phase_objective,modified_files,existing_tests | "
    "response=status,summary,coverage_analysis,edge_cases_discovered,additional_tests_recommended,test_execution_results,next_steps -->"
)

# Optional-lane contract fixtures (Hermes, Oracle, HEPHAESTUS)
# Include session=inherited and trace=required — required by the wave-3 registry.
_HERMES_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=explorer | layer=1 | "
    "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
    "request=goal,scope,constraints | "
    "response=intent_analysis,files,answer,next_steps -->"
)
_ORACLE_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=researcher | layer=1 | "
    "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
    "request=goal,context,constraints | "
    "response=relevant_files,key_functions_classes,patterns_conventions,"
    "existing_tests,implementation_options,open_questions -->"
)
_HEPHAESTUS_CONTRACT = (
    "<!-- runtime-contract | version=stable-runtime-v1 | role=ops_specialist | layer=1 | "
    "accepts=Atlas | returns=Atlas | session=inherited | trace=required | "
    "request=mode,scope,environment,context | "
    "response=mode,status,evidence,actions_taken,issues_found,recommended_next_steps -->"
)


class TestRuntimeContractParsing:
    def test_parses_valid_contract(self) -> None:
        """Valid runtime-contract comment → dict with all fields."""
        body = "<!-- runtime-contract | role=conductor | layer=0 | accepts=user | returns=user -->\n"
        result = _parse_runtime_contract(body)
        assert result is not None
        assert result["role"] == "conductor"
        assert result["layer"] == "0"
        assert result["accepts"] == "user"
        assert result["returns"] == "user"

    def test_returns_none_for_missing_contract(self) -> None:
        """Body without a runtime-contract comment → None."""
        body = "<!-- layer: 1 | domain: Planning -->\nSome body text.\n"
        result = _parse_runtime_contract(body)
        assert result is None

    def test_field_ordering_does_not_matter(self) -> None:
        """Fields in any order are all parsed correctly."""
        body = "<!-- runtime-contract | returns=user | accepts=user | role=conductor -->\n"
        result = _parse_runtime_contract(body)
        assert result is not None
        assert result["returns"] == "user"
        assert result["accepts"] == "user"
        assert result["role"] == "conductor"

    def test_parses_comma_separated_request_fields(self) -> None:
        """request value with comma-separated fields is preserved as-is."""
        body = "<!-- runtime-contract | request=goal,constraints,success_criteria | response=status,phase -->\n"
        result = _parse_runtime_contract(body)
        assert result is not None
        assert result["request"] == "goal,constraints,success_criteria"
        fields = {f.strip() for f in result["request"].split(",")}
        assert fields == {"goal", "constraints", "success_criteria"}

    def test_contract_on_second_body_line(self) -> None:
        """runtime-contract comment on the line after the layer comment is found."""
        body = "<!-- layer: 0 -->\n<!-- runtime-contract | role=conductor | accepts=user -->\nBody text.\n"
        result = _parse_runtime_contract(body)
        assert result is not None
        assert result["role"] == "conductor"

    def test_runtime_contract_not_on_rec_when_absent(self, tmp_path: Path) -> None:
        """Parsed AgentRecord has runtime_contract=None when comment is absent."""
        p = _write_agent(tmp_path, "a.agent.md", "SomeAgent", "<!-- layer: 1 -->")
        rec = _parse_agent(p)
        assert rec.runtime_contract is None

    def test_runtime_contract_present_on_rec_when_set(self, tmp_path: Path) -> None:
        """Parsed AgentRecord has runtime_contract populated when comment is present."""
        p = _write_agent(
            tmp_path, "a.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract="<!-- runtime-contract | role=conductor | accepts=user | returns=user -->",
        )
        rec = _parse_agent(p)
        assert rec.runtime_contract is not None
        assert rec.runtime_contract["role"] == "conductor"


# ---------------------------------------------------------------------------
# Stable runtime contract enforcement
# ---------------------------------------------------------------------------


class TestStableRuntimeContracts:
    def test_missing_contract_for_stable_agent_atlas(self, tmp_path: Path) -> None:
        """Atlas without a runtime-contract comment → MISSING RUNTIME CONTRACT violation."""
        p = _write_agent(tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->")
        _, violations = validate([p])
        assert any(
            "MISSING RUNTIME CONTRACT" in v and "Atlas" in v for v in violations
        ), violations

    def test_missing_contract_for_stable_agent_sisyphus(self, tmp_path: Path) -> None:
        """Sisyphus-subagent without a runtime-contract comment → MISSING violation."""
        p = _write_agent(
            tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->"
        )
        _, violations = validate([p])
        assert any(
            "MISSING RUNTIME CONTRACT" in v and "Sisyphus-subagent" in v for v in violations
        ), violations

    def test_valid_atlas_contract_passes(self, tmp_path: Path) -> None:
        """Atlas with valid contract → no runtime-contract violation."""
        p = _write_agent(
            tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract=_ATLAS_CONTRACT,
        )
        _, violations = validate([p])
        assert not any("RUNTIME CONTRACT" in v for v in violations), violations

    def test_wrong_returns_target_for_non_atlas(self, tmp_path: Path) -> None:
        """Sisyphus-subagent with returns=user (not Atlas) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | accepts=Atlas | returns=user | "
            "request=feature_id,phase,acceptance_criteria,constraints | "
            "response=status,scope_completed,feature_id,files_changed,tests_added,"
            "tasks_completed,next_phase,validation_run,risks_found -->"
        )
        p = _write_agent(
            tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "returns" in v and "Sisyphus-subagent" in v
            for v in violations
        ), violations

    def test_missing_request_field_violation(self, tmp_path: Path) -> None:
        """Sisyphus-subagent contract missing 'constraints' → REQUEST FIELDS violation."""
        bad_contract = (
            "<!-- runtime-contract | accepts=Atlas | returns=Atlas | "
            "request=feature_id,phase,acceptance_criteria | "
            "response=status,scope_completed,feature_id,files_changed,tests_added,"
            "tasks_completed,next_phase,validation_run,risks_found -->"
        )
        p = _write_agent(
            tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT REQUEST FIELDS" in v and "constraints" in v for v in violations
        ), violations

    def test_missing_response_field_violation(self, tmp_path: Path) -> None:
        """Atlas contract missing 'next' in response → RESPONSE FIELDS violation."""
        bad_contract = (
            "<!-- runtime-contract | role=conductor | layer=0 | "
            "accepts=user | returns=user | approval=explicit-only | session=required | trace=required | "
            "request=goal,constraints,success_criteria | "
            "response=status,phase,last_action_changes,delegations,decision,pending_approvals -->"
        )
        p = _write_agent(
            tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT RESPONSE FIELDS" in v and "next" in v for v in violations
        ), violations

    def test_wrong_accepts_for_atlas(self, tmp_path: Path) -> None:
        """Atlas contract with accepts=Atlas (should be user) → field violation."""
        bad_contract = (
            "<!-- runtime-contract | role=conductor | layer=0 | "
            "accepts=Atlas | returns=user | approval=explicit-only | session=required | trace=required | "
            "request=goal,constraints,success_criteria | "
            "response=status,phase,last_action_changes,delegations,decision,pending_approvals,next -->"
        )
        p = _write_agent(
            tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "accepts" in v and "Atlas" in v for v in violations
        ), violations

    def test_valid_full_stable_set_passes(self, tmp_path: Path) -> None:
        """All six stable agents with valid contracts → zero runtime-contract violations."""
        files = [
            _write_agent(
                tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
                runtime_contract=_ATLAS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
                runtime_contract=_PROMETHEUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
                runtime_contract=_SISYPHUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Argus-subagent.agent.md", "Argus - QA Testing Subagent", "<!-- layer: 1 -->",
                runtime_contract=_ARGUS_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        rc_violations = [v for v in violations if "RUNTIME CONTRACT" in v]
        assert rc_violations == [], f"Unexpected runtime contract violations: {rc_violations}"

    def test_non_stable_agent_without_contract_is_not_flagged(self, tmp_path: Path) -> None:
        """An agent not in the stable set is not required to have a runtime contract."""
        p = _write_agent(tmp_path, "SomePlugin.agent.md", "SomePlugin", "<!-- layer: 2 -->")
        _, violations = validate([p])
        assert not any("RUNTIME CONTRACT" in v for v in violations)

    # -- version enforcement --------------------------------------------------

    def test_version_wrong_for_stable_agent_violation(self, tmp_path: Path) -> None:
        """Atlas contract with wrong version string → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v0 | role=conductor | layer=0 | "
            "accepts=user | returns=user | approval=explicit-only | session=required | trace=required | "
            "request=goal,constraints,success_criteria | "
            "response=status,phase,last_action_changes,delegations,decision,pending_approvals,next -->"
        )
        p = _write_agent(
            tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "version" in v and "Atlas" in v
            for v in violations
        ), violations

    def test_version_absent_from_contract_violation(self, tmp_path: Path) -> None:
        """Prometheus contract without version field → RUNTIME CONTRACT FIELD violation."""
        no_version_contract = (
            "<!-- runtime-contract | role=planner | layer=1 | "
            "accepts=Atlas | returns=Atlas | "
            "request=goal,tech_stack,feature_id,plan_dir | "
            "response=feature_id,feature_dir,spec_path,plan_path,analysis_report,"
            "specify_pipeline_status,open_questions,atlas_notes -->"
        )
        p = _write_agent(
            tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
            runtime_contract=no_version_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "version" in v and "Prometheus" in v
            for v in violations
        ), violations

    # -- role / layer enforcement for non-Atlas stable agents -----------------

    def test_role_enforced_for_non_atlas_stable(self, tmp_path: Path) -> None:
        """Prometheus with wrong role → RUNTIME CONTRACT FIELD violation for role."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=wrong_role | layer=1 | "
            "accepts=Atlas | returns=Atlas | "
            "request=goal,tech_stack,feature_id,plan_dir | "
            "response=feature_id,feature_dir,spec_path,plan_path,analysis_report,"
            "specify_pipeline_status,open_questions,atlas_notes -->"
        )
        p = _write_agent(
            tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "role" in v and "Prometheus" in v
            for v in violations
        ), violations

    def test_layer_enforced_for_non_atlas_stable(self, tmp_path: Path) -> None:
        """Sisyphus-subagent contract with wrong layer → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=implementer | layer=2 | "
            "accepts=Atlas | returns=Atlas | "
            "request=feature_id,phase,acceptance_criteria,constraints | "
            "response=status,scope_completed,feature_id,files_changed,tests_added,"
            "tasks_completed,next_phase,validation_run,risks_found -->"
        )
        p = _write_agent(
            tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "layer" in v and "Sisyphus-subagent" in v
            for v in violations
        ), violations

    def test_correct_role_and_layer_for_all_non_atlas_stable_agents(self, tmp_path: Path) -> None:
        """Argus, Themis, Afrodita with correct role+layer → no role/layer violations."""
        files = [
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Argus-subagent.agent.md", "Argus - QA Testing Subagent", "<!-- layer: 1 -->",
                runtime_contract=_ARGUS_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        role_layer_violations = [
            v for v in violations
            if "RUNTIME CONTRACT FIELD" in v and ("role" in v or "layer" in v)
        ]
        assert role_layer_violations == [], role_layer_violations


# ---------------------------------------------------------------------------
# Stable agent completeness
# ---------------------------------------------------------------------------


class TestStableAgentCompleteness:
    def test_missing_one_stable_agent_flagged(self, tmp_path: Path) -> None:
        """Five of six stable agents present → MISSING STABLE AGENT for the absent one."""
        files = [
            _write_agent(
                tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
                runtime_contract=_ATLAS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
                runtime_contract=_PROMETHEUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
                runtime_contract=_SISYPHUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            # Argus deliberately omitted
        ]
        _, violations = validate(files)
        assert any(
            "MISSING STABLE AGENT" in v and "Argus - QA Testing Subagent" in v
            for v in violations
        ), violations

    def test_no_completeness_check_when_no_stable_agents_present(self, tmp_path: Path) -> None:
        """Input containing only non-stable agents → no MISSING STABLE AGENT violations."""
        files = [
            _write_agent(tmp_path, "SomePlugin.agent.md", "SomePlugin", "<!-- layer: 2 -->"),
            _write_agent(tmp_path, "AnotherPlugin.agent.md", "AnotherPlugin", "<!-- layer: 2 -->"),
        ]
        _, violations = validate(files)
        assert not any("MISSING STABLE AGENT" in v for v in violations)

    def test_all_six_stable_agents_present_no_completeness_violation(self, tmp_path: Path) -> None:
        """All six stable agents present → no MISSING STABLE AGENT violations."""
        files = [
            _write_agent(
                tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
                runtime_contract=_ATLAS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
                runtime_contract=_PROMETHEUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
                runtime_contract=_SISYPHUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Argus-subagent.agent.md", "Argus - QA Testing Subagent", "<!-- layer: 1 -->",
                runtime_contract=_ARGUS_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        assert not any("MISSING STABLE AGENT" in v for v in violations)

    def test_single_stable_agent_triggers_completeness_check(self, tmp_path: Path) -> None:
        """A single stable agent in an otherwise empty set → five MISSING STABLE AGENT violations."""
        p = _write_agent(
            tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
            runtime_contract=_ATLAS_CONTRACT,
        )
        _, violations = validate([p])
        missing = [v for v in violations if "MISSING STABLE AGENT" in v]
        assert len(missing) == 5, f"Expected 5 missing-agent violations, got: {missing}"


# ---------------------------------------------------------------------------
# _extract_agents_list — focused hardening tests
# ---------------------------------------------------------------------------


class TestExtractAgentsList:
    def test_multi_word_agent_name_preserved(self) -> None:
        """Full text after ``- `` is captured; multi-word names are not truncated."""
        frontmatter = "name: Atlas\nagents:\n  - Themis Subagent\n  - Argus - QA Testing Subagent\n"
        result = _extract_agents_list(frontmatter)
        assert result == ["Themis Subagent", "Argus - QA Testing Subagent"]

    def test_single_word_name_still_works(self) -> None:
        """Single-word names continue to work after the regex fix."""
        frontmatter = "name: Atlas\nagents:\n  - Prometheus\n  - Sisyphus\n"
        result = _extract_agents_list(frontmatter)
        assert result == ["Prometheus", "Sisyphus"]

    def test_blank_lines_inside_block_skipped(self) -> None:
        """Blank lines inside the ``agents:`` block do not terminate collection."""
        frontmatter = "name: Atlas\nagents:\n  - Prometheus\n\n  - Sisyphus\n"
        result = _extract_agents_list(frontmatter)
        assert result == ["Prometheus", "Sisyphus"]

    def test_comment_lines_inside_block_skipped(self) -> None:
        """``#`` comment lines inside the block are skipped without stopping collection."""
        frontmatter = "name: Atlas\nagents:\n  - Prometheus\n  # placeholder\n  - Sisyphus\n"
        result = _extract_agents_list(frontmatter)
        assert result == ["Prometheus", "Sisyphus"]

    def test_new_key_after_list_terminates_collection(self) -> None:
        """A new YAML key that follows the list stops collection."""
        frontmatter = "name: Atlas\nagents:\n  - Prometheus\nmodel: gpt-4\n"
        result = _extract_agents_list(frontmatter)
        assert result == ["Prometheus"]

    def test_multi_word_name_resolves_l0_to_l2_violation(self, tmp_path: Path) -> None:
        """L0 ``agents:`` referencing a multi-word L2 agent name triggers a violation."""
        l2 = _write_agent(
            tmp_path,
            "Argus-subagent.agent.md",
            "Argus - QA Testing Subagent",
            "<!-- layer: 2 | parent: Sisyphus -->",
        )
        atlas = tmp_path / "Atlas.agent.md"
        atlas.write_text(
            "---\nname: Atlas\nagents:\n  - Argus - QA Testing Subagent\n---\n<!-- layer: 0 -->\n",
            encoding="utf-8",
        )
        _, violations = validate([atlas, l2])
        assert any("L0\u2192L2" in v or "L0->L2" in v or "L0\u2192L2" in v for v in violations) or any(
            "L0" in v and "L2" in v and "Argus" in v for v in violations
        ), f"Expected L0→L2 violation, got: {violations}"

    def test_unreadable_file_returns_empty_record(self, tmp_path: Path) -> None:
        """OSError while reading a file → empty AgentRecord without crashing."""
        p = tmp_path / "unreadable.agent.md"
        p.write_text("---\nname: X\n---\n<!-- layer: 1 -->\n", encoding="utf-8")
        p.chmod(0o000)
        try:
            rec = _parse_agent(p)
            assert rec.name is None
            assert rec.layer is None
            assert rec.agents_list == []
        finally:
            p.chmod(0o644)  # restore for tmp_path cleanup


# ---------------------------------------------------------------------------
# Optional runtime contract enforcement
# ---------------------------------------------------------------------------


class TestOptionalRuntimeContracts:
    """Optional agents (Hermes, Oracle, HEPHAESTUS) are validated when present
    but are never part of the mandatory core stable completeness set."""

    # -- valid contract passes -----------------------------------------------

    def test_valid_hermes_contract_passes(self, tmp_path: Path) -> None:
        """Hermes-subagent with a valid contract → no runtime-contract violation."""
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=_HERMES_CONTRACT,
        )
        _, violations = validate([p])
        assert not any("RUNTIME CONTRACT" in v for v in violations), violations

    def test_valid_oracle_contract_passes(self, tmp_path: Path) -> None:
        """Oracle-subagent with a valid contract → no runtime-contract violation."""
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=_ORACLE_CONTRACT,
        )
        _, violations = validate([p])
        assert not any("RUNTIME CONTRACT" in v for v in violations), violations

    def test_valid_hephaestus_contract_passes(self, tmp_path: Path) -> None:
        """HEPHAESTUS with a valid contract → no runtime-contract violation."""
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
            runtime_contract=_HEPHAESTUS_CONTRACT,
        )
        _, violations = validate([p])
        assert not any("RUNTIME CONTRACT" in v for v in violations), violations

    # -- missing contract yields violation when the agent is present ----------

    def test_missing_hermes_contract_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent present without a contract → MISSING RUNTIME CONTRACT violation."""
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
        )
        _, violations = validate([p])
        assert any(
            "MISSING RUNTIME CONTRACT" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    def test_missing_oracle_contract_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent present without a contract → MISSING RUNTIME CONTRACT violation."""
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
        )
        _, violations = validate([p])
        assert any(
            "MISSING RUNTIME CONTRACT" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    def test_missing_hephaestus_contract_yields_violation(self, tmp_path: Path) -> None:
        """HEPHAESTUS present without a contract → MISSING RUNTIME CONTRACT violation."""
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
        )
        _, violations = validate([p])
        assert any(
            "MISSING RUNTIME CONTRACT" in v and "HEPHAESTUS" in v
            for v in violations
        ), violations

    # -- invalid optional contract fields yield violation --------------------

    def test_wrong_role_in_hermes_contract_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent with wrong role → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=implementer | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "role" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    def test_missing_request_field_in_oracle_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent contract missing 'context' → REQUEST FIELDS violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=researcher | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,constraints | "
            "response=relevant_files,key_functions_classes,patterns_conventions,"
            "existing_tests,implementation_options,open_questions -->"
        )
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT REQUEST FIELDS" in v and "context" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    def test_missing_response_field_in_hephaestus_yields_violation(self, tmp_path: Path) -> None:
        """HEPHAESTUS contract missing 'evidence' → RESPONSE FIELDS violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=ops_specialist | layer=1 | "
            "accepts=Atlas | returns=Atlas | session=inherited | trace=required | "
            "request=mode,scope,environment,context | "
            "response=mode,status,actions_taken,issues_found,recommended_next_steps -->"
        )
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT RESPONSE FIELDS" in v and "evidence" in v and "HEPHAESTUS" in v
            for v in violations
        ), violations

    # -- no completeness coupling between optional agents --------------------

    def test_hermes_alone_does_not_require_oracle_or_hephaestus(self, tmp_path: Path) -> None:
        """Hermes present alone → no completeness or missing violation for Oracle/HEPHAESTUS."""
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=_HERMES_CONTRACT,
        )
        _, violations = validate([p])
        assert not any(
            ("Oracle-subagent" in v or "HEPHAESTUS" in v) and "MISSING" in v
            for v in violations
        ), violations

    def test_optional_agents_alone_do_not_trigger_stable_completeness(self, tmp_path: Path) -> None:
        """Hermes + Oracle present (no stable agents) → no MISSING STABLE AGENT violations."""
        files = [
            _write_agent(
                tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
                runtime_contract=_HERMES_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
                runtime_contract=_ORACLE_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        assert not any("MISSING STABLE AGENT" in v for v in violations), violations

    # -- core stable completeness behavior preserved -------------------------

    def test_stable_completeness_unaffected_by_optional_presence(self, tmp_path: Path) -> None:
        """All six stable agents plus Hermes → stable completeness satisfied, no spurious violations."""
        files = [
            _write_agent(
                tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
                runtime_contract=_ATLAS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
                runtime_contract=_PROMETHEUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
                runtime_contract=_SISYPHUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Argus-subagent.agent.md", "Argus - QA Testing Subagent", "<!-- layer: 1 -->",
                runtime_contract=_ARGUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
                runtime_contract=_HERMES_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        assert not any("MISSING STABLE AGENT" in v for v in violations), violations
        assert not any("RUNTIME CONTRACT" in v for v in violations), violations

    def test_stable_completeness_still_fails_when_one_stable_missing_and_optional_present(
        self, tmp_path: Path
    ) -> None:
        """Five stable agents + Hermes (Argus absent) → MISSING STABLE AGENT for Argus."""
        files = [
            _write_agent(
                tmp_path, "Atlas.agent.md", "Atlas", "<!-- layer: 0 -->",
                runtime_contract=_ATLAS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Prometheus.agent.md", "Prometheus", "<!-- layer: 1 -->",
                runtime_contract=_PROMETHEUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Sisyphus-subagent.agent.md", "Sisyphus-subagent", "<!-- layer: 1 -->",
                runtime_contract=_SISYPHUS_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Afrodita-subagent.agent.md", "Afrodita-subagent", "<!-- layer: 1 -->",
                runtime_contract=_AFRODITA_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Themis-subagent.agent.md", "Themis Subagent", "<!-- layer: 1 -->",
                runtime_contract=_THEMIS_CONTRACT,
            ),
            # Argus deliberately omitted
            _write_agent(
                tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
                runtime_contract=_HERMES_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        assert any(
            "MISSING STABLE AGENT" in v and "Argus - QA Testing Subagent" in v
            for v in violations
        ), violations

    # -- session / trace field enforcement for optional agents ---------------

    def test_missing_session_in_hermes_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent contract with session field absent → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=explorer | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | trace=required | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "session" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    def test_missing_trace_in_oracle_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent contract with trace field absent → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=researcher | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | "
            "request=goal,context,constraints | "
            "response=relevant_files,key_functions_classes,patterns_conventions,"
            "existing_tests,implementation_options,open_questions -->"
        )
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "trace" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    def test_wrong_session_in_hephaestus_yields_violation(self, tmp_path: Path) -> None:
        """HEPHAESTUS contract with session=required (should be inherited) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=ops_specialist | layer=1 | "
            "accepts=Atlas | returns=Atlas | session=required | trace=required | "
            "request=mode,scope,environment,context | "
            "response=mode,status,evidence,actions_taken,issues_found,recommended_next_steps -->"
        )
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "session" in v and "HEPHAESTUS" in v
            for v in violations
        ), violations

    def test_wrong_trace_in_hermes_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent contract with trace=optional (should be required) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=explorer | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | trace=optional | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "trace" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    # -- parity: version enforcement for optional agents --------------------

    def test_wrong_version_in_optional_agent_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent contract with wrong version string → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v0 | role=explorer | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "version" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    # -- parity: accepts drift rejected for Hermes and Oracle ---------------

    def test_wrong_accepts_in_hermes_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent with accepts=Atlas (should be parent-agent) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=explorer | layer=1 | "
            "accepts=Atlas | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "accepts" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    def test_wrong_accepts_in_oracle_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent with accepts=user (should be parent-agent) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=researcher | layer=1 | "
            "accepts=user | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,context,constraints | "
            "response=relevant_files,key_functions_classes,patterns_conventions,"
            "existing_tests,implementation_options,open_questions -->"
        )
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "accepts" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    # -- parity: all three optional agents valid together -------------------

    def test_all_three_optional_agents_valid_together_pass(self, tmp_path: Path) -> None:
        """Hermes-subagent + Oracle-subagent + HEPHAESTUS all valid contracts together
        → zero runtime-contract violations and no stable-completeness noise."""
        files = [
            _write_agent(
                tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
                runtime_contract=_HERMES_CONTRACT,
            ),
            _write_agent(
                tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
                runtime_contract=_ORACLE_CONTRACT,
            ),
            _write_agent(
                tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
                runtime_contract=_HEPHAESTUS_CONTRACT,
            ),
        ]
        _, violations = validate(files)
        rc_violations = [v for v in violations if "RUNTIME CONTRACT" in v]
        completeness_violations = [v for v in violations if "MISSING STABLE AGENT" in v]
        assert rc_violations == [], f"Unexpected runtime contract violations: {rc_violations}"
        assert completeness_violations == [], f"Unexpected completeness violations: {completeness_violations}"

    # -- parity: returns drift rejected for optional agents -----------------

    def test_wrong_returns_in_hermes_yields_violation(self, tmp_path: Path) -> None:
        """Hermes-subagent with returns=Atlas (should be parent-agent) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=explorer | layer=1 | "
            "accepts=parent-agent | returns=Atlas | session=inherited | trace=required | "
            "request=goal,scope,constraints | "
            "response=intent_analysis,files,answer,next_steps -->"
        )
        p = _write_agent(
            tmp_path, "Hermes-subagent.agent.md", "Hermes-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "returns" in v and "Hermes-subagent" in v
            for v in violations
        ), violations

    def test_wrong_returns_in_oracle_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent with returns=user (should be parent-agent) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=researcher | layer=1 | "
            "accepts=parent-agent | returns=user | session=inherited | trace=required | "
            "request=goal,context,constraints | "
            "response=relevant_files,key_functions_classes,patterns_conventions,"
            "existing_tests,implementation_options,open_questions -->"
        )
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "returns" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    def test_wrong_returns_in_hephaestus_yields_violation(self, tmp_path: Path) -> None:
        """HEPHAESTUS with returns=parent-agent (should be Atlas) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=ops_specialist | layer=1 | "
            "accepts=Atlas | returns=parent-agent | session=inherited | trace=required | "
            "request=mode,scope,environment,context | "
            "response=mode,status,evidence,actions_taken,issues_found,recommended_next_steps -->"
        )
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "returns" in v and "HEPHAESTUS" in v
            for v in violations
        ), violations

    # -- parity: version absent from optional agent contract ----------------

    def test_version_absent_from_optional_agent_contract_yields_violation(self, tmp_path: Path) -> None:
        """Oracle-subagent contract with version field absent → RUNTIME CONTRACT FIELD violation."""
        no_version_contract = (
            "<!-- runtime-contract | role=researcher | layer=1 | "
            "accepts=parent-agent | returns=parent-agent | session=inherited | trace=required | "
            "request=goal,context,constraints | "
            "response=relevant_files,key_functions_classes,patterns_conventions,"
            "existing_tests,implementation_options,open_questions -->"
        )
        p = _write_agent(
            tmp_path, "Oracle-subagent.agent.md", "Oracle-subagent", "<!-- layer: 1 -->",
            runtime_contract=no_version_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "version" in v and "Oracle-subagent" in v
            for v in violations
        ), violations

    # -- parity: accepts drift rejected for HEPHAESTUS ----------------------

    def test_wrong_accepts_in_hephaestus_yields_violation(self, tmp_path: Path) -> None:
        """HEPHAESTUS with accepts=parent-agent (should be Atlas) → RUNTIME CONTRACT FIELD violation."""
        bad_contract = (
            "<!-- runtime-contract | version=stable-runtime-v1 | role=ops_specialist | layer=1 | "
            "accepts=parent-agent | returns=Atlas | session=inherited | trace=required | "
            "request=mode,scope,environment,context | "
            "response=mode,status,evidence,actions_taken,issues_found,recommended_next_steps -->"
        )
        p = _write_agent(
            tmp_path, "HEPHAESTUS.agent.md", "HEPHAESTUS", "<!-- layer: 1 -->",
            runtime_contract=bad_contract,
        )
        _, violations = validate([p])
        assert any(
            "RUNTIME CONTRACT FIELD" in v and "accepts" in v and "HEPHAESTUS" in v
            for v in violations
        ), violations


# ---------------------------------------------------------------------------
# _collect_agent_files — isolated coverage
# ---------------------------------------------------------------------------


class TestCollectAgentFiles:
    """Direct coverage for ``_collect_agent_files`` using a temporary fake repo layout."""

    def test_discovers_github_agents_and_plugins(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Files in both ``.github/agents/`` and ``plugins/`` subdirs are returned."""
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "Atlas.agent.md").write_text("", encoding="utf-8")
        (agents_dir / "Prometheus.agent.md").write_text("", encoding="utf-8")

        plugin_dir = tmp_path / "plugins" / "extra"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "MyPlugin.agent.md").write_text("", encoding="utf-8")

        monkeypatch.setattr(_vlh, "REPO_ROOT", tmp_path)
        files = _collect_agent_files()
        names = {f.name for f in files}
        assert "Atlas.agent.md" in names
        assert "Prometheus.agent.md" in names
        assert "MyPlugin.agent.md" in names

    def test_returns_empty_when_neither_dir_exists(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Neither ``.github/agents`` nor ``plugins`` present → empty list, no crash."""
        monkeypatch.setattr(_vlh, "REPO_ROOT", tmp_path)
        files = _collect_agent_files()
        assert files == []

    def test_non_agent_md_files_excluded(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Plain ``.md`` files in ``agents/`` are not collected; only ``*.agent.md``."""
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "README.md").write_text("", encoding="utf-8")
        (agents_dir / "Atlas.agent.md").write_text("", encoding="utf-8")

        monkeypatch.setattr(_vlh, "REPO_ROOT", tmp_path)
        files = _collect_agent_files()
        names = {f.name for f in files}
        assert "README.md" not in names
        assert "Atlas.agent.md" in names


# ---------------------------------------------------------------------------
# Real workspace scan (integration)
# ---------------------------------------------------------------------------


class TestRealWorkspace:
    def test_full_system_scan_no_orphans_no_violations(self) -> None:
        """Full workspace scan → 0 orphans, 0 violations (all agents have layer comments)."""
        from pathlib import Path as P

        root_dir = REPO_ROOT / ".github" / "agents"
        plugins_dir = REPO_ROOT / "plugins"

        files: list[Path] = []
        if root_dir.is_dir():
            files.extend(sorted(root_dir.glob("*.agent.md")))
        if plugins_dir.is_dir():
            files.extend(sorted(plugins_dir.rglob("*.agent.md")))

        assert files, "No agent files found — workspace path may be wrong"
        _, violations = validate(files)
        orphans = [v for v in violations if "ORPHAN" in v]
        assert orphans == [], f"Unexpected orphans: {orphans}"
        assert violations == [], f"Unexpected violations: {violations}"
