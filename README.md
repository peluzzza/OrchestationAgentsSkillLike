# Atlas Agents For VS Code

This repo is set up so you can start from zero with a simple experience:

- You see only `Atlas` in the agent picker.
- `Atlas` delegates internally to hidden specialist subagents when needed.
- No plugin marketplace setup is required for the default flow.

## Install From Zero (60 seconds)

1. Clone this repository.
2. Open the repository folder in VS Code.
3. Make sure Copilot Chat agents are enabled in your environment.
4. Confirm workspace setting `.vscode/settings.json` contains:

```json
{
  "chat.agentFilesLocations": {
    ".github/agents": true
  }
}
```

5. Run `Developer: Reload Window`.
6. Open Copilot Chat and select `Atlas`.
7. Ask for a task (for example: "Plan and implement X with tests").

Done. No extra installation steps are needed.

## What You Should See

- Visible agent: `Atlas` only.
- Hidden subagents: `Oracle`, `Explorer`, `Sisyphus`, `Argus`, `Code-Review`, `Hephaestus`, `Frontend-Engineer`, `PackCatalog`.
- `Atlas` chooses and calls subagents internally.

## Optional: Marketplace / Plugin Packs

Use this only if you want distribution through plugin packs. It is not required for normal use.

- Marketplace definition: `.github/plugin/marketplace.json`
- Plugin packs: `plugins/atlas-orchestration-team`, `plugins/agent-pack-catalog`
- Sync helper script: `scripts/sync_agent_packs.ps1`

Example (optional):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1
```

## Keep Setup Simple (Recommended)

If you are testing the default Atlas-only UX, remove `plugins/` to avoid duplicate sources:

```powershell
Remove-Item -Recurse -Force "plugins"
```

Then reload VS Code.

## Troubleshooting

If you see more than one visible agent:

1. Check all subagents have `user-invocable: false`.
2. Check `Atlas` has `user-invocable: true`.
3. Remove duplicate plugin sources (`plugins/`) if you are not using plugin mode.
4. Reload VS Code.

If `Atlas` does not delegate:

1. Verify `Atlas` frontmatter includes `tools: [agent, ...]`.
2. Verify `Atlas` includes `agents: ["*"]`.
3. Confirm subagent files exist under `.github/agents`.
