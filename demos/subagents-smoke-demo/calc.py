"""Tiny module for subagent-orchestration smoke testing.

The demo is intentionally small and self-contained. Use it as a sandbox
to run an orchestration loop (Oracle → Explorer → Sisyphus → Code-Review → Argus)
while keeping changes confined to this folder.
"""

from __future__ import annotations


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    """Return a / b.

    Raises:
        ZeroDivisionError: if b is zero.
    """

    if b == 0:
        raise ZeroDivisionError
    return a / b
