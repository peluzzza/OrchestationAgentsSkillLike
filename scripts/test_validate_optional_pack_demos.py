"""Tests for the optional-pack demo validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parent / "validate_optional_pack_demos.py"
SPEC = importlib.util.spec_from_file_location("validate_optional_pack_demos", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load validator module from {MODULE_PATH}")

validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidateOptionalPackDemosTests(unittest.TestCase):
    """Verify success and failure paths for demo validation."""

    def _create_demo(
        self,
        repo_root: Path,
        demo_name: str,
        plugin_path: str,
        *,
        include_prompt: bool = True,
        readme_text: str | None = None,
        prompt_text: str | None = None,
    ) -> Path:
        demo_path = repo_root / "demos" / demo_name
        demo_path.mkdir(parents=True, exist_ok=True)

        readme_content = readme_text or (
            "# Demo\n"
            "Canonical agents: .github/agents\n"
            "Optional plugin: "
            f"{plugin_path}\n"
            "Shared memory: .specify/memory/session-memory.md and .specify/memory/decision-log.md\n"
        )
        (demo_path / "README.md").write_text(readme_content, encoding="utf-8")

        if include_prompt:
            prompt_content = prompt_text or (
                "Use .github/agents plus the relevant plugin path only.\n"
                f"Enable {plugin_path}.\n"
                "Read .specify/memory/session-memory.md and .specify/memory/decision-log.md.\n"
            )
            (demo_path / "DEMO_PROMPT.md").write_text(prompt_content, encoding="utf-8")

        (demo_path / "module.py").write_text(
            '"""Demo module."""\n\nVALUE = 1\n',
            encoding="utf-8",
        )
        (demo_path / "test_module.py").write_text(
            "from __future__ import annotations\n\nimport unittest\n\n\n"
            "class DemoTests(unittest.TestCase):\n"
            "    def test_value(self) -> None:\n"
            "        self.assertEqual(1, 1)\n",
            encoding="utf-8",
        )
        return demo_path

    def test_collect_errors_accepts_valid_demo(self) -> None:
        """A valid demo directory should produce no validation errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "automation-mcp-workflow-smoke",
                "plugins/automation-mcp-workflow",
            )

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                errors = validator._collect_errors(
                    "automation-mcp-workflow-smoke",
                    "plugins/automation-mcp-workflow",
                )

        self.assertEqual([], errors)

    def test_collect_errors_reports_missing_demo_dir(self) -> None:
        """Missing demo directories should fail loudly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                errors = validator._collect_errors(
                    "automation-mcp-workflow-smoke",
                    "plugins/automation-mcp-workflow",
                )

        self.assertEqual(["automation-mcp-workflow-smoke: demo directory missing"], errors)

    def test_collect_errors_reports_missing_prompt(self) -> None:
        """Required prompt docs must exist for every demo."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "automation-mcp-workflow-smoke",
                "plugins/automation-mcp-workflow",
                include_prompt=False,
            )

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                errors = validator._collect_errors(
                    "automation-mcp-workflow-smoke",
                    "plugins/automation-mcp-workflow",
                )

        self.assertIn("automation-mcp-workflow-smoke: DEMO_PROMPT.md missing", errors)

    def test_collect_errors_reports_forbidden_phrase(self) -> None:
        """Docs should reject all-packs activation language."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "ux-enhancement-workflow-smoke",
                "plugins/ux-enhancement-workflow",
                readme_text=(
                    "# Demo\n"
                    "Canonical agents: .github/agents\n"
                    "Please enable all plugins for this demo.\n"
                ),
            )

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                errors = validator._collect_errors(
                    "ux-enhancement-workflow-smoke",
                    "plugins/ux-enhancement-workflow",
                )

        self.assertTrue(any("forbidden phrase 'enable all plugins'" in error for error in errors))

    def test_collect_errors_reports_missing_plugin_path(self) -> None:
        """The demo prompt must reference the specific plugin path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "ux-enhancement-workflow-smoke",
                "plugins/ux-enhancement-workflow",
                prompt_text=(
                    "Use .github/agents plus the relevant plugin path only.\n"
                    "Read .specify/memory/session-memory.md.\n"
                ),
            )

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                errors = validator._collect_errors(
                    "ux-enhancement-workflow-smoke",
                    "plugins/ux-enhancement-workflow",
                )

        self.assertIn(
            "ux-enhancement-workflow-smoke/DEMO_PROMPT.md: must reference the plugin path 'plugins/ux-enhancement-workflow'",
            errors,
        )

    def test_main_returns_zero_for_registered_clean_demos(self) -> None:
        """The CLI entrypoint should return zero when all demos are valid."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "automation-mcp-workflow-smoke",
                "plugins/automation-mcp-workflow",
            )
            self._create_demo(
                repo_root,
                "ux-enhancement-workflow-smoke",
                "plugins/ux-enhancement-workflow",
            )

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                result = validator.main()

        self.assertEqual(0, result)

    def test_main_returns_one_when_any_registered_demo_is_broken(self) -> None:
        """The CLI entrypoint should fail when one demo is incomplete."""
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._create_demo(
                repo_root,
                "automation-mcp-workflow-smoke",
                "plugins/automation-mcp-workflow",
            )

            broken_demo = self._create_demo(
                repo_root,
                "ux-enhancement-workflow-smoke",
                "plugins/ux-enhancement-workflow",
            )
            (broken_demo / "DEMO_PROMPT.md").unlink()

            with mock.patch.object(validator, "REPO_ROOT", repo_root):
                result = validator.main()

        self.assertEqual(1, result)


if __name__ == "__main__":
    unittest.main()