# Plan: Layered Agent Hierarchy — 3-Layer Architecture with Memory + External Integrations

**Creado**: 2026-03-23
**Estado**: Listo para ejecución de Atlas
**Feature ID**: `layered-agent-hierarchy`
**Spec**: `.specify/specs/layered-agent-hierarchy/spec.md`
**Design artifacts**: `.specify/specs/layered-agent-hierarchy/plan.md`
**SP-5 gate**: `.specify/specs/layered-agent-hierarchy/analysis-report.md` — **PASSED**

---

## Resumen

Implementar una arquitectura jerárquica estricta de 3 capas para el sistema de agentes VS Code Copilot del proyecto: Layer 0 (Atlas, único entry point), Layer 1 (11 dioses mitológicos + 7 aliases), Layer 2 (70+ especialistas en packs). Se corrigen 20+ declaraciones de tools inválidas en VS Code, se añade un protocolo de memoria persistente de 3 niveles (session + decision log + MCP knowledge graph), se integran agentes externos no duplicativos, y se entrega un demo con suite de tests que lleva el total ≥250. Ningún agente queda huérfano sin capa definida.

---

## Contexto y Análisis

### Ficheros relevantes

**Layer 0:**
- `.github/agents/Atlas.agent.md` — actualmente `agents: ["*"]`; cambia a lista explícita L1
- `plugins/atlas-orchestration-team/agents/Atlas.agent.md` — parity copy; misma actualización

**Layer 1 (canonical gods × 2 locations cada uno):**
- `.github/agents/{Prometheus,Sisyphus,Themis,Argus,Hermes,Oracle,Atenea,Ariadna,Clio,Hephaestus,Afrodita-UX}.agent.md`
- `plugins/atlas-orchestration-team/agents/<same 11>.agent.md`

**Root-only aliases (solo `.github/agents/`):**
- `Afrodita-subagent.agent.md`, `Argus-subagent.agent.md`, `Hermes-subagent.agent.md`, `Hephaestus-subagent.agent.md`, `Sisyphus-subagent.agent.md`, `Themis-subagent.agent.md`, `Oracle-subagent.agent.md`

**Layer 2 pack conductors:**
- `plugins/backend-workflow/agents/Backend-Atlas.agent.md`
- `plugins/data-workflow/agents/Data-Atlas.agent.md`
- `plugins/devops-workflow/agents/DevOps-Atlas.agent.md`
- `plugins/automation-mcp-workflow/agents/Automation-Atlas.agent.md`
- `plugins/frontend-workflow/agents/Afrodita.agent.md`
- `plugins/ux-enhancement-workflow/agents/UX-Atlas.agent.md`

**Registry + config:**
- `.github/plugin/pack-registry.json` — añadir `parentGod`, nuevos packs
- `.github/plugin/marketplace.json` — nuevas entradas
- `.vscode/settings.json` — nuevas rutas de agentes
- `.vscode/mcp.json` — crear con MCP memory server

**Scripts de validación (existentes):**
- `scripts/validate_plugin_packs.py`, `scripts/validate_pack_registry.py`, `scripts/validate_atlas_pack_parity.py`, `scripts/validate_optional_pack_demos.py`

### Funciones/Clases clave
- `count_user_invocable()` en `validate_plugin_packs.py` — debe actualizarse para permitir conductores `user-invocable: false`
- `CANONICAL_SHARED` en `validate_atlas_pack_parity.py` — 19 archivos; no cambia en esta feature
- `ROOT_ONLY` en `validate_atlas_pack_parity.py` — 7 aliases; no cambia

### Dependencias
- `@modelcontextprotocol/server-memory`: npm package para el MCP knowledge graph
- Existing Python validators: `pytest` tests pattern en `scripts/test_validate_*.py`
- `thedotmack/claude-mem`: referencia de arquitectura para el memory system (no instalar servidor; documentar)
- `athola/claude-night-market`: evaluar en Phase 6; no duplicar agentes existentes

### Patrones y convenciones
- Frontmatter siempre primero: `---\n...\n---\n`
- `<!-- layer: N | parent: ... -->` comment después del closing `---` (nuevo patrón)
- `user-invocable: false` para todos los agentes excepto Atlas y PackCatalog
- `agents:` siempre lista explícita; nunca `["*"]`
- Tools: lista deduplicada de nombres válidos VS Code (`agent`, `search`, `usages`, `problems`, `changes`, `testFailure`, `web`, `fetch`, `edit`, `execute`, `read`, `mcp`)
- Tests: `scripts/test_validate_X.py` con patrón `pytest`, sin dependencias externas

---

## Fase 1: Constitution + Spec (Specify Pipeline Setup)

**Objetivo**: Actualizar la constitución con Principio VIII (Strict Layer Isolation) y crear los artefactos Specify validados que guiarán todas las fases posteriores.

**Ficheros a modificar/crear:**
- `.specify/memory/constitution.md` — añadir Principio VIII
- `.specify/specs/layered-agent-hierarchy/spec.md` — ✅ YA CREADO
- `.specify/specs/layered-agent-hierarchy/plan.md` — ✅ YA CREADO
- `.specify/specs/layered-agent-hierarchy/analysis-report.md` — ✅ YA CREADO (SP-5 PASSED)

**Foco de QA:**
- Argus: verificar que constitution.md es válido Markdown; que el nuevo principio no contradice los anteriores
- Themis: validar que spec y plan son consistentes (ya verificado en analysis-report.md)

**Pasos:**
1. Agregar **Principio VIII: Strict Layer Isolation** a `.specify/memory/constitution.md`:
   ```markdown
   ### VIII. Strict Layer Isolation (NON-NEGOTIABLE)
   The agent system operates in exactly 3 layers: Layer 0 (Atlas), Layer 1 (Domain Gods),
   Layer 2 (Specialists). Hard rules:
   a) An agent at Layer N may ONLY call agents at Layer N+1 (its own subtree).
   b) Atlas (L0) MUST list only L1 gods in its `agents:` frontmatter. `agents: ["*"]` is FORBIDDEN.
   c) Any agent at Layer 2 is a leaf — it MAY NOT invoke other agents unless it is a pack conductor,
      in which case it may invoke only the leaf specialists within its own pack.
   d) Every agent file MUST carry a `<!-- layer: N -->` metadata comment after its frontmatter.
   e) No agent may be added to the system without a declared parent in the layer above it.
   ```
2. Sync constitution.md update to its template origin (document in `SPECIFY_PIPELINE_STATUS`).
3. Verify SP-5 analysis report status: PASSED (already at `.specify/specs/layered-agent-hierarchy/analysis-report.md`).

**Criterios de aceptación:**
- [ ] `.specify/memory/constitution.md` tiene Principio VIII
- [ ] Principio VIII enumera las 5 reglas hard (a–e)
- [ ] `spec.md`, `plan.md`, `analysis-report.md` existen en `.specify/specs/layered-agent-hierarchy/`
- [ ] SP-5 gate: `analysis-report.md` dice `READY_FOR_IMPLEMENTATION: true`

---

## Fase 2: Atlas L0 Layer Enforcement

**Objetivo**: Reemplazar `agents: ["*"]` en Atlas por la lista explícita de los 18 agentes L1, añadir la prohibición explicita de llamar L2, y corregir los nombres de tools inválidos. Mantener parity perfecta entre las dos copias de Atlas.

**Ficheros a modificar:**
- `.github/agents/Atlas.agent.md`
- `plugins/atlas-orchestration-team/agents/Atlas.agent.md`

**Foco de QA:**
- Argus: ejecutar `validate_atlas_pack_parity.py` — debe dar EXIT 0
- Themis: verificar que routing policy no menciona ningún agente L2 como target directo

**Pasos:**
1. En `.github/agents/Atlas.agent.md`:
   a. Reemplazar `agents: ["*"]` por:
      ```yaml
      agents:
        - Prometheus
        - Sisyphus
        - Themis
        - Argus
        - Hermes
        - Oracle
        - Atenea
        - Ariadna
        - Clio
        - Hephaestus
        - Afrodita-UX
        - Hermes-subagent
        - Oracle-subagent
        - Sisyphus-subagent
        - Afrodita-subagent
        - Argus-subagent
        - Themis-subagent
        - Hephaestus-subagent
      ```
   b. Añadir `<!-- layer: 0 -->` después del cierre `---`.
   c. Corregir tools: reemplazar `web/fetch` → `web`, `fetch`; `execute/getTerminalOutput` → `execute`; `execute/runInTerminal` → `execute` (deduplicar); `read/terminalLastCommand` → `read`; `read/terminalSelection` → `read` (deduplicar).
   d. En la sección "Routing policy", añadir al inicio:
      ```
      **Layer hierarchy rule:** Atlas operates at Layer 0. NEVER call Layer 2 specialists
      (Backend-Atlas, Service-Builder, UI-Designer, etc.) directly. All work is delegated
      exclusively through the Layer 1 domain gods listed in the `agents:` frontmatter.
      ```
2. Replicar todos los cambios en `plugins/atlas-orchestration-team/agents/Atlas.agent.md` para mantener parity.
3. Ejecutar `python scripts/validate_atlas_pack_parity.py` — EXIT 0 requerido.

**Criterios de aceptación:**
- [ ] `agents:` en Atlas no contiene `"*"` ni ningún agente L2
- [ ] `agents:` lista exactamente los 18 agentes L1 definidos en el plan
- [ ] `tools:` en Atlas contiene solo nombres válidos VS Code (sin `/`-patterns)
- [ ] `<!-- layer: 0 -->` comment presente en ambas copias
- [ ] `validate_atlas_pack_parity.py` pasa con EXIT 0
- [ ] Routing policy section tiene la regla de prohibición L2 en primer párrafo

---

## Fase 3: Layer 1 God Upgrades (22 archivos canónicos + 7 aliases)

**Objetivo**: Actualizar cada uno de los 11 dioses mitológicos canónicos para ser conductores explícitos de su dominio: lista L2 en frontmatter, sección "Layer 2 Roster", protocolo de memoria, corrección de tool names, comment de capa. Mantener parity entre `.github/agents/` y `plugins/atlas-orchestration-team/agents/`. Actualizar los 7 root-only aliases.

**Ficheros a modificar** (29 total):
- `.github/agents/` + `plugins/atlas-orchestration-team/agents/`: 11 gods × 2 = 22 archivos
- `.github/agents/` only: 7 root-only aliases = 7 archivos

**Sub-tareas por dios** (ejecutar una por una; correr parity check tras cada par):

### 3.1 Prometheus
- `agents:` → `["SpecifyConstitution", "SpecifySpec", "SpecifyClarify", "SpecifyPlan", "SpecifyTasks", "SpecifyAnalyze", "SpecifyImplement"]`
- Añadir "Layer 2 Roster" section en system prompt
- Añadir "Memory Protocol" section (template de plan.md)
- Tool fix: `web/fetch` → `web`, `fetch`
- Añadir `<!-- layer: 1 | domain: Planning + Specification + Memory -->` comment
- También: Prometheus es propietario de memory — añadir nota en "Memory Protocol" que Prometheus puede usar `mcp` tool para knowledge graph

### 3.2 Sisyphus
- `agents:` → `["Backend-Atlas", "Data-Atlas", "SpecifyTasks", "SpecifyAnalyze", "SpecifyImplement"]`
  > Nota: Sisyphus mantiene acceso a los Specify agents (EX pipeline) según su definición actual
- Añadir "Layer 2 Roster" section  
- Añadir "Memory Protocol" section
- Tool fix: `execute/getTerminalOutput` → `execute`; `execute/runInTerminal` → `execute` (dedup); `read/terminalLastCommand` → `read`; `read/terminalSelection` → `read` (dedup); `read/problems` → `problems`; `search/changes` → `changes`
- Añadir `<!-- layer: 1 | domain: Backend + Data Implementation -->` comment

### 3.3 Themis
- `agents:` → `["Backend-Reviewer", "Frontend-Reviewer", "Data-Reviewer", "Automation-Reviewer"]`
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section
- Tools: ya tiene nombres válidos (`changes`, `problems`, `usages`, `search`) — verificar
- Añadir `<!-- layer: 1 | domain: Code Review + Quality Gate -->` comment

### 3.4 Argus
- `agents:` → `["A11y-Auditor", "Test-Runner", "Coverage-Analyst", "Mutation-Tester"]`
  > Test-Runner, Coverage-Analyst, Mutation-Tester son nuevos (se crean en Fase 4)
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section (write: test outcomes + coverage metrics)
- Tools: ya usa `execute`, `search`; verificar completeness
- Añadir `<!-- layer: 1 | domain: QA + Testing -->` comment

### 3.5 Hermes
- `agents:` → `[]` (self-sufficient scout; no pack L2)
- Añadir "Memory Protocol" section (read only; Hermes is stateless scout)
- Tools: ya tiene nombres válidos (`search`, `usages`, `problems`, `changes`, `testFailure`) — verificar
- Añadir `<!-- layer: 1 | domain: Discovery + Codebase Mapping -->` comment

### 3.6 Oracle
- `agents:` → `[]` (self-sufficient researcher; no pack L2)
- Añadir "Memory Protocol" section (read decision log before research)
- Tool fix: `web/fetch` → `web`, `fetch`
- Añadir `<!-- layer: 1 | domain: Requirements + Architecture Research -->` comment

### 3.7 Atenea
- `agents:` → `["Security-Guard", "Security-Ops", "Compliance-Checker", "Secret-Scanner"]`
  > Compliance-Checker, Secret-Scanner son nuevos (se crean en Fase 4)
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section (read/write security findings)
- Tool fix: `execute/runInTerminal` → `execute`; `execute/getTerminalOutput` → `execute` (dedup)
- Añadir `<!-- layer: 1 | domain: Security + Safety -->` comment

### 3.8 Ariadna
- `agents:` → `[]` (self-sufficient dependency auditor)
- Añadir "Memory Protocol" section (read dependency decision log)
- Tools: ya usa `search`, `execute`, `changes`, `problems` — verificar nombres válidos
- Añadir `<!-- layer: 1 | domain: Dependency + Package Audit -->` comment

### 3.9 Clio
- `agents:` → `["Frontend-Handoff"]`
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section (write doc decisions)
- Tools: ya usa `edit`, `search`, `changes`, `usages`, `problems` — verificar
- Añadir `<!-- layer: 1 | domain: Documentation -->` comment

### 3.10 Hephaestus
- `agents:` → `["DevOps-Atlas", "Automation-Atlas", "Cost-Optimizer", "Incident-Responder"]`
  > Cost-Optimizer, Incident-Responder son nuevos (se crean en Fase 4)
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section (read incident log, write operational decisions)
- Tool fix: `execute/getTerminalOutput` → `execute`; `execute/runInTerminal` → `execute` (dedup); `read/terminalLastCommand` → `read`; `read/terminalSelection` → `read` (dedup)
- Añadir `<!-- layer: 1 | domain: Infrastructure + DevOps + Automation -->` comment

### 3.11 Afrodita-UX
- `agents:` → `["Afrodita", "UX-Atlas"]`
- Añadir "Layer 2 Roster" section
- Añadir "Memory Protocol" section
- Tool fix: `execute/runInTerminal` → `execute`; `execute/getTerminalOutput` → `execute` (dedup); `read/terminalLastCommand` → `read`; `read/terminalSelection` → `read` (dedup); `web/fetch` → `web`, `fetch`
- Añadir `<!-- layer: 1 | domain: Frontend + UX -->` comment

### 3.12 Root-only aliases (7 files, `.github/agents/` only)
Para cada alias (`Afrodita-subagent`, `Argus-subagent`, `Hermes-subagent`, `Hephaestus-subagent`, `Sisyphus-subagent`, `Themis-subagent`, `Oracle-subagent`):
- Añadir `<!-- layer: 1 | type: alias | delegates-to: <parent-god> -->` comment
- Tool fix: same patterns como su god padre
- Verificar que `user-invocable: false` (ya debería estar)

**Foco de QA:**
- Argus: `python scripts/validate_atlas_pack_parity.py` — EXIT 0 tras CADA sub-tarea 3.1–3.11
- Themis: verificar que `agents:` lists en gods no contienen agentes L0 o de otras ramas

**Criterios de aceptación:**
- [ ] Cada uno de los 11 gods tiene `<!-- layer: 1 -->` comment en ambas copias
- [ ] Cada god con L2 agents tiene "Layer 2 Roster" section en system prompt
- [ ] Cada god tiene "Memory Protocol" section con read/write instructions
- [ ] CERO tools con patterns `/`-slash en cualquier god file
- [ ] `validate_atlas_pack_parity.py` pasa con EXIT 0
- [ ] 7 aliases tienen `<!-- layer: 1 | type: alias -->` comment
- [ ] Ningún alias tiene `user-invocable: true`

---

## Fase 4: Layer 2 Conductor Updates + New Gap Agents

**Objetivo**: Actualizar los 6 conductores de pack para reportar a su dios padre (añadir `user-invocable: false`, parent reference, explicit `agents:` list, memory protocol comentario, fix tool names). Crear los 9 nuevos agentes L2 para cerrar gaps de cobertura.

### 4.1 Actualizar conductores existentes

**Para cada conductor, aplicar:**
- `user-invocable: false` (Constitution Principle I)
- Añadir en frontmatter comment: `<!-- layer: 2 | parent: <L1God> -->`
- Reemplazar `agents: ["*"]` por lista explícita de sus especialistas
- Fix tool names (especialmente `runCommands` → `execute`)
- Añadir `parentGod: <L1God>` como comment in YAML (informativo)

**Backend-Atlas** (`plugins/backend-workflow/agents/Backend-Atlas.agent.md`):
- Parent: Sisyphus
- `agents:` → `["API-Designer", "Service-Builder", "Database-Engineer", "Performance-Tuner", "Security-Guard", "Backend-Planner", "Backend-Reviewer"]`
- Fix tools (verificar tool names válidos)
- Añadir "Memory Protocol" section (lightweight: read session context, write implementation decisions)
- Añadir `<!-- layer: 2 | parent: Sisyphus -->`

**Data-Atlas** (`plugins/data-workflow/agents/Data-Atlas.agent.md`):
- Parent: Sisyphus
- `agents:` → `["Pipeline-Builder", "ML-Scientist", "Data-Architect", "Analytics-Engineer", "Data-Quality", "Data-Planner", "Data-Reviewer"]`
- Fix tools
- Añadir `<!-- layer: 2 | parent: Sisyphus -->`

**DevOps-Atlas** (`plugins/devops-workflow/agents/DevOps-Atlas.agent.md`):
- Parent: Hephaestus
- `agents:` → `["Infra-Architect", "Pipeline-Engineer", "Container-Master", "Deploy-Strategist", "Monitor-Sentinel", "Security-Ops", "DevOps-Planner", "Cost-Optimizer", "Incident-Responder"]`
- Fix tools
- Añadir `<!-- layer: 2 | parent: Hephaestus -->`

**Automation-Atlas** (`plugins/automation-mcp-workflow/agents/Automation-Atlas.agent.md`):
- Parent: Hephaestus
- `agents:` → `["Workflow-Composer", "MCP-Integrator", "Automation-Planner", "Automation-Reviewer", "n8n-Connector"]`
- Fix: `runCommands` → `execute`
- Añadir `<!-- layer: 2 | parent: Hephaestus -->`

**Afrodita (frontend conductor)** (`plugins/frontend-workflow/agents/Afrodita.agent.md`):
- Parent: Afrodita-UX
- `agents:` → `["UI-Designer", "Style-Engineer", "State-Manager", "Component-Builder", "Frontend-Planner", "Frontend-Reviewer", "A11y-Auditor"]`
- Fix: `runCommands` → `execute`
- Añadir `<!-- layer: 2 | parent: Afrodita-UX -->`

**UX-Atlas** (`plugins/ux-enhancement-workflow/agents/UX-Atlas.agent.md`):
- Parent: Afrodita-UX
- `agents:` → `["User-Flow-Designer", "Design-Critic", "Accessibility-Heuristics", "Frontend-Handoff", "UX-Planner"]`
- Fix: `runCommands` → `execute` (si aplica)
- Añadir `<!-- layer: 2 | parent: Afrodita-UX -->`

### 4.2 Añadir layer comments a todos los especialistas L2 existentes

Para CADA agente especialista en los 6 packs existentes (no conductores):
- Añadir `<!-- layer: 2 | parent: <conductor> > <L1God> -->` comment después del frontmatter
- **NO** cambiar otra cosa — solo el layer comment

Archivos afectados (~42 agentes):
- `plugins/backend-workflow/agents/`: 7 especialistas
- `plugins/data-workflow/agents/`: 7 especialistas
- `plugins/devops-workflow/agents/`: 7 especialistas
- `plugins/automation-mcp-workflow/agents/`: 4 especialistas
- `plugins/frontend-workflow/agents/`: 7 especialistas
- `plugins/ux-enhancement-workflow/agents/`: 5 especialistas

### 4.3 Crear nuevos agentes L2

**`plugins/qa-workflow/agents/Test-Runner.agent.md`**
```yaml
---
name: Test-Runner
description: Execute targeted test commands (unit, integration, e2e) and return structured pass/fail results with output excerpts.
user-invocable: false
argument-hint: Run tests for <scope>. Return: status, failures, coverage if available.
model:
  - Claude Haiku 4.5 (copilot)
  - GPT-5.2 (copilot)
tools:
  - execute
  - read
  - search
---
<!-- layer: 2 | parent: Argus -->
```

**`plugins/qa-workflow/agents/Coverage-Analyst.agent.md`**
```yaml
---
name: Coverage-Analyst
description: Measure test coverage, identify uncovered paths, and produce a prioritized gap report.
user-invocable: false
argument-hint: Analyze coverage for <scope>. Identify top 3 uncovered paths.
model:
  - Claude Haiku 4.5 (copilot)
tools:
  - execute
  - read
  - search
  - problems
---
<!-- layer: 2 | parent: Argus -->
```

**`plugins/qa-workflow/agents/Mutation-Tester.agent.md`**
```yaml
---
name: Mutation-Tester
description: Apply code mutations to high-risk logic and verify that existing tests detect them. Reports mutation score and surviving mutants.
user-invocable: false
argument-hint: Run mutation testing for <file/function>. Report mutation score and top surviving mutants.
model:
  - Claude Sonnet 4.6 (copilot)
tools:
  - execute
  - read
  - search
  - edit
---
<!-- layer: 2 | parent: Argus -->
```

**`plugins/security-workflow/agents/Compliance-Checker.agent.md`**
```yaml
---
name: Compliance-Checker
description: Audit code and configuration for regulatory compliance (GDPR, HIPAA, SOC2, PCI-DSS) and internal policy adherence.
user-invocable: false
argument-hint: Audit <scope> for compliance with <framework>. Return findings and remediation steps.
model:
  - GPT-5.4 (copilot)
  - Claude Sonnet 4.6 (copilot)
tools:
  - search
  - changes
  - problems
  - read
---
<!-- layer: 2 | parent: Atenea -->
```

**`plugins/security-workflow/agents/Secret-Scanner.agent.md`**
```yaml
---
name: Secret-Scanner
description: Detect hardcoded secrets, API keys, tokens, and credentials in code, config, and history.
user-invocable: false
argument-hint: Scan <scope> for hardcoded secrets. Return confirmed findings and false-positive notes.
model:
  - Claude Haiku 4.5 (copilot)
tools:
  - search
  - changes
  - read
---
<!-- layer: 2 | parent: Atenea -->
```

**`plugins/devops-workflow/agents/Cost-Optimizer.agent.md`**
```yaml
---
name: Cost-Optimizer
description: Analyze cloud resource usage, identify cost inefficiencies, and propose rightsizing or elimination recommendations.
user-invocable: false
argument-hint: Analyze <resource/service> costs. Return top 3 optimization recommendations with estimated savings.
model:
  - GPT-5.4 (copilot)
  - Claude Sonnet 4.6 (copilot)
tools:
  - search
  - execute
  - read
  - fetch
---
<!-- layer: 2 | parent: Hephaestus > DevOps-Atlas -->
```

**`plugins/devops-workflow/agents/Incident-Responder.agent.md`**
```yaml
---
name: Incident-Responder
description: Structured incident response: detect, triage, mitigate, and produce a root cause analysis report.
user-invocable: false
argument-hint: Respond to incident: <description/alert>. Produce: severity, timeline, RCA, mitigation steps.
model:
  - Claude Sonnet 4.6 (copilot)
  - GPT-5.4 (copilot)
tools:
  - search
  - execute
  - read
  - problems
---
<!-- layer: 2 | parent: Hephaestus > DevOps-Atlas -->
```

**`plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md`**
```yaml
---
name: n8n-Connector
description: Generate n8n workflow JSON definitions via MCP integration. Requires n8n MCP server configured in .vscode/mcp.json.
user-invocable: false
argument-hint: Generate n8n workflow for <automation goal>. Return: workflow JSON + setup instructions.
model:
  - Claude Sonnet 4.6 (copilot)
  - GPT-5.4 (copilot)
tools:
  - mcp
  - search
  - fetch
  - edit
# PREREQUISITE: n8n MCP server must be configured in .vscode/mcp.json
---
<!-- layer: 2 | parent: Hephaestus > Automation-Atlas -->
```

**`plugins/memory-system/agents/Memory-Guardian.agent.md`**
```yaml
---
name: Memory-Guardian
description: Capture, compress, and retrieve agent session memory. Manages session-memory.md, decision-log.md, and the MCP knowledge graph.
user-invocable: false
argument-hint: <capture|retrieve|summarize> memory for session <ID>. Use mode: capture|retrieve|compress.
model:
  - Claude Haiku 4.5 (copilot)
  - Claude Sonnet 4.6 (copilot)
tools:
  - mcp
  - edit
  - search
  - read
---
<!-- layer: 2 | parent: Prometheus -->
```

**Foco de QA (Fase 4):**
- Argus: run `validate_plugin_packs.py` — debe pasar con todos los nuevos agentes
- Themis: verificar que `user-invocable: false` en todos los conductores
- Argus: verificar que cada nuevo agente tiene layer comment y tools válidos

**Criterios de aceptación:**
- [ ] Los 6 conductores tienen `user-invocable: false`
- [ ] Los 6 conductores tienen `<!-- layer: 2 | parent: <L1God> -->` comment
- [ ] Los 6 conductores tienen `agents:` lista explícita (no `["*"]`)
- [ ] Los ~42 especialistas existentes tienen `<!-- layer: 2 -->` comment
- [ ] Los 9 nuevos agentes existen en sus directorios correctos
- [ ] Todos los nuevos agentes tienen tools válidos (solo nombres del set válido)
- [ ] `validate_plugin_packs.py` pasa con EXIT 0
- [ ] CERO herramientas con `/`-patterns en cualquier file de plugin packs

---

## Fase 5: Memory System Integration

**Objetivo**: Implementar el protocolo de memoria de 3 niveles en todos los agentes L1, configurar el MCP knowledge graph server, y crear el pack `memory-system`.

**Ficheros a crear:**
- `.vscode/mcp.json` — MCP server configuration
- `plugins/memory-system/README.md` — documentación del memory pack
- `plugins/memory-system/.github/plugin/plugin.json` — plugin metadata

**Pasos:**
1. **Crear `.vscode/mcp.json`**:
   - Verificar si el archivo ya existe; si sí, MERGE el nuevo server entry, no sobreescribir
   - Contenido (merge-safe):
     ```json
     {
       "servers": {
         "memory": {
           "command": "npx",
           "args": ["-y", "@modelcontextprotocol/server-memory"],
           "type": "stdio"
         }
       }
     }
     ```

2. **Verificar todos los agentes L1** tienen la sección "Memory Protocol" del template (ya hecho en Fase 3). Esta fase confirma completitud.

3. **Crear `plugins/memory-system/`** con estructura:
   ```
   plugins/memory-system/
     .github/
       plugin/
         plugin.json
     agents/
       Memory-Guardian.agent.md   ← ya creado en Fase 4
     README.md
   ```
   
4. **`plugin.json`**:
   ```json
   {
     "id": "memory-system",
     "name": "Memory System",
     "description": "Persistent 3-level memory for agent sessions: session-memory, decision-log, MCP knowledge graph.",
     "version": "1.0.0",
     "conductor": "Memory-Guardian",
     "parentGod": "Prometheus",
     "agentDirs": ["agents"]
   }
   ```

5. **`README.md`** debe documentar:
   - Los 3 niveles de memoria (session, decision-log, knowledge graph)
   - Cómo configurar `@modelcontextprotocol/server-memory`  
   - Referencia a `thedotmack/claude-mem` para memoria avanzada (TypeScript/SQLite/ChromaDB)
   - Instrucciones de uso de `Memory-Guardian`

6. **Agregar `mcp` tool** a la lista de tools de todos los agentes L1 que aún no lo tengan (para habilitarlos con el MCP server). Actualizar los files modificados en Fase 3 si fue omitido.

**Foco de QA (Fase 5):**
- Argus: verificar que `.vscode/mcp.json` es JSON válido
- Argus: verificar que todos los L1 gods tienen "Memory Protocol" section
- Themis: verificar que `Memory-Guardian` tiene tool `mcp` y tools válidos

**Criterios de aceptación:**
- [ ] `.vscode/mcp.json` existe y contiene `@modelcontextprotocol/server-memory` entry
- [ ] JSON de mcp.json válido (sin syntax errors)
- [ ] `plugins/memory-system/` existe con los 3 archivos requeridos
- [ ] `Memory-Guardian.agent.md` tiene `tools: [mcp, edit, search, read]` (valid names)
- [ ] Todos los 11 agentes L1 tienen "Memory Protocol" section
- [ ] `plugins/memory-system/.github/plugin/plugin.json` contiene `parentGod: "Prometheus"`

---

## Fase 6: External Agents + UX Knowledge Base + n8n Integration

**Objetivo**: Integrar evaluaciones de fuentes externas, crear la base de conocimiento UX por categoría de industria, y configurar los templates de automatización n8n.

**Ficheros a crear:**
- `plugins/ux-enhancement-workflow/skills/industry-verticals.md`
- `plugins/automation-mcp-workflow/templates/n8n-workflow-examples.md`
- `plugins/memory-system/research/external-sources-evaluation.md`

**Sub-tareas:**

### 6.1 Evaluar e integrar claude-night-market
1. Leer `athola/claude-night-market` (47 agents, 142 skills, 109 commands) via web fetch
2. Producir `plugins/memory-system/research/external-sources-evaluation.md` con:
   - Tabla: agente externo vs agente interno equivalente (duplicado = skip)
   - Lista de agentes/skills no duplicativos que aportan valor
   - Decisión de integración para cada uno
3. Para los no-duplicativos identificados: crear stub agents en el pack correspondiente con `<!-- SOURCE: athola/claude-night-market -->` comment
4. Evaluar `aplaceforallmystuff/claude-agent-borg` como skill de discovery: documentar su aporte en el evaluation report

### 6.2 UX Industry Knowledge Base
Crear `plugins/ux-enhancement-workflow/skills/industry-verticals.md` con:
- Mínimo 10 categorías principales (Healthcare, Finance, E-commerce, Education, Travel, Legal, Manufacturing, Government, Media, Real Estate)
- Por cada categoría: UX patterns clave, usuarios típicos, regulatory considerations, design priorities
- Estructura scannable: H2 por industria, bullet lists por sub-categoría
- Total: >500 líneas de knowledge base

Actualizar `UX-Atlas.agent.md` routing policy para referenciar este skill file cuando el usuario especifica un vertical de industria.

### 6.3 n8n Workflow Templates
Crear `plugins/automation-mcp-workflow/templates/n8n-workflow-examples.md` con:
- 5 workflow templates comunes: HTTP Webhook + Transform + Notify, Scheduled ETL, Code Review Notification, Multi-system Data Sync, Agent-to-n8n Bridge
- Para cada template: JSON skeleton, trigger config, node types, success criteria
- Instrucciones para `n8n-Connector` para usar estos templates como base

Actualizar `Automation-Atlas.agent.md` para referenciar `n8n-Connector` en su routing policy y los templates en su context.

**Foco de QA (Fase 6):**
- Themis: verificar que ningún agente importado duplica funcionalidad existente
- Argus: verificar que todos los nuevos agent files tienen frontmatter válido y layer comment
- Atenea: revisar que no hay secrets o patrones inseguros en los templates de n8n

**Criterios de aceptación:**
- [ ] `external-sources-evaluation.md` existe con tabla de duplicados evaluados
- [ ] `industry-verticals.md` tiene ≥10 industrias con UX patterns
- [ ] `n8n-workflow-examples.md` tiene ≥5 workflow templates con JSON skeletons
- [ ] Cualquier agente importado tiene `<!-- SOURCE: <repo> -->` en frontmatter comment
- [ ] `Automation-Atlas.agent.md` menciona `n8n-Connector` en su routing section
- [ ] UX-Atlas.agent.md referencia `skills/industry-verticals.md` cuando hay context de industria
- [ ] Todos los nuevos agents pasan `validate_plugin_packs.py`

---

## Fase 7: Pack Registry + Validation Scripts + Demo

**Objetivo**: Actualizar el registro oficial de packs, crear 2 nuevos scripts de validación con sus test suites, y entregar el demo `hierarchy-architecture-demo` con ≥24 tests. Verificar que el total de tests supera 250.

### 7.1 Actualizar pack-registry.json

Añadir a `.github/plugin/pack-registry.json`:
```json
{
  "id": "qa-workflow",
  "name": "QA & Testing Workflow",
  "installPath": "plugins/qa-workflow",
  "shipped": true,
  "defaultActive": false,
  "marketplacePublished": false,
  "activationPath": "plugins/qa-workflow/agents",
  "conductor": null,
  "parentGod": "Argus",
  "stability": "beta"
},
{
  "id": "security-workflow",
  "name": "Security & Compliance Workflow",
  "installPath": "plugins/security-workflow",
  "shipped": true,
  "defaultActive": false,
  "marketplacePublished": false,
  "activationPath": "plugins/security-workflow/agents",
  "conductor": null,
  "parentGod": "Atenea",
  "stability": "beta"
},
{
  "id": "memory-system",
  "name": "Memory System",
  "installPath": "plugins/memory-system",
  "shipped": true,
  "defaultActive": false,
  "marketplacePublished": false,
  "activationPath": "plugins/memory-system/agents",
  "conductor": "Memory-Guardian",
  "parentGod": "Prometheus",
  "stability": "alpha"
}
```

Añadir campo `"parentGod"` a todos los packs existentes:
- `frontend-workflow` → `"parentGod": "Afrodita-UX"`
- `backend-workflow` → `"parentGod": "Sisyphus"`
- `devops-workflow` → `"parentGod": "Hephaestus"`
- `data-workflow` → `"parentGod": "Sisyphus"`
- `automation-mcp-workflow` → `"parentGod": "Hephaestus"`
- `ux-enhancement-workflow` → `"parentGod": "Afrodita-UX"`
- `atlas-orchestration-team` → `"parentGod": null` (canonical source)
- `agent-pack-catalog` → `"parentGod": null` (exception)

### 7.2 Actualizar marketplace.json y settings.json

- Añadir entradas en `marketplace.json` para los 3 nuevos packs
- Añadir en `.vscode/settings.json`:
  ```json
  "plugins/qa-workflow/agents": true,
  "plugins/security-workflow/agents": true,
  "plugins/memory-system/agents": true
  ```

### 7.3 Crear scripts/validate_tool_names.py

Script que:
- Lee todos los `*.agent.md` en `.github/agents/` y `plugins/**/agents/`
- Para cada archivo, extrae la lista `tools:` del frontmatter
- Verifica que cada tool name pertenece al set válido
- Emite FAIL + lista de violations si encuentra inválidos; EXIT 0 si todo OK

Tests en `scripts/test_validate_tool_names.py` (≥20 test cases):
- Archivo con tools válidos → PASS
- Archivo con `web/fetch` → FAIL con mensaje descriptivo
- Archivo con `execute/runInTerminal` → FAIL
- Archivo con `read/terminalLastCommand` → FAIL
- Archivo con `runCommands` → FAIL
- Archivo sin frontmatter → ValidationError
- Archivo con tools vacíos → PASS (permitido)
- Archivo con `mcp` → PASS
- Todos los agents del repo actuales (después de fixes) → PASS

### 7.4 Crear scripts/validate_layer_hierarchy.py

Script que:
- Lee todos los `*.agent.md` en `.github/agents/` y `plugins/**/agents/`
- Para cada archivo, busca `<!-- layer: N` comment
- Verifica que se asigna la capa 0, 1, o 2
- Verifica que Atlas (L0) `agents:` list no contiene L2 agents
- Emite tabla: `file | layer | parent | status`
- Emite ORPHAN error para agents sin layer comment
- Sale con EXIT 1 si hay cualquier violación

Tests en `scripts/test_validate_layer_hierarchy.py` (≥25 test cases):
- Agent con `<!-- layer: 0 -->` → assigns layer 0
- Agent con `<!-- layer: 1 -->` → assigns layer 1
- Agent con `<!-- layer: 2 | parent: ... -->` → assigns layer 2 with parent
- Agent sin layer comment → ORPHAN error
- Atlas.agent.md sin L2 agents en `agents:` → PASS
- Atlas.agent.md con `Backend-Atlas` en `agents:` → FAIL (L2 directly in L0)
- Validar todos los agents del repo → EXIT 0

### 7.5 Actualizar validate_plugin_packs.py

- Añadir check: si un agent tiene `name:` matching un pack conductor, verificar `user-invocable: false`
- Añadir check: si un pack tiene `parentGod` en registry, verificar que el conductor tiene el comment `<!-- layer: 2 | parent: <parentGod> -->`

### 7.6 Demo: hierarchy-architecture-demo

Crear `demos/hierarchy-architecture-demo/`:
```
demos/hierarchy-architecture-demo/
  DEMO_PROMPT.md
  README.md
  tests/
    test_hierarchy_routing.py
    test_layer_boundaries.py
    test_memory_protocol.py
    test_tool_names.py
```

**`DEMO_PROMPT.md`** (guión del demo):
Guía a Atlas a ejecutar una tarea de extremo a extremo que demuestre los 3 layers:
1. Atlas recibe un task → delega a Prometheus (L0→L1)
2. Prometheus invoca SpecifySpec (L1→L2)
3. Atlas delega implementación a Sisyphus (L0→L1)
4. Sisyphus invoca Backend-Atlas (L1→L2)
5. Atlas delega revisión a Themis (L0→L1) → Themis invoca Backend-Reviewer (L1→L2)
6. Atlas delega QA a Argus (L0→L1)
7. Demostrar memory protocol: session-memory.md actualizado tras cada fase

**Tests** (≥24 casos distribuidos en 4 archivos):
- `test_hierarchy_routing.py`: 8 tests — Atlas routes to L1; no L2 in Atlas agents list; god files have L2 roster; no cross-domain calls
- `test_layer_boundaries.py`: 6 tests — every agent has layer comment; no orphans; Atlas L0 compliant; conductors L2 compliant
- `test_memory_protocol.py`: 5 tests — L1 gods have memory section; mcp.json exists; memory-system pack registered; Memory-Guardian has mcp tool
- `test_tool_names.py`: 5 tests — no invalid patterns in agent files; valid set check; new agents pass validation

**Foco de QA (Fase 7):**
- Argus: ejecutar FULL test suite — objetivo ≥250 tests pasando
- Argus: `validate_tool_names.py` → 0 violations
- Argus: `validate_layer_hierarchy.py` → 0 orphans, 0 violations
- Argus: `validate_atlas_pack_parity.py` → EXIT 0
- Argus: `validate_plugin_packs.py` → EXIT 0

**Criterios de aceptación:**
- [ ] `pack-registry.json` tiene `parentGod` en todos los packs
- [ ] 3 nuevos packs en registry (qa-workflow, security-workflow, memory-system)
- [ ] `.vscode/settings.json` tiene las 3 nuevas rutas de agents
- [ ] `scripts/validate_tool_names.py` existe y pasa con 0 violations
- [ ] `scripts/validate_layer_hierarchy.py` existe y pasa con 0 orphans
- [ ] `scripts/test_validate_tool_names.py` tiene ≥20 test cases, todos pasan
- [ ] `scripts/test_validate_layer_hierarchy.py` tiene ≥25 test cases, todos pasan
- [ ] `demos/hierarchy-architecture-demo/DEMO_PROMPT.md` existe con guión completo
- [ ] Demo test suite: ≥24 tests, todos pasan
- [ ] **Total test suite: ≥250 tests pasando**
- [ ] Todos los validators existentes siguen pasando (regression: ≥183 tests from before)

---

## Preguntas Abiertas

1. **¿Crear dios "Mnemo" para memoria cross-cutting?**
   - **Opción A:** Nuevo L1 god Mnemo (dedicado a memoria, observabilidad, knowledge graph). Pros: clean ownership. Cons: nueva entidad, actualiza routing de Atlas.
   - **Opción B (asumida):** Prometheus es dueño de la memoria. Prometheus ya gestiona `.specify/memory/`. Conservative.
   - **Recomendación:** Opción B. Revisitar si la memoria se vuelve un dominio propio en v2.

2. **¿Debería Oracle tener un pack de planners como L2?**
   - **Opción A:** Crear "Research-Planners Pack" bajo Oracle. Pros: clean L2. Cons: duplica planners existentes.
   - **Opción B (asumida):** Oracle es self-sufficient; usa sus tools directamente. Los planners permanecen en sus packs de dominio.
   - **Recomendación:** Opción B.

3. **¿Deberían las Fase 3–4 ejecutarse en paralelo?**
   - **Opción A (asumida):** Secuencial por god (3.1 → 3.11) para mantener parity checks intermedios controlados.
   - **Opción B:** Sisyphus paralelo por dominio (gods sin dependencias entre sí). More efficient pero riesgo de merge conflict.
   - **Recomendación:** Opción A para la primera ejecución; Opción B viable en re-ejecuciones.

---

## Riesgos y Mitigación

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Parity check falla tras Phase 3 | Alta | Correr `validate_atlas_pack_parity.py` tras cada sub-tarea 3.x; no agregar al mismo commit ambas copias si hay duda |
| `validate_plugin_packs.py` falla por `user-invocable: false` en conductores | Media | Actualizar el script en Phase 7 paso 7.5 ANTES de correr la suite completa |
| Tool name corrections introducen errores (e.g., deduplicación incorrecta) | Media | `validate_tool_names.py` actúa como safety net en Phase 7 |
| Phase 3 con 29 archivos pierde algún archivo | Alta | Usar checklist explícita (sub-tareas 3.1–3.12 marcadas como `[x]` al completar) |
| MCP server `@modelcontextprotocol/server-memory` no disponible en npm | Baja | Script de verificación en Phase 5 documenta si el package está disponible; fallback a file-only memory |
| claude-night-market tiene agentes con tools inválidos | Media | Corregir antes de integrar; `validate_tool_names.py` lo detecta |
| Ordenación de fases: Phase 4 crea nuevos agents antes que Phase 3 los referencia | Resuelta | Phase 3 god files referencian los nuevos agents por nombre; esos agents no necesitan existir para que el planificador valide la referencia (son strings en YAML) |

---

## Criterios de Éxito Globales

- [ ] `Atlas.agent.md` tiene lista explícita de SOLO agentes L1 (18 entradas) — no `["*"]`
- [ ] Cada uno de los 11 dioses L1 tiene "Layer 2 Roster" section en system prompt
- [ ] CERO agentes sin `<!-- layer: N -->` comment (validado por `validate_layer_hierarchy.py`)
- [ ] CERO tools con patterns inválidos en cualquier agent file (validado por `validate_tool_names.py`)
- [ ] Los 6 conductores de pack tienen `user-invocable: false`
- [ ] `.vscode/mcp.json` existe con `@modelcontextprotocol/server-memory` configurado
- [ ] Todos los L1 gods tienen "Memory Protocol" section con read/write instructions
- [ ] `plugins/memory-system/` pack existe con Memory-Guardian
- [ ] `plugins/qa-workflow/` con 3 nuevos agentes (Test-Runner, Coverage-Analyst, Mutation-Tester)
- [ ] `plugins/security-workflow/` con 2 nuevos agentes (Compliance-Checker, Secret-Scanner)
- [ ] `plugins/ux-enhancement-workflow/skills/industry-verticals.md` con ≥10 industrias
- [ ] `n8n-Connector.agent.md` existe en automation-mcp-workflow con tool `mcp`
- [ ] `validate_atlas_pack_parity.py` → EXIT 0
- [ ] `validate_plugin_packs.py` → EXIT 0
- [ ] `validate_layer_hierarchy.py` → EXIT 0 (0 orphans)
- [ ] `validate_tool_names.py` → EXIT 0 (0 violations)
- [ ] `demos/hierarchy-architecture-demo/` existe con ≥24 tests pasando
- [ ] **Total test suite ≥ 250 tests pasando**
- [ ] Todos los tests existentes (regression baseline ≥183) siguen pasando

---

## Notas para Atlas

### Skills para subagentes
- **Sisyphus** (Phases 2–4, 7): carga skill `agent-customization` (frontmatter YAML, agent file patterns, VS Code tool restrictions). Es el skill crítico para esta feature — cada cambio a `.agent.md` depende de él.
- **Sisyphus** (Phases 5, 7 — validación Python): carga skill `python-dev` para los scripts.
- **Argus** (Phase 7): carga skill `python-testing-patterns` para revisar los test files generados.

### Dependencias entre fases (CRÍTICO — no saltar)
1. **Phase 1 DEBE completarse antes de cualquier otra** — el Principio VIII de la constitución debe estar escrito antes de que Sisyphus modifique agents.
2. **Phase 2 ANTES de Phase 3** — Atlas debe tener su lista L1 fija antes de que los gods sean actualizados; evita confusión de qué agents están disponibles.
3. **Phase 3 ANTES de Phase 4** — Los gods deben tener sus `agents:` definidos antes de que los conductores de pack sean actualizados para reportar a ellos.
4. **Phase 4 ANTES de Phase 5** — Memory-Guardian (creado en 4.3) debe existir antes de que el memory pack sea configurado en Phase 5.
5. **Phase 5 y Phase 6 son independientes** — pueden ejecutarse en paralelo con instancias distintas de Sisyphus.
6. **Phase 7 DEBE ser último** — actualiza el registry y los validators; necesita que todos los agents existan.

### Condiciones de rollback
- Si `validate_atlas_pack_parity.py` falla tras Phase 3: NO avanzar a Phase 4. Corregir el agent afectado y volver a correr el validator.
- Si `validate_plugin_packs.py` falla tras Phase 4: NO avanzar a Phase 5. Identificar el agent problemático en el report y corregirlo.
- Si el total de tests cae por debajo de 183 al final de Phase 7: STOP — hay una regresión. Argus debe triagear antes de cerrar la feature.

### Comandos de validación intermedios
```bash
# Correr tras Phase 2 y cada sub-tarea de Phase 3:
python scripts/validate_atlas_pack_parity.py

# Correr tras Phase 4:
python scripts/validate_plugin_packs.py

# Correr al final (Phase 7):
python scripts/validate_tool_names.py
python scripts/validate_layer_hierarchy.py
python scripts/validate_atlas_pack_parity.py
python scripts/validate_plugin_packs.py
python scripts/validate_pack_registry.py
python scripts/validate_optional_pack_demos.py
pytest scripts/test_validate_tool_names.py
pytest scripts/test_validate_layer_hierarchy.py
pytest demos/hierarchy-architecture-demo/tests/
```

### Decisiones de diseño que NO deben sobreescribirse
- `agents: ["*"]` está **PROHIBIDO** para Atlas — siempre lista explícita
- Prometheus es el dueño de la memoria — no crear un "Mnemo" god adicional sin aprobación del usuario
- Oracle y Hermes NO tienen pack L2 — son self-sufficient con sus tools
- Los `-subagent` aliases son L1 (no L2) — son la vía de invocación delegada de Atlas a los gods
- `PackCatalog` permanece `user-invocable: true` — excepción aprobada por Principio I
- `n8n-Connector` debe tener `tools: [mcp, ...]` — necesita MCP tool para funcionar
