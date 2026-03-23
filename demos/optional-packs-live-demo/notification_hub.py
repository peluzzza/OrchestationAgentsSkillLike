"""notification_hub.py — Central notification dispatcher.

NotificationChannel: named channel with a webhook URL and dispatch counter.
NotificationHub:     register channels, dispatch payloads, report stats.

get_stats() is NOT YET IMPLEMENTED — stub raises NotImplementedError.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class NotificationChannel:
    name: str
    webhook_url: str
    _count: int = field(default=0, repr=False)

    def record_dispatch(self) -> None:
        self._count += 1

    @property
    def dispatch_count(self) -> int:
        return self._count


class NotificationHub:
    """Central notification dispatcher.

    Public API
    ----------
    register_channel(channel)           — add a NotificationChannel
    dispatch(channel_name, payload)     — send payload to channel
    get_stats() -> dict                 — NOT YET IMPLEMENTED
        Expected return shape:
        {
            "total_dispatched": int,
            "channels": {name: count, ...},
            "last_activity": str | None    # ISO-8601 UTC, or None if never dispatched
        }
    """

    def __init__(self) -> None:
        self._channels: dict[str, NotificationChannel] = {}
        self._total: int = 0
        self._last_activity: Optional[datetime] = None

    def register_channel(self, channel: NotificationChannel) -> None:
        self._channels[channel.name] = channel

    def dispatch(self, channel_name: str, payload: dict) -> None:
        if channel_name not in self._channels:
            raise KeyError(f"Channel not registered: {channel_name}")
        self._channels[channel_name].record_dispatch()
        self._total += 1
        self._last_activity = datetime.now(timezone.utc)

    # ------------------------------------------------------------------ #
    # TODO — implement this method                                         #
    # ------------------------------------------------------------------ #
    def get_stats(self) -> dict:
        return {
            "total_dispatched": self._total,
            "channels": {ch.name: ch.dispatch_count for ch in self._channels.values()},
            "last_activity": self._last_activity.isoformat() if self._last_activity is not None else None,
        }
