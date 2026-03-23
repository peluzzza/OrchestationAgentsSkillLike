"""alert_workflow.py — Threshold-based alert workflow for NotificationHub.

AlertWorkflow fires a user-supplied handler when the total dispatch count
exceeds (strictly greater than) a configured threshold.

is_triggered() and execute() are NOT YET IMPLEMENTED.
"""
from __future__ import annotations

from typing import Callable


class AlertWorkflow:
    """Threshold alert: fires when total_dispatched > threshold.

    Parameters
    ----------
    threshold : int
        Must be positive (> 0). Raises ValueError otherwise.

    Methods
    -------
    is_triggered(total_dispatched) -> bool
        Returns True iff total_dispatched > threshold.
        NOT YET IMPLEMENTED.

    execute(total_dispatched, handler) -> bool
        Calls handler(total_dispatched) if triggered.
        Returns True when the handler was called, False otherwise.
        NOT YET IMPLEMENTED.
    """

    def __init__(self, threshold: int) -> None:
        if threshold <= 0:
            raise ValueError(f"threshold must be positive, got {threshold!r}")
        self.threshold = threshold

    # ------------------------------------------------------------------ #
    # TODO — implement these methods                                       #
    # ------------------------------------------------------------------ #

    def is_triggered(self, total_dispatched: int) -> bool:
        return total_dispatched > self.threshold

    def execute(self, total_dispatched: int, handler: Callable[[int], None]) -> bool:
        """Calls handler if triggered. Returns True when handler was called."""
        if self.is_triggered(total_dispatched):
            handler(total_dispatched)
            return True
        return False
