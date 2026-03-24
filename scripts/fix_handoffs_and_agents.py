"""
fix_handoffs_and_agents.py
--------------------------
1. Add required `prompt:` to handoff items that are missing it.
2. Remove empty `agents: []` declarations (trigger spurious validation).
3. Convert inline `agents: ["A", "B"]` to block list format.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH_DIRS = [
    os.path.join(ROOT, ".github", "agents"),
    os.path.join(ROOT, "plugins"),
]

# Map handoff label to appropriate prompt text
HANDOFF_PROMPTS = {
    "Return findings to Atlas": "Exploration complete. Review the findings and decide the next step.",
    "Return Findings": "Exploration complete. Review the findings and decide the next step.",
    "Return Hermes Findings": "Exploration complete. Review the findings and decide the next step.",
    "Return QA findings to Atlas": "QA testing complete. If FAILED or NEEDS_MORE_TESTS, route back to Sisyphus for fixes. If PASSED, advance the phase or close.",
    "Return Atenea Findings": "Atenea review completed. Evaluate the findings and decide whether the phase can proceed.",
    "Return Ariadna Audit": "Dependency audit complete. Review findings and decide on any required upgrades or mitigations.",
    "Return Clio Updates": "Documentation updated. Review and confirm completeness before closing the phase.",
    "Return implementation results to Atlas": "Implementation complete. Review the phase output and advance to review.",
    "Report implementation results to Atlas": "Implementation complete. Review the phase output and advance to review.",
    "Report back to Atlas": "Work complete. Review results and determine next steps.",
    "Request Revision": "The implementation has issues. Please revise the code according to the feedback provided in the review.",
    "Return Themis Review": "Code review complete. Evaluate findings and decide whether to approve or request revision.",
    "Return Hephaestus Report": "Operations task complete. Review the status and decide on next steps.",
    "Return Hephaestus Findings": "Operations task complete. Review the status and decide on next steps.",
    "Start implementation with Atlas": "Implement the generated plan using phased orchestration.",
    "Start implementation with Backend-Atlas": "Implement the generated backend plan using phased orchestration.",
    "Start implementation with Data-Atlas": "Implement the generated data plan using phased orchestration.",
    "Start implementation with DevOps-Atlas": "Implement the generated DevOps plan using phased orchestration.",
    "Start frontend implementation": "Implement the generated frontend plan using phased orchestration.",
    "Return Oracle Findings": "Research complete. Review the findings and decide the implementation approach.",
    "Return Oracle findings to Atlas": "Research complete. Review the findings and decide the implementation approach.",
}
DEFAULT_PROMPT = "Task complete. Review the results and decide the next step."


def add_prompt_to_handoff(m):
    block = m.group(0)
    if "prompt:" in block:
        return block
    label_m = re.search(r"label:\s*(.+)", block)
    label = label_m.group(1).strip() if label_m else ""
    prompt = HANDOFF_PROMPTS.get(label, DEFAULT_PROMPT)
    return block + f"    prompt: {prompt}\n"


def inline_agents_to_block(m):
    items_str = m.group(1)
    items = [i.strip().strip('"').strip("'") for i in items_str.split(",") if i.strip().strip('"').strip("'")]
    block = "agents:\n"
    for item in items:
        block += f"  - {item}\n"
    return block


def fixup(content):
    # 1. Add prompt: to handoff items missing it
    content = re.sub(
        r"(  - label:[^\n]*\n(?:    [^\n]+\n)*)",
        add_prompt_to_handoff,
        content,
    )
    # 2. Remove empty agents: []
    content = re.sub(r"^agents: \[\]\s*\r?\n", "", content, flags=re.MULTILINE)
    # 3. Convert inline agents arrays to block lists
    content = re.sub(
        r"^agents: \[([^\]]+)\]\s*\r?\n",
        inline_agents_to_block,
        content,
        flags=re.MULTILINE,
    )
    return content


def main():
    changed = 0
    errors = 0
    visited = 0
    for base in SEARCH_DIRS:
        for dirpath, _, files in os.walk(base):
            for fname in sorted(files):
                if not fname.endswith(".agent.md"):
                    continue
                fpath = os.path.join(dirpath, fname)
                visited += 1
                try:
                    with open(fpath, "r", encoding="utf-8") as fh:
                        original = fh.read()
                    fixed = fixup(original)
                    if fixed != original:
                        with open(fpath, "w", encoding="utf-8", newline="") as fh:
                            fh.write(fixed)
                        rel = os.path.relpath(fpath, ROOT)
                        print(f"  fixed: {rel}")
                        changed += 1
                except Exception as exc:
                    print(f"  ERROR {fpath}: {exc}", file=sys.stderr)
                    errors += 1
    print(f"\n{visited} files scanned -> {changed} updated, {errors} errors.")


if __name__ == "__main__":
    main()
