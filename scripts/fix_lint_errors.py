"""Fix GPT-5.4 model names and other lint issues in all .agent.md files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def fix_gpt54(files):
    fixed = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "GPT-5.4 (copilot)" not in text:
            continue
        if "GPT-5.2 (copilot)" in text:
            # Already has GPT-5.2: remove the GPT-5.4 line
            new = re.sub(r"  - GPT-5\.4 \(copilot\)\r?\n", "", text)
        else:
            new = text.replace("GPT-5.4 (copilot)", "GPT-5.2 (copilot)")
        path.write_bytes(new.encode("utf-8"))
        fixed += 1
        print(f"  [GPT-5.4->5.2] {path.name}")
    return fixed

def fix_missing_agent_tool(path):
    """Add 'agent' to tools list if agents: is defined but agent tool is missing."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Check if file has agents: with entries and tools: without 'agent'
    fm_match = re.match(r"^(\ufeff?---\n)(.*?)(\n---\n)", text, re.DOTALL)
    if not fm_match:
        return False
    fm = fm_match.group(2)
    # Has agents list with at least one entry?
    has_agents = bool(re.search(r"^agents:\s*\n\s+- ", fm, re.MULTILINE))
    # Has tools section?
    has_tools = bool(re.search(r"^tools:\s*\n", fm, re.MULTILINE))
    # Already has 'agent' tool?
    has_agent_tool = bool(re.search(r"^  - agent\s*$", fm, re.MULTILINE))
    if has_agents and has_tools and not has_agent_tool:
        # Add 'agent' as first tool in the tools list
        new_fm = re.sub(r"(^tools:\s*\n)", r"\1  - agent\n", fm, count=1, flags=re.MULTILINE)
        new_text = fm_match.group(1) + new_fm + fm_match.group(3) + text[fm_match.end():]
        path.write_bytes(new_text.encode("utf-8"))
        print(f"  [+agent tool] {path.name}")
        return True
    return False

def fix_mcp_tool(path):
    """Remove 'mcp' tool since VS Code doesn't recognize it."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if "  - mcp\n" not in text:
        return False
    new = text.replace("  - mcp\n", "")
    path.write_bytes(new.encode("utf-8"))
    print(f"  [-mcp tool] {path.name}")
    return True

def fix_handoff_unknown_agents(path, unknown_agents):
    """Remove handoff blocks that reference unknown agents."""
    text = path.read_text(encoding="utf-8", errors="replace")
    changed = False
    for agent_name in unknown_agents:
        # Remove handoff block: "  - label: ...\n    agent: <name>\n    prompt: ...\n"
        # Handles multi-line prompts too
        pattern = rf'  - label: [^\n]+\n    agent: {re.escape(agent_name)}\n(?:    prompt: [^\n]+\n)?'
        new = re.sub(pattern, "", text)
        if new != text:
            text = new
            changed = True
    if changed:
        path.write_bytes(text.encode("utf-8"))
        print(f"  [-bad handoffs] {path.name}")
    return changed

if __name__ == "__main__":
    all_files = [p for p in ROOT.rglob("*.agent.md") if ".git" not in str(p)]
    print(f"Scanning {len(all_files)} agent files...\n")

    # Fix 1: GPT-5.4 -> GPT-5.2
    n1 = fix_gpt54(all_files)
    print(f"\nGPT-5.4 fixes: {n1}\n")

    # Fix 2: Add 'agent' tool where agents: list exists but 'agent' tool is missing
    n2 = sum(1 for p in all_files if fix_missing_agent_tool(p))
    print(f"\nagent-tool fixes: {n2}\n")

    # Fix 3: Remove 'mcp' tool (not recognized by VS Code)
    mcp_files = [
        ROOT / "plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md",
        ROOT / "plugins/memory-system/agents/Memory-Guardian.agent.md",
    ]
    n3 = sum(1 for p in mcp_files if p.exists() and fix_mcp_tool(p))
    print(f"\nmcp-tool fixes: {n3}\n")

    # Fix 4: Remove cross-pack handoffs to agents unrecognized in their contexts
    cross_pack_fixes = {
        ROOT / "plugins/backend-workflow/agents/Backend-Atlas.agent.md": ["Afrodita", "DevOps-Atlas", "Data-Atlas"],
        ROOT / "plugins/frontend-workflow/agents/Afrodita.agent.md": ["Backend-Atlas", "DevOps-Atlas"],
        ROOT / "plugins/devops-workflow/agents/DevOps-Atlas.agent.md": ["Backend-Atlas", "Afrodita", "Data-Atlas"],
        ROOT / "plugins/data-workflow/agents/Data-Atlas.agent.md": ["Backend-Atlas", "DevOps-Atlas"],
    }
    n4 = sum(1 for p, agents in cross_pack_fixes.items() if p.exists() and fix_handoff_unknown_agents(p, agents))
    print(f"\ncross-pack handoff fixes: {n4}\n")

    print("Done.")
