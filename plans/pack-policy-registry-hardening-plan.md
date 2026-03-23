## Plan: Pack Policy Registry Hardening
Make the repo policy for shipped packs machine-readable and validator-backed without changing the runtime default experience. The goal is to codify `shipped`, `default-active`, and `available-but-inactive` in one authoritative registry, then align validators and discovery surfaces to read from it.

**Phases 3**
1. **Phase 1: Add policy registry**
   - **Objective:** Introduce a single authoritative registry for shipped packs and activation policy.
   - **Files/Functions:** `.github/plugin/pack-registry.json`, `README.md`, `plugins/README.md`
   - **QA Focus:** Registry completeness, exactly one default-active pack, docs consistency with the new terminology.
   - **Steps:** 1. Add the registry with core-root plus all shipped plugin packs. 2. Mark only the canonical core as default-active. 3. Clarify docs so marketplace publication is a subset of shipped distribution.
2. **Phase 2: Make validators registry-aware**
   - **Objective:** Replace scattered hard-coded pack policy with registry-backed validation.
   - **Files/Functions:** `scripts/validate_pack_registry.py`, `scripts/test_validate_pack_registry.py`, `scripts/validate_plugin_packs.py`, `scripts/test_validate_plugin_packs.py`, `scripts/validate_optional_pack_demos.py`, `scripts/test_validate_optional_pack_demos.py`
   - **QA Focus:** Registry path validation, uniqueness rules, published-subset checks, demo coverage driven by registry metadata.
   - **Steps:** 1. Add a registry validator. 2. Refactor plugin-pack validation to consume the registry. 3. Refactor optional demo validation to derive demo packs from the registry. 4. Add/adjust unit tests.
3. **Phase 3: Align pack discovery consumers**
   - **Objective:** Make discovery surfaces distinguish shipped packs from marketplace-published packs.
   - **Files/Functions:** `plugins/agent-pack-catalog/agents/PackCatalog.agent.md`, `plugins/agent-pack-catalog/skills/agent-pack-search/SKILL.md`
   - **QA Focus:** Guidance accuracy for shipped-local vs marketplace-published packs.
   - **Steps:** 1. Update the catalog agent to read the registry first. 2. Update the search skill to use shipped-vs-published semantics. 3. Keep installation instructions honest for local-only packs.

**Open Questions 2**
1. Should `marketplace.json` remain the published subset only? Recommendation: yes.
2. Should local-only workflow packs get plugin manifests in this phase? Recommendation: no; keep scope focused on policy codification, not distribution expansion.
