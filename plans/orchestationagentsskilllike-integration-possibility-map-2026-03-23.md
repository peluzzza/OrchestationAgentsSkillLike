# Plan: OrchestationAgentsSkillLike Integration Possibility Map

**Created:** 2026-03-23  
**Status:** Ready for Atlas Execution (research / architecture guidance)

## Summary

`OrchestationAgentsSkillLike` already contains the core surfaces needed for a modern agent ecosystem: a canonical root agent pack in `.github/agents/`, a spec-driven memory/planning layer in `.specify/`, optional workflow packs in `plugins/`, validators in `scripts/`, onboarding demos in `demos/`, and a marketplace index in `.github/plugin/marketplace.json`.

The realistic integration question is **not** whether this repository should absorb more capability everywhere at once. The realistic question is how to ship all supported capabilities in-repo while keeping the root-first experience stable through selective activation. Public ecosystem signals strongly support that split: keep core instructions/agents small and reliable, keep portable workflows packaged but inactive until needed, keep MCP integrations isolated behind trust/sandbox boundaries, and keep memory lightweight unless usage proves a heavier layer is worth the operational cost.

The highest-value path is therefore:

1. **Keep `.github/agents/` authoritative and small enough to stay dependable.**
2. **Keep `.specify/` as the canonical continuity + planning spine.**
3. **Ship supported workflow/domain packs in `plugins/`, but keep them available-but-inactive until explicitly enabled.**
4. **Treat MCP, hooks, and marketplace-driven packaging as optional/preview lanes with explicit rollback.**

## Governing Principle

**Integrated distribution, selective activation**

- Ship supported capability packs inside the repository.
- Keep only the canonical core default-active.
- Treat every other shipped pack as available-but-inactive until explicitly enabled.
- Keep `.github/agents` authoritative even when mirrors or workflow packs are also distributed.

## Evidence Base

### Repository surfaces reviewed

- `README.md`
- `.github/agents/*.agent.md`
- `.specify/memory/{constitution.md,session-memory.md,decision-log.md}`
- `.specify/templates/{spec-template.md,plan-template.md,tasks-template.md}`
- `plugins/README.md`
- `plugins/*/README.md`
- `plugins/*/.github/plugin/plugin.json`
- `.github/plugin/marketplace.json`
- `scripts/{validate_plugin_packs.py,validate_atlas_pack_parity.py,validate_optional_pack_demos.py}`
- `demos/{atlas-orchestration-smoke,specify-pipeline-demo,automation-mcp-workflow-smoke,ux-enhancement-workflow-smoke}`

### Public ecosystem signals reviewed

- VS Code custom agents docs: scoped tools, hidden subagents, handoffs, least privilege, workspace/user/org distribution
- VS Code custom instructions docs: concise always-on instructions, nested `AGENTS.md`, selective `.instructions.md`, diagnostics-first troubleshooting
- VS Code MCP docs: shared/workspace `mcp.json`, trust prompts, sandboxing, secret handling, enable/disable boundaries
- VS Code agent plugins docs (Preview): plugins can package agents, skills, hooks, and MCP servers; plugins are installable from marketplaces or source; preview + trust caveats apply
- VS Code agent skills docs: task-specific portable capabilities should be skills, not always-on instructions
- MCP introduction: standardization and broad client/server ecosystem support
- `github/spec-kit` README + extensions README: spec → plan → tasks → implement flow, curated catalogs, extension-vs-preset separation, org-curated discoverability, read-only vs read-write extension framing

## Current Architectural Baseline

1. **Canonical core exists already.** The repo explicitly treats `.github/agents/` as the source of truth and already enforces hidden-specialist / visible-conductor behavior.
2. **Compatibility aliasing already exists.** The root pack includes a bounded root-only alias set, while the atlas mirror intentionally excludes those aliases.
3. **Memory is lightweight and bounded already.** `.specify/memory/` currently holds constitution, session memory, and a decision log.
4. **Optional packs already exist.** The repo has a real plugin split, not just a hypothetical one.
5. **Drift control already started.** There is a dedicated parity validator for the Atlas mirror and dedicated validation for plugin manifests and optional-pack demos.
6. **Demos already encode policy.** Optional demos require `.github/agents` plus one plugin path and explicitly reject “enable all plugins” language.

This means the repo does **not** need a foundational redesign. It needs a capability map and disciplined boundary management.

## Viable Integration Lanes

### Lane A — Conservative hardening of the core

**What it means**

- Keep `Atlas` as the only default visible conductor.
- Keep `.github/agents/` as the only required install path.
- Keep `.specify/memory/` and `.specify/specs/` as the continuity/planning substrate.
- Expand validation, docs, and demo coverage before expanding runtime surfaces.

**Why public signals support it**

- VS Code custom agents docs explicitly support hidden subagents with scoped tools.
- VS Code instructions docs recommend concise always-on workspace guidance, not sprawling global behavior.
- Spec Kit guidance supports a stable core workflow plus optional extensions/presets.

**Best fit for this repo**

- Add CI jobs for existing validators.
- Add agent-frontmatter linting and handoff validation.
- Add more root-only smoke tests and documentation diagnostics.

**Why it is attractive**

- Lowest operational risk.
- Keeps the zero-setup path intact.
- Improves trust in the root pack before new capability accretion.

**Rollback**

- Trivial: validators and docs can be removed without changing the user-facing core.

### Lane B — High-leverage `.specify/` maturity without heavy memory infrastructure

**What it means**

- Keep memory file-backed.
- Improve retention rules, summarization patterns, and feature-scoped artifacts.
- Use `.specify/` for continuity, governance, and planning—not as a dumping ground.

**Why public signals support it**

- VS Code instructions favor concise, focused context.
- Agent Skills docs emphasize progressive loading over bloated always-on context.
- Spec Kit strongly supports artifact-driven workflow and curated extension points.

**Realistic integrations here**

- Tighten `session-memory.md` rotation and summarization rules.
- Add a documented policy for when information belongs in `session-memory.md` vs `decision-log.md` vs feature-local `.specify/specs/<slug>/research.md`.
- Introduce optional `.specify/extensions.yml` conventions only after a concrete need exists.
- Add a repo-level “doctor/status” visibility script for `.specify/` health rather than adding a database-backed memory service.

**Hidden costs**

- Too much memory discipline becomes clerical busywork.
- Feature-local artifacts can drift if they are not tied to validators.

**Rollback**

- Revert to the current three-file memory model; no infrastructure teardown needed.

### Lane C — Optional workflow-pack deepening in `plugins/`

**What it means**

- Keep optional conductors and specialized workflows in `plugins/`.
- Expand only packs that have a sharp boundary, README, manifest, and demo/validator.
- Avoid turning `plugins/` into a second canonical core.

**Why public signals support it**

- VS Code agent plugins explicitly support packaged agents, skills, hooks, and MCP servers.
- Spec Kit extension catalogs recommend curated catalogs over unbounded “install everything” availability.
- VS Code skills docs support on-demand specialized capabilities rather than bloating core instructions.

**Realistic next integrations**

- Add a utility/bootstrap pack rather than pushing bootstrap logic into core agents.
- Add plugin-specific skills where a workflow needs reusable procedures or examples.
- Keep `agent-pack-catalog` as a discovery/onboarding helper, not a dependency of core orchestration.

**Hidden costs**

- Too many visible conductors make the picker noisy.
- Plugin docs and manifests become another drift surface.
- Mirroring core prompts into plugins creates maintenance burden unless validators are generalized.

**Rollback**

- Disable the plugin or remove the plugin path/marketplace recommendation; core continues to work.

### Lane D — Marketplace maturation and curated distribution

**What it means**

- Treat `.github/plugin/marketplace.json` as a curated catalog, not as a complete dump of every experimental pack.
- Separate “published/stable” packs from “local-only/example” packs.
- Improve metadata quality (category, effect, stability, dependencies, preview flags).

**Why public signals support it**

- Spec Kit extensions README recommends curated catalogs for organizations.
- VS Code agent plugins support marketplaces, local plugin sources, recommendations, enable/disable controls, and source installs.

**Realistic integrations here**

- Keep `atlas-orchestration-team` and `agent-pack-catalog` as the stable marketplace core.
- Mark automation/MCP and UX packs as opt-in and explicitly optional.
- Add stability metadata or equivalent manifest notes.
- Add recommendation docs for workspace-level `enabledPlugins` / marketplace settings once the repo adopts the current preview plugin model more directly.

**Hidden costs**

- Public plugin schemas are still preview and may change.
- Marketplace discoverability can outpace support maturity.

**Rollback**

- Keep local plugin-path activation as the fallback and reduce marketplace surface to the smallest stable set.

### Lane E — MCP integration as an optional, sandboxable capability

**What it means**

- Treat MCP as a modular capability lane, not a mandatory core dependency.
- Keep MCP-specific behavior inside optional workflow packs or plugin-bundled MCP configuration.

**Why public signals support it**

- MCP is broad and standardized, which supports optional interoperability.
- VS Code MCP docs strongly emphasize trust, secret handling, enable/disable boundaries, and sandboxing.
- VS Code plugin docs show that plugin-bundled MCP servers are possible, but plugin-installed servers are implicitly trusted—raising the bar for what should be bundled.

**Realistic integrations here**

- Keep automation/MCP design/planning agents optional.
- Add MCP example configuration as docs or demo fixtures before bundling live `.mcp.json` or plugin `.mcp.json` definitions.
- If bundling MCP later, prefer sandboxed local servers or narrowly scoped HTTP servers with explicit docs and no hardcoded secrets.

**Anti-pattern**

- Shipping live third-party MCP servers as default plugin behavior just because the preview platform allows it.

**Rollback**

- Disable the plugin or remove `.mcp.json`; no core breakage.

### Lane F — Skills as portable capabilities, not always-on clutter

**What it means**

- Use skills for repeatable procedures, pack discovery, diagnostics, or targeted maintainer flows.
- Avoid converting repo-wide conventions into skills when they should remain instructions or agent behavior.

**Why public signals support it**

- VS Code skills docs explicitly distinguish task-specific capabilities from always-on instructions.
- Skills load progressively, which is context-efficient.

**Realistic integrations here**

- Keep `agent-pack-catalog` skill-based discovery.
- Add optional maintainer skills for parity triage, plugin review, or demo authoring if repeated manual flows appear.

**Anti-pattern**

- Creating skills that duplicate agent bodies or README content without adding reusable procedure/resources.

**Rollback**

- Delete or disable the skill; no impact on core agent orchestration.

## Capability Matrix

| Capability | Where it fits | Merge style | Benefits | Risks / hidden costs | Community signal |
|---|---|---|---|---|---|
| Hidden specialist core + visible `Atlas` | `.github/agents/` | **core** | Stable zero-setup UX, least surprise | Too much core growth makes Atlas pack heavy | **Strongly supported** by VS Code custom agents + least-privilege guidance |
| Root handoffs and guided sequencing | `.github/agents/*.agent.md` | **core** | Makes workflows explicit and reviewable | Handoffs can become stale if not validated | **Supported** by VS Code handoff feature |
| Spec-driven planning pipeline | `.github/agents/`, `.specify/` | **core** | Bounded planning artifacts, better traceability | Template/agent drift | **Strongly supported** by Spec Kit |
| Lightweight session + decision memory | `.specify/memory/` | **core** | Cheap continuity, human-readable, resettable | Memory bloat / stale notes | **Supported** by instruction/context-efficiency patterns |
| Feature-local research / quickstart / analysis artifacts | `.specify/specs/<slug>/` | **core** | Better auditability and handoff quality | Artifact sprawl without cleanup | **Supported** by Spec Kit artifact model |
| Optional workflow conductors | `plugins/*/agents/` | **plugin** | Specialized workflows without polluting core | Picker noise, docs drift | **Supported** by VS Code plugins/custom agents |
| Discovery/catalog agent + skill | `plugins/agent-pack-catalog/` | **plugin** | Smallest-useful install guidance | Can become stale if metadata weak | **Supported** by curated catalog patterns |
| Plugin manifests + curated marketplace | `.github/plugin/marketplace.json`, `plugins/*/.github/plugin/plugin.json` | **plugin/docs** | Discoverability, explicit packaging | Preview-schema churn | **Supported with caution** (VS Code plugin preview + Spec Kit curated catalogs) |
| Generalized parity validators for mirrors | `scripts/` | **script/CI** | Prevents silent drift | More policies to maintain | **Strongly supported** by “single source + validation” practice |
| Demo-gated plugin adoption | `demos/`, `scripts/validate_optional_pack_demos.py` | **demo/script/CI** | Keeps optional packs honest | Demo maintenance tax | **Strongly supported** by public docs emphasizing examples + trust |
| Plugin-bundled skills | `plugins/*/skills/` | **plugin** | Portable reusable procedures | Duplicate docs if overused | **Supported** by VS Code skills + plugin packaging |
| Plugin-bundled hooks | plugin root / hooks files | **plugin later** | Automation and guardrails | Hooks run commands; security risk | **Supported but cautionary** in VS Code plugin docs |
| Plugin-bundled MCP servers | plugin root `.mcp.json` | **plugin later** | Powerful external integrations | Implicit trust on install, config/security burden | **Supported but high caution** |
| Database/service-backed memory | new infra surface | **never core (for now)** | Could improve retrieval later | Operational burden, overkill, trust/compliance cost | **Not supported by current evidence for this repo’s needs** |
| “Enable all plugins” activation model | docs/settings | **never** | None worth the cost | Duplicate/conflicting conductors, noisy UX | **Discouraged** by repo validators and curated-plugin practice |

## Core vs Optional vs Never Merge

### Should stay core

- `Atlas`-first orchestration under `.github/agents/`
- Hidden specialist pattern and bounded core roster
- Specify pipeline agents and `.specify/` templates
- `.specify/memory/` as the canonical continuity layer
- Core validators for root integrity, parity, manifests, and demo hygiene
- Root-first onboarding docs and smoke tests

### Should stay available-but-inactive by default

- Domain/workflow conductors beyond `Atlas`
- Catalog/discovery packs
- Plugin-specific skills
- MCP-specific planning/integration packs
- UX-specific upstream workflow packs
- Plugin-housed hooks or MCP servers
- Marketplace-first install paths

### Should never be merged into core (without a later evidence change)

- Mandatory plugin activation
- Duplicate memory stores outside `.specify/memory/`
- Live third-party MCP servers enabled by default
- Hook execution in core without strict, repo-owned justification
- A second “canonical” agent source alongside `.github/agents/`
- Alias proliferation for every pack/domain instead of bounded compatibility aliases

## Recommendation Tiers

### Now

1. **Wire existing validators into CI** (`validate_plugin_packs.py`, `validate_atlas_pack_parity.py`, `validate_optional_pack_demos.py`).
2. **Codify `shipped`, `default-active`, and `available-but-inactive` in one machine-readable registry.**
3. **Add one more validator for agent-frontmatter and handoff sanity** in `.github/agents/` and visible plugin conductors.
4. **Keep `.specify/memory/` lightweight but formalize retention policy** in docs.
5. **Keep marketplace curated and intentionally incomplete** rather than publishing every pack equally.

### Next

1. **Generalize parity rules** from Atlas mirror to any future mirrored pack.
2. **Add pack stability metadata** (stable / experimental / preview-required) in manifests and marketplace docs.
3. **Add maintainer-oriented skills or scripts** for pack review, demo creation, or drift diagnosis if repetition justifies them.
4. **Add root-vs-plugin recommendation docs using current VS Code plugin settings** where useful.

### Later

1. **Adopt fuller VS Code plugin packaging semantics** (skills, hooks, plugin-native MCP) only after preview churn settles or there is a concrete capability gap.
2. **Explore `.specify/extensions.yml` hooks** for bounded lifecycle automation once there is a demonstrated repeatable need.
3. **Add plugin recommendation automation** only after manifest stability metadata exists.

### Avoid

1. Making plugins mandatory for the default experience.
2. Shipping plugin-bundled MCP servers without a trust/sandbox story.
3. Turning `.specify/memory/` into a catch-all archive.
4. Expanding compatibility aliases beyond the bounded root-only set unless a validator-backed migration demands it.

## Risks, Anti-Patterns, and Rollback Strategies

- **Risk: root/plugin dual-authority confusion**  
  **Mitigation:** keep `.github/agents` authoritative in docs, validators, and manifests.  
  **Rollback:** disable/remove mirrored pack exposure.

- **Risk: plugin preview drift**  
  **Mitigation:** keep preview-only features optional and labeled experimental.  
  **Rollback:** fall back to local agent-path activation.

- **Risk: memory bloat**  
  **Mitigation:** short operational entries, durable decisions only in `decision-log.md`, feature details in feature-local artifacts.  
  **Rollback:** prune files; architecture remains intact.

- **Risk: alias sprawl**  
  **Mitigation:** maintain a bounded root-only alias inventory and validator coverage.  
  **Rollback:** deprecate aliases through docs + validator-assisted cleanup.

- **Risk: MCP trust surface expansion**  
  **Mitigation:** prefer docs/demos first, sandbox where possible, never hardcode secrets, keep disabled by default.  
  **Rollback:** disable plugin/server and remove associated docs.

## Open Questions

1. Should `marketplace.json` evolve toward explicit stability/category metadata, or stay intentionally minimal?
   - **Recommendation:** add metadata only if it drives validation or recommendation behavior.

2. Should future optional packs be mirrored from core, or authored independently?
   - **Recommendation:** mirror only when the pack is explicitly a distribution mirror; otherwise author independently and validate boundaries.

3. Should this repo adopt plugin-native hooks/MCP definitions now?
   - **Recommendation:** no — keep that lane experimental until there is a repo-owned use case and a trust model documented in-repo.

## Success Criteria

- [ ] Core/default experience remains `.github/agents` + `Atlas` first
- [ ] Optional packs remain truly optional and demo-backed
- [ ] No new capability introduces a second canonical source of truth
- [ ] Drift between mirrored/shared surfaces is validator-detectable
- [ ] MCP and plugin-preview adoption stays reversible
- [ ] `.specify/` remains the canonical continuity/planning spine

## Notes for Atlas

- No Specify feature artifacts were generated for this task because the current runtime did not expose the agent delegation / Specify subagent execution surface required by the pipeline.
- This plan is therefore a **direct fallback planning artifact** in `plans/`.
- The strongest next executable phase is **CI + drift hardening**, not new plugin surface area.
- Public evidence is weakest around long-term stability of preview plugin-marketplace behavior and plugin-bundled MCP trust semantics, so those lanes should stay opt-in/experimental.