## Phase 2 Complete: Sync mirrored and frontend workflow packs
Synchronized the mirrored `plugins/atlas-orchestration-team` prompts with the improved canonical core prompts, and updated the frontend workflow to a role-based model policy that stays close to the requested Flash-first strategy without introducing unsupported model labels. The mirror drift in `SpecifyImplement` was repaired and frontend conductors/planners/specialists now follow distinct role-appropriate distributions.

**Files:** `plugins/atlas-orchestration-team/agents/Atlas.agent.md`, `plugins/atlas-orchestration-team/agents/Prometheus.agent.md`, `plugins/atlas-orchestration-team/agents/Oracle.agent.md`, `plugins/atlas-orchestration-team/agents/Sisyphus.agent.md`, `plugins/atlas-orchestration-team/agents/Hermes.agent.md`, `plugins/atlas-orchestration-team/agents/Frontend-Engineer.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyAnalyze.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyClarify.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyConstitution.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyPlan.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifySpec.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyTasks.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyImplement.agent.md`, `plugins/frontend-workflow/agents/Afrodita.agent.md`, `plugins/frontend-workflow/agents/Frontend-Planner.agent.md`, `plugins/frontend-workflow/agents/UI-Designer.agent.md`, `plugins/frontend-workflow/agents/Style-Engineer.agent.md`, `plugins/frontend-workflow/agents/State-Manager.agent.md`, `plugins/frontend-workflow/agents/Component-Builder.agent.md`, `plugins/frontend-workflow/agents/A11y-Auditor.agent.md`, `plugins/frontend-workflow/agents/Frontend-Reviewer.agent.md`, `.github/agents/Frontend-Engineer.agent.md`
**Functions:** mirrored orchestration team prompts, frontend workflow conductor/planner/specialist model routing, mirrored SpecifyImplement cleanup
**Implementation Scope:** mirrored root improvements into plugin orchestration pack; normalized supported model labels in touched plugin files; aligned frontend workflow to conductor/planner/specialist role groupings; synchronized root/plugin `SpecifyImplement` escalation wording
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Prompt diagnostics checked on touched files; workspace-local unknown-agent warnings ignored because they reflect the active VS Code runtime rather than this repo’s local agent registry.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
refactor: sync mirrored and frontend agents

- mirror core prompt improvements into plugin orchestration pack
- update frontend workflow model routing by role
- fix mirrored specify implement prompt drift
