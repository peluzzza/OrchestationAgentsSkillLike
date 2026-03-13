from __future__ import annotations

from selection_engine import SourceMetadata, TaskProfile


def make_backend_task() -> TaskProfile:
    return TaskProfile(
        task_type="backend",
        required_capabilities=("codegen", "review"),
    )


def make_ui_task() -> TaskProfile:
    return TaskProfile(
        task_type="frontend",
        required_capabilities=("wireframe",),
    )


def make_task_with_unavailable_preference() -> TaskProfile:
    return TaskProfile(
        task_type="backend",
        required_capabilities=("codegen",),
        preferred_source="preferred-flow",
    )


def make_task_with_preference() -> TaskProfile:
    return TaskProfile(
        task_type="backend",
        required_capabilities=("codegen",),
        preferred_source="preferred-flow",
    )


def make_tie_break_sources() -> list[SourceMetadata]:
    return [
        SourceMetadata(
            source_id="zeta-router",
            origin="plugin",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
            priority=0,
        ),
        SourceMetadata(
            source_id="alpha-router",
            origin="plugin",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
            priority=0,
        ),
    ]


def make_capability_sources() -> list[SourceMetadata]:
    return [
        SourceMetadata(
            source_id="backend-only",
            origin="github",
            task_types=("backend",),
            capabilities=("wireframe", "codegen"),
            available=True,
        ),
        SourceMetadata(
            source_id="ui-specialist",
            origin="plugin",
            task_types=("frontend",),
            capabilities=("wireframe", "accessibility"),
            available=True,
        ),
    ]


def make_duplicate_sources() -> list[SourceMetadata]:
    return [
        SourceMetadata(
            source_id="shared-flow",
            origin="plugin",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
        ),
        SourceMetadata(
            source_id="shared-flow",
            origin="github",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
        ),
    ]


def make_preferred_fallback_sources() -> list[SourceMetadata]:
    return [
        SourceMetadata(
            source_id="preferred-flow",
            origin="github",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=False,
        ),
        SourceMetadata(
            source_id="fallback-flow",
            origin="plugin",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
        ),
        SourceMetadata(
            source_id="other-flow",
            origin="other",
            task_types=("backend",),
            capabilities=("codegen",),
            available=True,
        ),
    ]


def make_preferred_selected_sources() -> list[SourceMetadata]:
    return [
        SourceMetadata(
            source_id="preferred-flow",
            origin="plugin",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
        ),
        SourceMetadata(
            source_id="fallback-flow",
            origin="github",
            task_types=("backend",),
            capabilities=("codegen", "review"),
            available=True,
        ),
    ]
