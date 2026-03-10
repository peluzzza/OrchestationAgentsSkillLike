# Agent pack search (marketplace-aware)

Use this skill when the user asks for “which agent pack should I install?” or “what packs are available?”.

## Inputs

- The user’s goal (e.g., “Spring Boot hexagonal architecture review”, “write tests”, “frontend refactor”).

## Procedure

1. Read `.github/plugin/marketplace.json` in the current repository.
2. List available plugins from `plugins[]` with: `name`, `description`, `version`.
3. For each candidate plugin, also read its manifest at `plugins/<name>/.github/plugin/plugin.json` to extract `keywords` and whether it contains `agents` and/or `skills`.
4. Inspect the current workspace context (lightweight):
   - Look for language/framework signals like `pom.xml` (Java/Spring), `package.json` (Node), `pyproject.toml` (Python), `go.mod` (Go), `Cargo.toml` (Rust).
   - Prefer `search`/`read` over heavy scanning.
5. Match the user goal + workspace signals to plugins by `keywords` and description.

## Output format

Return:

1) Recommended plugin name(s) (exact `name`) with a 1–2 sentence rationale each.

2) Exact VS Code installation/enablement steps (do not claim automatic installation):

- Ensure Copilot agent plugins are enabled: Settings → set `chat.plugins.enabled` to `true`.
- Add this marketplace to VS Code (choose one):
  - Remote: add `peluzzza/OrchestationAgentsSkillLike` to `chat.plugins.marketplaces`.
  - Local: add the local repository path to `chat.plugins.marketplaces`.
- Open Copilot Chat → Agent Plugins (or type `@agentPlugins`) and install the recommended plugin(s) by name.

If the user cannot use marketplaces, suggest an alternative:

- Copy the desired `.agent.md` files into `.github/agents/` in their project.
