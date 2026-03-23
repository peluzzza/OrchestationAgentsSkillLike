"""
update_models.py
Assigns model priorities to every .agent.md file based on agent category.

Categories:
  planner  - Atlas, Prometheus, Oracle, Themis, Atenea, Ariadna, Clio, Argus,
             Specify* (except Implement), domain conductors (Backend-Atlas, Data-Atlas),
             domain planners (Backend-Planner, Data-Planner), PackCatalog, Memory-Guardian
  ux       - Afrodita*, UI-Designer, Component-Builder, Style-Engineer, State-Manager,
             A11y-Auditor, Frontend-Handoff, UX-Atlas, User-Flow-Designer, Design-Critic,
             Accessibility-Heuristics, UX-Planner, Frontend-Planner + all ux/frontend-workflow
  devops   - Hephaestus*, DevOps-Atlas, devops-workflow agents
  impl     - Sisyphus*, SpecifyImplement, Service-Builder, API-Designer, Database-Engineer,
             Performance-Tuner, Backend-Reviewer, Security-Guard, Compliance-Checker,
             Secret-Scanner, Test-Runner, Coverage-Analyst, Mutation-Tester, n8n-Connector,
             MCP-Integrator, Workflow-Composer, Automation*, ML-Scientist, Analytics-Engineer,
             Data-Architect, Pipeline-Builder, Data-Quality, Data-Reviewer + security/qa workflows
  explorer - Hermes*
"""

import os
import re
import glob

WORKSPACE = r'c:\Users\daniel.leyva\OneDrive - European Medicines Agency\Desktop\Projects'

MODEL_STRINGS = {
    'planner': (
        'model:\n'
        '  - GPT-5.4 (copilot)\n'
        '  - Claude Sonnet 4.6 (copilot)'
    ),
    'ux': 'model: Gemini Pro 3.1 (copilot)',
    'devops': 'model: Claude Sonnet 4.6 (copilot)',
    'impl': (
        'model:\n'
        '  - Claude Opus 4.6 (copilot)\n'
        '  - GPT-5.4-Codex (copilot)\n'
        '  - GPT-5.3-Codex (copilot)\n'
        '  - Claude Sonnet 4.6 (copilot)'
    ),
    'explorer': (
        'model:\n'
        '  - Gemini Flash 3.1 (copilot)\n'
        '  - Claude Haiku 4.6 (copilot)\n'
        '  - Claude Haiku 4.5 (copilot)'
    ),
}


def categorize(filepath: str) -> str:
    name = os.path.basename(filepath).replace('.agent.md', '').lower()
    path = filepath.replace('\\', '/').lower()

    # ── Explorers / Searchers ────────────────────────────────────────────────
    if 'hermes' in name:
        return 'explorer'

    # ── DevOps ───────────────────────────────────────────────────────────────
    if 'hephaestus' in name:
        return 'devops'
    if 'devops-workflow' in path:
        return 'devops'

    # ── UX / UI coding ───────────────────────────────────────────────────────
    ux_names = [
        'afrodita', 'ui-designer', 'component-builder', 'style-engineer',
        'state-manager', 'a11y-auditor', 'frontend-handoff', 'ux-atlas',
        'user-flow-designer', 'design-critic', 'accessibility-heuristics',
    ]
    if any(n in name for n in ux_names):
        return 'ux'
    if 'frontend-workflow' in path or 'ux-enhancement-workflow' in path:
        return 'ux'

    # ── Implementation – explicit conductor carve-outs ───────────────────────
    # Automation conductors live in automation-mcp-workflow and are impl-level
    if 'automation-atlas' in name or 'automation-planner' in name:
        return 'impl'
    if 'automation-mcp-workflow' in path:
        return 'impl'

    # ── Planner carve-outs inside backend/data workflow paths ────────────────
    # These are conductors / planners, not specialists
    if any(n in name for n in ['backend-atlas', 'data-atlas', 'backend-planner', 'data-planner']):
        return 'planner'

    # ── Implementation specialists ───────────────────────────────────────────
    impl_names = [
        'sisyphus', 'specifyimplement',
        'service-builder', 'api-designer', 'database-engineer', 'performance-tuner',
        'ml-scientist', 'analytics-engineer', 'data-architect', 'pipeline-builder',
        'data-quality', 'data-reviewer',
        'security-guard', 'compliance-checker', 'secret-scanner',
        'test-runner', 'coverage-analyst', 'mutation-tester',
        'n8n-connector', 'mcp-integrator', 'workflow-composer',
        'backend-reviewer', 'frontend-reviewer', 'automation-reviewer',
    ]
    if any(n in name for n in impl_names):
        return 'impl'
    # Remaining agents in dedicated specialist-workflow packs → impl
    if any(p in path for p in ['security-workflow', 'qa-workflow', 'backend-workflow', 'data-workflow']):
        return 'impl'

    # ── Default: Planner / Orchestrator ──────────────────────────────────────
    return 'planner'


# Matches the model field (single-line value OR multi-line YAML list)
MODEL_RE = re.compile(
    r'^model:(?:[ \t]+[^\n]*)?(?:\n[ \t]+[^\n]*)*',
    re.MULTILINE,
)


def main():
    # Use os.walk so hidden directories like .github are included
    files = sorted(
        os.path.join(root, fname)
        for root, _dirs, fnames in os.walk(WORKSPACE)
        for fname in fnames
        if fname.endswith('.agent.md')
    )
    updated = 0
    unchanged = 0
    skipped = 0

    for f in files:
        cat = categorize(f)
        new_model = MODEL_STRINGS[cat]

        with open(f, 'r', encoding='utf-8-sig') as fh:
            content = fh.read()

        new_content, n = MODEL_RE.subn(new_model, content, count=1)

        if n == 0:
            print(f'[SKIP-no-match] {os.path.relpath(f, WORKSPACE)}')
            skipped += 1
        elif new_content == content:
            unchanged += 1
            # Uncomment to see unchanged files:
            # print(f'[ok] {os.path.relpath(f, WORKSPACE)}')
        else:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            updated += 1
            print(f'[{cat}] {os.path.relpath(f, WORKSPACE)}')

    print(f'\nDone — updated: {updated} | unchanged: {unchanged} | skipped: {skipped} | total: {len(files)}')


if __name__ == '__main__':
    main()
