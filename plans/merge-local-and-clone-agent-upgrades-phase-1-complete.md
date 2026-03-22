## Phase 1 Complete: Upgrade core orchestration prompts
Merged the clone’s strongest orchestration prompts with selected high-value guidance from the local pack, while updating the canonical `.github/agents` role-model ordering. The clone architecture remains the backbone; the imported local improvements are tactical and execution-focused rather than structural.

**Files:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Oracle.agent.md`, `.github/agents/Sisyphus.agent.md`, `.github/agents/Hermes.agent.md`, `.github/agents/Frontend-Engineer.agent.md`, `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyClarify.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`
**Functions:** Atlas conductor flow, Prometheus planning pipeline, Oracle research workflow, Sisyphus implementation hygiene, Hermes exploration policy, root frontend specialist model routing, Specify planning/implementation model routing
**Implementation Scope:** Updated role-model ordering for orchestrator/planning/implementation/exploration/frontend root agents; added stronger subagent briefing detail to Atlas; added generic skills-routing and parallel-research guidance to Prometheus/Oracle/Sisyphus; repaired corrupted `SpecifyImplement.agent.md`
**Review:** APPROVED
**Testing (Argus):** SKIPPED
- Coverage: Lines N/A, Branches N/A, Functions N/A
- Edge cases: Prompt syntax checked through diagnostics; workspace-local unknown-agent warnings ignored because they reflect the active VS Code runtime rather than this repo’s local agent registry.

**Deployment (Hephaestus):** N/A
- Env: N/A
- Health: N/A

**Git Commit:**
refactor: improve core agent prompts

- merge local execution guidance into core clone prompts
- update root role-based model ordering
- repair specify implement prompt structure
