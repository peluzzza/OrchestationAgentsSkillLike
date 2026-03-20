## Plan: Orchestation Agents Second Pass
This pass closes the gap between the repo’s documented Specify workflow and its committed assets. It bootstraps the missing root `.specify` layer, adds generic governance specialists, and wires Atlas/docs so the default root-only experience stays coherent without forcing duplicate plugin activation.

**Phases 3**
1. **Phase 1: Bootstrap Specify Root Assets**
   - **Objective:** Add the minimum root `.specify` files required by the existing Specify agents and README promises.
   - **Files/Functions:** `.specify/memory/constitution.md`, `.specify/templates/constitution-template.md`, `.specify/templates/spec-template.md`, `.specify/templates/plan-template.md`, `.specify/templates/tasks-template.md`
   - **QA Focus:** Validate root `.specify` references resolve cleanly and no current agent instructions point to missing mandatory templates.
   - **Steps:** 1. Adapt minimal templates from `spec-kit` to the repo’s root workflow. 2. Add a concrete constitution matching Atlas orchestration principles. 3. Keep advanced Spec Kit Plus assets deferred unless consumed.

2. **Phase 2: Add Governance Specialists**
   - **Objective:** Add generic root-level `Security`, `Documentation`, and `Dependencies` agents aligned with Atlas naming and routing conventions.
   - **Files/Functions:** `.github/agents/Security.agent.md`, `.github/agents/Documentation.agent.md`, `.github/agents/Dependencies.agent.md`, mirrored plugin pack copies if plugin parity is preserved.
   - **QA Focus:** Validate frontmatter, naming, handoffs, and activation-guard behavior are consistent with repo conventions.
   - **Steps:** 1. Adapt external specialist prompts from `/home/daniel/Descargas/agents/agents/`. 2. Normalize handoffs to `Atlas`. 3. Keep responsibilities narrow and complementary to existing domain packs.

3. **Phase 3: Wire Atlas And Align Docs**
   - **Objective:** Teach `Atlas` when to route through the new specialists and update repo docs to reflect the real root-first installation model.
   - **Files/Functions:** `.github/agents/Atlas.agent.md`, plugin mirror if needed, `README.md`, `plugins/README.md`
   - **QA Focus:** Validate the documented install path does not require duplicate agent source activation and that Atlas routing guidance is coherent.
   - **Steps:** 1. Add conditional routing for security, dependency, and documentation-sensitive work. 2. Align README Specify instructions with root `.specify` bootstrap. 3. Fix plugin docs count/drift if plugin pack remains shipped.

**Open Questions 2**
1. Should plugin pack files remain mirrored with root agents? Recommendation: yes for now, but keep `.github/agents` as the recommended default source.
2. Should ADR/PHR templates be added now? Recommendation: no; defer until an agent actually consumes them.
