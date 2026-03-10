# Agent Plugin Marketplace (skills-like distribution for agent orchestration)

This repo demonstrates a “skills-like” distribution model for **agent orchestration** in VS Code: you publish a small **marketplace** definition that points to installable **plugin packs**, and each pack can bundle **agents** (custom agents) and optional **skills**.

## Quickstart

1) Enable agent plugins
- Set `chat.plugins.enabled` = true

2) Choose a consumption mode (A/B/C below)
- If you can use remote marketplaces, start with **A**.
- If you can’t (enterprise policy/network), use **B** (local plugin path) or **C** (copy agents).

3) Install or sync packs
- Marketplace UI: Copilot Chat → Agent Plugins (or type `@agentPlugins`) and install the pack(s).
- Local sync: run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1` and follow the printed settings snippet.
  - If you have PowerShell 7 installed, you can use `pwsh` instead of `powershell`.

## Architecture

- Marketplace: .github/plugin/marketplace.json
- Plugin packs: ./plugins/<pack>
   - Each pack can expose:
      - Agents (./agents/*.agent.md)
      - Skills (./skills/<skill>/SKILL.md)

Included packs:

- atlas-orchestration-team: Atlas coordinator + focused subagents for plan → implement → review → test → deploy.
- agent-pack-catalog: a catalog agent + discovery skill to list/recommend packs from the marketplace.

## Consume this repo (three options)

### A) Marketplace install (recommended)

1) Add the marketplace
- Settings: add one of these to `chat.plugins.marketplaces`
  - Remote: `peluzzza/OrchestationAgentsSkillLike`
  - Local: absolute path to a local clone of this repo

2) Install packs
- Open Copilot Chat → Agent Plugins (or type `@agentPlugins`)
- Install the pack(s) you want:
   - atlas-orchestration-team
   - agent-pack-catalog
- Reload VS Code if agents don’t appear immediately

### B) Local plugin path (no marketplace UI)

If you can’t use marketplaces (policy/sandbox/network), you can still “sync” agents locally:

- Clone this repo and add the plugin root to `chat.plugins.paths`
  - Point it at the folder that contains the pack folders (the `plugins/` directory in this repo)

Tip: `scripts/sync_agent_packs.ps1` can clone/pull the repo for you and print the exact settings snippet.

### C) Copy agents into `.github/agents` (agents-only)

If you want agent files to live inside a specific workspace (and avoid plugin packs entirely):

- Copy `*.agent.md` into `.github/agents/` in your repo
- Add `.github/agents` to `chat.agentFilesLocations`

Tip: `scripts/sync_agent_packs.ps1 -Mode agents` performs the copy, and will not overwrite existing files unless you pass `-Force`.

A VS Code reload may be required after changing these settings.

## Why this is “skills-like”

“Skills” often work through progressive disclosure: you start with a small capability, then the system discovers and enables more specialized tools when needed.

This repo emulates that pattern for agents:

- A small marketplace definition points to installable packs.
- Packs bundle a coordinator (Atlas) plus focused subagents, and optionally “skills” content.
- The coordinator is instructed to discover what’s available in the current workspace, proceed safely when things are missing, and guide the user through installation/sync steps instead of assuming capabilities.

## Windows/Enterprise notes

- There is no silent install/sandbox bypass: any cloning, pulling, or copying requires explicit user approval.
- Enterprise policies may restrict marketplace usage or network access. Prefer **B** (local plugin path) or **C** (agents-only copy) in locked-down environments.
- Execution policy can block scripts; the examples use `-ExecutionPolicy Bypass` for the current PowerShell process only.

## How Atlas bootstraps

The Atlas coordinator is designed to behave like “skills”: it attempts to **discover** whether its required subagents are available in the current workspace, and if they aren’t it:

- Continues in single-agent mode (no pretending subagents exist)
- Explains how to install/sync the missing pack(s)
- Can run terminal commands only if the user explicitly approves

## Limitations

- No fully automatic installation: agents can guide steps, but they cannot silently install VS Code plugins.
- Locked-down Windows/enterprise environments may restrict marketplace usage or require policy changes; use the local folder-reference mode when needed.
