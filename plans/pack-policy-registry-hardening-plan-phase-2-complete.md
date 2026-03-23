## Phase 2 Complete: Make validators registry-aware
Replaced scattered pack-policy assumptions with registry-backed validation and hardened the validator against malformed data. The new registry validator now checks canonical default-active behavior, marketplace alignment, malformed path fields, and malformed entry structures with deterministic failures instead of traceback surprises.

**Files:** `scripts/validate_pack_registry.py`, `scripts/test_validate_pack_registry.py`, `scripts/validate_optional_pack_demos.py`, `scripts/test_validate_optional_pack_demos.py`
**Functions:** `validate_registry`, `_validate_pack_entries`, `_validate_pack_identity`, `_validate_default_active_policy`, `_validate_entry`, `_validate_paths`, `_validate_marketplace_alignment`, `_load_demo_packs`
**Implementation Scope:** Added new registry validator + tests, moved demo coverage discovery to the registry, hardened JSON/path/entry validation for malformed inputs.
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines 99%, Functions 100% on `validate_pack_registry.py`
- Edge cases: malformed JSON, missing marketplace file, null/empty/non-string path fields, non-object pack entries, invalid ids, canonical default-active invariants

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A

**Git Commit:**
feat: harden pack registry validation

- add registry-backed policy validator and tests
- derive optional demo coverage from pack registry
- reject malformed pack entries and invalid path fields
