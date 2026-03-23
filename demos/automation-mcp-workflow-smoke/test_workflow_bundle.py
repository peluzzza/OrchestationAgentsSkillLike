"""Tests for workflow_bundle — automation-mcp-workflow-smoke demo.

Run with:
    python3 -m unittest -v demos/automation-mcp-workflow-smoke/test_workflow_bundle.py
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

import workflow_bundle as wb


class TestWorkflowBundle(unittest.TestCase):
    def test_empty_bundle_is_safe(self) -> None:
        bundle = wb.WorkflowBundle("empty")
        self.assertTrue(bundle.is_safe())

    def test_empty_bundle_step_count(self) -> None:
        bundle = wb.WorkflowBundle("empty")
        self.assertEqual(bundle.step_count(), 0)

    def test_add_step_increments_count(self) -> None:
        bundle = wb.WorkflowBundle("deploy")
        bundle.add_step("build", "npm run build")
        self.assertEqual(bundle.step_count(), 1)

    def test_steps_returns_snapshot(self) -> None:
        bundle = wb.WorkflowBundle("ci")
        bundle.add_step("lint", "pylint src/", reversible=True)
        steps = bundle.steps()
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0].name, "lint")
        self.assertEqual(steps[0].action, "pylint src/")

    def test_step_default_reversible_true(self) -> None:
        bundle = wb.WorkflowBundle("ci")
        bundle.add_step("test", "pytest")
        self.assertTrue(bundle.steps()[0].reversible)

    def test_irreversible_step_makes_bundle_unsafe(self) -> None:
        bundle = wb.WorkflowBundle("risky")
        bundle.add_step("clean", "rm -rf /tmp/cache", reversible=False)
        self.assertFalse(bundle.is_safe())

    def test_mixed_reversibility_makes_bundle_unsafe(self) -> None:
        bundle = wb.WorkflowBundle("mixed")
        bundle.add_step("fetch", "git fetch", reversible=True)
        bundle.add_step("purge", "drop table users", reversible=False)
        self.assertFalse(bundle.is_safe())

    def test_multiple_reversible_steps_remain_safe(self) -> None:
        bundle = wb.WorkflowBundle("pipeline")
        bundle.add_step("fetch", "git fetch", reversible=True)
        bundle.add_step("build", "make build", reversible=True)
        self.assertTrue(bundle.is_safe())

    def test_empty_step_name_raises(self) -> None:
        bundle = wb.WorkflowBundle("check")
        with self.assertRaises(ValueError):
            bundle.add_step("", "do something")

    def test_whitespace_step_name_raises(self) -> None:
        bundle = wb.WorkflowBundle("check")
        with self.assertRaises(ValueError):
            bundle.add_step("   ", "do something")

    def test_empty_action_raises(self) -> None:
        bundle = wb.WorkflowBundle("check")
        with self.assertRaises(ValueError):
            bundle.add_step("step1", "")

    def test_step_names_and_actions_trimmed(self) -> None:
        bundle = wb.WorkflowBundle("trim")
        bundle.add_step("  test  ", "  pytest  ")
        step = bundle.steps()[0]
        self.assertEqual(step.name, "test")
        self.assertEqual(step.action, "pytest")

    def test_bundle_name_trimmed(self) -> None:
        bundle = wb.WorkflowBundle("  pipeline  ")
        self.assertEqual(bundle.name, "pipeline")

    def test_empty_bundle_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            wb.WorkflowBundle("")

    def test_whitespace_bundle_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            wb.WorkflowBundle("   ")

    def test_dry_run_bundle_always_safe_with_irreversible_step(self) -> None:
        bundle = wb.WorkflowBundle("dry", dry_run=True)
        bundle.add_step("clean", "rm -rf /tmp/cache", reversible=False)
        self.assertTrue(bundle.is_safe())

    def test_dry_run_false_respects_reversibility(self) -> None:
        bundle = wb.WorkflowBundle("risky", dry_run=False)
        bundle.add_step("clean", "rm -rf /tmp/cache", reversible=False)
        self.assertFalse(bundle.is_safe())


if __name__ == "__main__":
    unittest.main()
