from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence


ORIGIN_PRIORITY = {
    "github": 3,
    "plugin": 2,
    "other": 1,
}


@dataclass(frozen=True)
class SourceMetadata:
    source_id: str
    origin: str
    task_types: tuple[str, ...]
    capabilities: tuple[str, ...]
    available: bool = True
    priority: int = 0


@dataclass(frozen=True)
class TaskProfile:
    task_type: str
    required_capabilities: tuple[str, ...] = ()
    preferred_source: Optional[str] = None


@dataclass(frozen=True)
class SelectionResult:
    selected: Optional[SourceMetadata]
    rationale: tuple[str, ...]


def _is_task_match(source: SourceMetadata, task_type: str) -> bool:
    return "*" in source.task_types or task_type in source.task_types


def _has_required_capabilities(source: SourceMetadata, required: Sequence[str]) -> bool:
    source_caps = set(source.capabilities)
    return all(capability in source_caps for capability in required)


def _rank_key(source: SourceMetadata) -> tuple[int, int, str, str]:
    return (
        ORIGIN_PRIORITY.get(source.origin, 0),
        source.priority,
        source.origin,
        source.source_id,
    )


def _stable_choice(candidates: Iterable[SourceMetadata]) -> Optional[SourceMetadata]:
    ordered = sorted(
        candidates,
        key=lambda item: (
            -_rank_key(item)[0],
            -_rank_key(item)[1],
            item.source_id,
            item.origin,
        ),
    )
    return ordered[0] if ordered else None


def select_source(sources: Sequence[SourceMetadata], task: TaskProfile) -> SelectionResult:
    rationale: list[str] = []

    if not sources:
        return SelectionResult(selected=None, rationale=("No sources provided.",))

    available_sources = [source for source in sources if source.available]
    if not available_sources:
        return SelectionResult(selected=None, rationale=("No available sources.",))

    def compatible_pool(pool: Sequence[SourceMetadata]) -> list[SourceMetadata]:
        return [
            source
            for source in pool
            if _is_task_match(source, task.task_type)
            and _has_required_capabilities(source, task.required_capabilities)
        ]

    if task.preferred_source:
        preferred_sources = [
            source for source in sources if source.source_id == task.preferred_source
        ]
        available_preferred = [source for source in preferred_sources if source.available]
        preferred_compatible = compatible_pool(available_preferred)
        if preferred_compatible:
            selected = _stable_choice(preferred_compatible)
            rationale.append(
                "Preferred source is available and compatible; selected preferred candidate."
            )
            rationale.append(
                f"Tie-break uses origin priority github > plugin > other and then source_id."
            )
            return SelectionResult(selected=selected, rationale=tuple(rationale))

        if preferred_sources and not available_preferred:
            rationale.append(
                "Preferred source is unavailable; fallback to best available compatible source."
            )
        elif preferred_sources:
            rationale.append(
                "Preferred source is available but not compatible; fallback to best available compatible source."
            )
        else:
            rationale.append(
                "Preferred source is not present; fallback to best available compatible source."
            )

    candidates = compatible_pool(available_sources)
    if not candidates:
        rationale.append("No compatible sources for task type and required capabilities.")
        return SelectionResult(selected=None, rationale=tuple(rationale))

    selected = _stable_choice(candidates)
    rationale.append("Selected best compatible source.")
    rationale.append("Ranking factors: origin precedence, source priority, deterministic tie-break.")
    return SelectionResult(selected=selected, rationale=tuple(rationale))
