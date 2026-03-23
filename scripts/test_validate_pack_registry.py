"""Tests for validate_pack_registry."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parent / "validate_pack_registry.py"
_SPEC = importlib.util.spec_from_file_location("validate_pack_registry", MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError(f"Unable to load validator module from {MODULE_PATH}")

validator = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(validator)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_marketplace(sources: list[str]) -> dict:
    return {"plugins": [{"source": s} for s in sources]}


def _minimal_pack(
    pack_id: str,
    *,
    install_subdir: str = "some-pack",
    default_active: bool = False,
    marketplace_published: bool = False,
    stability: str = "stable",
    activation_path: str | None = "plugins/some-pack/agents",
) -> dict:
    return {
        "id": pack_id,
        "name": f"Pack {pack_id}",
        "installPath": install_subdir,
        "shipped": True,
        "defaultActive": default_active,
        "marketplacePublished": marketplace_published,
        "activationPath": activation_path,
        "conductor": "SomeConductor",
        "stability": stability,
    }


def _write_dir(root: Path, rel: str) -> Path:
    """Create a directory inside *root* and return it."""
    target = root / rel
    target.mkdir(parents=True, exist_ok=True)
    return target


# ---------------------------------------------------------------------------
# validate_registry — happy path
# ---------------------------------------------------------------------------


class TestValidRegistryPasses(unittest.TestCase):
    def test_single_default_active_pack_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        marketplace_published=False,
                        activation_path=None,
                    )
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertEqual([], errors)

    def test_multiple_packs_valid_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            _write_dir(root, "plugins/frontend-workflow")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        marketplace_published=False,
                        activation_path=None,
                    ),
                    _minimal_pack(
                        "frontend-workflow",
                        install_subdir="plugins/frontend-workflow",
                        default_active=False,
                        marketplace_published=False,
                        activation_path="plugins/frontend-workflow/agents",
                    ),
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertEqual([], errors)


# ---------------------------------------------------------------------------
# validate_registry — uniqueness / structural
# ---------------------------------------------------------------------------


class TestRegistryStructure(unittest.TestCase):
    def test_non_object_registry_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            errors = validator.validate_registry([], {"plugins": []}, root)
        self.assertTrue(any("registry: top-level JSON value must be an object" in e for e in errors))

    def test_non_object_pack_entry_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = {"packs": ["not-an-object"]}
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("pack at index 0 must be an object" in e for e in errors))

    def test_non_string_id_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            pack = _minimal_pack("pack-a", install_subdir="plugins/pack-a")
            pack["id"] = ["pack-a"]
            registry = {"packs": [pack]}
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("must have a non-empty string 'id'" in e for e in errors))

    def test_empty_string_id_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            pack = _minimal_pack("pack-a", install_subdir="plugins/pack-a")
            pack["id"] = ""
            registry = {"packs": [pack]}
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("must have a non-empty string 'id'" in e for e in errors))

    def test_duplicate_id_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir="plugins/pack-a",
                        default_active=True,
                        activation_path=None,
                    ),
                    _minimal_pack(
                        "canonical-root",
                        install_subdir="plugins/pack-a",
                    ),
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("duplicate id 'canonical-root'" in e for e in errors))

    def test_packs_not_a_list_reports_error(self) -> None:
        root = Path("/nonexistent")
        registry = {"packs": "not-a-list"}
        errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("'packs' must be a list" in e for e in errors))


# ---------------------------------------------------------------------------
# validate_registry — defaultActive rules
# ---------------------------------------------------------------------------


class TestDefaultActiveRules(unittest.TestCase):
    def test_zero_default_active_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            registry = {
                "packs": [
                    _minimal_pack("pack-a", install_subdir="plugins/pack-a")
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("expected exactly 1 defaultActive entry" in e for e in errors))

    def test_two_default_active_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            _write_dir(root, "plugins/pack-a")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        activation_path=None,
                    ),
                    _minimal_pack(
                        "pack-a",
                        install_subdir="plugins/pack-a",
                        default_active=True,
                        activation_path=None,
                    ),
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("expected exactly 1 defaultActive entry" in e for e in errors))

    def test_default_active_not_shipped_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            pack = _minimal_pack(
                "canonical-root",
                install_subdir=".github/agents",
                default_active=True,
                activation_path=None,
            )
            pack["shipped"] = False
            registry = {"packs": [pack]}
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("must have shipped: true" in e for e in errors))

    def test_default_active_marketplace_published_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            pack = _minimal_pack(
                "canonical-root",
                install_subdir=".github/agents",
                default_active=True,
                marketplace_published=True,
                activation_path=None,
            )
            marketplace = _minimal_marketplace(["canonical-root"])
            registry = {"packs": [pack]}
            errors = validator.validate_registry(registry, marketplace, root)
        self.assertTrue(any("must not have marketplacePublished: true" in e for e in errors))


# ---------------------------------------------------------------------------
# _validate_entry — field-level checks
# ---------------------------------------------------------------------------


class TestValidateEntry(unittest.TestCase):
    def test_missing_required_field_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("my-pack", install_subdir="missing")
        del pack["conductor"]
        errors = validator._validate_entry(pack, root)
        self.assertIn("my-pack: missing required field 'conductor'", errors)

    def test_non_boolean_shipped_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("my-pack", install_subdir="missing")
        pack["defaultActive"] = True
        pack["activationPath"] = None
        pack["shipped"] = "yes"
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("'shipped' must be a boolean" in e for e in errors))

    def test_non_default_active_null_activation_path_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="missing", activation_path=None)
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("non-defaultActive entry must supply" in e for e in errors))

    def test_invalid_stability_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="missing", stability="beta")
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("invalid stability 'beta'" in e for e in errors))

    def test_valid_stability_values_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            for s in ("stable", "preview", "experimental"):
                pack = _minimal_pack("pack-a", install_subdir="plugins/pack-a", stability=s)
                errors = validator._validate_entry(pack, root)
                stability_errors = [e for e in errors if "invalid stability" in e]
                self.assertEqual([], stability_errors, msg=f"stability '{s}' should be valid")

    def test_missing_install_path_dir_reports_error(self) -> None:
        root = Path("/nonexistent-root")
        pack = _minimal_pack("pack-a", install_subdir="plugins/no-such-dir")
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("does not exist on disk" in e for e in errors))


# ---------------------------------------------------------------------------
# _validate_marketplace_alignment
# ---------------------------------------------------------------------------


class TestMarketplaceAlignment(unittest.TestCase):
    def test_published_registry_missing_from_marketplace_reports_error(self) -> None:
        packs = [
            _minimal_pack("my-pack", marketplace_published=True)
        ]
        errors = validator._validate_marketplace_alignment(packs, {"plugins": []})
        self.assertTrue(
            any("marketplacePublished=true in registry but not found in marketplace.json" in e for e in errors)
        )

    def test_marketplace_entry_missing_from_registry_reports_error(self) -> None:
        packs: list[dict] = []
        marketplace = _minimal_marketplace(["orphan-pack"])
        errors = validator._validate_marketplace_alignment(packs, marketplace)
        self.assertTrue(
            any("present in marketplace.json but registry has no matching" in e for e in errors)
        )

    def test_aligned_registry_and_marketplace_passes(self) -> None:
        packs = [
            _minimal_pack("pub-pack", marketplace_published=True)
        ]
        marketplace = _minimal_marketplace(["pub-pack"])
        errors = validator._validate_marketplace_alignment(packs, marketplace)
        self.assertEqual([], errors)


# ---------------------------------------------------------------------------
# main — CLI integration
# ---------------------------------------------------------------------------


class TestMainIntegration(unittest.TestCase):
    def _write_registry(self, root: Path, packs: list[dict]) -> None:
        target = root / ".github" / "plugin"
        target.mkdir(parents=True, exist_ok=True)
        (target / "pack-registry.json").write_text(
            json.dumps({"version": "1.0.0", "packs": packs}), encoding="utf-8"
        )

    def _write_marketplace(self, root: Path, sources: list[str]) -> None:
        target = root / ".github" / "plugin"
        target.mkdir(parents=True, exist_ok=True)
        (target / "marketplace.json").write_text(
            json.dumps({"plugins": [{"source": s} for s in sources]}),
            encoding="utf-8",
        )

    def test_main_returns_zero_for_valid_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            self._write_registry(
                root,
                [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        activation_path=None,
                    )
                ],
            )
            self._write_marketplace(root, [])
            with mock.patch.object(validator, "REPO_ROOT", root), \
                 mock.patch.object(validator, "REGISTRY_PATH", root / ".github/plugin/pack-registry.json"), \
                 mock.patch.object(validator, "MARKETPLACE_PATH", root / ".github/plugin/marketplace.json"):
                result = validator.main()
        self.assertEqual(0, result)

    def test_main_returns_one_for_broken_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            # Two defaultActive entries — should fail
            self._write_registry(
                root,
                [
                    _minimal_pack(
                        "pack-a",
                        install_subdir="plugins/pack-a",
                        default_active=True,
                        activation_path=None,
                    ),
                    _minimal_pack(
                        "pack-b",
                        install_subdir="plugins/pack-a",
                        default_active=True,
                        activation_path=None,
                    ),
                ],
            )
            self._write_marketplace(root, [])
            with mock.patch.object(validator, "REPO_ROOT", root), \
                 mock.patch.object(validator, "REGISTRY_PATH", root / ".github/plugin/pack-registry.json"), \
                 mock.patch.object(validator, "MARKETPLACE_PATH", root / ".github/plugin/marketplace.json"):
                result = validator.main()
        self.assertEqual(1, result)

    def test_main_returns_one_when_registry_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(validator, "REGISTRY_PATH", root / "nonexistent.json"):
                result = validator.main()
        self.assertEqual(1, result)


# ---------------------------------------------------------------------------
# _validate_entry — edge-case hardening (QA review)
# ---------------------------------------------------------------------------


class TestValidateEntryEdgeCases(unittest.TestCase):
    def test_null_install_path_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="plugins/pack-a")
        pack["installPath"] = None
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("must be a non-empty string" in e for e in errors))

    def test_empty_string_install_path_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="plugins/pack-a")
        pack["installPath"] = ""
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("must be a non-empty string" in e for e in errors))

    def test_empty_string_activation_path_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="missing")
        pack["activationPath"] = ""
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("non-empty string 'activationPath'" in e for e in errors))

    def test_null_default_active_triggers_activation_path_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="missing")
        pack["defaultActive"] = None
        pack["activationPath"] = None
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("non-empty string 'activationPath'" in e for e in errors))

    def test_non_string_activation_path_reports_error(self) -> None:
        root = Path("/nonexistent")
        pack = _minimal_pack("pack-a", install_subdir="missing")
        pack["activationPath"] = ["plugins/pack-a/agents"]
        errors = validator._validate_entry(pack, root)
        self.assertTrue(any("non-empty string 'activationPath'" in e for e in errors))


# ---------------------------------------------------------------------------
# validate_registry — canonical-core defaultActive rule (QA review)
# ---------------------------------------------------------------------------


class TestCanonicalCoreDefaultActive(unittest.TestCase):
    def test_non_canonical_id_and_path_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, "plugins/pack-a")
            registry = {
                "packs": [
                    _minimal_pack(
                        "pack-a",
                        install_subdir="plugins/pack-a",
                        default_active=True,
                        activation_path=None,
                    )
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertTrue(any("must target the default-active root runtime surface" in e for e in errors))

    def test_canonical_install_path_passes_check(self) -> None:
        """installPath '.github/agents' qualifies even without id 'canonical-root'."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            registry = {
                "packs": [
                    _minimal_pack(
                        "my-custom-id",
                        install_subdir=".github/agents",
                        default_active=True,
                        activation_path=None,
                    )
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": []}, root)
        self.assertFalse(any("must target the default-active root runtime surface" in e for e in errors))


# ---------------------------------------------------------------------------
# main — additional edge-case coverage (QA review)
# ---------------------------------------------------------------------------


class TestMainIntegrationEdgeCases(unittest.TestCase):
    def _write_valid_registry(self, root: Path) -> None:
        plugin_dir = root / ".github" / "plugin"
        plugin_dir.mkdir(parents=True, exist_ok=True)
        (plugin_dir / "pack-registry.json").write_text(
            json.dumps(
                {
                    "version": "1.0.0",
                    "packs": [
                        _minimal_pack(
                            "canonical-root",
                            install_subdir=".github/agents",
                            default_active=True,
                            activation_path=None,
                        )
                    ],
                }
            ),
            encoding="utf-8",
        )

    def test_main_returns_one_when_marketplace_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            self._write_valid_registry(root)
            # marketplace.json intentionally NOT written
            with mock.patch.object(validator, "REPO_ROOT", root), \
                 mock.patch.object(validator, "REGISTRY_PATH", root / ".github/plugin/pack-registry.json"), \
                 mock.patch.object(validator, "MARKETPLACE_PATH", root / ".github/plugin/marketplace.json"):
                result = validator.main()
        self.assertEqual(1, result)

    def test_main_handles_malformed_registry_json_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plugin_dir = root / ".github" / "plugin"
            plugin_dir.mkdir(parents=True, exist_ok=True)
            (plugin_dir / "pack-registry.json").write_text("{invalid json}", encoding="utf-8")
            (plugin_dir / "marketplace.json").write_text("{}", encoding="utf-8")
            with mock.patch.object(validator, "REPO_ROOT", root), \
                 mock.patch.object(validator, "REGISTRY_PATH", root / ".github/plugin/pack-registry.json"), \
                 mock.patch.object(validator, "MARKETPLACE_PATH", root / ".github/plugin/marketplace.json"):
                result = validator.main()
        self.assertEqual(1, result)

    def test_main_handles_malformed_marketplace_json_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            self._write_valid_registry(root)
            plugin_dir = root / ".github" / "plugin"
            (plugin_dir / "marketplace.json").write_text("{invalid json}", encoding="utf-8")
            with mock.patch.object(validator, "REPO_ROOT", root), \
                 mock.patch.object(validator, "REGISTRY_PATH", root / ".github/plugin/pack-registry.json"), \
                 mock.patch.object(validator, "MARKETPLACE_PATH", root / ".github/plugin/marketplace.json"):
                result = validator.main()
        self.assertEqual(1, result)

    def test_validate_registry_rejects_non_object_marketplace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        activation_path=None,
                    )
                ]
            }
            errors = validator.validate_registry(registry, [], root)
        self.assertTrue(any("marketplace: top-level JSON value must be an object" in e for e in errors))

    def test_validate_registry_rejects_non_list_marketplace_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_dir(root, ".github/agents")
            registry = {
                "packs": [
                    _minimal_pack(
                        "canonical-root",
                        install_subdir=".github/agents",
                        default_active=True,
                        activation_path=None,
                    )
                ]
            }
            errors = validator.validate_registry(registry, {"plugins": None}, root)
        self.assertTrue(any("marketplace: 'plugins' must be a list" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
