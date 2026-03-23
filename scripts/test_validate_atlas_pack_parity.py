"""Tests for validate_atlas_pack_parity."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent / "validate_atlas_pack_parity.py"
)
_SPEC = importlib.util.spec_from_file_location(
    "validate_atlas_pack_parity", MODULE_PATH
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(
        f"Unable to load validator module from {MODULE_PATH}"
    )
validator = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(validator)  # type: ignore[union-attr]

# ---------------------------------------------------------------------------
# Shared test fixtures
# ---------------------------------------------------------------------------

_VALID_MD = "---\nname: TestAgent\nuser-invocable: false\n---\n# body\n"
_VALID_MD_CRLF = (
    "---\r\nname: TestAgent\r\nuser-invocable: false\r\n---\r\n# body\r\n"
)
_VALID_MD_BOM = (
    "\ufeff---\nname: TestAgent\nuser-invocable: false\n---\n# body\n"
)
_INVALID_MD = "# No frontmatter block here\n"


def _write_agents(
    directory: Path,
    names: frozenset[str],
    content: str = _VALID_MD,
) -> None:
    """Write *content* for every filename in *names* under *directory*."""
    for name in names:
        (directory / name).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# _normalize
# ---------------------------------------------------------------------------


class TestNormalize(unittest.TestCase):
    def test_strips_bom(self) -> None:
        self.assertEqual(validator._normalize("\ufeffhello"), "hello")

    def test_normalizes_crlf(self) -> None:
        self.assertEqual(validator._normalize("a\r\nb"), "a\nb")

    def test_normalizes_bare_cr(self) -> None:
        self.assertEqual(validator._normalize("a\rb"), "a\nb")

    def test_clean_text_unchanged(self) -> None:
        self.assertEqual(
            validator._normalize("hello\nworld"), "hello\nworld"
        )

    def test_empty_string(self) -> None:
        self.assertEqual(validator._normalize(""), "")


# ---------------------------------------------------------------------------
# _collect_names
# ---------------------------------------------------------------------------


class TestCollectNames(unittest.TestCase):
    def test_finds_agent_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "Foo.agent.md").write_text("x")
            (d / "Bar.agent.md").write_text("x")
            (d / "other.md").write_text("x")
            (d / "notes.txt").write_text("x")
            result = validator._collect_names(d)
            self.assertEqual(
                result, frozenset({"Foo.agent.md", "Bar.agent.md"})
            )

    def test_empty_dir_returns_empty_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                validator._collect_names(Path(tmp)), frozenset()
            )

    def test_ignores_non_agent_md_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "README.md").write_text("x")
            (d / "SKILL.md").write_text("x")
            self.assertEqual(validator._collect_names(d), frozenset())


# ---------------------------------------------------------------------------
# check_root_agents
# ---------------------------------------------------------------------------


class TestCheckRootAgents(unittest.TestCase):
    def _make_root(self, tmp: str) -> Path:
        d = Path(tmp) / "root"
        d.mkdir()
        return d

    def test_passes_with_complete_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(
                root, validator.CANONICAL_SHARED | validator.ROOT_ONLY
            )
            self.assertEqual(validator.check_root_agents(root), [])

    def test_fails_on_missing_shared_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(
                root,
                (validator.CANONICAL_SHARED - {"Atlas.agent.md"})
                | validator.ROOT_ONLY,
            )
            errors = validator.check_root_agents(root)
            self.assertTrue(
                any(
                    "Atlas.agent.md" in e and "shared agent missing" in e
                    for e in errors
                ),
                errors,
            )

    def test_fails_on_missing_root_only_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(
                root,
                validator.CANONICAL_SHARED
                | (validator.ROOT_ONLY - {"Sisyphus-subagent.agent.md"}),
            )
            errors = validator.check_root_agents(root)
            self.assertTrue(
                any("Sisyphus-subagent.agent.md" in e for e in errors),
                errors,
            )

    def test_fails_on_unexpected_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(
                root, validator.CANONICAL_SHARED | validator.ROOT_ONLY
            )
            (root / "Surprise.agent.md").write_text(_VALID_MD)
            errors = validator.check_root_agents(root)
            self.assertTrue(
                any(
                    "Surprise.agent.md" in e and "unexpected file" in e
                    for e in errors
                ),
                errors,
            )

    def test_error_count_for_multiple_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            subset = validator.CANONICAL_SHARED - {
                "Atlas.agent.md",
                "Clio.agent.md",
                "Argus.agent.md",
            }
            _write_agents(root, subset | validator.ROOT_ONLY)
            errors = validator.check_root_agents(root)
            missing = [e for e in errors if "shared agent missing" in e]
            self.assertEqual(len(missing), 3)


# ---------------------------------------------------------------------------
# check_source_agents
# ---------------------------------------------------------------------------


class TestCheckSourceAgents(unittest.TestCase):
    def _make_source(self, tmp: str) -> Path:
        d = Path(tmp) / "source"
        d.mkdir()
        return d

    def test_passes_with_complete_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(source, validator.CANONICAL_SHARED)
            self.assertEqual(validator.check_source_agents(source), [])

    def test_fails_on_missing_shared_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(
                source,
                validator.CANONICAL_SHARED - {"Prometheus.agent.md"},
            )
            errors = validator.check_source_agents(source)
            self.assertTrue(
                any(
                    "Prometheus.agent.md" in e and "shared agent missing" in e
                    for e in errors
                ),
                errors,
            )

    def test_fails_on_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(source, validator.CANONICAL_SHARED)
            (source / "Extra.agent.md").write_text(_VALID_MD)
            errors = validator.check_source_agents(source)
            self.assertTrue(
                any(
                    "Extra.agent.md" in e and "unexpected extra file" in e
                    for e in errors
                ),
                errors,
            )

    def test_fails_if_root_only_alias_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(source, validator.CANONICAL_SHARED)
            (source / "Sisyphus-subagent.agent.md").write_text(_VALID_MD)
            errors = validator.check_source_agents(source)
            self.assertTrue(
                any(
                    "Sisyphus-subagent.agent.md" in e
                    and "must not appear in source" in e
                    for e in errors
                ),
                errors,
            )

    def test_all_root_only_aliases_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(
                source,
                validator.CANONICAL_SHARED | validator.ROOT_ONLY,
            )
            errors = validator.check_source_agents(source)
            blocked = [e for e in errors if "must not appear in source" in e]
            self.assertEqual(len(blocked), len(validator.ROOT_ONLY))

    def test_fails_on_malformed_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(source, validator.CANONICAL_SHARED)
            (source / "Atlas.agent.md").write_text(_INVALID_MD)
            errors = validator.check_source_agents(source)
            self.assertTrue(
                any("Atlas.agent.md" in e and "frontmatter" in e for e in errors),
                errors,
            )

    def test_passes_with_crlf_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(
                source, validator.CANONICAL_SHARED, content=_VALID_MD_CRLF
            )
            self.assertEqual(validator.check_source_agents(source), [])

    def test_passes_with_bom_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            _write_agents(
                source, validator.CANONICAL_SHARED, content=_VALID_MD_BOM
            )
            self.assertEqual(validator.check_source_agents(source), [])

    def test_passes_with_crlf_bom_combined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = self._make_source(tmp)
            bom_crlf = (
                "\ufeff---\r\nname: A\r\nuser-invocable: false\r\n"
                "---\r\n# ok\r\n"
            )
            _write_agents(
                source, validator.CANONICAL_SHARED, content=bom_crlf
            )
            self.assertEqual(validator.check_source_agents(source), [])


class TestCheckSharedContent(unittest.TestCase):
    def _make_dirs(self, tmp: str) -> tuple[Path, Path]:
        root = Path(tmp) / "root"
        root.mkdir()
        source = Path(tmp) / "source"
        source.mkdir()
        return root, source

    def test_detects_content_drift_for_shared_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            _write_agents(root, validator.CANONICAL_SHARED | validator.ROOT_ONLY)
            _write_agents(source, validator.CANONICAL_SHARED)
            (source / "Atlas.agent.md").write_text(
                "---\nname: Different\nuser-invocable: true\n---\n# changed\n",
                encoding="utf-8",
            )

            errors = validator.check_shared_content(root, source)

        self.assertIn("parity: root runtime drift detected from source -> Atlas.agent.md", errors)

    def test_ignores_bom_and_crlf_only_differences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            _write_agents(root, validator.CANONICAL_SHARED | validator.ROOT_ONLY, content=_VALID_MD)
            _write_agents(source, validator.CANONICAL_SHARED, content=_VALID_MD_BOM.replace("\n", "\r\n"))

            errors = validator.check_shared_content(root, source)

        self.assertEqual([], errors)


# ---------------------------------------------------------------------------
# run_checks  (integration)
# ---------------------------------------------------------------------------


class TestRunChecks(unittest.TestCase):
    def _make_dirs(self, tmp: str) -> tuple[Path, Path]:
        root = Path(tmp) / "root"
        root.mkdir()
        source = Path(tmp) / "source"
        source.mkdir()
        return root, source

    def test_passes_with_valid_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            _write_agents(
                root, validator.CANONICAL_SHARED | validator.ROOT_ONLY
            )
            _write_agents(source, validator.CANONICAL_SHARED)
            self.assertEqual(
                validator.run_checks(root_dir=root, source_dir=source), []
            )

    def test_aggregates_errors_from_both_sides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            _write_agents(
                root,
                (validator.CANONICAL_SHARED - {"Oracle.agent.md"})
                | validator.ROOT_ONLY,
            )
            _write_agents(
                source,
                validator.CANONICAL_SHARED - {"Oracle.agent.md"},
            )
            (source / "Intruder.agent.md").write_text(_VALID_MD)
            errors = validator.run_checks(root_dir=root, source_dir=source)
            # root missing Oracle, source missing Oracle, source extra Intruder
            self.assertGreaterEqual(len(errors), 3)

    def test_includes_content_drift_in_aggregated_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            _write_agents(root, validator.CANONICAL_SHARED | validator.ROOT_ONLY)
            _write_agents(source, validator.CANONICAL_SHARED)
            (source / "Prometheus.agent.md").write_text(
                "---\nname: Prometheus\nuser-invocable: false\n---\n# drift\n",
                encoding="utf-8",
            )

            errors = validator.run_checks(root_dir=root, source_dir=source)

        self.assertIn("parity: root runtime drift detected from source -> Prometheus.agent.md", errors)

    def test_empty_dirs_produce_expected_error_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, source = self._make_dirs(tmp)
            errors = validator.run_checks(root_dir=root, source_dir=source)
            expected = (
                len(validator.CANONICAL_SHARED) * 2
                + len(validator.ROOT_ONLY)
            )
            self.assertEqual(len(errors), expected)

    def test_canonical_shared_count(self) -> None:
        self.assertEqual(len(validator.CANONICAL_SHARED), 19)

    def test_root_only_count(self) -> None:
        self.assertEqual(len(validator.ROOT_ONLY), 7)


if __name__ == "__main__":
    unittest.main()
