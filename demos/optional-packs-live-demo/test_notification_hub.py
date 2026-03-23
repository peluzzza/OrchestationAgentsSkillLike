"""Tests for NotificationHub — register, dispatch, and get_stats()."""
import unittest
from notification_hub import NotificationChannel, NotificationHub


def _hub_with(*names: str) -> NotificationHub:
    hub = NotificationHub()
    for n in names:
        hub.register_channel(NotificationChannel(name=n, webhook_url=f"https://example.com/{n}"))
    return hub


# ===================================================================== #
#  PASSING — registration and dispatch basics                           #
# ===================================================================== #

class TestRegistrationAndDispatch(unittest.TestCase):

    def test_register_channel_stored(self):
        ch = NotificationChannel(name="alerts", webhook_url="https://x.com/wh")
        hub = NotificationHub()
        hub.register_channel(ch)
        self.assertEqual(hub._channels["alerts"], ch)

    def test_dispatch_increments_channel_count(self):
        hub = _hub_with("alerts")
        hub.dispatch("alerts", {"msg": "hello"})
        self.assertEqual(hub._channels["alerts"].dispatch_count, 1)

    def test_dispatch_increments_total(self):
        hub = _hub_with("alerts", "ops")
        hub.dispatch("alerts", {})
        hub.dispatch("ops", {})
        hub.dispatch("alerts", {})
        self.assertEqual(hub._total, 3)

    def test_dispatch_unknown_channel_raises(self):
        hub = _hub_with("alerts")
        with self.assertRaises(KeyError):
            hub.dispatch("missing", {})

    def test_no_dispatch_last_activity_is_none(self):
        hub = _hub_with("alerts")
        self.assertIsNone(hub._last_activity)


# ===================================================================== #
#  FAILING until get_stats() is implemented                             #
# ===================================================================== #

class TestGetStats(unittest.TestCase):

    def test_stats_returns_dict(self):
        hub = _hub_with("alerts")
        hub.dispatch("alerts", {})
        result = hub.get_stats()
        self.assertIsInstance(result, dict)

    def test_stats_total_dispatched(self):
        hub = _hub_with("a", "b")
        hub.dispatch("a", {})
        hub.dispatch("b", {})
        hub.dispatch("a", {})
        self.assertEqual(hub.get_stats()["total_dispatched"], 3)

    def test_stats_channels_breakdown(self):
        hub = _hub_with("x", "y")
        hub.dispatch("x", {})
        hub.dispatch("x", {})
        hub.dispatch("y", {})
        stats = hub.get_stats()
        self.assertEqual(stats["channels"]["x"], 2)
        self.assertEqual(stats["channels"]["y"], 1)

    def test_stats_last_activity_none_before_dispatch(self):
        hub = _hub_with("alerts")
        self.assertIsNone(hub.get_stats()["last_activity"])

    def test_stats_last_activity_is_string_after_dispatch(self):
        hub = _hub_with("alerts")
        hub.dispatch("alerts", {})
        ts = hub.get_stats()["last_activity"]
        self.assertIsInstance(ts, str)
        # Must be parseable as an ISO-8601 datetime
        from datetime import datetime
        parsed = datetime.fromisoformat(ts)
        self.assertIsNotNone(parsed)

    def test_stats_channels_empty_when_no_dispatches(self):
        hub = _hub_with("alerts")
        stats = hub.get_stats()
        self.assertEqual(stats["channels"].get("alerts", 0), 0)

    def test_stats_keys_present(self):
        hub = _hub_with("alerts")
        stats = hub.get_stats()
        for key in ("total_dispatched", "channels", "last_activity"):
            self.assertIn(key, stats, f"Missing key: {key}")


if __name__ == "__main__":
    unittest.main()
