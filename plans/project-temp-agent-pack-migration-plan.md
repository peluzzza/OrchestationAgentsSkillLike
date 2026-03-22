# Plan: Project Temp agent-pack migration

**Created:** 2026-03-22
**Status:** Ready for Atlas Execution

## Summary

This plan migrates the proven behavioral baseline from `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents` into `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.github/agents`, but as a careful selective merge instead of a blind overwrite. The target repo already has stronger invocation topology, root-first packaging rules, extra governance agents, and heavy internal coupling to its current flat agent names, so the safest approach is to preserve the target’s external naming and orchestration contract while importing canonical behavior and upstream Specify improvements where they clearly strengthen the pack.

## Context & Analysis

**Relevant Files:**
- `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents/Atlas.agent.md`: canonical baseline for conductor identity, delegation discipline, Atlassian-aware operational guidance, and completion artifact expectations.
- `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents/Prometheus.agent.md`: canonical planning agent with strong fallback/direct-plan behavior, explicit Specify pipeline contract, and strict research/delegation rules.
- `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents/Sisyphus-subagent.agent.md`: canonical execution controller with tighter phase scoping and stricter execution-side Specify gating.
- `/home/daniel/Desktop/develop/Develope/temp/Projects/project_temp/.github/agents/SpecifyImplement.agent.md`: canonical phase-scoped executor; important because the target implementation chain currently leaks into “implement all tasks” semantics.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.github/agents/Atlas.agent.md`: target conductor with stronger discovery, richer gating (`Security`, `Documentation`, `Dependencies`), clearer output contract, and explicit `.github/agents` precedence.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.github/agents/Prometheus.agent.md`: target planner already incorporates `SpecifyConstitution` and `SpecifyClarify`, which are closer to upstream Spec Kit than the canonical project_temp version.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.github/agents/Sisyphus.agent.md`: target implementation conductor; strong phased structure, but currently permits extra delegation (`Hermes` / `Oracle`) and is looser than the canonical containment model.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.github/agents/SpecifySpec.agent.md`, `SpecifyPlan.agent.md`, `SpecifyAnalyze.agent.md`, `SpecifyTasks.agent.md`, `SpecifyImplement.agent.md`, `SpecifyClarify.agent.md`, `SpecifyConstitution.agent.md`: the main Specify surface to refresh.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/spec-kit/templates/commands/specify.md`, `plan.md`, `clarify.md`, `constitution.md`, `tasks.md`, `analyze.md`, `implement.md`: upstream workflow reference; these are the real Spec Kit source of behavior, not `.github/agents` files.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/spec-kit/src/specify_cli/agents.py`: confirms Spec Kit’s GitHub Copilot target is `.github/agents/*.agent.md`, but the command source of truth still lives in templates/commands.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/README.md`: documents current flat agent names (`Hermes`, `Sisyphus`, `Frontend-Engineer`, `SpecifyConstitution`, `SpecifyClarify`, etc.) and declares `.github/agents/` as the canonical source of truth.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/.specify/memory/constitution.md`: hard-codes current target agent names and routing expectations.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/plugins/atlas-orchestration-team/agents/*.agent.md`: mirror/distribution copies that should only be synced after root `.github/agents` is stabilized.
- `/home/daniel/Desktop/develop/Develope/temp/review_clones/OrchestationAgentsSkillLike/scripts/sync_agent_packs.ps1`: reinforces that `.github/agents` is the primary root surface and plugin packs are copied outward.

**Key Findings:**
- The canonical `project_temp` pack uses `*-subagent` names (`Hermes-subagent`, `Sisyphus-subagent`, `Oracle-subagent`, etc.), while the target repo is broadly documented and internally wired around flat names (`Hermes`, `Sisyphus`, `Oracle`, etc.).
- The target repo references current flat names in `README.md`, `.specify/memory/constitution.md`, demos, plans, plugin mirrors, and workflow documentation. A full rename to `*-subagent` in the target root pack would create widespread churn and break internal consistency.
- Upstream Spec Kit improvements are strongest in these areas: constitution stage, clarification stage, hook lifecycle vocabulary, checklist gating, task-by-user-story structure, and cross-artifact analysis. However, several upstream commands rely on scripts (`create-new-feature.sh`, `setup-plan.sh`, `check-prerequisites.sh`, `update-agent-context.sh`) that do **not** exist in the target repo.
- The target repo already adopted some upstream Specify behavior, but not uniformly. Example: `Prometheus.agent.md` already includes `SpecifyConstitution` + `SpecifyClarify`, while `SpecifySpec.agent.md` and `SpecifyPlan.agent.md` still omit some upstream setup/hook semantics.
- There is a concrete semantic mismatch in the target execution chain: `Sisyphus.agent.md` frames `SpecifyImplement` as a phase-scoped executor, but `SpecifyImplement.agent.md` still describes itself as executing all tasks in `tasks.md`. The canonical `project_temp` `SpecifyImplement.agent.md` is more tightly phase-scoped and should inform the merge.
- Because `OrchestationAgentsSkillLike` already has a `plans/` directory and no repo-level `AGENTS.md` prescribing another plan path, `plans/` is the correct execution-plan destination for this repo.

**Merge Strategy Matrix:**

| Target file / surface | Canonical source | Upstream source | Strategy | Why |
|---|---|---|---|---|
| `.github/agents/Atlas.agent.md` | `project_temp/.github/agents/Atlas.agent.md` | N/A | **Selective merge** | Keep target discovery/routing/gates/output contract; import canonical operational discipline, small-task delegation, and artifact rigor. |
| `.github/agents/Prometheus.agent.md` | `project_temp/.github/agents/Prometheus.agent.md` | `spec-kit/templates/commands/constitution.md`, `clarify.md`, `plan.md`, `analyze.md` | **Selective merge** | Keep target SP-1 constitution + SP-3 clarify stages; import canonical fallback/direct-plan rigor and pipeline return discipline. |
| `.github/agents/Sisyphus.agent.md` | `project_temp/.github/agents/Sisyphus-subagent.agent.md` | N/A | **Selective merge** | Preserve target flat naming and phased execution contract; import canonical tighter containment and phase-only scope. |
| `.github/agents/SpecifyImplement.agent.md` | `project_temp/.github/agents/SpecifyImplement.agent.md` | `spec-kit/templates/commands/implement.md` | **Selective merge (high priority)** | Align executor with phase-scoped semantics; keep useful hook/checklist ideas from target/upstream where supported. |
| `.github/agents/SpecifyTasks.agent.md` | `project_temp/.github/agents/SpecifyTasks.agent.md` | `spec-kit/templates/commands/tasks.md` | **Selective merge** | The target file is already closer to upstream than canonical; only import canonical handoff clarity if it improves the Sisyphus chain. |
| `.github/agents/SpecifyAnalyze.agent.md` | `project_temp/.github/agents/SpecifyAnalyze.agent.md` | `spec-kit/templates/commands/analyze.md` | **Selective merge, target-biased** | The target analyze prompt is richer than canonical and closer to upstream; keep target reporting shape unless it conflicts with root pipeline consistency. |
| `.github/agents/SpecifySpec.agent.md` | `project_temp/.github/agents/SpecifySpec.agent.md` | `spec-kit/templates/commands/specify.md` | **Selective merge** | Preserve target spec quality checklist + current flat names; port only upstream/canonical behaviors that fit repo tooling. |
| `.github/agents/SpecifyPlan.agent.md` | `project_temp/.github/agents/SpecifyPlan.agent.md` | `spec-kit/templates/commands/plan.md` | **Selective merge** | Keep target plan output structure; do not import literal script steps unless supporting scripts are also introduced. |
| `.github/agents/SpecifyClarify.agent.md` | N/A | `spec-kit/templates/commands/clarify.md` | **Retain current target, selective upstream refresh** | This stage does not exist in canonical `project_temp`; target already matches upstream direction and should be preserved. |
| `.github/agents/SpecifyConstitution.agent.md` | N/A | `spec-kit/templates/commands/constitution.md` | **Retain current target, selective upstream refresh** | Same reason as Clarify; target already carries governance logic absent from canonical. |
| `.github/agents/Hermes.agent.md`, `.github/agents/Oracle.agent.md` | `Hermes-subagent.agent.md`, `Oracle-subagent.agent.md` | N/A | **Selective merge** | Keep target names; translate canonical naming references and tighten invocation wording where needed. |
| `.github/agents/Security.agent.md`, `Documentation.agent.md`, `Dependencies.agent.md`, `Frontend-Engineer.agent.md` | N/A or optional canonical analogues | N/A | **Retain current target** | These are target-specific strengths and should only be touched if core routing or naming changes require it. |
| `plugins/atlas-orchestration-team/agents/*.agent.md` | stabilized root `.github/agents/*` | N/A | **Wholesale copy after root pass** | Mirrors should follow the root pack, not lead it. |
| `README.md`, `.specify/memory/constitution.md`, demos, docs | stabilized root `.github/agents/*` | N/A | **Deferred / selective update** | Only update after root pack behavior is stable; avoid docs churn during prompt merge. |

**No blind-overwrite rule:** No root `.github/agents/*.agent.md` file should be copied wholesale from `project_temp` into `OrchestationAgentsSkillLike` without a reference pass for naming, tool availability, and current repo coupling. The only safe wholesale-copy candidates are downstream mirrors after the root pack is stable.

## Implementation Phases

### Phase 1: Merge the control-plane pair (`Atlas` + `Prometheus`)

**Objective:** Establish the migration backbone by merging the canonical behavioral baseline into the two highest-leverage control-plane files while preserving the target repo’s invocation topology, current flat names, discovery logic, and extra gate structure.

**Files to Modify/Create:**
- `.github/agents/Atlas.agent.md`
- `.github/agents/Prometheus.agent.md`

**QA Focus:**
- Confirm `.github/agents` remains the canonical root surface.
- Confirm no stale `*-subagent` references are introduced into the target root pack.
- Confirm `Atlas` still routes through current flat names (`Prometheus`, `Hermes`, `Sisyphus`, `Frontend-Engineer`, etc.).
- Confirm `Prometheus` still includes `SpecifyConstitution` and `SpecifyClarify` where intended.

**Steps:**
1. Start from the current target files, not from empty replacements.
2. Port canonical `Atlas` strengths that do not fight the target conductor architecture: tighter delegation discipline, explicit artifact rigor, small-task briefing language, and operational continuity cues.
3. Keep target `Atlas` sections that are stronger than canonical: agent discovery, root `.github/agents` precedence, richer security/docs/dependencies gates, explicit output contract, and degraded-mode routing.
4. Port canonical `Prometheus` strengths that improve planning safety: direct-plan fallback logic, clearer return contract, stronger research/delegation constraints, and explicit “do not implement” boundaries.
5. Preserve target `Prometheus` stages derived from upstream Spec Kit: SP-1 `SpecifyConstitution` and SP-3 `SpecifyClarify`.
6. Translate any imported canonical subagent references (`Hermes-subagent`, `Oracle-subagent`) into the target repo’s actual flat names.
7. Do **not** import literal Spec Kit script commands or shell-dependent setup steps in this phase.

**Acceptance Criteria:**
- [ ] `Atlas.agent.md` keeps target discovery + routing + gate structure.
- [ ] `Prometheus.agent.md` keeps target constitution/clarify stages.
- [ ] Imported canonical behavior does not reintroduce `*-subagent` names in root prompts.
- [ ] No literal upstream script references are added unless the scripts exist locally.
- [ ] The first-pass merge reduces ambiguity instead of increasing prompt length gratuitously.

---

### Phase 2: Tighten the execution chain (`Sisyphus` + `SpecifyImplement` + `SpecifyTasks`)

**Objective:** Resolve the execution-side mismatch so that the target implementation path becomes as disciplined as the canonical pack while retaining the target repo’s flat naming and current execution flow.

**Files to Modify/Create:**
- `.github/agents/Sisyphus.agent.md`
- `.github/agents/SpecifyImplement.agent.md`
- `.github/agents/SpecifyTasks.agent.md`

**QA Focus:**
- Confirm `Sisyphus` remains phase-scoped and does not become a general conductor.
- Confirm `SpecifyImplement` becomes phase-scoped instead of “implement all tasks” by default.
- Confirm `SpecifyTasks` return format still matches what `Sisyphus` expects.

**Steps:**
1. Port canonical containment from `Sisyphus-subagent.agent.md`: implement only the assigned phase, do not decide global completion, do not improvise extra delegation unless explicitly allowed.
2. Reconcile the target line that currently allows `Sisyphus` to call `Hermes`/`Oracle`; either remove it or narrow it to explicit Atlas-authorized exceptions.
3. Rework `SpecifyImplement.agent.md` around the canonical phase-scoped contract while keeping any useful target checklist/hook patterns that are tool-supported locally.
4. Preserve the target’s good checklist gate language only where it does not conflict with phase-scoped execution.
5. Keep `SpecifyTasks.agent.md` mostly target/upstream-shaped; only import canonical wording if it simplifies the handoff to `Sisyphus` and `SpecifyImplement`.
6. Recheck return tokens so `Sisyphus`, `SpecifyTasks`, `SpecifyAnalyze`, and `SpecifyImplement` all agree on scope and next-step semantics.

**Acceptance Criteria:**
- [ ] `Sisyphus.agent.md` and `SpecifyImplement.agent.md` no longer disagree about phase scope.
- [ ] `Sisyphus` is not allowed to roam into uncontrolled extra delegation.
- [ ] `SpecifyTasks` / `SpecifyImplement` / `Sisyphus` return contracts are mutually consistent.
- [ ] The execution-side Specify chain still supports tasks → analyze → implement.

---

### Phase 3: Refresh the planning-side Specify specialists

**Objective:** Bring the planning-side Specify specialists up to the strongest combined version of canonical discipline and upstream Spec Kit workflow, without importing unsupported script assumptions.

**Files to Modify/Create:**
- `.github/agents/SpecifyConstitution.agent.md`
- `.github/agents/SpecifySpec.agent.md`
- `.github/agents/SpecifyClarify.agent.md`
- `.github/agents/SpecifyPlan.agent.md`
- `.github/agents/SpecifyAnalyze.agent.md`

**QA Focus:**
- Confirm each agent still matches the target repo’s current `.specify/` layout and root-first flow.
- Confirm no prompt depends on missing scripts from upstream Spec Kit.
- Confirm gate terminology stays aligned between `Prometheus`, `SpecifyAnalyze`, and `Sisyphus`.

**Steps:**
1. Treat upstream Spec Kit command templates as behavior references, not as copy-paste payloads.
2. Keep `SpecifyConstitution` and `SpecifyClarify` because they are target strengths and are absent from the canonical `project_temp` pack.
3. Port useful upstream concepts only when locally supportable: hook vocabulary, coverage taxonomy, constitution propagation, and clarification structure.
4. Avoid porting upstream shell/bootstrap steps unless the target repo first imports the corresponding scripts.
5. Align `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze` with the canonical plan/report discipline where it improves return clarity to `Prometheus`.
6. Preserve the target’s richer `SpecifyAnalyze` reporting unless it conflicts with pipeline determinism.

**Acceptance Criteria:**
- [ ] `SpecifyConstitution` and `SpecifyClarify` remain first-class parts of the target planning flow.
- [ ] `SpecifySpec`, `SpecifyPlan`, and `SpecifyAnalyze` are strengthened without becoming shell-script dependent.
- [ ] `Prometheus` can call every Specify agent using consistent return semantics.
- [ ] No upstream-only file path or script path is introduced without local support.

---

### Phase 4: Invocation consistency sweep across the root pack

**Objective:** Remove cross-file naming drift and stale call contracts after the core merges land.

**Files to Modify/Create:**
- `.github/agents/Atlas.agent.md`
- `.github/agents/Prometheus.agent.md`
- `.github/agents/Hermes.agent.md`
- `.github/agents/Oracle.agent.md`
- `.github/agents/Sisyphus.agent.md`
- `.github/agents/Specify*.agent.md`
- Any other root agent file whose `agents:` list, examples, or routing text changed indirectly

**QA Focus:**
- Confirm every `agents: [...]` array matches actual filenames / `name:` values in the target repo.
- Confirm prompt examples and allow/block list examples use the same naming convention.
- Confirm no lingering `Hermes-subagent`, `Oracle-subagent`, `Sisyphus-subagent`, `Afrodita-subagent`, etc. remain in the root pack unless intentionally documented as external references.

**Steps:**
1. Sweep all root agent files for imported canonical names that no longer match target files.
2. Normalize internal references to current target names.
3. Check examples, return-block labels, allow-list examples, and tool-invocation wording for consistency.
4. Touch `Hermes.agent.md` and `Oracle.agent.md` only as needed to align with the stabilized control-plane and execution chain.
5. Leave `Security`, `Documentation`, `Dependencies`, and `Frontend-Engineer` unchanged unless this sweep proves they contain stale references.

**Acceptance Criteria:**
- [ ] The root pack contains one coherent naming model.
- [ ] Internal references resolve to existing target agents.
- [ ] The pack no longer mixes canonical `*-subagent` names with current flat target names in operational instructions.

---

### Phase 5: Stabilize secondary surfaces after root-core is proven

**Objective:** Sync mirrors and public surfaces only after the root `.github/agents` pack is stable.

**Files to Modify/Create:**
- `plugins/atlas-orchestration-team/agents/*.agent.md` (only if parity is still desired)
- `README.md`
- `.specify/memory/constitution.md`
- relevant docs/demos only if naming or visible behavior changed materially

**QA Focus:**
- Confirm `.github/agents` remains the only primary source of truth.
- Confirm plugin mirrors are wholesale copies from the stabilized root pack, not divergent hand-edits.
- Confirm README / constitution / demos do not advertise stale behavior.

**Steps:**
1. Decide whether plugin mirror parity is still desired for this pass; default to yes only after root files are stable.
2. If syncing mirrors, copy from root `.github/agents` outward rather than re-editing mirrors independently.
3. Update `README.md` and `.specify/memory/constitution.md` only where the root pack behavior visibly changed.
4. Defer doc/demo churn if the changes are internal prompt hygiene rather than externally visible workflow change.
5. Keep `scripts/sync_agent_packs.ps1` logic intact unless the sync model itself changes.

**Acceptance Criteria:**
- [ ] Root `.github/agents` remains the primary maintained surface.
- [ ] Mirror packs, if updated, are derived from root final state.
- [ ] README / constitution / demos are only touched when necessary.

## Open Questions

1. Should the target root pack be renamed back to the canonical `*-subagent` identity model?
   - **Option A:** Yes; rename files and `name:` fields to match `project_temp` exactly.
   - **Option B:** No; preserve target flat names in `.github/agents`, and translate canonical behavior into that naming model.
   - **Recommendation:** **Option B**. The target repo already couples flat names into `README.md`, `.specify/memory/constitution.md`, demos, plans, and plugin mirrors. Preserving current target names is the conservative default.

2. Should literal upstream Spec Kit script/bootstrap commands be ported into the target agents now?
   - **Option A:** Yes; copy them as written from `templates/commands/*.md`.
   - **Option B:** No; port only the workflow concepts unless the corresponding scripts are first added to the target repo.
   - **Recommendation:** **Option B**. The target repo does not currently contain the upstream shell script set, so literal script references would create dead instructions.

3. Should plugin mirrors be kept in sync during the same merge pass?
   - **Option A:** Yes; edit `.github/agents` and `plugins/atlas-orchestration-team/agents` together.
   - **Option B:** No; stabilize root `.github/agents` first, then mirror by copy.
   - **Recommendation:** **Option B**. This minimizes drift and review noise while respecting the repo’s own “root pack first” rule.

4. Should `Frontend-Engineer.agent.md` be replaced with canonical `Afrodita-subagent` behavior?
   - **Option A:** Yes; align frontend specialist identity to canonical source.
   - **Option B:** No; keep `Frontend-Engineer` in the root pack and only revisit frontend persona later if explicitly requested.
   - **Recommendation:** **Option B**. The target repo documents `Frontend-Engineer` throughout public and constitutional surfaces, and the current task is centered on Atlas/Prometheus/Sisyphus/Specify flow integrity.

## Risks & Mitigation

- **Risk:** Blindly importing canonical `*-subagent` names breaks target repo routing, docs, demos, and constitutional references.
  - **Mitigation:** Preserve target root names as the default and translate canonical behavior into that naming model.

- **Risk:** Literal upstream Spec Kit script instructions are copied into agents that cannot actually run them.
  - **Mitigation:** Port concepts first; import scripts only in a separate, explicit tooling phase.

- **Risk:** `Sisyphus` and `SpecifyImplement` remain semantically inconsistent after the merge.
  - **Mitigation:** Treat execution-chain alignment as a dedicated high-priority phase, not an incidental cleanup.

- **Risk:** Secondary plugin mirrors and docs drift during the merge.
  - **Mitigation:** Do not edit mirrors or public docs until the root pack is stable; then mirror by copy from root.

- **Risk:** Scope explodes beyond the user’s requested focus.
  - **Mitigation:** Keep the merge centered on Atlas orchestration, Prometheus planning, Sisyphus execution, Specify agents, and invocation consistency. Leave extras mostly unchanged unless they are touched by reference drift.

## Success Criteria

- [ ] The target root pack uses the `project_temp` pack as the behavioral baseline without losing the target repo’s stronger invocation topology.
- [ ] `Atlas`, `Prometheus`, and `Sisyphus` are internally consistent with the target repo’s actual agent names and routing model.
- [ ] The target Specify pipeline preserves `SpecifyConstitution` and `SpecifyClarify` while absorbing the strongest upstream/canonical improvements.
- [ ] `Sisyphus` and `SpecifyImplement` agree on phase-scoped execution.
- [ ] No unsupported upstream script dependency is introduced accidentally.
- [ ] `.github/agents` remains the root source of truth, with mirrors/docs updated only after stabilization.

## Notes for Atlas

- **Default naming assumption for execution:** Preserve the target root names (`Hermes`, `Oracle`, `Sisyphus`, `Frontend-Engineer`, etc.) during this pass. Do not rename the root pack unless the user explicitly re-opens that decision.
- **Do not start with docs or plugin mirrors.** Root `.github/agents` first; secondary surfaces later.
- **First phase for Sisyphus:** `Phase 1: Merge the control-plane pair (Atlas + Prometheus)`.
  - Smallest high-value scope.
  - Highest leverage on downstream routing.
  - Establishes the naming and pipeline policy before touching the execution chain.
- **Explicit non-goal for the first pass:** do not import upstream shell-script steps or rebrand `Frontend-Engineer` to `Afrodita`.
- **Evidence note:** if a canonical snippet mentions `Hermes-subagent`, `Oracle-subagent`, `Sisyphus-subagent`, or `Afrodita-subagent`, translate the behavior, not the literal identity, unless Atlas intentionally opens a separate rename migration.