# Plan: Canonical Agent Pack Depth Upgrade

**Created:** 2026-03-23
**Status:** Ready for Atlas Execution

## Summary

Upgrade the target repo’s canonical `.github/agents/` pack by selectively importing the stronger instruction patterns from `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents` without blindly copying donor files. The highest-value first batch is the research/planning layer (`Prometheus`, `Hermes-subagent`, `Oracle-subagent`, `SpecifySpec`, `SpecifyPlan`, `SpecifyAnalyze`), followed by the thin execution/review/QA/ops/design aliases, then a minimal execution-side Specify alignment pass, and finally plugin-mirror sync for shared files.

This plan intentionally stays inside **agent customization files only**. It preserves the repo’s canonical `.github/agents` precedence, `-subagent` compatibility names, existing `.specify/specs/<feature>/` pathing, current model/runtime compatibility, and the already-dirty non-agent working tree by keeping each phase small and independently committable.

## Context & Analysis

**Relevant Files:**
- `.github/agents/Prometheus.agent.md`: canonical planner already has local Specify pipeline extensions (`SpecifyConstitution`, fallback logic), but still trails the donor pack in context-conservation discipline, explicit skill routing, and clearer phase guidance.
- `.github/agents/Hermes-subagent.agent.md`: currently a very thin compatibility alias; strongest low-risk target for donor-style exploration contracts.
- `.github/agents/Oracle-subagent.agent.md`: currently a thin research alias; good candidate for richer subsystem-analysis guidance and clearer structured output.
- `.github/agents/Sisyphus-subagent.agent.md`: currently a thin compatibility wrapper, while the execution-side contract in this repo expects far more structure.
- `.github/agents/Themis-subagent.agent.md`: thin review alias that lacks the donor pack’s richer review workflow and explicit severity framing.
- `.github/agents/Argus-subagent.agent.md`: thin QA alias missing donor-style coverage/edge-case guidance.
- `.github/agents/Hephaestus-subagent.agent.md`: thin DevOps/SRE alias missing donor mode framing, workflow detail, and evidence structure.
- `.github/agents/Afrodita-subagent.agent.md`: thin UI alias missing donor-level scope control and accessibility/responsiveness execution guidance.
- `.github/agents/SpecifySpec.agent.md`, `.github/agents/SpecifyPlan.agent.md`, `.github/agents/SpecifyAnalyze.agent.md`: overlapping planning-side Specify agents already exist, but their instructions are older and more tool-heavy than the donor pack’s tighter, runtime-aware variants.
- `.github/agents/SpecifyTasks.agent.md`, `.github/agents/SpecifyImplement.agent.md`: execution-side Specify agents are already relatively rich in the target repo; they should only receive selective edits if the upgraded alias/planning contracts expose real mismatches.
- `.github/agents/Atlas.agent.md`: already enforces canonical `.github/agents` precedence and `-subagent` routing; it is the contract surface that all upgraded agent files must remain compatible with.
- `plugins/atlas-orchestration-team/agents/Prometheus.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifySpec.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyPlan.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyAnalyze.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyTasks.agent.md`, `plugins/atlas-orchestration-team/agents/SpecifyImplement.agent.md`: shared mirror files that must stay aligned whenever their canonical `.github/agents` counterparts change.

**Key Functions/Classes:**
- `Prometheus` in `.github/agents/Prometheus.agent.md`: planning conductor that must stay compatible with local Specify pathing and fallback behavior.
- `Hermes-subagent` in `.github/agents/Hermes-subagent.agent.md`: discovery specialist alias currently too shallow to be reliably useful.
- `Oracle-subagent` in `.github/agents/Oracle-subagent.agent.md`: research specialist alias that should return deeper, more structured findings.
- `Sisyphus-subagent` in `.github/agents/Sisyphus-subagent.agent.md`: implementation alias that should become a true execution shim instead of a stub.
- `Themis-subagent`, `Argus-subagent`, `Hephaestus-subagent`, `Afrodita-subagent`: thin compatibility agents whose bodies should be upgraded without renaming or widening scope beyond their specialist roles.
- `SpecifySpec`, `SpecifyPlan`, `SpecifyAnalyze`: planning-side Specify pipeline agents whose contracts should be refreshed from the donor pack while preserving local repo-specific behaviors.
- `SpecifyTasks`, `SpecifyImplement`: execution-side Specify agents that define the compatibility boundary for any `Sisyphus-subagent` upgrade.

**Dependencies:**
- Donor reference pack: `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents/*.agent.md` — source of stronger patterns only, not a blind-copy target.
- Canonical precedence rule: `.github/agents/` remains authoritative over `plugins/**/agents`.
- Existing local pipeline contracts: `.specify/specs/<feature>/...` pathing and Atlas ↔ Prometheus ↔ Specify ↔ Sisyphus handoff expectations must remain stable.

**Patterns & Conventions:**
- Root-first authority: `.github/agents` is the canonical source of truth and must stay the first-class pack.
- Compatibility alias names are intentional: `Hermes-subagent`, `Oracle-subagent`, `Sisyphus-subagent`, `Afrodita-subagent`, `Argus-subagent`, `Themis-subagent`, and `Hephaestus-subagent` must keep their `name:` values and stay root-only.
- Shared-vs-root-only split matters: shared canonical files may need plugin-mirror updates; root-only alias files must not be mirrored.
- Local Specify behavior is already customized: `Prometheus` currently references `SpecifyConstitution` and local clarify/fallback rules that do not exist in the donor pack and therefore must be preserved.
- Dirty-tree safety matters: the repo already has unrelated registry/docs/test changes in flight, so the agent-pack upgrade must stay layered, narrow, and committable without touching non-agent files.

## Implementation Phases

### Phase 1: Harden the research and planning layer

**Objective:**
Bring the donor pack’s stronger context-conservation, activation-guard, delegation, skill-routing, and output-discipline patterns into the target repo’s highest-value planning/research files while preserving local Specify pathing and pipeline extensions.

**Files to Modify/Create:**
- `.github/agents/Prometheus.agent.md`: merge donor planning discipline into the local SP pipeline instead of replacing repo-specific `SpecifyConstitution`/clarify behavior.
- `.github/agents/Hermes-subagent.agent.md`: expand from thin alias into a real read-only exploration specialist.
- `.github/agents/Oracle-subagent.agent.md`: expand from thin alias into a deeper research specialist with explicit structured findings.
- `.github/agents/SpecifySpec.agent.md`: refresh spec-generation workflow and return contract, but preserve local `.specify/specs/<feature>/` conventions.
- `.github/agents/SpecifyPlan.agent.md`: refresh technical-plan workflow and output contract while keeping local constitution/path assumptions intact.
- `.github/agents/SpecifyAnalyze.agent.md`: refresh analysis gate instructions and return contract without dropping the repo’s SP-5 / EX-1 semantics.

**QA Focus:**
- Frontmatter remains valid and tool/model lists stay runtime-compatible with the target repo.
- `Prometheus` still references the target repo’s local Specify pipeline shape and default `plans/` fallback.
- All paths remain `.specify/specs/<feature>/...` and no donor-only pathing leaks in.
- No agent rename, handoff rename, or canonical-precedence regression is introduced.

**Steps:**
1. Diff each target file against its donor counterpart and classify content into: safe donor pattern, target-only behavior to preserve, and incompatible donor details to reject.
2. Upgrade `Hermes-subagent` and `Oracle-subagent` first so their richer contracts are available to `Prometheus` and the planning-side Specify agents.
3. Refactor `Prometheus.agent.md` to absorb donor context-conservation, research routing, and fallback discipline while retaining local `SpecifyConstitution` and conservative-default behavior.
4. Refresh `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze` using donor structure and return-contract patterns, but preserve the target repo’s existing local path conventions and constitution semantics.
5. Do a final canonical-pack-only pass to ensure the Phase 1 files still align with `Atlas.agent.md` expectations and do not reference absent agents or unsupported runtime tools.

**Acceptance Criteria:**
- [ ] `Prometheus.agent.md` includes donor-grade context-conservation and fallback guidance without removing local `SpecifyConstitution` / clarify / `.specify/specs/<feature>/` behavior.
- [ ] `Hermes-subagent.agent.md` and `Oracle-subagent.agent.md` are no longer thin aliases; each has a concrete workflow and structured return contract.
- [ ] `SpecifySpec.agent.md`, `SpecifyPlan.agent.md`, and `SpecifyAnalyze.agent.md` keep the repo’s current Specify pathing and remain compatible with Atlas/Sisyphus expectations.
- [ ] No non-agent files are touched in this phase.

---

### Phase 2: Upgrade the thin execution, review, QA, ops, and UI aliases

**Objective:**
Replace the current superficial compatibility wrappers with rich, donor-informed specialist instructions while keeping the existing alias names, scope boundaries, and Atlas handoff expectations intact.

**Files to Modify/Create:**
- `.github/agents/Sisyphus-subagent.agent.md`
- `.github/agents/Themis-subagent.agent.md`
- `.github/agents/Argus-subagent.agent.md`
- `.github/agents/Hephaestus-subagent.agent.md`
- `.github/agents/Afrodita-subagent.agent.md`

**QA Focus:**
- Each alias remains a compatibility surface, not a renamed canonical agent.
- Output contracts are explicit enough for Atlas to consume deterministically.
- Tool/model lists remain compatible with current runtime expectations instead of donor-only assumptions.
- No alias widens into responsibilities already owned by another specialist.

**Steps:**
1. Use donor alias files as the primary pattern source, but preserve any target-only role boundaries already assumed by `Atlas.agent.md`.
2. Upgrade `Sisyphus-subagent` first so it becomes a real execution shim with Specify-aware execution discipline rather than a stub.
3. Upgrade `Themis-subagent` and `Argus-subagent` next so review and QA phases become non-superficial and structurally consistent.
4. Upgrade `Hephaestus-subagent` and `Afrodita-subagent`, preserving their specialist boundaries and evidence/reporting expectations.
5. Cross-check all five aliases against Atlas’s delegation briefs so field names, phase expectations, and handoff text remain coherent.

**Acceptance Criteria:**
- [ ] Every targeted `-subagent` file contains concrete workflow steps, strict limits, and a structured return contract.
- [ ] All targeted aliases preserve their current `name:` values and remain rooted in `.github/agents/` only.
- [ ] No targeted alias references an unavailable sibling agent or unsupported runtime tool.
- [ ] The canonical pack is materially less superficial after this phase even before any mirror sync.

---

### Phase 3: Align the execution-side Specify boundary only where needed

**Objective:**
Perform the smallest possible follow-up on the execution-side Specify agents so the richer planning/alias contracts do not clash with the target repo’s already-customized task-generation and implementation pipeline.

**Files to Modify/Create:**
- `.github/agents/SpecifyTasks.agent.md`: only if the upgraded `Sisyphus-subagent` contract exposes a real mismatch in task-generation expectations.
- `.github/agents/SpecifyImplement.agent.md`: only if the upgraded execution contract exposes a real mismatch in phase-execution expectations.
- `.github/agents/Sisyphus.agent.md`: conditional only if its canonical non-alias execution guidance must be updated to stay consistent with the upgraded alias + execution-side Specify boundary.

**QA Focus:**
- Preserve target-only checklist and hook support already present in `SpecifyImplement.agent.md`.
- Preserve the repo’s current tasks-phase structure and `.specify/specs/<feature>/` pathing.
- Avoid churn: this is a compatibility-tightening phase, not a donor-pack rewrite of already-strong files.

**Steps:**
1. Audit the post-Phase-2 contract boundary between `Sisyphus-subagent`, `SpecifyTasks`, and `SpecifyImplement`.
2. If no contract mismatch is found, skip edits to `SpecifyTasks.agent.md`, `SpecifyImplement.agent.md`, and `Sisyphus.agent.md` and record the audit result.
3. If a mismatch is found, apply the smallest targeted wording changes needed to keep the execution-side pipeline coherent.
4. Re-check that local hook/checklist behavior survives intact and that no donor-only simplification removes repo-specific safety features.

**Acceptance Criteria:**
- [ ] `SpecifyTasks.agent.md` and `SpecifyImplement.agent.md` are changed only if a concrete contract mismatch is found.
- [ ] Any edits preserve local checklist/hook semantics and `.specify/specs/<feature>/` pathing.
- [ ] `Sisyphus-subagent` and the execution-side Specify agents describe a consistent execution flow after this phase.
- [ ] No docs, validators, registry files, or other non-agent surfaces are touched.

---

### Phase 4: Sync the shared plugin mirror without touching unrelated WIP

**Objective:**
Propagate only the shared canonical-agent changes into the atlas-orchestration-team mirror so the repo does not end up with a stronger root pack and a stale shared plugin surface.

**Files to Modify/Create:**
- `plugins/atlas-orchestration-team/agents/Prometheus.agent.md`
- `plugins/atlas-orchestration-team/agents/SpecifySpec.agent.md`
- `plugins/atlas-orchestration-team/agents/SpecifyPlan.agent.md`
- `plugins/atlas-orchestration-team/agents/SpecifyAnalyze.agent.md`
- `plugins/atlas-orchestration-team/agents/SpecifyTasks.agent.md` (only if Phase 3 changed its canonical counterpart)
- `plugins/atlas-orchestration-team/agents/SpecifyImplement.agent.md` (only if Phase 3 changed its canonical counterpart)

**QA Focus:**
- Shared mirror files match their canonical counterparts exactly after normalization.
- Root-only `-subagent` aliases remain absent from the plugin mirror.
- The mirror sync is isolated from current registry/docs/test WIP so it can be staged or committed independently.

**Steps:**
1. List every canonical file changed in Phases 1–3 and split it into shared-vs-root-only categories.
2. Copy only the shared canonical agent bodies into the plugin mirror, preserving exact content for parity.
3. Verify that no root-only alias file is introduced into `plugins/atlas-orchestration-team/agents/`.
4. Do a final staging audit to ensure the implementation batch contains only agent customization files and does not absorb the current unrelated non-agent working-tree changes.

**Acceptance Criteria:**
- [ ] Every changed shared canonical agent has a synchronized mirror counterpart.
- [ ] No root-only alias appears in the plugin mirror.
- [ ] The upgraded agent pack can be committed separately from the current non-agent WIP.
- [ ] Canonical `.github/agents` precedence remains unchanged after sync.

## Open Questions

1. Should `Prometheus.agent.md` keep the target repo’s local `SpecifyConstitution` stage even though it is absent from the donor pack?
   - **Option A:** Simplify to the donor pack’s three-step Specify flow.
   - **Option B:** Keep the local constitution stage and selectively import donor structure around it.
   - **Recommendation:** **Option B.** The local constitution stage is a repo-specific behavior already referenced in the target pack and should not be deleted in a “make agents less superficial” pass.

2. Should `SpecifyTasks.agent.md` and `SpecifyImplement.agent.md` be edited in the same batch as `Sisyphus-subagent.agent.md`?
   - **Option A:** Rewrite them immediately for symmetry.
   - **Option B:** Audit first, then touch them only if a real contract mismatch appears.
   - **Recommendation:** **Option B.** They are already materially richer than the thin aliases, so automatic churn would add risk without guaranteed value.

3. Should plugin-mirror sync happen in the same phase commit as the canonical file edits?
   - **Option A:** Delay mirror sync to a later cleanup pass.
   - **Option B:** Pair each shared canonical batch with an immediately adjacent mirror-sync phase.
   - **Recommendation:** **Option B.** It keeps parity drift short-lived and avoids forgetting shared-file updates while the working tree is already dirty.

## Risks & Mitigation

- **Risk:** Blind donor-copying could remove target-only logic such as `SpecifyConstitution`, local clarify behavior, hook/checklist support, or repo-specific return contracts.
  - **Mitigation:** Treat the donor pack as a pattern source only; classify donor content into “import”, “adapt”, and “reject” before editing each file.

- **Risk:** Upgrading shared canonical files without mirror sync would leave the plugin mirror stale and likely break later parity expectations.
  - **Mitigation:** Keep shared-file mirror sync as an explicit final phase and do not treat it as optional once shared canonical files change.

- **Risk:** Donor tool/model lists may reference runtime assumptions that do not match the target repo’s current compatibility envelope.
  - **Mitigation:** Preserve existing target model/runtime compatibility unless a donor change is clearly safe and supported in the target repo.

- **Risk:** The current working tree already contains unrelated registry/docs/test changes, so a broad agent-pack sweep could create mixed commits.
  - **Mitigation:** Limit this implementation plan to agent customization files only and keep each phase independently stageable.

- **Risk:** Phase 3 could become a churn magnet if Atlas edits already-strong execution-side Specify files just for style symmetry.
  - **Mitigation:** Treat Phase 3 as audit-first and allow it to end with “no edits required” if compatibility is already good enough.

## Success Criteria

- [ ] The targeted canonical `.github/agents` files no longer read like superficial compatibility stubs.
- [ ] `Prometheus`, `Hermes-subagent`, `Oracle-subagent`, `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze` reflect donor-grade planning/research depth while preserving target-specific pipeline behavior.
- [ ] `Sisyphus-subagent`, `Themis-subagent`, `Argus-subagent`, `Hephaestus-subagent`, and `Afrodita-subagent` become substantive specialist aliases without losing compatibility names or scope boundaries.
- [ ] Execution-side Specify files are only changed where compatibility actually requires it.
- [ ] Shared plugin-mirror agent files are synced after shared canonical edits.
- [ ] The entire upgrade remains isolated to agent customization files and can be landed before committing the repo’s unrelated pending changes.

## Notes for Atlas

- Use the donor folder at `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents` as a **pattern library**, not a wholesale replacement source.
- Load the `agent-customization` skill before editing `.agent.md` files so frontmatter, discovery descriptions, and file-type conventions stay correct.
- Start with **Phase 1 only** if you need the smallest safe first improvement batch; it gives the highest upgrade value with the lowest interaction risk.
- Do **not** touch the current non-agent WIP (`.github/plugin/*`, `README.md`, `plugins/README.md`, validator tests, `.specify/memory/*`, etc.) while executing this plan.
- Preserve these invariants throughout implementation:
  - canonical precedence remains `.github/agents` first
  - `-subagent` names remain unchanged
  - shared-vs-root-only split remains intact
  - `.specify/specs/<feature>/` pathing remains intact
  - model/runtime compatibility remains conservative
- This planning artifact was written directly to `plans/` because Specify subagent execution was not available in the current runtime; treat it as the authoritative fallback plan for this task.