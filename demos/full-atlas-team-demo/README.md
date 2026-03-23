# Demo: Full Atlas Team Exercise

Smoke test que verifica los **26 agentes** del ecosistema Atlas en una sola sesión.
Escenario: un micro-servicio Python de gestión de tareas (`task_service.py`) que
necesita un feature nuevo, revisión de dependencias, docs actualizadas, y release
readiness check.

---

## Qué agente se activa y por qué

| Agente | Activado por | En qué paso |
|---|---|---|
| `Atlas` | Usuario | Todo |
| `Prometheus` | Tarea de código → Specify pipeline | Planificación |
| `Hermes` | Codebase desconocido para Prometheus | SP-0 discovery |
| `Oracle` | Research de patrones Python async | SP-0 research |
| `SpecifyConstitution` | Primer artefacto del pipeline | SP-1 |
| `SpecifySpec` | Feature a especificar | SP-2 |
| `SpecifyClarify` | Ambigüedades en el spec | SP-3 |
| `SpecifyPlan` | Diseño técnico | SP-4 |
| `SpecifyAnalyze` | Puerta SP-5 (pre-tareas) y EX-1 (pre-impl) | SP-5 / EX-1 |
| `SpecifyTasks` | Desglose de tareas | SP-5 |
| `SpecifyImplement` | Ejecución de fases | EX-2..4 |
| `Sisyphus` | Implementación fase a fase | Fase 1-3 |
| `Themis` | Code review tras cada fase | 2B |
| `Atenea` | Endpoint HTTP + rate limiting = seguridad | 2C |
| `Argus` | QA/testing tras implementación | 2D |
| `Clio` | README desactualizado detectado | 2E |
| `Ariadna` | `pyproject.toml` añadido con deps nuevas | 2E |
| `Hephaestus` | Último paso: release readiness v1.1.0 | 2F release-readiness |
| `Afrodita-UX` | *Activado solo con Opción B (demo frontend)* | Fase UI |

---

## Archivos de la demo

| Archivo | Propósito |
|---|---|
| `DEMO_PROMPT.md` | Prompt listo para `@Atlas` (3 opciones) |
| `EXPECTED_FLOW.md` | Traza agente por agente |
| `task_service.py` | Código inicial con TODO marcado |
| `pyproject.toml` | Manifiesto con deps desactualizadas (Ariadna) |
| `full_team_harness.py` | Validador post-demo |
| `test_full_team_harness.py` | Suite de tests del harness |

---

## Cómo ejecutar

### Pre-demo (verifica arranque)
```bash
cd demos/full-atlas-team-demo
py -m unittest -v
# Esperado: TestHarnessUnit OK, TestAgentRoster OK, demás SKIP
```

### La demo
1. Copia el prompt deseado de `DEMO_PROMPT.md`
2. Pégalo en Copilot Chat con `@Atlas`
3. Observa la cascada de agentes

### Post-demo (verifica resultados)
```bash
cd demos/full-atlas-team-demo
py full_team_harness.py
py -m unittest -v
# Esperado: todos los tests activos pasan
```

---

## API Reference

All methods belong to `TaskService` (`task_service.py`). The service uses an in-memory store; no persistence layer is required for the demo.

---

### `create(title, priority=3, tags=None) -> Task`

Creates a new task and adds it to the store.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | — | Non-empty task title (whitespace-stripped). |
| `priority` | `int` | `3` | Priority level 1 (highest) – 5 (lowest). |
| `tags` | `list` | `None` | Optional list of string labels. |

**Returns:** the newly created `Task` dataclass instance.  
**Raises:** `ValueError` if `title` is empty or `priority` is outside 1–5.

---

### `get(task_id) -> Task | None`

Retrieves a single task by its integer ID.

| Parameter | Type | Description |
|---|---|---|
| `task_id` | `int` | ID assigned at creation time. |

**Returns:** the matching `Task`, or `None` if not found.

---

### `list_all() -> list[Task]`

Returns all tasks currently in the store, in insertion order.

**Returns:** `list[Task]` (empty list when the store is empty).

---

### `complete(task_id) -> bool`

Marks a task as done (`task.done = True`).

| Parameter | Type | Description |
|---|---|---|
| `task_id` | `int` | ID of the task to complete. |

**Returns:** `True` if the task existed and was updated; `False` if not found.

---

### `delete(task_id) -> bool`

Permanently removes a task from the store.

| Parameter | Type | Description |
|---|---|---|
| `task_id` | `int` | ID of the task to remove. |

**Returns:** `True` if the task existed and was deleted; `False` if not found.

---

### `stats(since=None, limit=100) -> dict`

Returns aggregate statistics over the task store, optionally scoped to a time window and capped at a maximum task count.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `since` | `datetime` \| `None` | `None` | Naive UTC lower bound (inclusive). Only tasks with `created_at >= since` are included. Pass `None` to include all tasks. |
| `limit` | `int` | `100` | Maximum number of tasks to aggregate after the `since` filter is applied. Valid range: **1 – 500**. |

**Returns:** `dict` with the following keys:

| Key | Type | Description |
|---|---|---|
| `total` | `int` | Number of tasks in the aggregated window. |
| `done` | `int` | Tasks with `done=True`. |
| `pending` | `int` | Tasks with `done=False` (`total - done`). |
| `by_priority` | `dict[int, int]` | Count per priority level; always contains keys 1–5 (value `0` when none present). |
| `by_tag` | `dict[str, int]` | Count per tag string; empty dict when no tags are present. |

**Raises:**

- `ValueError` — if `limit` is not an `int`, or is outside the range 1–500.
- `TypeError` — if `since` is not a `datetime` instance (and not `None`).

**Example:**

```python
from datetime import datetime
from task_service import TaskService

svc = TaskService()
svc.create("Write tests", priority=1, tags=["dev", "qa"])
svc.create("Update docs", priority=2, tags=["docs"])
svc.create("Deploy", priority=1, tags=["ops"])
svc.complete(1)

# All tasks
print(svc.stats())
# {
#   'total': 3, 'done': 1, 'pending': 2,
#   'by_priority': {1: 2, 2: 1, 3: 0, 4: 0, 5: 0},
#   'by_tag': {'dev': 1, 'qa': 1, 'docs': 1, 'ops': 1}
# }

# Tasks created on or after a specific timestamp, capped at 50
cutoff = datetime(2026, 1, 1)
print(svc.stats(since=cutoff, limit=50))
```
