"""
Tests for SpecifyValidator — Specify Pipeline Demo

Test classes:
  TestConstitutionValidation  — unit tests with fixture file (always pass)
  TestSpecValidation          — unit tests with fixture file (always pass)
  TestPlanValidation          — unit tests with fixture file (always pass)
  TestTasksValidation         — unit tests with fixture file (always pass)
  TestValidateFile            — unit tests for file-not-found handling (always pass)
  TestPipelineIntegration     — SKIPPED until Specify pipeline runs via @Atlas
  TestImplementationSmoke     — SKIPPED until Sisyphus implements expenses.py

Run:
    py -m unittest -v
"""

import re
import unittest
from pathlib import Path

from spec_validator import CheckResult, PipelineReport, SpecifyValidator, ValidationResult

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SPECIFY_DIR = Path(__file__).parent / ".specify"
FEATURE_DIR = SPECIFY_DIR / "specs" / "expense-tracker"
EXPENSES_PY = Path(__file__).parent / "expenses.py"


def fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


# ================================================================== #
#  Unit tests — always pass, use fixture files                        #
# ================================================================== #

class TestConstitutionValidation(unittest.TestCase):
    """Validator logic against constitution_sample.md."""

    def setUp(self):
        self.v = SpecifyValidator()
        self.content = fixture("constitution_sample.md")

    def test_valid_constitution_passes(self):
        result = self.v.validate_constitution(self.content)
        self.assertTrue(
            result.passed,
            f"Failures: {[(c.name, c.detail) for c in result.failures]}"
        )

    def test_missing_principles_section_fails(self):
        bad = self.content.replace("## Principles", "## Philosophy")
        self.assertFalse(self.v.validate_constitution(bad).passed)

    def test_missing_version_metadata_fails(self):
        bad = "\n".join(l for l in self.content.splitlines() if "Version" not in l)
        self.assertFalse(self.v.validate_constitution(bad).passed)


class TestSpecValidation(unittest.TestCase):
    """Validator logic against spec_sample.md."""

    def setUp(self):
        self.v = SpecifyValidator()
        self.content = fixture("spec_sample.md")

    def test_valid_spec_passes(self):
        result = self.v.validate_spec(self.content)
        self.assertTrue(
            result.passed,
            f"Failures: {[(c.name, c.detail) for c in result.failures]}"
        )

    def test_missing_user_stories_section_fails(self):
        bad = self.content.replace("## User Stories", "## Stories")
        self.assertFalse(self.v.validate_spec(bad).passed)

    def test_missing_functional_requirements_section_fails(self):
        bad = self.content.replace("## Functional Requirements", "## Requirements")
        self.assertFalse(self.v.validate_spec(bad).passed)

    def test_missing_fr_references_fails(self):
        bad = re.sub(r"FR-\d{3}", "FUNC-001", self.content)
        self.assertFalse(self.v.validate_spec(bad).passed)

    def test_missing_given_when_then_fails(self):
        bad = (
            self.content
            .replace("Given", "Setup")
            .replace("When", "Action")
            .replace("Then", "Result")
        )
        self.assertFalse(self.v.validate_spec(bad).passed)


class TestPlanValidation(unittest.TestCase):
    """Validator logic against plan_sample.md."""

    def setUp(self):
        self.v = SpecifyValidator()
        self.content = fixture("plan_sample.md")

    def test_valid_plan_passes(self):
        result = self.v.validate_plan(self.content)
        self.assertTrue(
            result.passed,
            f"Failures: {[(c.name, c.detail) for c in result.failures]}"
        )

    def test_missing_technical_context_fails(self):
        bad = self.content.replace("## Technical Context", "## Context")
        self.assertFalse(self.v.validate_plan(bad).passed)

    def test_missing_implementation_phases_fails(self):
        bad = self.content.replace("## Implementation Phases", "## Phases")
        self.assertFalse(self.v.validate_plan(bad).passed)

    def test_missing_phase_headings_fails(self):
        bad = re.sub(r"### Phase \d+", "### Step", self.content)
        self.assertFalse(self.v.validate_plan(bad).passed)


class TestTasksValidation(unittest.TestCase):
    """Validator logic against tasks_sample.md."""

    def setUp(self):
        self.v = SpecifyValidator()
        self.content = fixture("tasks_sample.md")

    def test_valid_tasks_passes(self):
        result = self.v.validate_tasks(self.content)
        self.assertTrue(
            result.passed,
            f"Failures: {[(c.name, c.detail) for c in result.failures]}"
        )

    def test_insufficient_tasks_fails(self):
        bad = "- [ ] T001 Only one task\n- [ ] T002 Only two tasks\n"
        self.assertFalse(self.v.validate_tasks(bad).passed)

    def test_missing_t001_fails(self):
        bad = self.content.replace("T001", "T100")
        self.assertFalse(self.v.validate_tasks(bad).passed)

    def test_wrong_task_format_fails(self):
        bad = (
            "- [ ] TASK-001 wrong format\n"
            "- [ ] TASK-002 wrong format\n"
            "- [ ] TASK-003 wrong format\n"
        )
        self.assertFalse(self.v.validate_tasks(bad).passed)


class TestValidateFile(unittest.TestCase):
    """Edge cases for validate_file helper."""

    def setUp(self):
        self.v = SpecifyValidator()

    def test_nonexistent_file_returns_failed_result(self):
        result = self.v.validate_file(Path("nonexistent/path/spec.md"), "spec")
        self.assertFalse(result.passed)
        self.assertTrue(len(result.failures) > 0)
        self.assertIn("not found", result.failures[0].detail.lower())

    def test_valid_fixture_constitution_via_validate_file(self):
        result = self.v.validate_file(FIXTURES_DIR / "constitution_sample.md", "constitution")
        self.assertTrue(result.passed)

    def test_valid_fixture_tasks_via_validate_file(self):
        result = self.v.validate_file(FIXTURES_DIR / "tasks_sample.md", "tasks")
        self.assertTrue(result.passed)


# ================================================================== #
#  Integration tests — skipped until pipeline runs                   #
# ================================================================== #

_pipeline_reason = (
    f"\n\n  Pipeline artifacts not found at:\n  {FEATURE_DIR}\n\n"
    "  Run the full Specify pipeline first:\n"
    "  1. Open VS Code Copilot Chat\n"
    "  2. Paste the prompt from DEMO_PROMPT.md into @Atlas\n"
    "  3. Wait for Prometheus to complete SP-0..SP-5\n"
)


@unittest.skipUnless(FEATURE_DIR.exists(), _pipeline_reason)
class TestPipelineIntegration(unittest.TestCase):
    """
    Verify actual .specify/ artifacts generated by the Prometheus/Specify pipeline.

    SKIPPED until you run the pipeline via @Atlas.
    After the pipeline runs, these tests validate every artifact's structure.
    """

    def setUp(self):
        self.v = SpecifyValidator()

    def test_constitution_artifact_is_valid(self):
        result = self.v.validate_file(
            SPECIFY_DIR / "memory" / "constitution.md", "constitution"
        )
        self.assertTrue(
            result.passed,
            "constitution.md failures:\n" +
            "\n".join(f"  x {c.name}: {c.detail}" for c in result.failures)
        )

    def test_spec_artifact_is_valid(self):
        result = self.v.validate_file(FEATURE_DIR / "spec.md", "spec")
        self.assertTrue(
            result.passed,
            "spec.md failures:\n" +
            "\n".join(f"  x {c.name}: {c.detail}" for c in result.failures)
        )

    def test_plan_artifact_is_valid(self):
        result = self.v.validate_file(FEATURE_DIR / "plan.md", "plan")
        self.assertTrue(
            result.passed,
            "plan.md failures:\n" +
            "\n".join(f"  x {c.name}: {c.detail}" for c in result.failures)
        )

    def test_tasks_artifact_is_valid(self):
        result = self.v.validate_file(FEATURE_DIR / "tasks.md", "tasks")
        self.assertTrue(
            result.passed,
            "tasks.md failures:\n" +
            "\n".join(f"  x {c.name}: {c.detail}" for c in result.failures)
        )

    def test_data_model_artifact_exists(self):
        path = FEATURE_DIR / "data-model.md"
        self.assertTrue(
            path.exists(),
            f"data-model.md not found at {path}\n"
            "  SpecifyPlan (Phase 1) should have generated this artifact"
        )

    def test_research_artifact_exists(self):
        path = FEATURE_DIR / "research.md"
        self.assertTrue(
            path.exists(),
            f"research.md not found at {path}\n"
            "  SpecifyPlan (Phase 0) should have generated this artifact"
        )

    def test_full_pipeline_report_passes(self):
        report = self.v.validate_pipeline(FEATURE_DIR)
        report.print_report()
        self.assertTrue(
            report.passed,
            f"Pipeline validation failed: {report.summary}"
        )


# ================================================================== #
#  Smoke test — skipped until Sisyphus implements expenses.py         #
# ================================================================== #

_impl_reason = (
    "\n\n  expenses.py not found in demo folder.\n\n"
    "  Run the full pipeline (planning + implementation) via @Atlas,\n"
    "  or use the 'Full Pipeline' prompt from DEMO_PROMPT.md.\n"
)


@unittest.skipUnless(EXPENSES_PY.exists(), _impl_reason)
class TestImplementationSmoke(unittest.TestCase):
    """
    Smoke test for the implemented expense tracker CLI.

    SKIPPED until Sisyphus creates expenses.py.
    """

    def test_expenses_module_imports_cleanly(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("expenses", EXPENSES_PY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        has_entry = hasattr(module, "main") or hasattr(module, "ExpenseStore")
        self.assertTrue(
            has_entry,
            "expenses.py should expose main() or ExpenseStore class"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
