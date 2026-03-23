# Ariadna Dependency Audit Report

**Demo**: `demos/full-atlas-team-demo`
**Manifest**: `pyproject.toml`
**Date**: 2026-03-23
**Auditor**: Ariadna — dependency audit subagent
**Audit tool**: `pip-audit` (PyPI Advisory Database)

---

## Status: FAILED

**Summary**: The pinned dependency manifest contains **8 confirmed CVEs across 5 packages** (3 direct, 2 transitive). The most critical issues are: `python-multipart==0.0.5` carries three CVEs including a vulnerability published in 2026 (CVE-2026-24486); `starlette==0.27.0` (transitive via `fastapi`) carries two CVEs — one DoS advisory from 2024 and a 2025 advisory requiring `>=0.47.2`; and `pydantic==1.10.7` is on an **end-of-life v1 branch** with an unpatched ReDoS (CVE-2024-3772). Several packages are severely version-drifted: `uvicorn` is 22 minor versions behind (`0.20.0` vs `0.42.0`); `fastapi` is 40 minor versions behind (`0.95.2` vs `0.135.2`). No license concerns were identified — all packages are MIT or BSD licensed. **Immediate remediation is required before this manifest is used in any deployed environment.**

---

## Version Drift

### Runtime Dependencies

| Package | Pinned | Latest Stable | Gap |
|---------|--------|---------------|-----|
| `fastapi` | `0.95.2` | `0.135.2` | 40 minor versions |
| `uvicorn` | `0.20.0` | `0.42.0` | 22 minor versions |
| `pydantic` | `1.10.7` | `2.12.5` (v1 EOL: `1.10.21`) | EOL branch + 14 v1 patches missed |
| `python-multipart` | `0.0.5` | `0.0.22` | 17 patch versions |

### Dev Dependencies

| Package | Pinned | Latest Stable | Gap |
|---------|--------|---------------|-----|
| `pytest` | `7.3.1` | `9.0.2` | 2 major versions |
| `httpx` | `0.24.0` | `0.28.1` | 4 minor versions |
| `coverage` | `7.2.5` | `7.13.5` | 11 patch versions |

---

## CVE / Security Advisory Findings

### Direct Dependencies

- **[HIGH]** `python-multipart==0.0.5` — **CVE-2026-24486** (2026): Active vulnerability in multipart parsing. Fix: `>=0.0.22`. **Currently exposed.**
- **[HIGH]** `python-multipart==0.0.5` — **CVE-2024-53981**: Improper handling of malformed multipart Content-Type headers, potential remote DoS. Fix: `>=0.0.18`.
- **[HIGH]** `python-multipart==0.0.5` — **PYSEC-2024-38**: Content-Type boundary parsing allows form data bypass. Fix: `>=0.0.7`.
- **[MEDIUM]** `pydantic==1.10.7` — **CVE-2024-3772**: Regular expression denial-of-service (ReDoS) in `EmailStr` validation. Fix: `>=1.10.13` (v1 branch) or `>=2.4.0` (v2).
- **[MEDIUM]** `fastapi==0.95.2` — **PYSEC-2024-38**: Propagated from the starlette boundary vulnerability pulled in as a pinned transitive dep. Fix: `>=0.109.1`.

### Transitive Dependencies (pulled in by pinned versions above)

- **[HIGH]** `starlette==0.27.0` (via `fastapi==0.95.2`) — **CVE-2025-54121**: Unspecified vulnerability in request handling. Fix: `>=0.47.2` (requires `fastapi>=0.115.x`).
- **[HIGH]** `starlette==0.27.0` (via `fastapi==0.95.2`) — **CVE-2024-47874**: Denial of service via multipart upload abuse. Fix: `>=0.40.0` (requires `fastapi>=0.109.x`).
- **[MEDIUM]** `h11==0.14.0` (via `uvicorn==0.20.0`) — **CVE-2025-43859**: HTTP/1.1 protocol parsing flaw allowing request smuggling or connection spoofing. Fix: `>=0.16.0` (requires `uvicorn>=0.34.0`).

**Total: 8 confirmed CVEs in 5 packages (pip-audit exit code 1)**

---

## EOL / Maintenance Risk

- **[HIGH]** `pydantic==1.10.7` — Pydantic **v1 is end-of-life** since the release of v2 (June 2023). The author team has stated that only critical security patches may be backported; all feature development, performance improvements, and bug fixes target v2 exclusively. Running on v1 accumulates compounding technical debt.

---

## License Assessment

All packages use MIT or BSD-3-Clause licences. No GPL, LGPL, AGPL, or proprietary licences detected. No CLA requirements. **No license concerns.**

---

## Recommended Actions

*(Prioritised by urgency)*

### Immediate — block-on-merge

1. **Upgrade `python-multipart` to `0.0.22`**
   - Resolves: CVE-2026-24486, CVE-2024-53981, PYSEC-2024-38
   - Blast radius: **LOW** — drop-in patch upgrade, no API changes.
   - Action: `python-multipart==0.0.22`

2. **Upgrade `fastapi` to `0.135.2`**
   - Resolves: PYSEC-2024-38 (direct), CVE-2024-47874 and CVE-2025-54121 (via starlette transitive fix)
   - Blast radius: **MEDIUM** — fastapi 0.100+ deprecates `response_model_include/exclude` as direct constructor arguments; review any custom response models. Python 3.6/3.7 support dropped (not relevant here). `Depends()` ordering changes in 0.110+.
   - Action: `fastapi==0.135.2`

3. **Upgrade `uvicorn` to `0.42.0`**
   - Resolves: CVE-2025-43859 (via h11 transitive fix; h11>=0.16.0 pulled in at uvicorn>=0.34.0)
   - Blast radius: **LOW** — primarily internal changes. Default `--host` changed from `127.0.0.1` to explicit in some contexts; pin `--host 0.0.0.0` explicitly in startup scripts/Dockerfiles.
   - Action: `uvicorn==0.42.0`

### Short-term — next sprint

4. **Upgrade `pydantic` to `1.10.21`** (v1 branch — minimum safe)
   - Resolves: CVE-2024-3772 (ReDoS in EmailStr)
   - Blast radius: **LOW** — patch within v1, no API changes.
   - Action: `pydantic==1.10.21`
   - **Note**: This is a stopgap only. See item 8 for the full v2 migration.

5. **Upgrade `pytest` to `9.0.2`**
   - No CVEs; maintenance currency and compatibility with modern Python.
   - Blast radius: **MEDIUM** — pytest 8 dropped legacy `@pytest.mark` parametrize string parsing and changed `pytest.warns` strict semantics. Run the test suite before committing.
   - Action: `pytest==9.0.2`

6. **Upgrade `httpx` to `0.28.1`**
   - No CVEs; httpx 0.27+ removed deprecated `AsyncClient.send` transport overrides.
   - Blast radius: **LOW** — verify `TestClient` usage in `test_full_team_harness.py` and `test_task_stats.py`.
   - Action: `httpx==0.28.1`

7. **Upgrade `coverage` to `7.13.5`**
   - Patch-level only; no API changes, no CVEs.
   - Blast radius: **VERY LOW**.
   - Action: `coverage==7.13.5`

### Planned — tracked technical debt

8. **Migrate `pydantic` from v1 to v2** (`pydantic==2.12.5`)
   - Blast radius: **HIGH** — all model definitions, `@validator` decorators → `@field_validator`, `Config` class → `model_config = ConfigDict(...)`, `.dict()` → `.model_dump()`, `.json()` → `.model_dump_json()`. Use the `pydantic.v1` compatibility shim for staged migration.
   - Recommendation: Migrate in isolation before co-upgrading fastapi; verify with the existing test suite at each step.

---

## Suggested `pyproject.toml` Patch (immediate fixes only)

```toml
dependencies = [
    "fastapi==0.135.2",
    "uvicorn==0.42.0",
    "pydantic==1.10.21",          # stopgap; plan v2 migration
    "python-multipart==0.0.22",
]

[project.optional-dependencies]
dev = [
    "pytest==9.0.2",
    "httpx==0.28.1",
    "coverage==7.13.5",
]
```

---

## Next Steps for Atlas

`Status: FAILED` — **Do not deploy or promote this manifest without applying at minimum items 1–3.**

1. Apply the `pyproject.toml` patch above.
2. Re-run `pip-audit` and confirm **0 known vulnerabilities**.
3. Run `py -m pytest` to validate no regressions from the fastapi/uvicorn/httpx upgrades.
4. Open a tracked work item for the pydantic v2 migration (item 8).
