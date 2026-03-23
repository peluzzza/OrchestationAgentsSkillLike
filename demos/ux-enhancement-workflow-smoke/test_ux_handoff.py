"""Tests for ux_handoff — ux-enhancement-workflow-smoke demo.

Run with:
    python3 -m unittest -v demos/ux-enhancement-workflow-smoke/test_ux_handoff.py
Or from this folder:
    python3 -m unittest -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import ux_handoff as ux


class TestHandoffSpec(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = ux.HandoffSpec(feature="login-flow")

    def test_initial_state_not_ready(self) -> None:
        self.assertFalse(self.spec.is_ready())

    def test_flows_initially_empty(self) -> None:
        self.assertEqual(self.spec.flows(), [])

    def test_add_flow_recorded(self) -> None:
        self.spec.add_flow("User enters credentials")
        self.assertEqual(len(self.spec.flows()), 1)

    def test_flows_returns_snapshot(self) -> None:
        self.spec.add_flow("User enters credentials")
        snapshot = self.spec.flows()
        self.assertEqual(snapshot[0], "User enters credentials")

    def test_not_ready_without_accessibility_review(self) -> None:
        self.spec.add_flow("User enters credentials")
        self.spec.mark_heuristics_passed()
        self.assertFalse(self.spec.is_ready())

    def test_not_ready_without_heuristics_review(self) -> None:
        self.spec.add_flow("User enters credentials")
        self.spec.mark_accessibility_passed()
        self.assertFalse(self.spec.is_ready())

    def test_not_ready_without_flows(self) -> None:
        self.spec.mark_heuristics_passed()
        self.spec.mark_accessibility_passed()
        self.assertFalse(self.spec.is_ready())

    def test_ready_with_flow_and_both_reviews(self) -> None:
        self.spec.add_flow("User enters credentials")
        self.spec.mark_heuristics_passed()
        self.spec.mark_accessibility_passed()
        self.assertTrue(self.spec.is_ready())

    def test_empty_flow_raises(self) -> None:
        with self.assertRaises(ux.ValidationError):
            self.spec.add_flow("")

    def test_whitespace_flow_raises(self) -> None:
        with self.assertRaises(ux.ValidationError):
            self.spec.add_flow("   ")

    def test_empty_feature_raises(self) -> None:
        with self.assertRaises(ux.ValidationError):
            ux.HandoffSpec(feature="")

    def test_whitespace_feature_raises(self) -> None:
        with self.assertRaises(ux.ValidationError):
            ux.HandoffSpec(feature="   ")

    def test_feature_name_trimmed(self) -> None:
        spec = ux.HandoffSpec(feature="  password-reset  ")
        self.assertEqual(spec.feature, "password-reset")

    def test_flow_descriptions_trimmed(self) -> None:
        self.spec.add_flow("  forgot password link  ")
        self.assertEqual(self.spec.flows()[0], "forgot password link")

    def test_summary_not_ready(self) -> None:
        summary = self.spec.summary()
        self.assertIn("NOT_READY", summary)
        self.assertIn("login-flow", summary)

    def test_summary_ready(self) -> None:
        self.spec.add_flow("auth step")
        self.spec.mark_heuristics_passed()
        self.spec.mark_accessibility_passed()
        summary = self.spec.summary()
        self.assertIn("READY", summary)
        self.assertNotIn("NOT_READY", summary)

    def test_multiple_flows_counted(self) -> None:
        self.spec.add_flow("step A")
        self.spec.add_flow("step B")
        self.assertEqual(len(self.spec.flows()), 2)


if __name__ == "__main__":
    unittest.main()
