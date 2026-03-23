# Data Model: task-stats

**Feature slug:** `task-stats`
**Creado:** 2026-03-23

---

## 1. Entidades existentes (sin cambios)

### `Task` (dataclass)

```python
@dataclass
class Task:
    id: int
    title: str
    priority: int          # 1–5
    done: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: list = field(default_factory=list)
```

| Campo | Tipo | Notas |
|---|---|---|
| `id` | `int` | Clave primaria en memoria |
| `title` | `str` | Texto de la tarea |
| `priority` | `int` | Rango 1–5, validado en `create()` |
| `done` | `bool` | Estado de completación |
| `created_at` | `datetime` | Timestamp UTC de creación, no modificable |
| `tags` | `list` | Lista de strings; puede ser vacía |

**No se modifica esta entidad.**

---

## 2. Contrato de retorno de `stats()`

### Tipo de retorno: `dict`

```python
{
    "total":       int,
    "done":        int,
    "pending":     int,
    "by_priority": dict[int, int],   # siempre claves {1, 2, 3, 4, 5}
    "by_tag":      dict[str, int],   # puede ser {}
}
```

#### Invariantes del retorno:

| Invariante | Expresión |
|---|---|
| `total == done + pending` | Siempre |
| `total <= limit` | Siempre |
| `set(by_priority.keys()) == {1, 2, 3, 4, 5}` | Siempre |
| `sum(by_priority.values()) == total` | Siempre |
| `all(v >= 0 for v in by_tag.values())` | Siempre |
| Si `since is None` → considera todas las tareas del store | Siempre |
| Si `since is not None` → solo tareas con `created_at >= since` | Siempre |

---

## 3. Parámetros de entrada

| Parámetro | Tipo anotado | Rango válido | Default | Error si inválido |
|---|---|---|---|---|
| `since` | `datetime \| None` | Cualquier datetime o None | `None` | — (cualquier datetime es válido) |
| `limit` | `int` | `[1, 500]` | `100` | `ValueError: limit must be between 1 and 500, got {limit}` |

---

## 4. Pipeline interno de datos

```
self._tasks.values()
    │
    ├─ [filtro since] → task.created_at >= since  (si since is not None)
    │
    ├─ [:limit]       → primeros `limit` elementos (orden de inserción)
    │
    └─ [agregación]
           ├─ total       = len(tasks)
           ├─ done        = sum(1 for t in tasks if t.done)
           ├─ pending     = total - done
           ├─ by_priority = {p: count for p in 1..5}
           └─ by_tag      = {tag: count for each tag in each task.tags}
```

---

## 5. Notas de serialización

- El dict retornado es directamente serializable a JSON (todos los valores son `int`, `str`, o dicts anidados con claves `int`/`str`).
- Las claves de `by_priority` son `int` (1–5), no strings. Si se usa `json.dumps()`, Python convierte automáticamente las claves a strings (`"1"`, `"2"`, …). Documentar este comportamiento en el docstring.
