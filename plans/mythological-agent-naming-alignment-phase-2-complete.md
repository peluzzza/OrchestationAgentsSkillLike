## Phase 2 Complete: Sync docs and mirror behavior
Aligned the live docs and plugin mirror with the renamed canonical pack so the change is consistent beyond filenames. The mirror `Atlas` and `Hephaestus` prompts now match the canonical root lifecycle more closely, and the main architecture document no longer reports stale agent counts for the orchestration-team pack.

**Files:** `README.md`, `.specify/memory/constitution.md`, `.specify/templates/constitution-template.md`, `docs/Atlas_Agents_Project_Document.md`, `plugins/README.md`, `plugins/atlas-orchestration-team/agents/Atlas.agent.md`, `plugins/atlas-orchestration-team/agents/Hephaestus.agent.md`
**Functions:** Hidden-agent roster docs, constitutional routing examples, Atlas mirror workflow lifecycle, Hephaestus mirror operations contract, architecture document pack inventory
**Implementation Scope:** Updated live docs to reference `Afrodita-UX`, `Atenea`, `Clio`, and `Ariadna`; kept `Hephaestus` explicitly in scope; resynced plugin mirror `Atlas` and `Hephaestus` with the canonical root prompts; corrected the orchestration-team pack counts from 9 to 19 and the total optional specialist count from 41+ to 51+
**Review:** APPROVED
**Testing (Argus):** PASSED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Prompt/doc diagnostics passed on the modified mirror/docs files; remaining editor warnings are environment-relative to the current VS Code agent registry rather than stale live references in the clone’s prompt/docs surfaces.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Operations Mode (if non-deploy):** N/A
**Operations Status:** N/A
- The status must be valid for the declared operations mode; do not mix tokens across modes.

**Git Commit:**
refactor: sync mythological naming surfaces

- align live docs and constitution with the renamed specialist pack
- resync plugin atlas and hephaestus prompts with the root pack
- fix stale orchestration-team agent counts in the project document
