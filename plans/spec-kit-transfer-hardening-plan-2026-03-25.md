## Plan: Spec-kit transfer hardening
Port the highest-value, repo-fit orchestration discipline from `spec-kit` into the Atlas Specify pipeline without changing the 3-layer hierarchy. The focus is on lifecycle symmetry and determinism around `SpecifySpec`, `SpecifyPlan`, and `SpecifyTasks`, not on rewriting their core reasoning.

**Phases 3**
1. **Phase 1: Harden SP-stage lifecycle wrappers**
   - **Objective:** Add donor-style pre-execution and post-execution hook semantics to `SpecifySpec`, `SpecifyPlan`, and `SpecifyTasks`, mirroring the existing implement-stage model.
   - **Files/Functions:** `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`
   - **QA Focus:** Hooks stay optional when `.specify/extensions.yml` is absent, preserve layer ownership, and distinguish optional vs mandatory hook behavior consistently.
   - **Steps:** 1. Reuse the `before_*` / `after_*` extension semantics from donor `spec-kit` command templates. 2. Normalize enabled/disabled handling and non-evaluation of hook conditions. 3. Keep execution ownership with parent conductors rather than leaf-to-leaf handoffs.
2. **Phase 2: Tighten planning-stage preflight and context sync**
   - **Objective:** Make `SpecifyPlan` more deterministic by replacing vague context-sync language with an explicit memory update contract inspired by donor `update-agent-context.sh`.
   - **Files/Functions:** `.github/agents/SpecifyPlan.agent.md`, `.specify/memory/decision-log.md`, `.specify/memory/session-memory.md`
   - **QA Focus:** Planning agents record normalized technology/project decisions in `.specify/memory/` rather than mutating unrelated agent files.
   - **Steps:** 1. Add authoritative preflight checks for feature/artifact paths. 2. Add explicit decision-log/session-memory update guidance. 3. Keep the changes prompt-level and additive.
3. **Phase 3: Verify prompt consistency and close the loop**
   - **Objective:** Review the updated agents for consistency with `Prometheus`, `SpecifyImplement`, and the local constitution.
   - **Files/Functions:** `.github/agents/Prometheus.agent.md`, `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyTasks.agent.md`
   - **QA Focus:** No prompt introduces executable leaf-to-leaf handoffs or behavior that conflicts with the 3-layer rule.
   - **Steps:** 1. Re-read the touched prompts against `Prometheus` and the constitution. 2. Validate that hook vocabulary is symmetrical across SP and EX stages. 3. Summarize the transferred improvements and any future follow-ups.

**Open Questions 2**
1. Should planning-stage hooks escalate mandatory execution back to `Prometheus` or only describe them?
   - **Recommendation:** Escalate/wait on the parent conductor, matching the existing implement-stage pattern.
2. Should donor-style context sync update agent files directly in this repo?
   - **Recommendation:** No. Restrict sync to `.specify/memory/` to preserve repo-local determinism and avoid mutating live runtime prompts during normal planning.
