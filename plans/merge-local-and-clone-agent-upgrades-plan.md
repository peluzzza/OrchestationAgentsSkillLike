## Plan: Merge Local + Clone Agents
Merge the clone’s stronger orchestration architecture with the local pack’s best tactical guidance, then normalize agent model preferences to the requested 2026 role distribution. The result should keep the clone portable and disciplined while improving day-to-day execution quality and keeping mirrored/plugin packs consistent.

**Phases 3**
1. **Phase 1: Upgrade core orchestration prompts**
   - **Objective:** Improve the canonical `.github/agents` prompts by keeping the clone’s architecture and importing only the local pack’s highest-value guidance.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, `.github/agents/Prometheus.agent.md`, `.github/agents/Oracle.agent.md`, `.github/agents/Sisyphus.agent.md`, `.github/agents/Hermes.agent.md`, `.github/agents/Frontend-Engineer.agent.md`, `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyClarify.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`
   - **QA Focus:** Verify the merged prompts preserve clone-first orchestration flow, add the intended local improvements, and use the requested model order for orchestrator, planning, exploration, implementation, and frontend roles.
   - **Steps:** 1. Update the role-specific `model:` lists in canonical core agents. 2. Port targeted local improvements into Atlas, Prometheus, Oracle, and Sisyphus without replacing the clone’s stronger lifecycle structure. 3. Keep Hermes clone-style read-only behavior while updating exploration model priorities. 4. Update root frontend specialist to the requested frontend model ordering.

2. **Phase 2: Sync mirrored and frontend workflow packs**
   - **Objective:** Apply the same role-model policy and relevant prompt improvements to mirrored/plugin agent packs so distribution surfaces do not drift.
   - **Files/Functions:** `plugins/atlas-orchestration-team/agents/*.agent.md` counterparts for the edited core agents, `plugins/frontend-workflow/agents/Afrodita.agent.md`, `plugins/frontend-workflow/agents/Frontend-Planner.agent.md`, `plugins/frontend-workflow/agents/Component-Builder.agent.md`, `plugins/frontend-workflow/agents/UI-Designer.agent.md`, `plugins/frontend-workflow/agents/Style-Engineer.agent.md`, `plugins/frontend-workflow/agents/State-Manager.agent.md`, `plugins/frontend-workflow/agents/A11y-Auditor.agent.md`, `plugins/frontend-workflow/agents/Frontend-Reviewer.agent.md`
   - **QA Focus:** Verify mirrored atlas-orchestration agents stay aligned with `.github/agents`, and that the frontend workflow consistently uses the requested frontend/orchestrator/planning distributions.
   - **Steps:** 1. Mirror updated core agent changes into `plugins/atlas-orchestration-team/agents`. 2. Update frontend workflow conductor and specialist model lists according to frontend/planning/implementation categories. 3. Ensure no stale deprecated Gemini Pro model remains in the edited frontend files.

3. **Phase 3: Refresh strategy docs and validate consistency**
   - **Objective:** Bring model strategy documentation in line with the new prompt files and validate the repository for stale model references or prompt diagnostics.
   - **Files/Functions:** `plans/model-selection-strategy.md`, `plugins/README.md`, `docs/Atlas_Agents_Project_Document.md`
   - **QA Focus:** Confirm the docs match the implemented model policy and that edited prompt files parse cleanly with no stale role/model mismatches.
   - **Steps:** 1. Rewrite role-model strategy docs to reflect the new requested distribution and supported role groupings. 2. Update plugin README and architecture docs so they no longer advertise obsolete model assignments. 3. Run prompt diagnostics and targeted searches for stale/deprecated model references.

**Open Questions 2**
1. Should backend/devops/data workflow packs also be remapped to the new role distribution now?
   - **Option A:** Leave them unchanged and limit this change to the core orchestration team plus frontend workflow.
   - **Option B:** Infer categories across every workflow pack and remap them all now.
   - **Recommendation:** Option A for this pass, because the user explicitly named orchestration/planning/implementation/exploration/frontend categories and the greatest value is in the core pack plus frontend workflow.
2. Some requested model labels may differ from currently evidenced names in this workspace.
   - **Option A:** Use the requested labels exactly in prompt files.
   - **Option B:** Substitute only already-evidenced labels from the current workspace.
   - **Recommendation:** Use the requested labels exactly in the clone so the repo reflects the target policy, then validate prompt syntax locally and call out any runtime availability caveat if diagnostics complain.
