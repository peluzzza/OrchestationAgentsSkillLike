# Plan: Zeus runtime rename and hook traceability

**Created:** 2026-03-25
**Status:** Ready for Zeus Execution

## Summary

Rename the root Layer-0 conductor from `Atlas` to `Zeus` across the live runtime surfaces without performing a naive family-wide rename of every `*-Atlas` optional conductor. In parallel, add a hook-based traceability system centered on workspace hooks so Zeus can maintain a global attendance ledger of every invoked subagent, while still preserving deeper stage-level proof for the Specify pipeline.

This migration should treat `.github/agents` as the operational source of truth for this clone, use `.github/hooks/` as the team-shared attendance-control surface, update runtime-contract and validator expectations accordingly, and keep the optional `Backend-Atlas` / `DevOps-Atlas` / `Data-Atlas` / `Automation-Atlas` / `UX-Atlas` names stable for now to avoid an unnecessary second blast radius.

## Context & Analysis

**Relevant Files:**
- `.github/agents/Atlas.agent.md` — current Layer-0 conductor definition and root runtime contract.
- `.github/agents/Prometheus.agent.md` — root planner contract currently `accepts=Atlas` / `returns=Atlas`.
- `.github/agents/Sisyphus-subagent.agent.md` — implementation lane that participates in the EX pipeline and will need root-conductor reference updates.
- `.github/agents/Afrodita-subagent.agent.md` — UI implementation alias that may reference the root conductor in stable-runtime semantics.
- `.github/agents/Themis-subagent.agent.md` — review gate returning to the root conductor.
- `.github/agents/Argus-subagent.agent.md` — QA gate returning to the root conductor.
- `.github/agents/Hephaestus-subagent.agent.md` — optional ops lane with runtime-contract fields currently tied to `Atlas`.
- `.github/agents/Backend-Atlas.agent.md` — optional Layer-2 nested conductor; evidence that `Atlas` also exists as a family suffix, not just the root conductor name.
- `.github/agents/DevOps-Atlas.agent.md` — optional Layer-2 nested conductor with cross-workflow references.
- `.github/agents/Data-Atlas.agent.md` — optional Layer-2 nested conductor with cross-workflow references.
- `.github/agents/Automation-Atlas.agent.md` — optional Layer-2 nested conductor with root escalation language.
- `.github/agents/UX-Atlas.agent.md` — optional Layer-2 nested conductor with root escalation language.
- `.github/agents/SpecifySpec.agent.md` — already has `before_specify` / `after_specify` hook semantics.
- `.github/agents/SpecifyPlan.agent.md` — already has `before_plan` / `after_plan` hook semantics.
- `.github/agents/SpecifyTasks.agent.md` — already participates in the Specify execution path and should join the same trace proof protocol.
- `.github/agents/SpecifyImplement.agent.md` — implementation-stage hook participant.
- `.github/agents/SpecifyAnalyze.agent.md` — part of both SP-5 and EX-1 proof paths but currently needs hook-parity review.
- `README.md` — user-facing runtime identity, installation, routing, and troubleshooting text currently centered on `Atlas`.
- `docs/Atlas_Agents_Project_Document.md` — long-form public architecture document containing many `Atlas` references and optional `*-Atlas` pack references.
- `.github/plugin/pack-registry.json` — root runtime and optional pack metadata, including `conductor` fields for `Atlas` and `*-Atlas` conductors.
- `.github/plugin/marketplace.json` — marketplace/distribution metadata still branded around Atlas.
- `.github/hooks/` — new workspace-owned hook surface for global subagent attendance and Zeus-visible runtime evidence.
- `plugins/README.md` — optional workflow documentation that currently distinguishes `Atlas` from `*-Atlas` conductors.
- `scripts/validate_layer_hierarchy.py` — stable and optional runtime-contract enforcement; exact string checks make rename drift visible immediately.
- `scripts/test_validate_layer_hierarchy.py` — broad regression suite for stable and optional runtime contracts.
- `scripts/validate_atlas_pack_parity.py` — completeness checker whose filename and messaging are Atlas-branded and will drift after the rename.
- `plans/atlas-static-trace-test-case-2026-03-25.md` — existing dry-trace artifact that should inform Zeus proof expectations.
- `.specify/extensions.yml` — does not exist yet; clean seam for hook-based trace instrumentation.

**Key Functions/Structures:**
- `_STABLE_RUNTIME_AGENTS` in `scripts/validate_layer_hierarchy.py` — exact stable contract registry that must be updated from `Atlas` to `Zeus`.
- `_OPTIONAL_RUNTIME_AGENTS` in `scripts/validate_layer_hierarchy.py` — optional contract registry already enforcing `session` / `trace` semantics for Hermes, Oracle, and HEPHAESTUS.
- `_check_runtime_contract(...)` — current exact-match validator used for contract enforcement.
- `ALL_AGENTS` in `scripts/validate_atlas_pack_parity.py` — active runtime completeness list if filenames are renamed.
- pre/post hook semantics in `SpecifySpec`, `SpecifyPlan`, `SpecifyTasks`, `SpecifyImplement` — current prompt-level mechanism to leverage for telemetry.

**Patterns & Conventions:**
- Runtime truth is encoded in both prompt prose and machine-readable `runtime-contract` comments.
- Optional conductors are shipped in `.github/agents` but are inactive by default.
- The repo already prefers declarative `session` / `trace` contract fields over heavyweight runtime-state machinery.
- The Specify pipeline already has prompt-level hook vocabulary, but no concrete `.specify/extensions.yml`, no workspace hook configuration under `.github/hooks/`, and no trace ledger.
- Historical plans are abundant; migration should focus on live runtime and active validation surfaces rather than retro-editing old completion notes.

## Implementation Phases

### Phase 1: Freeze rename boundary and define canonical naming policy

**Objective:** Define exactly what “Atlas → Zeus” means in this batch, and avoid a family-wide rename that expands scope unnecessarily.

**Files to Modify/Create:**
- `README.md`
- `docs/Atlas_Agents_Project_Document.md`
- `.github/plugin/pack-registry.json`
- `.github/plugin/marketplace.json`
- `plugins/README.md`
- `.github/hooks/README.md`
- new plan artifact under `plans/`

**QA Focus:**
- The documented rename boundary must cleanly distinguish root-conductor identity from optional `*-Atlas` conductor brands.
- No document should imply that optional conductors are part of the default-visible root rename scope for this batch.

**Steps:**
1. Define `Zeus` as the new canonical Layer-0 root conductor identity.
2. Document that optional `Backend-Atlas`, `DevOps-Atlas`, `Data-Atlas`, `Automation-Atlas`, and `UX-Atlas` remain unchanged in this migration.
3. Normalize docs to treat `.github/agents` as the operational source of truth for this clone.
4. Add a Zeus-owned hook documentation surface that explains the global attendance model and the difference between workspace hooks and prompt-local stage hooks.
5. Identify which `Atlas` occurrences are true root-conductor references versus optional conductor brand references.
6. Record the rename policy in a migration note so later contributors do not blindly rename the optional family.

**Acceptance Criteria:**
- [ ] Root-conductor rename scope is explicitly defined.
- [ ] Optional `*-Atlas` conductors are explicitly marked out-of-scope for this batch.
- [ ] `.github/agents` is documented as the operational runtime source for this clone.
- [ ] `.github/hooks/` is documented as the workspace-owned attendance-control surface for Zeus.
- [ ] No migration step assumes a live `plugins/atlas-orchestration-team/agents/` mirror that is absent in this checkout.

---

### Phase 2: Rename the root conductor and propagate root-runtime contracts

**Objective:** Replace the live root runtime identity `Atlas` with `Zeus` everywhere the string means “the Layer-0 conductor”.

**Files to Modify/Create:**
- `.github/agents/Atlas.agent.md` or renamed `Zeus.agent.md` (depending on cutover strategy)
- `.github/agents/Prometheus.agent.md`
- `.github/agents/Sisyphus-subagent.agent.md`
- `.github/agents/Afrodita-subagent.agent.md`
- `.github/agents/Themis-subagent.agent.md`
- `.github/agents/Argus-subagent.agent.md`
- `.github/agents/Hephaestus-subagent.agent.md`
- any other `.github/agents/*.agent.md` files whose prose escalates to the root conductor
- `README.md`
- `docs/Atlas_Agents_Project_Document.md`
- `.github/plugin/pack-registry.json`
- `.github/plugin/marketplace.json`
- `plugins/README.md`

**QA Focus:**
- Exact contract strings (`accepts`, `returns`, `name`) must align across prompts, docs, and registries.
- Root rename must not accidentally rename optional `*-Atlas` conductor identities.

**Steps:**
1. Rename the root conductor identity from `Atlas` to `Zeus` in the live agent definition.
2. Update all root-targeted `accepts=Atlas` / `returns=Atlas` runtime-contract fields to `Zeus` where they refer to the Layer-0 conductor.
3. Update root escalation prose such as “route back to Atlas” to “route back to Zeus” where the reference is truly the root conductor.
4. Update user-facing installation, routing, troubleshooting, and conductor descriptions to use `Zeus`.
5. Update pack registry `conductor` fields only for the root conductor entries; leave optional `*-Atlas` conductor fields unchanged.
6. Decide whether to keep a deprecated compatibility shim for `Atlas` or perform a hard cutover.

**Acceptance Criteria:**
- [ ] `Zeus` is the canonical root-conductor name across the live runtime.
- [ ] All root-conductor runtime-contract fields point to `Zeus`.
- [ ] User-facing docs instruct users to select `Zeus`, not `Atlas`.
- [ ] Optional `Backend-Atlas` / `DevOps-Atlas` / `Data-Atlas` / `Automation-Atlas` / `UX-Atlas` identities remain unchanged.
- [ ] No accidental cross-family rename landed.

---

### Phase 3: Update validators, tests, and runtime metadata to enforce Zeus

**Objective:** Make the rename machine-checkable so any future Atlas/Zeus drift fails fast.

**Files to Modify/Create:**
- `scripts/validate_layer_hierarchy.py`
- `scripts/test_validate_layer_hierarchy.py`
- `scripts/validate_atlas_pack_parity.py` (or renamed successor)
- any tests referencing `Atlas` as the required Layer-0 stable agent name
- optional new compatibility wrapper script if the old path is retained temporarily

**QA Focus:**
- Validator behavior should reflect the new root identity without weakening current coverage.
- Rename should not break optional runtime validation or stable completeness semantics.

**Steps:**
1. Update stable runtime registries to require `Zeus` instead of `Atlas` where applicable.
2. Update unit tests and fixtures that currently assert `accepts=Atlas`, `returns=Atlas`, or `name: Atlas` for the root conductor.
3. Decide whether `scripts/validate_atlas_pack_parity.py` should be renamed to a neutral or Zeus-branded name.
4. If script renaming occurs, provide a minimal compatibility wrapper only if external tooling depends on the old path.
5. Recheck that optional runtime tests for Hermes/Oracle/HEPHAESTUS still pass with the root rename applied to any relevant parent/return relationships.

**Acceptance Criteria:**
- [ ] Validators fail on stale `Atlas` root references and pass on `Zeus`.
- [ ] Existing stable/optional runtime coverage remains intact.
- [ ] Script naming drift is either removed or consciously wrapped for compatibility.
- [ ] No validator continues to encode `Atlas` as the canonical root conductor unless explicitly marked deprecated.

---

### Phase 4: Add a workspace hook-based attendance and traceability system

**Objective:** Introduce a repo-owned, hook-driven attendance path proving which subagents were actually invoked across the runtime, with global workspace hooks first and Specify-stage proof as the deeper second layer.

**Files to Modify/Create:**
- new `.github/hooks/zeus-subagent-attendance.json`
- new `.github/hooks/README.md`
- new `.specify/extensions.yml`
- `.github/agents/SpecifySpec.agent.md`
- `.github/agents/SpecifyPlan.agent.md`
- `.github/agents/SpecifyTasks.agent.md`
- `.github/agents/SpecifyImplement.agent.md`
- `.github/agents/SpecifyAnalyze.agent.md`
- new `scripts/trace_hook_event.py`
- new `scripts/render_trace_report.py`
- optional new `scripts/validate_traceability_contracts.py`
- new or updated tests for trace scripts and hook contract coverage

**QA Focus:**
- Hooks must remain repo-owned and deterministic.
- Proof must come from actual leaf invocation points, not from parent-agent prose alone.
- The system must work even though `.specify/extensions.yml` is currently absent.

**Steps:**
1. Create a workspace hook config in `.github/hooks/zeus-subagent-attendance.json` using `SubagentStart` and `SubagentStop` so every invoked subagent emits attendance evidence.
2. Document the attendance model in `.github/hooks/README.md`, including the difference between:
   - workspace hooks for global attendance,
   - prompt-level stage hooks for Specify local proof,
   - Zeus summaries vs raw evidence artifacts.
3. Create `.specify/extensions.yml` with mandatory stage hook entries for:
   - `before_specify`, `after_specify`
   - `before_plan`, `after_plan`
   - `before_tasks`, `after_tasks`
   - `before_implement`, `after_implement`
   - newly added `before_analyze`, `after_analyze`
4. Standardize a parent-supplied context bundle: `trace_id`, `parent_agent`, `feature_id`, `phase`, `layer_from`, `layer_to`.
5. Implement `scripts/trace_hook_event.py` to append structured JSONL events under `.specify/traces/<trace-id>.jsonl`.
6. Implement `scripts/render_trace_report.py` to produce a human-readable proof summary under `.specify/traces/<trace-id>.md`.
7. Extend `SpecifyAnalyze.agent.md` with the same hook semantics already used by the other Specify leaves.
8. Add unit tests proving event append, paired before/after events, and required field validation.

**Acceptance Criteria:**
- [ ] `.github/hooks/zeus-subagent-attendance.json` exists and defines the global attendance hook set.
- [ ] `.github/hooks/README.md` explains the attendance contract Zeus uses.
- [ ] `.specify/extensions.yml` exists and defines the stage-level proof hook set.
- [ ] `SpecifySpec`, `SpecifyPlan`, `SpecifyTasks`, `SpecifyImplement`, and `SpecifyAnalyze` all support symmetric hook-driven trace emission.
- [ ] Each trace event includes `trace_id`, parent, child, layers, hook name, and status.
- [ ] The raw ledger and rendered report are both generated deterministically.
- [ ] The proof mechanism is hook-based, not just prose-based.

---

### Phase 5: Surface Zeus-visible orchestration evidence and prove L1→L2 paths

**Objective:** Make the attendance and trace data useful to Zeus and validate that the current layered orchestration path can be proven end-to-end.

**Files to Modify/Create:**
- `.github/agents/Zeus.agent.md` or the renamed root conductor file
- `.github/agents/Prometheus.agent.md`
- `.github/agents/Sisyphus-subagent.agent.md`
- `.github/hooks/README.md`
- `plans/zeus-static-trace-test-case-2026-03-25.md`
- relevant demo or expected-flow artifacts under `demos/`
- optional new README traceability section

**QA Focus:**
- Zeus should receive concise evidence, not raw log spam.
- The first visible artifact should read like a subagent attendance sheet before it reads like a low-level trace dump.
- Proof should focus first on the deterministic core:
  - `Prometheus → SpecifySpec → SpecifyPlan → SpecifyAnalyze`
  - `Sisyphus-subagent → SpecifyTasks → SpecifyAnalyze → SpecifyImplement`

**Steps:**
1. Define a small evidence summary contract for parent agents, e.g. `TRACE_EVIDENCE: trace_id, report_path, observed_edges, attendance_count`.
2. Update Prometheus and Sisyphus guidance so they aggregate child hook proof into a compact summary returned to Zeus.
3. Add a dry-trace or smoke artifact that defines the required ordered edges for planning and implementation.
4. Validate that the rendered trace report can prove at least one real planning path and one real implementation path.
5. Document the difference between:
   - declared capability (`agents:` / runtime contracts)
   - observed invocation attendance (workspace hook ledger)
   - stage-level proof (Specify hook ledger)

**Acceptance Criteria:**
- [ ] Zeus can see a compact evidence summary for core orchestration runs.
- [ ] Planning proof shows `Prometheus → SpecifySpec → SpecifyPlan → SpecifyAnalyze`.
- [ ] Implementation proof shows `Sisyphus-subagent → SpecifyTasks → SpecifyAnalyze → SpecifyImplement`.
- [ ] The evidence report clearly distinguishes declared routes from observed routes.
- [ ] The proof path does not rely on optional nested conductors.

---

### Phase 6: Add Zeus shared-memory continuity

**Objective:** Make Zeus consume the shared memory feature explicitly without violating the Layer-0 → Layer-2 hierarchy, using a hook-refreshed compact context artifact under `.specify/memory/`.

**Files to Modify/Create:**
- `.github/agents/Zeus.agent.md`
- `.github/agents/Memory-Guardian.agent.md`
- `plugins/memory-system/agents/Memory-Guardian.agent.md`
- new `.github/hooks/zeus-memory-context.json`
- new `scripts/sync_memory_context.py`
- new `scripts/test_sync_memory_context.py`
- `.specify/memory/session-memory.md`
- `.specify/memory/decision-log.md`
- new `.specify/memory/zeus-context.md`
- `.vscode/mcp.json`
- `README.md`
- `plugins/memory-system/README.md`

**QA Focus:**
- Zeus must gain a deterministic memory continuity path without directly invoking Layer-2 `Memory-Guardian`.
- The compact context artifact must stay derived from shared memory rather than becoming a parallel memory store.
- MCP Level 3 expectations must be declared consistently across docs, config, and agent contracts.

**Steps:**
1. Add a Zeus-facing shared-memory consultation section that prioritizes a compact hook-refreshed snapshot under `.specify/memory/`.
2. Create `scripts/sync_memory_context.py` to derive `zeus-context.md` from `session-memory.md` and `decision-log.md`.
3. Wire a dedicated workspace hook in `.github/hooks/zeus-memory-context.json` using `SubagentStart` so the snapshot refresh remains deterministic and separate from attendance.
4. Create `.vscode/mcp.json` with `@modelcontextprotocol/server-memory` so Level 3 memory is configured in-repo.
5. Align `Memory-Guardian` docs/contracts with the new Zeus snapshot flow while keeping `Memory-Guardian` opt-in through higher-layer workflows.
6. Refresh memory/docs/plans so the runtime truth is consistent (`.github/agents` active source, Zeus visible root, plugins optional in this clone).

**Acceptance Criteria:**
- [ ] Zeus explicitly consults `.specify/memory/zeus-context.md`, then falls back to `session-memory.md` and `decision-log.md`.
- [ ] A dedicated workspace hook refreshes `zeus-context.md` deterministically.
- [ ] No direct Zeus → Memory-Guardian delegation path is introduced.
- [ ] `.vscode/mcp.json` exists and references `@modelcontextprotocol/server-memory`.
- [ ] `Memory-Guardian` agent contracts and docs consistently describe Level 3 MCP behavior.
- [ ] Memory source-of-truth notes align with the current `.github/agents` runtime model for this clone.

## Open Questions

1. Should the migration be a hard cutover or include a deprecated `Atlas` compatibility shim?
   - **Option A:** Hard cutover to `Zeus`.
   - **Option B:** Temporary compatibility shim for `Atlas`.
   - **Recommendation:** Hard cutover unless an external consumer of `@Atlas` is known and must be preserved.

2. Should optional `*-Atlas` conductors be renamed in the same batch?
   - **Option A:** Yes, full family rename now.
   - **Option B:** No, keep them stable and defer to a second rebrand pass.
   - **Recommendation:** Option B. They are optional Layer-2 brands and not worth the extra blast radius in this migration.

3. Should the Atlas-branded script/doc filenames be renamed in the same batch?
   - **Option A:** Rename all active runtime-facing filenames now.
   - **Option B:** Keep filenames and only update contents.
   - **Recommendation:** Rename active operational filenames if they are part of live tooling; defer historical/demo slug cleanup to a later cosmetic pass.

4. Should hook-based proof extend beyond the Specify leaves in the first batch?
   - **Option A:** Yes, instrument optional nested conductors too.
   - **Option B:** No, start with the deterministic Specify path.
   - **Recommendation:** Option B. It proves the most important L1→L2 path with the smallest compatible surface.

5. How should the repo handle the missing `plugins/atlas-orchestration-team/agents/` path referenced in docs?
   - **Option A:** Reintroduce a real shared mirror now.
   - **Option B:** Treat `.github/agents` as the only operational source in this clone and fix docs accordingly.
   - **Recommendation:** Option B for this migration; do not mix a source-of-truth repair and a root rename unless explicitly requested.

## Risks & Mitigation

- **Risk:** A naive rename catches optional `*-Atlas` conductors and explodes scope.
  - **Mitigation:** Freeze scope early and distinguish root-conductor references from optional conductor brand references.

- **Risk:** Validators and runtime contracts drift, leaving a half-Atlas / half-Zeus runtime.
  - **Mitigation:** Update registries, validators, tests, and prompt contracts in the same controlled batch.

- **Risk:** Hook telemetry becomes merely descriptive, not proof-bearing.
  - **Mitigation:** Emit raw hook-ledger events from the child invocation point and require paired before/after events.

- **Risk:** The repo’s source-of-truth drift (`.github/agents` vs absent plugin mirror) causes contributors to edit the wrong surface.
  - **Mitigation:** Treat `.github/agents` as operational truth in this clone and document that explicitly during the migration.

- **Risk:** Traceability scope expands into a generalized orchestration engine.
  - **Mitigation:** Keep v1 limited to hook-driven JSONL ledger + rendered report for the Specify path only.

## Success Criteria

- [ ] The visible root conductor is `Zeus`, not `Atlas`.
- [ ] All live root-runtime contracts refer to `Zeus` where they target the Layer-0 conductor.
- [ ] Optional `*-Atlas` conductors remain stable and unchanged in the first batch.
- [ ] A concrete `.specify/extensions.yml` exists and drives trace event emission.
- [ ] Core L1→L2 paths are provable via raw and rendered evidence artifacts.
- [ ] Zeus has a hook-refreshed shared-memory continuity path under `.specify/memory/`.
- [ ] Validators and tests enforce the new root identity and traceability expectations.
- [ ] The migration leaves no ambiguity about the operational source of truth for this clone.

## Notes for Zeus

- Treat this as a runtime/contract migration first and a cosmetic rebrand second.
- Do not retro-edit historical `plans/*complete*.md` files unless the user explicitly wants archival cleanup.
- Prefer a test-and-validator-first sequence after each contract rename slice so Atlas/Zeus drift is caught immediately.
- The most valuable proof target is the current Specify path; optional nested-conductor proof can be a later expansion.
