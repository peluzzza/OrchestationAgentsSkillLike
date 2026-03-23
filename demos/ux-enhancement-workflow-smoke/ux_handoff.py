"""Tiny UX handoff module for the ux-enhancement-workflow-smoke demo.

The demo is intentionally small and self-contained. Use it as a sandbox
to run an orchestration loop (UX-Atlas -> UX-Planner -> User-Flow-Designer
-> Design-Critic -> Accessibility-Heuristics -> Frontend-Handoff) while
keeping changes confined to this folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class ValidationError(Exception):
    """Raised when a HandoffSpec operation fails validation."""


@dataclass
class HandoffSpec:
    """Spec package produced by the Frontend-Handoff agent.

    Aggregates flow descriptions and review outcomes from the UX pipeline
    before handoff to implementation (Afrodita / frontend-workflow).

    Attributes:
        feature: Name of the feature being specified.
        notes: Optional free-text notes for the implementation team.
    """

    feature: str
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate and normalise fields on construction.

        Raises:
            ValidationError: if *feature* is empty or blank.
        """
        if not self.feature or not self.feature.strip():
            raise ValidationError("feature name must not be empty")
        self.feature = self.feature.strip()
        self._flows: list[str] = []
        self._heuristics_passed: bool = False
        self._accessibility_passed: bool = False

    def add_flow(self, description: str) -> None:
        """Append a user-flow description to the spec.

        Args:
            description: Plain-text flow narrative.

        Raises:
            ValidationError: if *description* is empty or blank.
        """
        if not description or not description.strip():
            raise ValidationError("flow description must not be empty")
        self._flows.append(description.strip())

    def flows(self) -> list[str]:
        """Return a snapshot of the registered flow descriptions."""
        return list(self._flows)

    def mark_heuristics_passed(self) -> None:
        """Record that the Design-Critic heuristic review passed."""
        self._heuristics_passed = True

    def mark_accessibility_passed(self) -> None:
        """Record that the Accessibility-Heuristics review passed."""
        self._accessibility_passed = True

    def is_ready(self) -> bool:
        """Return True only if at least one flow exists and both reviews passed."""
        return (
            bool(self._flows)
            and self._heuristics_passed
            and self._accessibility_passed
        )

    def checklist(self) -> list[str]:
        """Return an ordered checklist of flow descriptions.

        Each item is prefixed with ``[x]`` when ``is_ready()`` is True,
        or ``[ ]`` otherwise.
        """
        prefix = "[x]" if self.is_ready() else "[ ]"
        return [f"{prefix} {flow}" for flow in self._flows]

    def summary(self) -> str:
        """Return a one-line readiness summary for the handoff report."""
        status = "READY" if self.is_ready() else "NOT_READY"
        return (
            f"{self.feature}: {len(self._flows)} flow(s) | "
            f"heuristics={self._heuristics_passed} | "
            f"a11y={self._accessibility_passed} | {status}"
        )
