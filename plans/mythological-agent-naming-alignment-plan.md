## Plan: Mythological Agent Naming Alignment
Align the canonical root pack and its mirror with mythological specialist names so the agent taxonomy matches the desired style and keeps `Hephaestus` visibly in scope. The work replaces the remaining functional-name specialists, updates routing/docs, and then closes the loop with mirror/doc consistency validation.

**Phases 2**
1. **Phase 1: Rename core specialists**
   - **Objective:** Replace the remaining functional specialist identities in the canonical root pack and plugin mirror with mythological names.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Afrodita-UX.agent.md`, `.github/agents/Atenea.agent.md`, `.github/agents/Clio.agent.md`, `.github/agents/Ariadna.agent.md`, matching plugin mirror files, and deletion of legacy `Frontend-Engineer` / `Security` / `Documentation` / `Dependencies` files.
   - **QA Focus:** Verify the old functional identities are no longer live in the core pack and that `Hephaestus` remains explicitly routed and documented.
   - **Steps:** 1. Create mythological specialist files. 2. Retarget routing to the new names. 3. Remove the legacy functional-name files from root and mirror.

2. **Phase 2: Sync docs and mirror behavior**
   - **Objective:** Update live docs and mirror prompts so the rename is consistent beyond filenames.
   - **Files/Functions:** `README.md`, `.specify/memory/constitution.md`, `.specify/templates/constitution-template.md`, `docs/Atlas_Agents_Project_Document.md`, `plugins/README.md`, `plugins/atlas-orchestration-team/agents/Atlas.agent.md`, `plugins/atlas-orchestration-team/agents/Hephaestus.agent.md`.
   - **QA Focus:** Validate that live prompt/docs surfaces use the new mythological names consistently, that the mirror follows the canonical root flow, and that stale pack counts/references are gone.
   - **Steps:** 1. Refresh routing/docs references. 2. Resync mirror `Atlas` and `Hephaestus` from the canonical root behavior. 3. Run prompt/doc diagnostics and consistency sweeps.

**Open Questions 1**
1. Should the plugin mirror remain behaviorally identical to the root pack after naming changes?
   - **Recommendation:** Yes — keep `.github/agents` as canonical and resync the mirror whenever root lifecycle or governance routing changes.
