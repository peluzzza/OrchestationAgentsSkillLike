## Plan: Specify family consistency pass
Small hardening pass to finish the remaining Layer-2 `Specify*` agents that were still lagging behind the newer constitution-aligned prompt standard. The goal is to normalize metadata and activation/leaf guardrails without changing the actual planning workflow semantics.

**Phases 2**
1. **Phase 1: Normalize remaining agent metadata**
   - **Objective:** Align the remaining `Specify*` leaf agents with the constitution-mandated layer metadata and leaf-language pattern.
   - **Files/Functions:** `.github/agents/SpecifyAnalyze.agent.md`, `.github/agents/SpecifyClarify.agent.md`, `.github/agents/SpecifyConstitution.agent.md`
   - **QA Focus:** Verify metadata format, activation guard wording, and leaf-behavior consistency without altering functional pipeline behavior.
   - **Steps:** 1. Replace outdated `parent:` metadata with constitution-compatible `domain:` metadata. 2. Add missing Layer-2 leaf guidance where absent. 3. Add missing activation guard handling for disabled/excluded execution contexts.
2. **Phase 2: Validate prompt integrity**
   - **Objective:** Confirm the prompt files still satisfy repo validation rules and focused tests after the normalization.
   - **Files/Functions:** `scripts/validate_layer_hierarchy.py`, `scripts/test_validate_layer_hierarchy.py`
   - **QA Focus:** Ensure no hierarchy regression and no prompt-file diagnostics are introduced.
   - **Steps:** 1. Run the hierarchy validator. 2. Run the focused validator pytest suite. 3. Capture results in completion artifacts.

**Open Questions 1**
1. Should hook vocabulary also be documented in public README files next, or remain internal prompt discipline for now?
