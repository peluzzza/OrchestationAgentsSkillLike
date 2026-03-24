# Plan: Optional runtime parity and explicit trace/session semantics

**Created:** 2026-03-24
**Status:** Ready for Atlas Execution

## Summary

This batch should implement two tightly scoped changes together: low-priority parity tests for optional runtime contracts, and a minimal third wave of explicit trace/session semantics for the research and ops lanes. The work stays additive and lightweight: no resumable engine, no workflow-state machine, and no change to the stable core completeness rules.

The intended implementation path is to extend the existing optional contract registry and prose envelopes for `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS`, then lock the behavior with a few focused validator tests. Optional agents remain optional; they are validated only when present.

## Context & Analysis

**Relevant Files:**
- `scripts/validate_layer_hierarchy.py`: owns `_OPTIONAL_RUNTIME_AGENTS`, `_check_runtime_contract`, `_collect_agent_files`, and the stable-completeness guard that must remain unchanged.
- `scripts/test_validate_layer_hierarchy.py`: already contains fixture-driven tests for stable and optional runtime contracts; it is the natural place to add parity cases and any low-cost helper coverage.
- `.github/agents/Hermes-subagent.agent.md`: current optional exploration alias with a `stable-runtime-v1` envelope but no explicit `session`/`trace` fields yet.
- `.github/agents/Oracle-subagent.agent.md`: current optional research alias with the same gap.
- `.github/agents/Hephaestus-subagent.agent.md`: current optional ops alias with mode/status semantics already defined; only lightweight trace/session clarification should be added.

**Key Functions / Structures:**
- `_OPTIONAL_RUNTIME_AGENTS` in `scripts/validate_layer_hierarchy.py`: the contract registry to extend for wave-3 semantics.
- `_check_runtime_contract(...)`: already validates exact string fields plus required request/response fields, so it should be reused rather than rewritten.
- `_check_stable_agent_completeness(...)`: must not be altered; this preserves the stable core completeness semantics.
- `_collect_agent_files()`: helper worth direct testing only if it can be covered with a tiny isolated fixture.

**Patterns & Conventions:**
- Runtime contracts are declared twice on purpose: compact HTML comment for machine validation and prose envelope for human-facing semantics.
- Optional lanes are validated when present, but never completeness-coupled to one another or to the stable core.
- Tests rely on `_write_agent(...)` and local `tmp_path` fixtures; new parity tests should follow that style.
- Existing validator behavior already supports optional-field enforcement through the registry alone; avoid adding bespoke logic unless a truly missing seam appears.

## Implementation Phases

### Phase 1: Optional parity regression matrix

**Objective:** Add the missing low-cost parity tests for optional runtime contracts before or alongside the semantics update.

**Files to Modify:**
- `scripts/test_validate_layer_hierarchy.py`

**QA Focus:**
- Optional contracts should now have the same basic enforcement confidence as the stable set for version and caller-target drift.
- Optional-agent validity must remain presence-based only.

**Steps:**
1. Add a negative test showing a wrong `version` on an optional agent yields a `RUNTIME CONTRACT FIELD` violation.
2. Add a negative test showing `accepts=parent-agent` drift is rejected for `Hermes-subagent` and/or `Oracle-subagent`.
3. Add a positive test showing all three optional agents valid together yield zero runtime-contract violations and no stable-completeness noise.
4. If still cheap after the above, add direct `_collect_agent_files()` coverage using an isolated fake repo layout and temporary `REPO_ROOT` override; otherwise skip explicitly.

**Acceptance Criteria:**
- [ ] Wrong optional `version` is caught by the validator tests.
- [ ] Wrong `accepts` drift for `Hermes-subagent`/`Oracle-subagent` is caught.
- [ ] Valid `Hermes-subagent` + `Oracle-subagent` + `HEPHAESTUS` passes cleanly.
- [ ] Any `_collect_agent_files()` test added is isolated and non-brittle.

---

### Phase 2: Minimal wave-3 trace/session semantics

**Objective:** Introduce explicit trace/session semantics for the research and ops lanes without introducing resumability or new orchestration behavior.

**Files to Modify:**
- `.github/agents/Hermes-subagent.agent.md`
- `.github/agents/Oracle-subagent.agent.md`
- `.github/agents/Hephaestus-subagent.agent.md`
- `scripts/validate_layer_hierarchy.py`

**QA Focus:**
- The new semantics must remain declarative contract metadata, not a new runtime protocol.
- HEPHAESTUS mode/status semantics must stay intact.

**Steps:**
1. Extend each optional runtime-contract comment with explicit `session` and `trace` fields.
2. Mirror those semantics in each agent’s prose envelope with one or two explicit lines describing participation in the caller’s session/trace context.
3. Extend `_OPTIONAL_RUNTIME_AGENTS` to require those new fields.
4. Keep all request/response shapes and caller/return targets unchanged except where already defined.

**Acceptance Criteria:**
- [ ] `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` expose explicit trace/session fields in both comment and prose form.
- [ ] No resumable-engine, checkpoint, or heavy workflow semantics are introduced.
- [ ] Existing `accepts`/`returns` semantics stay lightweight and consistent with prior work.

---

### Phase 3: Validator alignment and non-regression lock

**Objective:** Ensure the new semantics are enforced by the current validator flow without destabilizing the stable core rules.

**Files to Modify:**
- `scripts/validate_layer_hierarchy.py`
- `scripts/test_validate_layer_hierarchy.py`

**QA Focus:**
- Stable completeness semantics remain untouched.
- Optional agents remain optional and presence-gated only.
- The real workspace scan should continue to pass once the three agent files are updated.

**Steps:**
1. Update the optional test fixtures to include the new trace/session fields.
2. Reuse `_check_runtime_contract(...)` instead of adding special-case validator branches unless strictly necessary.
3. Keep `_check_stable_agent_completeness(...)` and its tests unchanged except for explicit non-regression confirmation.
4. Verify the real-workspace scan expectation still reflects zero violations after the three alias files are updated.

**Acceptance Criteria:**
- [ ] Stable-core completeness behavior is unchanged.
- [ ] Optional-agents-only input still does not trigger `MISSING STABLE AGENT` violations.
- [ ] Real workspace validation remains green after the additive updates.

## Open Questions Resolved

1. **Should the new semantics include durable resume/checkpoint behavior?**
   - **Decision:** No.
   - **Reasoning:** Prior research only justified explicit trace/session semantics, not a resumable engine. This batch should stay declarative and repo-fit.

2. **What should `accepts` remain for the research lanes?**
   - **Decision:** Keep `Hermes-subagent` and `Oracle-subagent` on `accepts=parent-agent` / `returns=parent-agent`.
   - **Reasoning:** Their role is intentionally parent-invoked and lightweight; hard-coding them to `Atlas` would regress the existing delegation model.

3. **What should `accepts` remain for the ops lane?**
   - **Decision:** Keep `HEPHAESTUS` on `accepts=Atlas` / `returns=Atlas`.
   - **Reasoning:** Its existing contract and prose already model Atlas-only operational routing, and this batch is not changing that lane boundary.

4. **Should session/trace be optional or required for the three optional agents?**
   - **Decision:** Treat both as required contract fields for this wave.
   - **Reasoning:** The point of the batch is to make these semantics explicit and machine-checkable, while still keeping them metadata-only.

5. **Should `_collect_agent_files()` get direct coverage?**
   - **Decision:** Yes, but only if implemented as a tiny isolated unit test; otherwise skip with no behavior change.
   - **Reasoning:** It is low-cost only when done without brittle workspace assumptions.

## Risks & Mitigation

- **Risk:** Trace/session semantics accidentally grow into behavioral promises.
  - **Mitigation:** Keep wording limited to explicit contract participation in an invocation/session/trace context; do not add resume/checkpoint language.

- **Risk:** Optional-lane updates accidentally affect stable completeness behavior.
  - **Mitigation:** Do not modify `_check_stable_agent_completeness(...)`; add or keep non-regression tests that prove optional agents do not participate in completeness.

- **Risk:** Test churn grows beyond the “small batch” target.
  - **Mitigation:** Reuse existing fixtures and helper patterns; add only the specific parity gaps called out in this task.

## Success Criteria

- [ ] Optional runtime contracts have parity coverage for wrong version, wrong caller-target drift, and all-valid-together behavior.
- [ ] `Hermes-subagent`, `Oracle-subagent`, and `HEPHAESTUS` declare explicit trace/session semantics in a lightweight way.
- [ ] Validator enforcement remains additive and registry-driven.
- [ ] Stable core completeness semantics are unchanged.
- [ ] Optional agents remain optional and are validated only when present.

## Notes for Atlas

- The cheapest implementation path is mostly data-and-test work: update the three alias files, extend `_OPTIONAL_RUNTIME_AGENTS`, and add a handful of focused pytest cases.
- If `_collect_agent_files()` coverage starts requiring awkward monkeypatching or fragile filesystem setup, drop it from this batch and keep the existing real-workspace integration scan as the main coverage path.
- Favor the test-first order here: the parity cases will make the trace/session extension safer and visibly confirm that stable completeness semantics did not move an inch.