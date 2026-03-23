"""
Task Service — micro-servicio de ejemplo para la demo Full Atlas Team.

Estado inicial INTENCIONAL:
  - Solo tiene operaciones CRUD básicas
  - Falta: endpoint de estadísticas con filtro por fecha y límite de tasa
  - Falta: validación de input robusta
  - pyproject.toml tiene deps que Ariadna debe auditar
  - README omite el endpoint nuevo (Clio debe actualizarlo)
  - No hay cabeceras de seguridad (Atenea debe marcarlas)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    priority: int          # 1–5
    done: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: list = field(default_factory=list)


class TaskService:
    """In-memory task store. Persisted layer to be added in future phase."""

    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    # ── Basic CRUD ────────────────────────────────────────────────────────────

    def create(self, title: str, priority: int = 3, tags: list = None) -> Task:
        if not title or not title.strip():
            raise ValueError("title cannot be empty")
        if not (1 <= priority <= 5):
            raise ValueError("priority must be between 1 and 5")
        task = Task(
            id=self._next_id,
            title=title.strip(),
            priority=priority,
            tags=tags or [],
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())

    def complete(self, task_id: int) -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.done = True
        return True

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    # ── Stats ─────────────────────────────────────────────────────────────────

    def stats(self, since: datetime = None, limit: int = 100) -> dict:
        """
        Return aggregate statistics over the task store.

        Parameters
        ----------
        since : datetime, optional
            Naive UTC lower bound (inclusive). Only tasks whose
            ``created_at >= since`` are included. Insertion order preserved.
        limit : int, default 100
            Maximum number of tasks to aggregate after applying the ``since``
            filter. Valid range: 1–500.

        Returns
        -------
        dict
            ``total``, ``done``, ``pending``,
            ``by_priority`` (always keys 1–5, value 0 when absent),
            ``by_tag`` (empty dict when no tags present).
        """
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise ValueError("limit must be an integer")
        if not (1 <= limit <= 500):
            raise ValueError(f"limit must be between 1 and 500, got {limit}")
        if since is not None and not isinstance(since, datetime):
            raise TypeError("since must be a datetime or None")

        filtered = [
            t for t in self._tasks.values()
            if since is None or t.created_at >= since
        ]
        tasks = filtered[:limit]

        total = len(tasks)
        done = sum(1 for t in tasks if t.done)
        pending = total - done

        by_priority = {p: sum(1 for t in tasks if t.priority == p) for p in range(1, 6)}

        by_tag: dict = {}
        for t in tasks:
            for tag in t.tags:
                key = str(tag)
                by_tag[key] = by_tag.get(key, 0) + 1

        return {
            "total": total,
            "done": done,
            "pending": pending,
            "by_priority": by_priority,
            "by_tag": by_tag,
        }
