# Plan: Optional runtime parity cleanup + README alignment batch

**Created:** 2026-03-25
**Status:** Ready for Atlas Execution

## Summary

This batch should stay intentionally small: close the last optional-contract parity gaps that still matter in tests, then align only the README surfaces that now drift from the live runtime truth. The existing runtime implementation already includes optional `session`/`trace` semantics and much of the earlier parity coverage, so the safest path is test-first and docs-second.

The work must remain additive. Do not change stable-core completeness semantics, do not introduce new runtime behavior, and do not broaden README edits beyond surfaces that actually describe the root runtime or the optional lanes.

## Context & Analysis

**Relevant Files:**
- `scripts/test_validate_layer_hierarchy.py`: main target for the remaining low-priority parity regressions and any single-fault fixture cleanup.
- `scripts/validate_layer_hierarchy.py`: already enforces optional-agent contracts when present; touch only if a truly missing validator seam is proven by tests.
- `README.md`: definitely affected; it documents the live root runtime and should reflect stable core six vs optional validated lanes plus session/trace semantics.
- `plugins/atlas-orchestration-team/README.md`: likely affected because it summarizes the live Atlas runtime surface from the pack/distribution angle.
- `plugins/README.md`: conditional target; update only if its current runtime-surface wording would remain inconsistent after the root README is corrected.
- `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md`: read-only truth sources for runtime semantics; only touch if documentation review proves a tiny prose mismatch still exists.

**Already Landed (do not redo blindly):**
- Optional registry already requires `session=inherited` and `trace=required` for `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS`.
- The test suite already contains coverage for wrong optional version, Hermes/Oracle `accepts` drift, all-three-valid-together, and isolated `_collect_agent_files()` coverage.
- Therefore this batch should first confirm what is still missing before adding more tests.

**Likely Remaining Gaps To Close:**
- optional `returns` parity coverage is still missing or incomplete
- missing optional `version` case is not clearly covered yet
- `HEPHAESTUS` `accepts` drift parity is still missing
- some existing negative fixtures appear multi-fault (for example, wrong-version or wrong-accepts cases that also omit `session`/`trace`), so they should be normalized if touched

**Patterns & Conventions:**
- Runtime-contract enforcement is registry-driven; prefer extending tests over validator branching.
- Negative tests should be single-fault-clean whenever practical so failures point at one intended field.
- Docs in this repo distinguish the stable default runtime from optional shipped-but-inactive/plugin surfaces; preserve that framing.

## Implementation Phases

### Phase 1: Confirm and close the remaining optional parity gaps

**Objective:** Finish the last targeted optional-contract regressions without reworking already-landed behavior.

**Files to Modify/Create:**
- `scripts/test_validate_layer_hierarchy.py`
- `scripts/validate_layer_hierarchy.py` *(only if tests expose a real missing rule)*

**QA Focus:**
- Optional agents remain validated only when present.
- Stable core completeness remains untouched.
- Negative fixtures fail for the intended reason, not a pile-up of unrelated missing fields.

**Steps:**
1. Reconfirm which parity cases are already covered so the batch does not duplicate landed work.
2. Add the smallest missing negative tests for optional `returns`, missing optional `version`, and `HEPHAESTUS` `accepts` drift.
3. Normalize any touched bad-contract fixtures so they preserve correct unrelated fields (`session`, `trace`, request/response shape, etc.) and stay single-fault-clean.
4. Only modify `scripts/validate_layer_hierarchy.py` if one of the new tests proves the validator lacks enforcement rather than the tests lacking coverage.
5. Keep `_check_stable_agent_completeness(...)` and all stable-core expectations unchanged.

**Acceptance Criteria:**
- [ ] Missing optional `version` is covered by a focused regression.
- [ ] Optional `returns` drift is covered for the relevant optional lanes.
- [ ] `HEPHAESTUS` `accepts` drift is covered.
- [ ] Any edited negative fixture is single-fault-clean.
- [ ] Stable completeness behavior is unchanged.

---

### Phase 2: Align the README surfaces that describe runtime truth

**Objective:** Bring only the actually affected READMEs into sync with the current runtime/documentation truth.

**Files to Modify/Create:**
- `README.md`
- `plugins/atlas-orchestration-team/README.md`
- `plugins/README.md` *(only if its runtime-surface wording would otherwise stay stale)*
- `.github/agents/Hermes-subagent.agent.md`, `.github/agents/Oracle-subagent.agent.md`, `.github/agents/Hephaestus-subagent.agent.md` *(only if a tiny prose mismatch is found while documenting)*

**QA Focus:**
- Root docs clearly separate the stable core six from optional validated utility lanes.
- Hermes/Oracle/HEPHAESTUS session/trace semantics are described accurately but lightly.
- No README claims or implies new runtime features.

**Steps:**
1. Update `README.md` to state the stable core six explicitly and describe `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` as optional validated lanes.
2. Add lightweight wording for session/trace semantics: these lanes inherit session context and require trace propagation; do not introduce resumability/checkpoint language.
3. Refresh only the directly affected setup/validation/troubleshooting notes touched by the runtime-contract changes.
4. Mirror the same runtime truth in `plugins/atlas-orchestration-team/README.md` because it summarizes the live Atlas runtime surface.
5. Update `plugins/README.md` only if its current runtime-surface guidance would otherwise contradict the root README after the change.

**Acceptance Criteria:**
- [ ] `README.md` reflects stable core six vs optional validated lanes.
- [ ] Session/trace semantics for Hermes/Oracle/HEPHAESTUS are documented accurately.
- [ ] No README expands the runtime contract beyond existing behavior.
- [ ] Only genuinely affected README files are touched.

---

### Phase 3: Clean verification and Atlas handoff

**Objective:** Finish the batch with clean, narrow verification so Atlas can commit and push confidently.

**Files to Modify/Create:**
- none expected unless verification reveals a tiny follow-up fix

**QA Focus:**
- Targeted runtime-contract tests pass.
- Real-workspace validation remains green.
- Documentation edits match implemented truth.

**Steps:**
1. Run the targeted validator test module first to confirm the parity regressions and fixture cleanup behave as intended.
2. Run the broader scripts test sweep if the repo norm for this area is still `python -m pytest scripts/ -q`.
3. Recheck any README claims against the actual runtime-contract comments and validator registry before handoff.
4. Hand back a small change set with verification notes so Atlas can perform the final commit/push step.

**Acceptance Criteria:**
- [ ] Targeted tests pass cleanly.
- [ ] Broader validation is clean or any narrower scope is justified explicitly.
- [ ] README wording matches the runtime truth in code.
- [ ] Batch is ready for Atlas commit/push.

## Open Questions

1. Does `plugins/README.md` need an edit in this batch?
   - **Option A:** Yes, if its runtime-surface wording would remain inconsistent after `README.md` is updated.
   - **Option B:** No, if the root README and atlas-pack README fully cover the changed truth and `plugins/README.md` stays accurate.
   - **Recommendation:** Start with A as a conditional check, but skip the file unless an actual contradiction is found.

2. Do the optional alias agent files themselves need more prose edits?
   - **Option A:** No; treat them as already-correct truth sources and update docs only.
   - **Option B:** Yes, but only for a tiny wording mismatch discovered while validating docs.
   - **Recommendation:** Default to A. Only touch agent files if documentation review exposes a direct prose mismatch.

## Risks & Mitigation

- **Risk:** Re-adding tests for cases already landed creates noisy duplicate coverage.
  - **Mitigation:** Confirm current coverage first and only add the truly missing cases.

- **Risk:** Negative fixtures continue to fail for multiple reasons, making regressions harder to interpret.
  - **Mitigation:** Normalize any touched bad contracts so unrelated fields stay valid.

- **Risk:** README edits overstate the optional runtime semantics.
  - **Mitigation:** Keep wording limited to validated-when-present behavior plus `session=inherited` / `trace=required`; avoid resumability or lifecycle promises.

- **Risk:** Stable core semantics are accidentally altered while cleaning optional parity.
  - **Mitigation:** Treat `_check_stable_agent_completeness(...)` as off-limits unless a failing test proves otherwise.

## Success Criteria

- [ ] Remaining optional parity gaps are closed with small, focused tests.
- [ ] Wrong-field optional regressions are single-fault-clean where touched.
- [ ] `README.md` and only the truly affected plugin README surfaces match current runtime truth.
- [ ] Stable core completeness semantics remain unchanged.
- [ ] The batch ends with clean verification and is ready for Atlas to commit/push.

## Notes for Atlas

- Assume the cheapest path is **tests + docs**, not validator logic.
- The current codebase already contains more optional parity coverage than the user summary suggests; verify before editing.
- Prefer a minimal doc footprint: `README.md` is mandatory, `plugins/atlas-orchestration-team/README.md` is highly likely, `plugins/README.md` is conditional.