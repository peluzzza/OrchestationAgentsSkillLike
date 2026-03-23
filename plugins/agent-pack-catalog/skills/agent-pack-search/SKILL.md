---
name: agent-pack-search
description: >-
  Identify which agent pack to install or enable based on user goal and workspace
  context. Reads pack-registry.json and marketplace.json, classifies each pack as
  default-active-runtime, canonical-shared-source, marketplace-installable, or shipped-local, and
  outputs exact VS Code activation steps.
---

# Agent pack search (registry-aware)

Use this skill when the user asks for "which agent pack should I install?" or "what packs are available?".

## Inputs

- The user's goal (e.g., "Spring Boot hexagonal architecture review", "write tests", "frontend refactor").

## Procedure

1. Read `.github/plugin/pack-registry.json` in the current repository.
   - This is the authoritative list of **all shipped packs**.
   - Classify each pack by type:
  - **Default-active runtime surface**: `defaultActive: true` — `.github/agents`; already active with zero-setup; no user action needed.
  - **Canonical shared Atlas source**: `id: atlas-orchestration-team` — `plugins/atlas-orchestration-team/agents`; authoring source for the shared 19-agent Atlas pack.
     - **Marketplace-installable**: `marketplacePublished: true` — available via VS Code marketplace UI.
     - **Shipped-local**: `shipped: true`, `marketplacePublished: false`, `defaultActive: false` — in-repo only; must be enabled by adding `activationPath` to `.vscode/settings.json`.
2. Also read `.github/plugin/marketplace.json` for metadata about marketplace-published packs.
3. For each marketplace-published pack, also read its manifest at `plugins/<id>/.github/plugin/plugin.json` to extract `keywords` and whether it contains `agents` and/or `skills`.
4. Inspect the current workspace context (lightweight):
   - Look for language/framework signals like `pom.xml` (Java/Spring), `package.json` (Node), `pyproject.toml` (Python), `go.mod` (Go), `Cargo.toml` (Rust).
   - Prefer `search`/`read` over heavy scanning.
5. Match the user goal + workspace signals to packs by `keywords`, `conductor`, and description.

## Output format

Return:

1) Recommended pack name(s) (exact `id`) with a 1-2 sentence rationale each, and whether it is **marketplace-installable** or **shipped-local**.

2) Activation steps - choose the correct set based on pack type:

**Marketplace-installable packs** (`marketplacePublished: true`):
- Ensure Copilot agent plugins are enabled: Settings -> set `chat.plugins.enabled` to `true`.
- Add this marketplace to VS Code (choose one):
  - Remote: add `peluzzza/OrchestationAgentsSkillLike` to `chat.plugins.marketplaces`.
  - Local: add the local repository path to `chat.plugins.marketplaces`.
- Open Copilot Chat -> Agent Plugins (or type `@agentPlugins`) and install the recommended plugin by name.

**Shipped-local packs** (`marketplacePublished: false`; e.g. `frontend-workflow`, `backend-workflow`, `devops-workflow`, `data-workflow`):
- These packs are in the repository but not in the marketplace.
- Add the pack's `activationPath` to `.vscode/settings.json`:
  ```json
  {
    "chat.agentFilesLocations": {
      ".github/agents": true,
      "plugins/<pack-id>/agents": true
    }
  }
  ```
- Reload VS Code (`Developer: Reload Window`).
- The marketplace UI cannot install these packs; path activation is the only route.
