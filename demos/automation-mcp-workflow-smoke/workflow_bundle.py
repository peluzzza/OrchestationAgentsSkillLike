"""Tiny workflow bundle module for the automation-mcp-workflow-smoke demo.

The demo is intentionally small and self-contained. Use it as a sandbox
to run an orchestration loop (Automation-Atlas -> Automation-Planner ->
Workflow-Composer -> Automation-Reviewer) while keeping changes confined
to this folder.
"""

from __future__ import annotations

from typing import NamedTuple


class WorkflowStep(NamedTuple):
    name: str
    action: str
    reversible: bool = True


class WorkflowBundle:
    """Ordered collection of workflow steps with basic safety validation.

    Attributes:
        name: Human-readable bundle identifier.
    """

    def __init__(self, name: str, dry_run: bool = False) -> None:
        """Initialise the bundle.

        Args:
            name: Bundle name.  Must not be empty or blank.
            dry_run: When True, is_safe() always returns True.

        Raises:
            ValueError: if *name* is empty or blank.
        """
        if not name or not name.strip():
            raise ValueError("bundle name must not be empty")
        self.name = name.strip()
        self.dry_run = dry_run
        self._steps: list[WorkflowStep] = []

    def add_step(
        self, name: str, action: str, *, reversible: bool = True
    ) -> None:
        """Append a named step to the bundle.

        Args:
            name: Step name.  Must not be empty or blank.
            action: Shell-like action string.  Must not be empty or blank.
            reversible: Whether the step can be safely undone.

        Raises:
            ValueError: if *name* or *action* is empty or blank.
        """
        if not name or not name.strip():
            raise ValueError("step name must not be empty")
        if not action or not action.strip():
            raise ValueError("step action must not be empty")
        self._steps.append(
            WorkflowStep(
                name=name.strip(), action=action.strip(), reversible=reversible
            )
        )

    def steps(self) -> list[WorkflowStep]:
        """Return a snapshot of the current step list."""
        return list(self._steps)

    def is_safe(self) -> bool:
        """Return True only if every step is marked reversible (or dry_run is True)."""
        if self.dry_run:
            return True
        return all(s.reversible for s in self._steps)

    def step_count(self) -> int:
        """Return the number of steps currently in the bundle."""
        return len(self._steps)
