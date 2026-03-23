# Demo Prompt — Optional Packs Live Exercise

Copia y pega en Copilot Chat dirigido a `@Atlas`.

Este demo fuerza que Atlas delegue a los **conductores de packs opcionales**
(`Backend-Atlas`, `Automation-Atlas`, `UX-Atlas`, `PackCatalog`) en lugar del
equipo canónico por defecto; ejercita la cadena de especialistas dentro de cada pack.

Estado inicial: `24 tests — FAILED (errors=16)` porque `get_stats()` y
`AlertWorkflow.is_triggered/execute` son stubs con `NotImplementedError`.

---

## Opción A — Ejercicio completo (todos los packs opcionales)

```
@Atlas Tengo dos módulos Python con stubs en demos/optional-packs-live-demo/
que necesitan implementación, más una especificación UX y una auditoría de packs.
Quiero que USES EXPLÍCITAMENTE LOS CONDUCTORES DE PACKS OPCIONALES para cada dominio.

─────────────────────────────────────────────────────────────
TAREA 0 — Pack Discovery (PackCatalog)
─────────────────────────────────────────────────────────────
Invoca PackCatalog. Pídele que lea .github/plugin/pack-registry.json
y marketplace.json y diga qué packs son relevantes para este proyecto
(Python, notificaciones, automatización, UX). Confirma que los 4 packs
ya están habilitados en .vscode/settings.json antes de continuar.

─────────────────────────────────────────────────────────────
TAREA 1 — Backend (Backend-Atlas chain)
─────────────────────────────────────────────────────────────
Usa Backend-Atlas (plugins/backend-workflow) para implementar get_stats()
en demos/optional-packs-live-demo/notification_hub.py.

Spec de get_stats():
  - Sin parámetros
  - Retorna dict con:
      total_dispatched: int          — totales del hub
      channels: {nombre: count}     — dispatches por canal; solo canales registrados
      last_activity: str | None     — ISO-8601 UTC si ha habido dispatch, else None
  - No lanza excepciones

Backend-Atlas debe usar al menos Backend-Planner + Service-Builder.
Backend-Reviewer debe revisar el resultado antes de pasar al siguiente.

─────────────────────────────────────────────────────────────
TAREA 2 — Automation (Automation-Atlas chain)
─────────────────────────────────────────────────────────────
Usa Automation-Atlas (plugins/automation-mcp-workflow) para implementar
AlertWorkflow en demos/optional-packs-live-demo/alert_workflow.py.

Spec de AlertWorkflow:
  - is_triggered(total_dispatched: int) -> bool
      True iff total_dispatched > self.threshold (estrictamente mayor que)
  - execute(total_dispatched: int, handler: Callable[[int], None]) -> bool
      Llama a handler(total_dispatched) si is_triggered; retorna True si llamó, False si no

Automation-Atlas debe pasar el workflow por Automation-Reviewer antes de cerrar.

─────────────────────────────────────────────────────────────
TAREA 3 — UX Spec (UX-Atlas chain)
─────────────────────────────────────────────────────────────
Usa UX-Atlas (plugins/ux-enhancement-workflow) para producir una especificación
UX del "Notification Channel Dashboard" — la pantalla donde un operador ve
el estado de los canales y las alertas activas.

El resultado debe ser un fichero:
  demos/optional-packs-live-demo/ux-notification-dashboard-spec.md

UX-Atlas debe ejecutar la cadena completa:
  UX-Planner → User-Flow-Designer → Design-Critic → Accessibility-Heuristics → Frontend-Handoff

El archivo final debe incluir: user flows, critique (heurísticas de Nielsen),
checklist de accesibilidad WCAG 2.1 AA, y el handoff bundle para Afrodita.

─────────────────────────────────────────────────────────────
VERIFICACIÓN FINAL (agentes canónicos)
─────────────────────────────────────────────────────────────
Una vez completadas las tareas 1 y 2, el equipo canónico de Atlas verifica:
- Themis: revisa la implementación de get_stats() y AlertWorkflow
- Argus: ejecuta los tests y confirma 24/24 OK

Definition of done:
  cd demos/optional-packs-live-demo
  py -m unittest discover .
  # Esperado: Ran 24 tests — OK

IMPORTANTE: Registra en tu respuesta qué agente de qué pack ejecutó cada paso.
Ejemplo: "Backend-Planner (backend-workflow) → Service-Builder (backend-workflow)
→ Backend-Reviewer (backend-workflow) → Themis (canonical)"
```

---

## Opción B — Solo Backend + Automation (sin UX, más rápido)

```
@Atlas En demos/optional-packs-live-demo/ hay dos stubs que necesito implementar.
Usa los conductores de packs opcionales, NO Sisyphus directamente.

TAREA 1 — Backend-Atlas implementa get_stats() en notification_hub.py:
  Retorna: {total_dispatched: int, channels: {name: count}, last_activity: str|None}
  last_activity es ISO-8601 UTC o None si nunca hubo dispatch.
  Usa: Backend-Planner → Service-Builder → Backend-Reviewer.

TAREA 2 — Automation-Atlas implementa AlertWorkflow en alert_workflow.py:
  is_triggered(n) → True iff n > threshold (estrictamente mayor)
  execute(n, handler) → llama handler(n) si triggered, retorna bool
  Pasa por Automation-Reviewer antes de cerrar.

Al final: Themis revisa, Argus confirma 24/24 OK.

Definition of done:
  cd demos/optional-packs-live-demo
  py -m unittest discover .
  Ran 24 tests — OK

Registra qué conductor y qué especialista ejecutó cada paso.
```

---

## Opción C — Solo UX Spec (ningún código)

```
@Atlas Necesito una especificación UX completa para el "Notification Channel Dashboard".
Usa UX-Atlas (del pack ux-enhancement-workflow).

El dashboard muestra:
- Lista de canales registrados con su conteo de dispatches
- Total global de mensajes enviados
- Timestamp de última actividad
- Alertas activas (umbral superado = rojo, por debajo = verde)

UX-Atlas debe ejecutar la cadena completa:
  1. UX-Planner — brief + user personas + goals
  2. User-Flow-Designer — flujo principal del operador
  3. Design-Critic — evaluación con heurísticas de Nielsen
  4. Accessibility-Heuristics — checklist WCAG 2.1 AA
  5. Frontend-Handoff — bundle final para Afrodita

Guarda el resultado en:
  demos/optional-packs-live-demo/ux-notification-dashboard-spec.md

Sin tocar notification_hub.py ni alert_workflow.py.
```

---

## Opción D — Solo Pack Discovery (PackCatalog)

```
@Atlas Invoca PackCatalog y pídele que:

1. Lea .github/plugin/pack-registry.json y .github/plugin/marketplace.json
2. Detecte señales en este workspace (Python, automatización, UX, notificaciones)
3. Recomiende qué packs activar y por qué
4. Muestre los conductores y especialistas que cada pack añade
5. Confirme cuáles ya están habilitados en .vscode/settings.json

No implementes nada. Solo discovery y recomendación.
```

---

## Estado inicial de referencia

```
py -m unittest discover -s demos/optional-packs-live-demo

# ANTES de la demo:
Ran 24 tests — FAILED (errors=16)
  8 pasan  → constructor validation (NotificationHub básico + AlertWorkflow.__init__)
  16 fallan → NotImplementedError en get_stats() [7] y AlertWorkflow [9]

# DESPUÉS de la demo (Opción A o B):
Ran 24 tests — OK
```

## Mapa de packs ↔ agentes involucrados

| Pack | Conductor | Especialistas |
|---|---|---|
| `agent-pack-catalog` | `PackCatalog` | skill `agent-pack-search` |
| `backend-workflow` | `Backend-Atlas` | `Backend-Planner`, `API-Designer`, `Service-Builder`, `Backend-Reviewer` |
| `automation-mcp-workflow` | `Automation-Atlas` | `Automation-Planner`, `MCP-Integrator`, `Workflow-Composer`, `Automation-Reviewer` |
| `ux-enhancement-workflow` | `UX-Atlas` | `UX-Planner`, `User-Flow-Designer`, `Design-Critic`, `Accessibility-Heuristics`, `Frontend-Handoff` |
| Canónico `.github/agents` | — | `Themis`, `Argus`, `Atenea` (verificación final) |
