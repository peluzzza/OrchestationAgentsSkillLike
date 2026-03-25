## Plan Complete: Spec-kit transfer hardening
Reviewed the new orchestration-relevant behavior in `spec-kit` and ported the parts that genuinely fit this repo: lifecycle hook symmetry, stronger planning preflight, and deterministic planning-stage context sync. The result is a tighter Specify pipeline in `OrchestationAgentsSkillLike` that borrows `spec-kit` discipline without importing its command-layer assumptions or violating the local 3-layer constitution.

**Phases:** 3 of 3
1. ✅ Phase 1: Harden SP-stage lifecycle wrappers
2. ✅ Phase 2: Tighten planning-stage preflight and context sync
3. ✅ Phase 3: Verify prompt consistency and close the loop

**Files:** `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`, `plans/spec-kit-transfer-hardening-plan-2026-03-25.md`, `plans/spec-kit-transfer-hardening-plan-2026-03-25-phase-1-complete.md`, `plans/spec-kit-transfer-hardening-plan-2026-03-25-phase-2-complete.md`, `plans/spec-kit-transfer-hardening-plan-2026-03-25-phase-3-complete.md`
**Key Functions/Classes:** `SpecifySpec`, `SpecifyPlan`, `SpecifyTasks`, `SpecifyImplement`
**Tests:** 86 validator tests, All ✅

**Next Steps:**
- Extend the same hook-vocabulary docs into README or contributor guidance if you want hook usage to become a supported public contract
- Review the remaining Layer-2 `Specify*` agents (`SpecifyAnalyze`, `SpecifyClarify`, `SpecifyConstitution`) for the same constitution-level metadata normalization if you want full family-wide consistency
