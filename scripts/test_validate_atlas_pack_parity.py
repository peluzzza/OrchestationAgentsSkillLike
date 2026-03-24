"""Tests for validate_atlas_pack_parity.

The validator now treats .github/agents/ as the single source of truth for
all 79 agents. The plugins/atlas-orchestration-team/ source pack no longer
exists, so all source/parity logic has been removed.
"""

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

_VALID_MD = "---\nname: TestAgent\nuser-invocable: false\n---\n# body\n"
_VALID_MD_CRLF = "---\r\nname: TestAgent\r\nuser-invocable: false\r\n---\r\n# body\r\n"
_VALID_MD_BOM = "\ufeff---\nname: TestAgent\nuser-invocable: false\n---\n# body\n"
_INVALID_MD = "# No frontmatter block here\n"


def _write_agents(directory, names, content=_VALID_MD):
    for name in names:
        (directory / name).write_bytes(content.encode("utf-8"))


class TestNormalize(unittest.TestCase):
    def test_strips_bom(self): self.assertEqual(validator._normalize("\ufeffhello"), "hello")
    def test_normalizes_crlf(self): self.assertEqual(validator._normalize("a\r\nb"), "a\nb")
    def test_normalizes_bare_cr(self): self.assertEqual(validator._normalize("a\rb"), "a\nb")
    def test_clean_text_unchanged(self): self.assertEqual(validator._normalize("hello\nworld"), "hello\nworld")
    def test_empty_string(self): self.assertEqual(validator._normalize(""), "")


class TestCollectNames(unittest.TestCase):
    def test_finds_agent_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "Foo.agent.md").write_text("x")
            (d / "Bar.agent.md").write_text("x")
            (d / "other.md").write_text("x")
            self.assertEqual(validator._collect_names(d), frozenset({"Foo.agent.md", "Bar.agent.md"}))

    def test_empty_dir_returns_empty_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(validator._collect_names(Path(tmp)), frozenset())

    def test_ignores_non_agent_md_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "README.md").write_text("x")
            (d / "SKILL.md").write_text("x")
            self.assertEqual(validator._collect_names(d), frozenset())


class TestCheckRootAgents(unittest.TestCase):
    def _make_root(self, tmp):
        d = Path(tmp) / "root"; d.mkdir(); return d

    def test_passes_with_all_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS)
            self.assertEqual(validator.check_root_agents(root), [])

    def test_fails_on_missing_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS - {"Atlas.agent.md"})
            errors = validator.check_root_agents(root)
            self.assertTrue(any("Atlas.agent.md" in e and "agent missing" in e for e in errors), errors)

    def test_fails_on_unexpected_extra_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS)
            (root / "Surprise.agent.md").write_text(_VALID_MD)
            errors = validator.check_root_agents(root)
            self.assertTrue(any("Surprise.agent.md" in e and "unexpected file" in e for e in errors), errors)

    def test_fails_on_malformed_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS)
            (root / "Atlas.agent.md").write_text(_INVALID_MD)
            errors = validator.check_root_agents(root)
            self.assertTrue(any("Atlas.agent.md" in e and "frontmatter" in e for e in errors), errors)

    def test_passes_with_crlf_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS, content=_VALID_MD_CRLF)
            self.assertEqual(validator.check_root_agents(root), [])

    def test_passes_with_bom_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS, content=_VALID_MD_BOM)
            self.assertEqual(validator.check_root_agents(root), [])

    def test_error_count_for_multiple_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            subset = validator.ALL_AGENTS - {"Atlas.agent.md", "Clio.agent.md", "Argus.agent.md"}
            _write_agents(root, subset)
            errors = validator.check_root_agents(root)
            missing = [e for e in errors if "agent missing" in e]
            self.assertEqual(len(missing), 3)


class TestBackwardsCompatStubs(unittest.TestCase):
    def test_check_source_agents_always_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(validator.check_source_agents(Path(tmp)), [])

    def test_check_shared_content_always_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(validator.check_shared_content(Path(tmp), Path(tmp)), [])


class TestRunChecks(unittest.TestCase):
    def _make_root(self, tmp):
        d = Path(tmp) / "root"; d.mkdir(); return d

    def test_passes_with_all_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS)
            self.assertEqual(validator.run_checks(root_dir=root), [])

    def test_fails_on_missing_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS - {"Oracle.agent.md"})
            errors = validator.run_checks(root_dir=root)
            self.assertTrue(any("Oracle.agent.md" in e for e in errors), errors)

    def test_empty_dir_produces_expected_error_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            errors = validator.run_checks(root_dir=root)
            self.assertEqual(len(errors), len(validator.ALL_AGENTS))

    def test_all_agents_count(self):
        self.assertEqual(len(validator.ALL_AGENTS), 79)

    def test_source_dir_arg_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._make_root(tmp)
            _write_agents(root, validator.ALL_AGENTS)
            self.assertEqual(validator.run_checks(root_dir=root, source_dir=Path(tmp)), [])


class TestEdgeCases(unittest.TestCase):
    def test_canonical_shared_alias_still_works(self):
        self.assertIs(validator.CANONICAL_SHARED, validator.ALL_AGENTS)

    def test_root_only_is_empty(self):
        self.assertEqual(validator.ROOT_ONLY, frozenset())
