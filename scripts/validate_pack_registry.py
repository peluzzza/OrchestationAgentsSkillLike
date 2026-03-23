"""Validate the pack policy registry for correctness and consistency.

Rules enforced:

1.  Registry file loads as valid JSON.
2.  Every entry has all required fields.
3.  ``id`` values are unique across all entries.
4.  Exactly one entry has ``defaultActive: true``.
5.  The ``defaultActive`` entry must be ``shipped: true``.
6.  The ``defaultActive`` entry must NOT be ``marketplacePublished: true``.
7.  Entries that are not ``defaultActive: true`` must supply a non-empty
    ``activationPath``.
8.  ``stability`` must be one of: experimental, preview, stable.
9.  Every ``marketplacePublished: true`` entry must appear in marketplace.json.
10. Every marketplace.json entry must match a registry entry with
    ``marketplacePublished: true``.
11. ``installPath`` must point to an existing directory on disk.
12. ``installPath`` must not be an empty string.
13. The single ``defaultActive: true`` entry must target the root runtime
    surface (``installPath`` equal to ``.github/agents``).

Usage::

    python3 scripts/validate_pack_registry.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / ".github" / "plugin" / "pack-registry.json"
MARKETPLACE_PATH = REPO_ROOT / ".github" / "plugin" / "marketplace.json"

REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "name",
    "installPath",
    "shipped",
    "defaultActive",
    "marketplacePublished",
    "activationPath",
    "conductor",
    "stability",
)

VALID_STABILITY: frozenset[str] = frozenset({"stable", "preview", "experimental"})


def load_json(path: Path) -> dict:
    """Load and return a JSON file as a dict."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_registry(registry: dict, marketplace: dict, repo_root: Path) -> list[str]:
    """Validate the registry against all policy rules.

    Args:
        registry: Parsed pack-registry.json content.
        marketplace: Parsed marketplace.json content.
        repo_root: Absolute path to the repository root (used for disk checks).

    Returns:
        List of error strings.  Empty list means the registry is valid.
    """
    if not isinstance(registry, dict):
        return ["registry: top-level JSON value must be an object"]

    if not isinstance(marketplace, dict):
        return ["marketplace: top-level JSON value must be an object"]

    errors: list[str] = []
    packs: list[dict] = registry.get("packs", [])

    if not isinstance(packs, list):
        return ["registry: 'packs' must be a list"]

    errors.extend(_validate_pack_entries(packs, repo_root))
    errors.extend(_validate_default_active_policy(packs))

    errors.extend(_validate_marketplace_alignment(packs, marketplace))
    return errors


def _validate_pack_entries(packs: list[dict], repo_root: Path) -> list[str]:
    """Validate each registry entry plus uniqueness constraints."""
    errors: list[str] = []
    seen_ids: set[str] = set()

    for idx, pack in enumerate(packs):
        if not isinstance(pack, dict):
            errors.append(f"registry: pack at index {idx} must be an object")
            continue

        errors.extend(_validate_pack_identity(pack, idx, seen_ids))
        errors.extend(_validate_entry(pack, repo_root))

    return errors


def _validate_pack_identity(pack: dict, idx: int, seen_ids: set[str]) -> list[str]:
    """Validate pack id type/uniqueness for one entry."""
    errors: list[str] = []
    raw_pack_id = pack.get("id")

    if not isinstance(raw_pack_id, str) or not raw_pack_id:
        errors.append(
            f"registry: pack at index {idx} must have a non-empty string 'id'"
        )
        return errors

    if raw_pack_id in seen_ids:
        errors.append(f"registry: duplicate id '{raw_pack_id}' at index {idx}")
    seen_ids.add(raw_pack_id)
    return errors


def _validate_default_active_policy(packs: list[dict]) -> list[str]:
    """Validate uniqueness and invariants for the default-active pack."""
    errors: list[str] = []
    default_active = [p for p in packs if isinstance(p, dict) and p.get("defaultActive") is True]
    if len(default_active) != 1:
        errors.append(
            f"registry: expected exactly 1 defaultActive entry,"
            f" found {len(default_active)}"
        )
        return errors

    da = default_active[0]
    if not da.get("shipped"):
        errors.append(
            f"registry: defaultActive entry '{da.get('id')}'"
            " must have shipped: true"
        )
    if da.get("marketplacePublished"):
        errors.append(
            f"registry: defaultActive entry '{da.get('id')}'"
            " must not have marketplacePublished: true"
        )
    if da.get("installPath") != ".github/agents":
        errors.append(
            f"registry: defaultActive entry '{da.get('id')}'"
            " must target the default-active root runtime surface"
            " (installPath '.github/agents')"
        )

    return errors


def _validate_entry(pack: dict, repo_root: Path) -> list[str]:
    """Validate a single pack entry against field and value rules."""
    errors: list[str] = []
    pack_id = pack.get("id", "<unknown>")

    for field in REQUIRED_FIELDS:
        if field not in pack:
            errors.append(f"{pack_id}: missing required field '{field}'")

    for bool_field in ("shipped", "defaultActive", "marketplacePublished"):
        value = pack.get(bool_field)
        if value is not None and not isinstance(value, bool):
            errors.append(
                f"{pack_id}: field '{bool_field}' must be a boolean,"
                f" got {type(value).__name__}"
            )

    errors.extend(_validate_paths(pack, repo_root, pack_id))

    stability = pack.get("stability")
    if stability is not None and stability not in VALID_STABILITY:
        errors.append(
            f"{pack_id}: invalid stability '{stability}';"
            f" must be one of {sorted(VALID_STABILITY)}"
        )

    return errors


def _validate_paths(pack: dict, repo_root: Path, pack_id: str) -> list[str]:
    """Validate activation/install path policy for one pack entry."""
    errors: list[str] = []

    activation_path = pack.get("activationPath")
    if pack.get("defaultActive") is not True:
        if not isinstance(activation_path, str) or not activation_path:
            errors.append(
                f"{pack_id}: non-defaultActive entry must supply"
                " a non-empty string 'activationPath'"
            )

    install_path = pack.get("installPath")
    if not isinstance(install_path, str) or not install_path:
        errors.append(f"{pack_id}: 'installPath' must be a non-empty string")
    elif not (repo_root / install_path).is_dir():
        errors.append(
            f"{pack_id}: installPath '{install_path}' does not exist on disk"
        )

    return errors


def _validate_marketplace_alignment(packs: list[dict], marketplace: dict) -> list[str]:
    """Cross-check registry marketplacePublished flags against marketplace.json."""
    errors: list[str] = []
    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list):
        return ["marketplace: 'plugins' must be a list"]

    published_in_registry: set[str] = {
        p["id"]
        for p in packs
        if isinstance(p, dict)
        and p.get("marketplacePublished")
        and isinstance(p.get("id"), str)
        and p.get("id")
    }
    marketplace_sources: set[str] = {
        entry["source"]
        for entry in plugins
        if isinstance(entry, dict)
        and isinstance(entry.get("source"), str)
        and entry.get("source")
    }

    for pack_id in sorted(published_in_registry):
        if pack_id not in marketplace_sources:
            errors.append(
                f"{pack_id}: marketplacePublished=true in registry"
                " but not found in marketplace.json"
            )

    for source in sorted(marketplace_sources):
        if source not in published_in_registry:
            errors.append(
                f"{source}: present in marketplace.json but registry has"
                " no matching marketplacePublished=true entry"
            )

    return errors


def main() -> int:
    """Run the pack registry validation.

    Returns:
        0 on success, 1 on any validation error.
    """
    if not REGISTRY_PATH.is_file():
        print(f"PACK REGISTRY VALIDATION FAILED: registry not found at {REGISTRY_PATH}")
        return 1

    if not MARKETPLACE_PATH.is_file():
        print(
            f"PACK REGISTRY VALIDATION FAILED:"
            f" marketplace not found at {MARKETPLACE_PATH}"
        )
        return 1

    try:
        registry = load_json(REGISTRY_PATH)
    except json.JSONDecodeError as exc:
        print(f"PACK REGISTRY VALIDATION FAILED: registry JSON is malformed: {exc}")
        return 1

    try:
        marketplace = load_json(MARKETPLACE_PATH)
    except json.JSONDecodeError as exc:
        print(f"PACK REGISTRY VALIDATION FAILED: marketplace JSON is malformed: {exc}")
        return 1

    errors = validate_registry(registry, marketplace, REPO_ROOT)

    if errors:
        print("PACK REGISTRY VALIDATION FAILED")
        for error in errors:
            print(f"  - {error}")
        return 1

    packs: list[dict] = registry.get("packs", [])
    print(f"PACK REGISTRY VALIDATION OK ({len(packs)} packs checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
