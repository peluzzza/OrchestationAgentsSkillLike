## Plan: Agent Pack Compatibility
Normalize the active root agent pack so imported subagent-style names exist, Atlas/Prometheus reference runtime-safe names, and unsupported tool identifiers are removed from active frontmatter.

**Phases 3**
1. **Phase 1: Diagnose active pack**
   - **Objective:** Confirm which root files are active and which diagnostics are actually blocking runtime compatibility.
   - **Files/Functions:** `.vscode/settings.json`, `.github/agents/Prometheus.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `.github/agents/Afrodita-UX.agent.md`
   - **QA Focus:** Confirm the active pack is only `.github/agents` and capture exact failing names/tools.
   - **Steps:** 1. Inspect active agent loading settings. 2. Read the blocking root agent files. 3. Gather diagnostics and suspicious tool identifiers.
2. **Phase 2: Add compatibility aliases**
   - **Objective:** Add missing subagent-style aliases directly into the root active pack so imported prompts can resolve them.
   - **Files/Functions:** New `.github/agents/*-subagent.agent.md` files for Hermes, Oracle, Sisyphus, Afrodita, Argus, Themis, Hephaestus
   - **QA Focus:** Ensure each new alias uses only supported tools and has a valid runtime-facing name.
   - **Steps:** 1. Create minimal, functional alias agents. 2. Keep each alias scoped to its specialist role. 3. Avoid unsupported tools or dead references.
3. **Phase 3: Rewire and validate**
   - **Objective:** Point root orchestrators to the new aliases and clean unsupported tools in active files.
   - **Files/Functions:** `Atlas.agent.md`, `Prometheus.agent.md`, `SpecifySpec.agent.md`, `SpecifyPlan.agent.md`, `SpecifyConstitution.agent.md`, `Afrodita-UX.agent.md`
   - **QA Focus:** Zero agent-pack errors and no unsupported `fetch`, `todos`, or `runCommands` entries in `.github/agents`.
   - **Steps:** 1. Replace failing agent references with runtime-safe alias names. 2. Remove or normalize unsupported tools. 3. Re-run diagnostics and root pack searches.

**Open Questions 2**
1. Should `Prometheus` hard-depend on `SpecifyConstitution` and `SpecifyClarify` when those names are not always surfaced by the runtime? Recommendation: no; use conditional fallback behavior.
2. Should plugin agent packs be fixed now as well? Recommendation: no; only `.github/agents` is active in the current workspace settings.
