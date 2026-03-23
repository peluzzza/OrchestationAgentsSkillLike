# Research: task-stats

**Feature slug:** `task-stats`
**Creado:** 2026-03-23

---

## 1. Análisis del código existente

### Hallazgos en `task_service.py`

| Aspecto | Observación |
|---|---|
| `Task.created_at` | Usa `datetime.utcnow()` como default_factory — timezone-naive, UTC |
| `Task.tags` | `list` sin tipo parametrizado; puede contener cualquier tipo |
| `Task.priority` | `int` validado en `create()` al rango 1–5 |
| `TaskService._tasks` | `dict[int, Task]` — orden de inserción garantizado (Python 3.7+) |
| Patrón de validación | `raise ValueError(mensaje)` — ya establecido en `create()` |
| Import de `datetime` | Ya presente en línea 2 — no requiere import adicional |

### Bloque TODO existente (referencia)

```python
# def stats(self, since: datetime = None, limit: int = 100) -> dict:
#     """
#     Devuelve estadísticas de tareas:
#       - total, done, pending
#       - por prioridad: {1: n, 2: n, ...}
#       - por tag: {tag: n, ...}
#     Filtrable por fecha de creación >= since.
#     limit: máx número de tareas a considerar (rate-limiting interno).
#     """
#     raise NotImplementedError("Pendiente de implementar — ver Specify pipeline")
```

La firma ya está definida por el TODO. La implementación debe seguirla exactamente.

---

## 2. Alternativas consideradas

### 2.1 Implementación con `collections.Counter`

```python
from collections import Counter
priority_counts = Counter(t.priority for t in tasks)
by_priority = {p: priority_counts.get(p, 0) for p in range(1, 6)}
```

**Pros:** Más idiomático para conteo.
**Cons:** Requiere import adicional de `collections`. No aporta ventaja sobre comprensión de dict.
**Decisión:** Comprensión de dict nativa — sin imports adicionales, más legible para este contexto simple.

### 2.2 Ordenar por `created_at` antes de aplicar `limit`

```python
tasks = sorted(tasks, key=lambda t: t.created_at)[:limit]
```

**Pros:** Resultado determinístico incluso si el dict se reordena (hipotético).
**Cons:** O(n log n) innecesario para un store in-memory donde el orden de inserción ya es determinístico.
**Decisión:** No ordenar — usar orden de inserción del dict. El store es secuencial por `_next_id`.

### 2.3 Validar `limit` con `isinstance` antes de comparar

```python
if not isinstance(limit, int) or not (1 <= limit <= 500):
    raise ValueError(...)
```

**Pros:** Protección ante callers que pasen `float` o `str`.
**Cons:** Over-engineering para un método de dominio interno con firma tipada.
**Decisión:** No añadir `isinstance` — la anotación `int` es suficiente para uso interno.

### 2.4 Retornar `None` para `by_tag` cuando no hay tags

**Pros:** Diferencia semántica entre "no hay información de tags" y "cero tags".
**Cons:** Rompe la consistencia de tipos del retorno; obliga al caller a manejar `None`.
**Decisión:** Siempre retornar `{}` para `by_tag`.

---

## 3. Decisiones de diseño finales

| Decisión | Justificación |
|---|---|
| `limit` se aplica sobre el conjunto ya filtrado por `since` | Garantiza que `total <= limit` en cualquier caso |
| `by_priority` siempre con 5 claves | Simplicidad para el consumidor, sin `KeyError` posibles |
| `by_tag` siempre `dict`, nunca `None` | Consistencia de tipos, serialización JSON directa |
| Orden de iteración: inserción (dict nativo) | Python 3.7+ garantía, O(n) sin sort |
| Sin imports adicionales | Restricción de diseño: stdlib sólo, sin nuevas dependencias |
| `str(tag)` para claves de `by_tag` | Robustez ante tags no-string que pudieran existir en la lista |

---

## 4. Dependencias y compatibilidad

- **Python 3.10+** — requerido por `pyproject.toml`. Las anotaciones `dict[int, int]` en cuerpo de función son compatibles.
- **No hay cambios en pyproject.toml** — esta feature es stdlib only.
- **Compatibilidad con FastAPI** (cuando se exponga vía HTTP): el dict retornado es JSON-serializable con `json.dumps()` estándar, salvo que las claves de `by_priority` son `int` y se convierten a strings en JSON. Documentar en docstring.

---

## 5. Riesgos identificados

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| `task.tags` contiene no-strings | Claves inesperadas en `by_tag` | Baja | Usar `str(tag)` al construir `by_tag` |
| `since` con timezone-aware vs naive | `TypeError` en comparación | Baja | Documentar que `since` debe ser naive UTC; no añadir lógica de TZ |
| Store muy grande antes de aplicar `limit` | Iteración O(n) sobre el store completo | Media | Aceptado para esta fase; el filtro `since` reduce en práctica |
| Test `test_stats_since_filter` con `datetime.utcnow()` timing | Intermitencia si el reloj cambia en el instante del test | Baja | Usar `datetime(2025, 1, 1)` como `since` hardcoded, no `datetime.utcnow()` |
