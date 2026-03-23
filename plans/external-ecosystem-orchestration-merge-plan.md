## Plan: External Ecosystem Merge
Este plan adapta la investigación de ecosistemas externos al repositorio `review_clones/OrchestationAgentsSkillLike`. La estrategia mantiene la raíz canónica del sistema, mueve capacidades externas a lanes claras por carpeta y evita convertir el repo en un Frankenstein con Wi‑Fi emocional inestable.

**Phases 5**
1. **Phase 1: Freeze Merge Lanes**
   - **Objective:** Document the target lanes, donor roles, and folder-by-folder adoption policy inside the orchestration repo.
   - **Files/Functions:** `plans/external-ecosystem-orchestration-investigation.md`, `plans/external-ecosystem-orchestration-merge-plan.md`, `README.md`, `plugins/README.md`
   - **QA Focus:** Validate docs align with current root-first architecture and do not imply unsupported runtime changes.
   - **Steps:** 1. Write investigation report. 2. Define merge phases. 3. Add README merge lanes. 4. Clarify plugin-space intent.

2. **Phase 2: Add Memory Lite Layer**
   - **Objective:** Introduce a lightweight memory strategy inspired by Claude-Mem without adding heavy infrastructure.
   - **Files/Functions:** `.specify/memory/`, memory guidance docs, relevant conductor references if needed
   - **QA Focus:** Validate memory conventions stay bounded, file-backed, and opt-in for workflow continuity.
   - **Steps:** 1. Define session and decision memory files. 2. Document write/read rules. 3. Wire only minimal references.

3. **Phase 3: Introduce Optional Automation And UX Packs**
   - **Objective:** Prepare plugin-pack lanes for MCP/automation and richer UI/UX specialization.
   - **Files/Functions:** `plugins/`, pack README/manifests, optional workflow conductors
   - **QA Focus:** Ensure packs remain optional and do not disturb the default root-only experience.
   - **Steps:** 1. Define automation pack contract. 2. Define UX enhancement pack scope. 3. Keep activation opt-in.

4. **Phase 4: Merge Utility Scripts And Demos**
   - **Objective:** Add operational helpers and focused demonstrations that validate the new capabilities.
   - **Files/Functions:** `scripts/`, `demos/`, optional validators
   - **QA Focus:** Validate scripts are narrow, demos are small, and documentation explains how to use them.
   - **Steps:** 1. Add sync/bootstrap helpers. 2. Add demo scenarios. 3. Add minimal validation scripts where useful.

5. **Phase 5: Clean Parity And Catalog Surface**
   - **Objective:** Keep root agents canonical while improving plugin catalog metadata and parity hygiene.
   - **Files/Functions:** `.github/plugin/`, parity helpers, docs
   - **QA Focus:** Validate no ambiguity exists about what is canonical, mirrored, experimental, or deprecated.
   - **Steps:** 1. Review marketplace metadata. 2. Add parity notes or tooling. 3. Trim drift-prone duplication.

**Open Questions 3**
1. Should memory live under `.specify/memory/` only, or also expose a top-level `memory/` directory? Recommendation: keep it under `.specify/memory/` first.
2. Should future plugin packs be mirrored from root agents automatically? Recommendation: only after parity tooling exists.
3. Which donor should drive the first optional pack: UX or MCP automation? Recommendation: MCP automation first if operator leverage is the priority; UX first if demo value is the priority.
