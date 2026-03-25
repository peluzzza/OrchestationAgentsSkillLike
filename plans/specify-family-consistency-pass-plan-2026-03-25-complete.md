## Plan Complete: Specify family consistency pass
This hardening batch finished the remaining `Specify*` Layer-2 prompt files that were still lagging behind the constitution-aligned standard introduced in the previous rounds. The result is a fully normalized Specify leaf family with consistent `domain:` metadata, explicit activation-guard behavior for disabled runs, and leaf-only wording that matches the repo's 3-layer constitution.

The work stayed intentionally narrow and low-risk: no production logic, no task semantics rewrite, and no new orchestration paths. Validation stayed green through prompt diagnostics, hierarchy checks, focused tests, and a final review pass.

**Phases:** 2 of 2
1. ✅ Phase 1: Normalize remaining agent metadata
2. ✅ Phase 2: Validate prompt integrity

**Files:** `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyClarify.agent.md`, `.github/agents/SpecifyConstitution.agent.md`, `plans/specify-family-consistency-pass-plan-2026-03-25.md`, `plans/specify-family-consistency-pass-plan-2026-03-25-phase-1-complete.md`, `plans/specify-family-consistency-pass-plan-2026-03-25-phase-2-complete.md`
**Key Functions/Classes:** Layer metadata comments, activation guards, Layer-2 leaf guidance, focused hierarchy validation
**Tests:** Total 86, All ✅

**Next Steps:**
- Normalize any remaining wording drift across the wider Specify family only if it adds real clarity, not just cosmetic symmetry.
- Decide whether hook vocabulary should stay internal prompt discipline or be surfaced in README-level documentation.
