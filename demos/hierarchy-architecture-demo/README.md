# Hierarchy Architecture Demo

Validates the correctness of the Atlas 3-layer agent hierarchy through automated tests and a reproducible demo prompt.

## What This Demo Validates

### 1. Three-Layer Hierarchy Correctness
The Atlas system uses a strict 3-layer delegation model:

| Layer | Role | Examples |
|-------|------|---------|
| **L0** | Universal Conductor (user-visible) | `Atlas` |
| **L1** | Domain Specialist Gods + Aliases | `Prometheus`, `Sisyphus`, `Themis`, `Argus`, `Hephaestus`, `Afrodita-UX`, `Hermes`, `Oracle`, `Atenea`, `Ariadna`, `Clio` + 7 subagent aliases |
| **L2** | Pack Specialists (pack conductors + executors) | `Backend-Atlas`, `Data-Atlas`, `DevOps-Atlas`, `Automation-Atlas`, `UX-Atlas`, `SpecifySpec`, `SpecifyImplement`, etc. |

Each agent file must declare its layer via an HTML comment immediately after the closing `---`:

```
<!-- layer: 0 | domain: Universal Conductor -->
<!-- layer: 1 | domain: Planning + Specification -->
<!-- layer: 2 | parent: Sisyphus -->
```

### 2. Routing Correctness
- **Atlas (L0)** only delegates to **L1 gods** — never directly to L2 specialists.
- **L1 gods** delegate to **L2 pack specialists** within their domain.
- **L2 specialists** are never `user-invocable: true`.

### 3. Tool Name Cleanliness
All agent `tools:` blocks must use canonical tool names from the authorised set:
`agent`, `search`, `usages`, `problems`, `changes`, `testFailure`, `web`, `fetch`, `edit`, `execute`, `read`, `mcp`.

Sub-tool slash notation (`execute/runInTerminal`, `web/fetch`) and aliases (`runCommands`) are invalid. Running `scripts/validate_tool_names.py` across the full workspace must exit with code 0.

### 4. Memory Protocol Integrity
The memory system is managed by `Memory-Guardian` (L2) and backed by an MCP knowledge graph server configured in `.vscode/mcp.json`. This demo validates that:
- `.vscode/mcp.json` is valid JSON and contains the `@modelcontextprotocol/server-memory` server.
- `Memory-Guardian` exists with `mcp` in its tools.
- The `plugins/memory-system/` pack has a README.

## Test Structure

```
demos/hierarchy-architecture-demo/tests/
├── test_hierarchy_routing.py   # Atlas agents list, L1 gods, pack wiring
├── test_layer_boundaries.py    # Layer comment presence, counts, L0/L1/L2 totals
├── test_memory_protocol.py     # MCP config and Memory-Guardian checks
└── test_tool_names.py          # validate_tool_names.py integration
```

## Running the Demo Tests

```bash
python -m pytest demos/hierarchy-architecture-demo/tests/ -v
```

## Running All Validators

```bash
python scripts/validate_tool_names.py
python scripts/validate_layer_hierarchy.py
python scripts/validate_plugin_packs.py
python scripts/validate_atlas_pack_parity.py
```
